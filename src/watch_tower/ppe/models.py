"""PPE 감지 및 위반 판정을 위한 데이터 모델.

yolo11m-construction-hazard 모델의 클래스 인덱스 기반으로
Zone 내 PPE 착용 규칙과 위반 이벤트를 정의한다.

Model class IDs (yolo11m-construction-hazard):
    0: Hardhat         7: Safety Vest
    2: NO-Hardhat      4: NO-Safety Vest
    5: Person
"""

from dataclasses import dataclass, field
from enum import IntEnum


class PPEClass(IntEnum):
    """hazard 모델 클래스 인덱스 중 PPE 관련 클래스."""

    HARDHAT = 0
    NO_HARDHAT = 2
    NO_SAFETY_VEST = 4
    PERSON = 5
    SAFETY_VEST = 7


# PPE 착용 여부를 확인할 수 있는 클래스 쌍: (positive, negative)
# positive: 착용 확인, negative: 미착용 명시 탐지
PPE_CLASS_PAIRS: dict[PPEClass, PPEClass] = {
    PPEClass.HARDHAT: PPEClass.NO_HARDHAT,
    PPEClass.SAFETY_VEST: PPEClass.NO_SAFETY_VEST,
}


@dataclass(frozen=True)
class ZonePPERule:
    """Zone 내에서 작업자가 갖춰야 할 PPE 요구사항."""

    zone_id: str
    required_ppe: tuple[PPEClass, ...] = field(default_factory=tuple)


@dataclass
class PPEViolationEvent:
    """PPE 미착용 위반 이벤트."""

    zone_id: str
    tracker_id: int
    missing_ppe: list[PPEClass]
    frame_idx: int
    timestamp_ms: float
    confidence: float = 1.0  # 위반 확신도: 1.0=명시적 탐지, 0.5=착용 클래스 미탐지
