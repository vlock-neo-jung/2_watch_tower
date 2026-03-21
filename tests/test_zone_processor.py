"""ZoneProcessor 단위 테스트.

모델이나 영상 없이 합성 좌표만으로 enter/stay/exit 상태 관리를 검증한다.
Zone은 100x100 픽셀 전체를 덮는 사각형(0.0~1.0)을 사용한다.
"""

import numpy as np
import pytest
import supervision as sv

from watch_tower.zone import GeoJSONPolygon, ZoneDefinition, ZoneType
from watch_tower.zone.logic import ZoneEvent, ZoneEventType, ZoneProcessor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_zone_def(
    zone_id: str = "test_zone",
    min_consecutive_frames: int = 1,
    cooldown_ms: int = 0,
    target_classes: list[int] | None = None,
) -> ZoneDefinition:
    """100x100 픽셀 프레임 전체를 덮는 zone 정의."""
    return ZoneDefinition(
        zone_id=zone_id,
        zone_name="테스트 구역",
        zone_type=ZoneType.DANGER,
        geometry=GeoJSONPolygon(
            coordinates=[[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]]
        ),
        min_consecutive_frames=min_consecutive_frames,
        cooldown_ms=cooldown_ms,
        target_classes=target_classes if target_classes is not None else [0],
    )


def _make_processor(
    frame_width: int = 100,
    frame_height: int = 100,
    **zone_kwargs,
) -> ZoneProcessor:
    return ZoneProcessor(_make_zone_def(**zone_kwargs), frame_width, frame_height)


def _det(
    bboxes: list[list[int]],
    tracker_ids: list[int] | None = None,
    class_ids: list[int] | None = None,
) -> sv.Detections:
    """합성 sv.Detections 생성."""
    if not bboxes:
        return sv.Detections.empty()
    det = sv.Detections(xyxy=np.array(bboxes, dtype=np.float32))
    det.tracker_id = np.array(tracker_ids, dtype=int) if tracker_ids is not None else None
    det.class_id = (
        np.array(class_ids, dtype=int) if class_ids is not None
        else np.zeros(len(bboxes), dtype=int)
    )
    return det


# 100x100 프레임 기준 bbox
# INSIDE: foot=(30, 90), zone 내 (0-100)
INSIDE = [10, 10, 50, 90]
# OUTSIDE: foot=(225, 250), zone 밖
OUTSIDE = [200, 200, 250, 250]


def _enter_events(events: list[ZoneEvent]) -> list[ZoneEvent]:
    return [e for e in events if e.event_type == ZoneEventType.ENTER]


def _exit_events(events: list[ZoneEvent]) -> list[ZoneEvent]:
    return [e for e in events if e.event_type == ZoneEventType.EXIT]


def _stay_events(events: list[ZoneEvent]) -> list[ZoneEvent]:
    return [e for e in events if e.event_type == ZoneEventType.STAY]


# ---------------------------------------------------------------------------
# ENTER 이벤트
# ---------------------------------------------------------------------------


class TestEnterEvent:
    def test_single_frame_enter_with_min_1(self):
        proc = _make_processor(min_consecutive_frames=1)
        events = proc.process(_det([INSIDE], tracker_ids=[1]))
        assert len(_enter_events(events)) == 1
        assert _enter_events(events)[0].tracker_id == 1

    def test_enter_requires_consecutive_frames(self):
        proc = _make_processor(min_consecutive_frames=3)
        det = _det([INSIDE], tracker_ids=[1])

        assert not _enter_events(proc.process(det))  # frame 0: count=1
        assert not _enter_events(proc.process(det))  # frame 1: count=2
        assert _enter_events(proc.process(det))       # frame 2: count=3 → ENTER

    def test_consecutive_reset_when_out_of_zone(self):
        proc = _make_processor(min_consecutive_frames=3)
        in_det = _det([INSIDE], tracker_ids=[1])
        out_det = _det([OUTSIDE], tracker_ids=[1])

        proc.process(in_det)   # count=1
        proc.process(in_det)   # count=2
        proc.process(out_det)  # 이탈 → count 리셋
        proc.process(in_det)   # count=1
        proc.process(in_det)   # count=2
        events = proc.process(in_det)  # count=3 → ENTER
        assert _enter_events(events)

    def test_enter_event_zone_id(self):
        proc = _make_processor(zone_id="zone_a", min_consecutive_frames=1)
        events = proc.process(_det([INSIDE], tracker_ids=[7]))
        assert _enter_events(events)[0].zone_id == "zone_a"

    def test_enter_event_frame_idx(self):
        proc = _make_processor(min_consecutive_frames=1)
        events = proc.process(_det([INSIDE], tracker_ids=[1]))
        assert _enter_events(events)[0].frame_idx == 0

    def test_enter_dwell_is_zero(self):
        proc = _make_processor(min_consecutive_frames=1)
        events = proc.process(_det([INSIDE], tracker_ids=[1]))
        assert _enter_events(events)[0].dwell_frames == 0


