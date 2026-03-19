"""Zone 정의를 위한 Pydantic 데이터 모델.

GeoJSON Polygon 포맷, 정규화 좌표 (0-1), supervision PolygonZone 변환을 지원한다.
"""

from enum import StrEnum
from typing import Literal

import numpy as np
import supervision as sv
from pydantic import BaseModel, field_validator, model_validator
from supervision.geometry.core import Position


class ZoneType(StrEnum):
    DANGER = "danger"
    WARNING = "warning"
    ENTRY = "entry"


class GeoJSONPolygon(BaseModel):
    """GeoJSON Polygon geometry. 좌표는 0-1 정규화 범위."""

    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[list[float]]]

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, v: list[list[list[float]]]) -> list[list[list[float]]]:
        if len(v) == 0:
            raise ValueError("coordinates는 최소 1개의 링을 포함해야 합니다")

        ring = v[0]

        # closing point 자동 추가
        if len(ring) >= 2 and ring[0] != ring[-1]:
            ring = [*ring, ring[0]]

        # 고유 꼭짓점 수 검증 (closing point 제외)
        unique_points = ring[:-1] if len(ring) >= 2 else ring
        if len(unique_points) < 3:
            raise ValueError(f"최소 3개 꼭짓점이 필요합니다 (현재 {len(unique_points)}개)")

        # 좌표 범위 검증
        for point in ring:
            if len(point) != 2:
                raise ValueError(f"각 좌표는 [x, y] 형태여야 합니다: {point}")
            x, y = point
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError(f"좌표가 0-1 범위를 벗어났습니다: ({x}, {y})")

        v[0] = ring
        return v


class ZoneDefinition(BaseModel):
    """단일 zone 정의."""

    zone_id: str
    zone_name: str
    zone_type: ZoneType
    geometry: GeoJSONPolygon
    triggering_anchor: str = "BOTTOM_CENTER"
    target_classes: list[int] = [0]
    min_consecutive_frames: int = 3
    cooldown_ms: int = 30000

    @field_validator("zone_id")
    @classmethod
    def validate_zone_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("zone_id는 비어있을 수 없습니다")
        return v

    def to_polygon_zone(self, frame_width: int, frame_height: int) -> sv.PolygonZone:
        """정규화 좌표를 픽셀 좌표로 변환하여 supervision PolygonZone을 생성한다."""
        ring = self.geometry.coordinates[0]
        # closing point 제외
        points = ring[:-1] if len(ring) >= 2 and ring[0] == ring[-1] else ring
        pixel_coords = np.array(
            [[x * frame_width, y * frame_height] for x, y in points],
            dtype=np.float32,
        )
        anchor = Position[self.triggering_anchor]
        return sv.PolygonZone(
            polygon=pixel_coords,
            triggering_anchors=[anchor],
        )


class ZoneConfig(BaseModel):
    """여러 zone 정의를 담는 설정 컨테이너."""

    zones: list[ZoneDefinition] = []

    @model_validator(mode="after")
    def validate_unique_zone_ids(self) -> "ZoneConfig":
        ids = [z.zone_id for z in self.zones]
        duplicates = [zid for zid in ids if ids.count(zid) > 1]
        if duplicates:
            raise ValueError(f"zone_id 중복: {set(duplicates)}")
        return self
