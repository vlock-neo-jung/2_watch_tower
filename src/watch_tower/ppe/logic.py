"""PPE 미착용 위반 감지 런타임 로직.

Zone 내 작업자 각각에 대해 PPE 착용 여부를 판정하고
위반 이벤트를 생성한다.

판정 방식:
1. (우선) hazard 모델이 NO-Hardhat / NO-Safety Vest를 직접 탐지한 경우
   → confidence=1.0 의 명시적 위반
2. 모델이 Hardhat / Safety Vest를 탐지하지 못한 경우
   → confidence=0.5 의 추정 위반 (오탐 가능성 있음)

PPE-Person 매핑:
    PPE bbox 중심점이 Person bbox 내부에 있으면 해당 작업자에 귀속.
"""

import numpy as np
import supervision as sv

from watch_tower.ppe.models import PPE_CLASS_PAIRS, PPEClass, PPEViolationEvent, ZonePPERule


def _xyxy_contains_point(xyxy: np.ndarray, point: np.ndarray) -> bool:
    """단일 bbox [x1,y1,x2,y2]가 점 [px,py]를 포함하는지 확인한다."""
    x1, y1, x2, y2 = xyxy
    px, py = point
    return bool(x1 <= px <= x2 and y1 <= py <= y2)


def _ppe_center(xyxy: np.ndarray) -> np.ndarray:
    """bbox [x1,y1,x2,y2]의 중심점 [cx,cy]를 반환한다."""
    return np.array([(xyxy[0] + xyxy[2]) / 2, (xyxy[1] + xyxy[3]) / 2])


class PPEViolationProcessor:
    """Zone 내 작업자의 PPE 착용 상태를 검사하는 프로세서.

    Parameters
    ----------
    rule:
        Zone별 PPE 필수 착용 규칙.
    """

    def __init__(self, rule: ZonePPERule) -> None:
        self.rule = rule
        self._frame_idx: int = 0

    def check_violations(
        self,
        detections: sv.Detections,
        inside_tracker_ids: set[int],
        fps: float = 30.0,
    ) -> list[PPEViolationEvent]:
        """프레임 한 장의 detections에서 PPE 위반 이벤트를 생성한다.

        Parameters
        ----------
        detections:
            현재 프레임의 모든 감지 결과 (class_id, tracker_id, xyxy 포함).
        inside_tracker_ids:
            Zone 내부에 있는 작업자 tracker_id 집합 (ZoneProcessor 제공).
        fps:
            영상 FPS (timestamp 계산용).

        Returns
        -------
        list[PPEViolationEvent]:
            PPE 미착용 위반 이벤트 목록.
        """
        events: list[PPEViolationEvent] = []
        now_ms = (self._frame_idx / fps) * 1000.0
        self._frame_idx += 1

        if not inside_tracker_ids or self.rule.required_ppe == ():
            return events

        if detections.class_id is None or len(detections) == 0:
            # 감지 없음 → 모든 zone 내 작업자가 PPE 미착용으로 추정
            for tid in inside_tracker_ids:
                events.append(PPEViolationEvent(
                    zone_id=self.rule.zone_id,
                    tracker_id=tid,
                    missing_ppe=list(self.rule.required_ppe),
                    frame_idx=self._frame_idx - 1,
                    timestamp_ms=now_ms,
                    confidence=0.5,
                ))
            return events

        class_ids = detections.class_id
        tracker_ids = detections.tracker_id if detections.tracker_id is not None else np.full(len(detections), -1, dtype=int)
        xyxys = detections.xyxy  # shape (N, 4)

        # Person 감지 목록: zone 내 tracker_id만
        person_mask = class_ids == int(PPEClass.PERSON)
        person_indices = np.where(person_mask)[0]

        # tracker_id별 person bbox 매핑
        person_bboxes: dict[int, np.ndarray] = {}
        for idx in person_indices:
            tid = int(tracker_ids[idx])
            if tid in inside_tracker_ids:
                person_bboxes[tid] = xyxys[idx]

        # PPE 감지 수집: 착용(positive) / 미착용(negative) 분리
        positive_ppe_indices: dict[PPEClass, list[int]] = {c: [] for c in PPEClass if c != PPEClass.PERSON}
        for idx, cls_id in enumerate(class_ids):
            try:
                ppe_cls = PPEClass(cls_id)
            except ValueError:
                continue
            if ppe_cls != PPEClass.PERSON:
                positive_ppe_indices[ppe_cls].append(idx)

        # zone 내 각 작업자의 PPE 착용 상태 판정
        for tid, person_bbox in person_bboxes.items():
            # 이 작업자에 귀속된 PPE 중심점이 person bbox 내에 있는지 확인
            assigned: dict[PPEClass, bool] = {}
            for ppe_cls, indices in positive_ppe_indices.items():
                for idx in indices:
                    center = _ppe_center(xyxys[idx])
                    if _xyxy_contains_point(person_bbox, center):
                        assigned[ppe_cls] = True
                        break

            missing: list[PPEClass] = []
            for req in self.rule.required_ppe:
                neg_cls = PPE_CLASS_PAIRS.get(req)

                # 명시적 미착용 탐지 (confidence=1.0)
                if neg_cls is not None and neg_cls in assigned:
                    missing.append(req)
                    continue

                # 착용 클래스 미탐지 (confidence=0.5)
                if req not in assigned:
                    missing.append(req)

            if missing:
                # 명시적 NO-* 탐지가 있으면 confidence=1.0
                has_explicit = any(
                    PPE_CLASS_PAIRS.get(m) in assigned
                    for m in missing
                )
                events.append(PPEViolationEvent(
                    zone_id=self.rule.zone_id,
                    tracker_id=tid,
                    missing_ppe=missing,
                    frame_idx=self._frame_idx - 1,
                    timestamp_ms=now_ms,
                    confidence=1.0 if has_explicit else 0.5,
                ))

        return events

    def reset(self) -> None:
        self._frame_idx = 0