# ---------------------------------------------------------------------------
# EXIT 이벤트
# ---------------------------------------------------------------------------


class TestExitEvent:
    def test_exit_after_enter(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))           # ENTER
        events = proc.process(_det([OUTSIDE], tracker_ids=[1]))  # EXIT
        assert _exit_events(events)
        assert _exit_events(events)[0].tracker_id == 1

    def test_no_exit_without_enter(self):
        proc = _make_processor(min_consecutive_frames=1)
        events = proc.process(_det([OUTSIDE], tracker_ids=[1]))
        assert not _exit_events(events)

    def test_exit_when_tracker_disappears(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))  # ENTER
        events = proc.process(sv.Detections.empty())   # tracker 소실
        assert _exit_events(events)

    def test_no_exit_when_candidate_disappears(self):
        """연속 프레임 미충족 상태(candidate)에서 사라지면 EXIT 없어야 함."""
        proc = _make_processor(min_consecutive_frames=3)
        proc.process(_det([INSIDE], tracker_ids=[1]))  # count=1, not inside
        events = proc.process(sv.Detections.empty())   # 사라짐
        assert not _exit_events(events)


# ---------------------------------------------------------------------------
# 체류 시간 카운팅
# ---------------------------------------------------------------------------


class TestDwellTracking:
    def test_stay_events_increment_dwell(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE], tracker_ids=[1])

        proc.process(det)  # frame 0: ENTER (dwell=0)
        stay_events = []
        for _ in range(4):
            events = proc.process(det)
            stay_events.extend(_stay_events(events))

        assert [e.dwell_frames for e in stay_events] == [1, 2, 3, 4]

    def test_exit_event_contains_dwell_count(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE], tracker_ids=[1])

        proc.process(det)  # ENTER
        proc.process(det)  # STAY dwell=1
        proc.process(det)  # STAY dwell=2
        events = proc.process(_det([OUTSIDE], tracker_ids=[1]))  # EXIT
        assert _exit_events(events)[0].dwell_frames == 2

    def test_dwell_resets_after_reentry(self):
        proc = _make_processor(min_consecutive_frames=1, cooldown_ms=0)
        det_in = _det([INSIDE], tracker_ids=[1])
        det_out = _det([OUTSIDE], tracker_ids=[1])

        proc.process(det_in)  # ENTER
        proc.process(det_in)  # STAY dwell=1
        proc.process(det_out)  # EXIT
        proc.process(det_in)   # 재진입 ENTER → dwell 리셋
        events = proc.process(det_in)  # STAY
        assert _stay_events(events)[0].dwell_frames == 1


# ---------------------------------------------------------------------------
# 쿨다운
# ---------------------------------------------------------------------------


class TestCooldown:
    def test_reentry_suppressed_within_cooldown(self):
        """쿨다운 내 재진입은 ENTER 이벤트를 발생시키지 않는다."""
        proc = _make_processor(min_consecutive_frames=1, cooldown_ms=5000)
        det_in = _det([INSIDE], tracker_ids=[1])
        det_out = _det([OUTSIDE], tracker_ids=[1])

        # fps=1 → 1frame=1000ms
        proc.process(det_in, fps=1.0)   # frame 0: ENTER
        proc.process(det_out, fps=1.0)  # frame 1: EXIT, last_exit=1000ms
        events = proc.process(det_in, fps=1.0)  # frame 2: now=2000ms, elapsed=1000ms < 5000ms
        assert not _enter_events(events)

    def test_reentry_allowed_after_cooldown(self):
        """쿨다운 경과 후 재진입은 ENTER 이벤트를 발생시킨다."""
        proc = _make_processor(min_consecutive_frames=1, cooldown_ms=1000)
        det_in = _det([INSIDE], tracker_ids=[1])
        det_out = _det([OUTSIDE], tracker_ids=[1])

        # fps=1 → 1frame=1000ms
        proc.process(det_in, fps=1.0)   # frame 0: ENTER, now=0ms
        proc.process(det_out, fps=1.0)  # frame 1: EXIT, last_exit=1000ms
        events = proc.process(det_in, fps=1.0)  # frame 2: now=2000ms, elapsed=1000ms >= 1000ms
        assert _enter_events(events)

    def test_first_entry_not_blocked_by_cooldown(self):
        """최초 진입은 쿨다운과 무관하게 허용된다."""
        proc = _make_processor(min_consecutive_frames=1, cooldown_ms=999999)
        events = proc.process(_det([INSIDE], tracker_ids=[1]))
        assert _enter_events(events)


