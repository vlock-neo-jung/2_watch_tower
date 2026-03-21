"""Zone 침입 감지 런타임 로직.

supervision PolygonZone 기반으로 tracker ID별 enter/stay/exit 상태를 관리하고
침입 이벤트를 생성한다.
"""

from dataclasses import dataclass, field
from enum import StrEnum

import numpy as np
import supervision as sv

from watch_tower.zone.models import ZoneDefinition


class ZoneEventType(StrEnum):
    ENTER = "enter"
    STAY = "stay"
    EXIT = "exit"


@dataclass
class ZoneEvent:
    zone_id: str
    tracker_id: int
    event_type: ZoneEventType
    frame_idx: int
    timestamp_ms: float
    dwell_frames: int = 0


@dataclass
class _TrackerState:
    """단일 tracker의 zone 내 상태."""

    consecutive_frames: int = 0  # 연속 in-zone 프레임 수
    inside: bool = False         # 진입 확정 여부
    dwell_frames: int = 0        # 진입 후 체류 프레임 수
    last_exit_ms: float = -1.0   # 마지막 이탈 시각 (-1 = 미이탈)


class ZoneProcessor:
    """단일 Zone의 침입 감지 런타임.

    - enter: min_consecutive_frames 이상 연속 in-zone이면 확정 진입 이벤트 발생
    - stay: 확정 진입 후 매 프레임마다 체류 이벤트 발생
    - exit: in-zone에서 out-of-zone(또는 tracker 소실) 시 이탈 이벤트 발생
    - cooldown_ms: 이탈 후 재진입 쿨다운 (해당 시간 내 ENTER 이벤트 억제)
    """

    def __init__(
        self,
        zone_def: ZoneDefinition,
        frame_width: int,
        frame_height: int,
    ) -> None:
        self.zone_def = zone_def
        self.polygon_zone = zone_def.to_polygon_zone(frame_width, frame_height)
        self._states: dict[int, _TrackerState] = {}
        self._frame_idx: int = 0

    def process(self, detections: sv.Detections, fps: float = 30.0) -> list[ZoneEvent]:
        """프레임 하나를 처리하여 이벤트 목록을 반환한다."""
        events: list[ZoneEvent] = []
        now_ms = (self._frame_idx / fps) * 1000.0

        # tracker_id가 없거나 빈 detections → 모든 inside tracker를 exit 처리
        if detections.tracker_id is None or len(detections) == 0:
            for tid, state in self._states.items():
                if state.inside:
                    events.append(self._make_exit_event(tid, state, now_ms))
                    state.inside = False
                    state.consecutive_frames = 0
                    state.last_exit_ms = now_ms
            self._frame_idx += 1
            return events

        # target_classes 필터
        if detections.class_id is not None:
            target_mask = np.isin(detections.class_id, self.zone_def.target_classes)
        else:
            target_mask = np.ones(len(detections), dtype=bool)

        # zone trigger 판정
        in_zone_mask = self.polygon_zone.trigger(detections)

        current_tids: set[int] = set()

        for i, tid in enumerate(detections.tracker_id):
            tid = int(tid)
            if not target_mask[i]:
                continue
            current_tids.add(tid)

            state = self._states.setdefault(tid, _TrackerState())
            is_inside = bool(in_zone_mask[i])

            if is_inside:
                state.consecutive_frames += 1
                if state.inside:
                    # 확정 진입 상태 → STAY
                    state.dwell_frames += 1
                    events.append(ZoneEvent(
                        zone_id=self.zone_def.zone_id,
                        tracker_id=tid,
                        event_type=ZoneEventType.STAY,
                        frame_idx=self._frame_idx,
                        timestamp_ms=now_ms,
                        dwell_frames=state.dwell_frames,
                    ))
                elif state.consecutive_frames >= self.zone_def.min_consecutive_frames:
                    # 연속 프레임 충족 → ENTER (쿨다운 체크)
                    cooldown_elapsed = (
                        state.last_exit_ms < 0
                        or (now_ms - state.last_exit_ms) >= self.zone_def.cooldown_ms
                    )
                    if cooldown_elapsed:
                        state.inside = True
                        state.dwell_frames = 0
                        events.append(ZoneEvent(
                            zone_id=self.zone_def.zone_id,
                            tracker_id=tid,
                            event_type=ZoneEventType.ENTER,
                            frame_idx=self._frame_idx,
                            timestamp_ms=now_ms,
                            dwell_frames=0,
                        ))
            else:
                state.consecutive_frames = 0
                if state.inside:
                    # 확정 진입 상태에서 이탈 → EXIT
                    events.append(self._make_exit_event(tid, state, now_ms))
                    state.inside = False
                    state.last_exit_ms = now_ms

        # 현재 프레임에 없는 tracker가 inside 상태이면 EXIT
        for tid, state in self._states.items():
            if tid not in current_tids and state.inside:
                events.append(self._make_exit_event(tid, state, now_ms))
                state.inside = False
                state.consecutive_frames = 0
                state.last_exit_ms = now_ms

        self._frame_idx += 1
        return events

    def _make_exit_event(self, tid: int, state: _TrackerState, now_ms: float) -> ZoneEvent:
        return ZoneEvent(
            zone_id=self.zone_def.zone_id,
            tracker_id=tid,
            event_type=ZoneEventType.EXIT,
            frame_idx=self._frame_idx,
            timestamp_ms=now_ms,
            dwell_frames=state.dwell_frames,
        )

    @property
    def inside_tracker_ids(self) -> set[int]:
        """현재 zone 내에 있는 tracker_id 집합."""
        return {tid for tid, s in self._states.items() if s.inside}

    def reset(self) -> None:
        """상태 초기화."""
        self._states.clear()
        self._frame_idx = 0
