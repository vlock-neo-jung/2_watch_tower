"""PPEViolationProcessor 단위 테스트.

모델이나 영상 없이 합성 detections로 PPE 위반 판정 로직을 검증한다.
"""

import numpy as np
import pytest
import supervision as sv

from watch_tower.ppe.logic import PPEViolationProcessor
from watch_tower.ppe.models import PPEClass, PPEViolationEvent, ZonePPERule


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_detections(
    class_ids: list[int],
    xyxys: list[tuple[float, float, float, float]],
    tracker_ids: list[int] | None = None,
) -> sv.Detections:
    """테스트용 sv.Detections 생성."""
    n = len(class_ids)
    det = sv.Detections(
        xyxy=np.array(xyxys, dtype=float).reshape(n, 4),
        class_id=np.array(class_ids, dtype=int),
    )
    if tracker_ids is not None:
        det.tracker_id = np.array(tracker_ids, dtype=int)
    return det


def _make_rule(
    zone_id: str = "zone_a",
    required_ppe: tuple[PPEClass, ...] = (PPEClass.HARDHAT, PPEClass.SAFETY_VEST),
) -> ZonePPERule:
    return ZonePPERule(zone_id=zone_id, required_ppe=required_ppe)


# ---------------------------------------------------------------------------
# 기본 동작
# ---------------------------------------------------------------------------

class TestNoViolation:
    def test_person_with_hardhat_and_vest_no_violation(self):
        """Hardhat + Safety Vest 착용 → 위반 없음."""
        rule = _make_rule()
        proc = PPEViolationProcessor(rule)

        # Person bbox: (0, 0, 100, 200)
        # Hardhat center (50, 20): person 내부
        # Safety Vest center (50, 100): person 내부
        dets = _make_detections(
            class_ids=[5, 0, 7],
            xyxys=[(0, 0, 100, 200), (20, 10, 80, 50), (20, 70, 80, 130)],
            tracker_ids=[1, -1, -1],
        )
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert events == []

    def test_empty_inside_tracker_ids_no_events(self):
        """Zone 내 작업자 없음 → 이벤트 없음."""
        proc = PPEViolationProcessor(_make_rule())
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        events = proc.check_violations(dets, inside_tracker_ids=set())
        assert events == []

    def test_no_required_ppe_no_events(self):
        """required_ppe 없는 rule → 이벤트 없음."""
        rule = ZonePPERule(zone_id="zone_a", required_ppe=())
        proc = PPEViolationProcessor(rule)
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert events == []


class TestViolation:
    def test_person_no_ppe_detected(self):
        """Person만 감지되고 PPE 없음 → confidence=0.5 위반."""
        proc = PPEViolationProcessor(_make_rule())
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        events = proc.check_violations(dets, inside_tracker_ids={1})

        assert len(events) == 1
        ev = events[0]
        assert ev.tracker_id == 1
        assert PPEClass.HARDHAT in ev.missing_ppe
        assert PPEClass.SAFETY_VEST in ev.missing_ppe
        assert ev.confidence == 0.5

    def test_explicit_no_hardhat_detected(self):
        """NO-Hardhat 클래스 명시 탐지 → confidence=1.0 위반."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        # Person + NO-Hardhat (center 50,20 within person bbox)
        dets = _make_detections(
            class_ids=[5, 2],
            xyxys=[(0, 0, 100, 200), (20, 10, 80, 50)],
            tracker_ids=[1, -1],
        )
        events = proc.check_violations(dets, inside_tracker_ids={1})

        assert len(events) == 1
        assert events[0].confidence == 1.0
        assert PPEClass.HARDHAT in events[0].missing_ppe

    def test_hardhat_outside_person_bbox_counts_as_missing(self):
        """Hardhat bbox 중심이 Person bbox 밖 → 미착용으로 판정."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        # Person: (0,0,100,200), Hardhat: (200,200,250,250) → 중심 (225,225) 밖
        dets = _make_detections(
            class_ids=[5, 0],
            xyxys=[(0, 0, 100, 200), (200, 200, 250, 250)],
            tracker_ids=[1, -1],
        )
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert len(events) == 1
        assert PPEClass.HARDHAT in events[0].missing_ppe

    def test_only_hardhat_missing(self):
        """Safety Vest 착용, Hardhat 미착용 → Hardhat만 위반."""
        proc = PPEViolationProcessor(_make_rule())
        # Person: (0,0,100,200), Vest center (50,100): 내부, Hardhat 없음
        dets = _make_detections(
            class_ids=[5, 7],
            xyxys=[(0, 0, 100, 200), (20, 70, 80, 130)],
            tracker_ids=[1, -1],
        )
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert len(events) == 1
        assert PPEClass.HARDHAT in events[0].missing_ppe
        assert PPEClass.SAFETY_VEST not in events[0].missing_ppe


class TestMultiplePersons:
    def test_two_persons_one_violating(self):
        """2명 중 1명만 PPE 미착용 → 1개 이벤트."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        # Person 1: (0,0,100,200) — Hardhat center (50,20): 내부
        # Person 2: (200,0,300,200) — Hardhat 없음
        dets = _make_detections(
            class_ids=[5, 5, 0],
            xyxys=[(0, 0, 100, 200), (200, 0, 300, 200), (20, 10, 80, 50)],
            tracker_ids=[1, 2, -1],
        )
        events = proc.check_violations(dets, inside_tracker_ids={1, 2})
        assert len(events) == 1
        assert events[0].tracker_id == 2

    def test_person_outside_zone_not_checked(self):
        """Zone 밖 작업자는 PPE 미착용이어도 이벤트 없음."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[99])
        # 99번은 zone 밖
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert events == []


class TestEdgeCases:
    def test_empty_detections_all_missing(self):
        """Detections 없음 → Zone 내 모든 tracker 위반."""
        proc = PPEViolationProcessor(_make_rule())
        empty = sv.Detections.empty()
        events = proc.check_violations(empty, inside_tracker_ids={1, 2})
        tids = {e.tracker_id for e in events}
        assert tids == {1, 2}
        for ev in events:
            assert ev.confidence == 0.5

    def test_zone_id_propagated(self):
        """PPEViolationEvent에 zone_id가 올바르게 설정된다."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="danger_zone", required_ppe=(PPEClass.HARDHAT,)))
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        events = proc.check_violations(dets, inside_tracker_ids={1})
        assert events[0].zone_id == "danger_zone"

    def test_frame_idx_increments(self):
        """프레임 인덱스가 호출마다 증가한다."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        ev0 = proc.check_violations(dets, inside_tracker_ids={1})
        ev1 = proc.check_violations(dets, inside_tracker_ids={1})
        assert ev0[0].frame_idx == 0
        assert ev1[0].frame_idx == 1

    def test_reset_clears_frame_counter(self):
        """reset() 후 frame_idx가 0으로 초기화된다."""
        proc = PPEViolationProcessor(ZonePPERule(zone_id="z", required_ppe=(PPEClass.HARDHAT,)))
        dets = _make_detections(class_ids=[5], xyxys=[(0, 0, 100, 200)], tracker_ids=[1])
        proc.check_violations(dets, inside_tracker_ids={1})
        proc.reset()
        ev = proc.check_violations(dets, inside_tracker_ids={1})
        assert ev[0].frame_idx == 0