# ---------------------------------------------------------------------------
# 복수 tracker
# ---------------------------------------------------------------------------


class TestMultipleTrackers:
    def test_two_trackers_enter_independently(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE, INSIDE], tracker_ids=[1, 2])
        events = proc.process(det)
        enter_tids = {e.tracker_id for e in _enter_events(events)}
        assert enter_tids == {1, 2}

    def test_one_inside_one_outside(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE, OUTSIDE], tracker_ids=[1, 2])
        events = proc.process(det)
        enter_tids = {e.tracker_id for e in _enter_events(events)}
        assert 1 in enter_tids
        assert 2 not in enter_tids

    def test_independent_exit_events(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE, INSIDE], tracker_ids=[1, 2]))  # 둘 다 ENTER
        events = proc.process(_det([OUTSIDE, OUTSIDE], tracker_ids=[1, 2]))
        exit_tids = {e.tracker_id for e in _exit_events(events)}
        assert exit_tids == {1, 2}


# ---------------------------------------------------------------------------
# target_classes 필터
# ---------------------------------------------------------------------------


class TestTargetClassFilter:
    def test_non_target_class_ignored(self):
        proc = _make_processor(min_consecutive_frames=1, target_classes=[0])
        events = proc.process(_det([INSIDE], tracker_ids=[1], class_ids=[5]))
        assert not _enter_events(events)

    def test_target_class_detected(self):
        proc = _make_processor(min_consecutive_frames=1, target_classes=[5])
        events = proc.process(_det([INSIDE], tracker_ids=[1], class_ids=[5]))
        assert _enter_events(events)

    def test_mixed_class_only_target_enters(self):
        proc = _make_processor(min_consecutive_frames=1, target_classes=[0])
        det = _det([INSIDE, INSIDE], tracker_ids=[1, 2], class_ids=[0, 5])
        events = proc.process(det)
        enter_tids = {e.tracker_id for e in _enter_events(events)}
        assert enter_tids == {1}


# ---------------------------------------------------------------------------
# inside_tracker_ids 프로퍼티
# ---------------------------------------------------------------------------


class TestInsideTrackerIds:
    def test_empty_initially(self):
        proc = _make_processor()
        assert proc.inside_tracker_ids == set()

    def test_populated_after_enter(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))
        assert proc.inside_tracker_ids == {1}

    def test_cleared_after_exit(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))
        proc.process(_det([OUTSIDE], tracker_ids=[1]))
        assert proc.inside_tracker_ids == set()

    def test_multiple_trackers_tracked(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE, INSIDE], tracker_ids=[1, 2]))
        assert proc.inside_tracker_ids == {1, 2}

    def test_partial_exit_updates_set(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE, INSIDE], tracker_ids=[1, 2]))
        proc.process(_det([INSIDE, OUTSIDE], tracker_ids=[1, 2]))
        assert proc.inside_tracker_ids == {1}


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_clears_state(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))
        assert proc.inside_tracker_ids == {1}
        proc.reset()
        assert proc.inside_tracker_ids == set()

    def test_reset_clears_frame_index(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))
        proc.reset()
        assert proc._frame_idx == 0

    def test_reprocess_after_reset(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))
        proc.reset()
        events = proc.process(_det([INSIDE], tracker_ids=[1]))
        assert _enter_events(events)


# ---------------------------------------------------------------------------
# tracker_id 없는 경우
# ---------------------------------------------------------------------------


class TestNoTrackerId:
    def test_detections_without_tracker_id_not_processed(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE])  # tracker_id=None
        events = proc.process(det)
        assert not _enter_events(events)

    def test_empty_detections_cause_exit(self):
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))      # ENTER
        events = proc.process(sv.Detections.empty())       # exit
        assert _exit_events(events)

    def test_no_tracker_id_causes_exit(self):
        """tracker_id=None 프레임 → inside tracker EXIT 발생."""
        proc = _make_processor(min_consecutive_frames=1)
        proc.process(_det([INSIDE], tracker_ids=[1]))  # ENTER
        det_no_id = _det([INSIDE])                     # tracker_id=None
        events = proc.process(det_no_id)
        assert _exit_events(events)


# ---------------------------------------------------------------------------
# 타임스탬프
# ---------------------------------------------------------------------------


class TestTimestamp:
    def test_timestamp_matches_frame_and_fps(self):
        proc = _make_processor(min_consecutive_frames=1)
        det = _det([INSIDE], tracker_ids=[1])

        proc.process(det, fps=10.0)  # frame 0: now=0ms
        proc.process(det, fps=10.0)  # frame 1: stay, now=100ms
        events = proc.process(_det([OUTSIDE], tracker_ids=[1]), fps=10.0)  # EXIT, now=200ms
        assert _exit_events(events)[0].timestamp_ms == pytest.approx(200.0)
