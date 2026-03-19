"""Zone Logic 단위 테스트.

supervision PolygonZone의 anchor point 판정, 경계선 동작, 좌표 변환을 검증한다.
모델이나 영상 없이 합성 좌표만으로 테스트한다.
"""

import numpy as np
import supervision as sv
from supervision.geometry.core import Position

from watch_tower.zone import GeoJSONPolygon, ZoneDefinition, ZoneType


def _make_zone_sv(
    polygon: list[list[int]],
    anchor: Position = Position.BOTTOM_CENTER,
) -> sv.PolygonZone:
    return sv.PolygonZone(
        polygon=np.array(polygon, dtype=np.float32),
        triggering_anchors=[anchor],
    )


def _make_detections(bboxes: list[list[int]]) -> sv.Detections:
    if len(bboxes) == 0:
        return sv.Detections.empty()
    return sv.Detections(xyxy=np.array(bboxes, dtype=np.float32))


# --- 사각형 zone: (20,20) ~ (80,80) ---
SQUARE_ZONE_COORDS = [[20, 20], [80, 20], [80, 80], [20, 80]]


# --- 7.1 zone 내부 중앙 bbox → True ---


class TestInsideZone:
    def test_foot_point_clearly_inside(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # bbox: x1=30, y1=30, x2=60, y2=70 → foot=(45, 70), zone 안
        detections = _make_detections([[30, 30, 60, 70]])
        result = zone.trigger(detections)
        assert result[0] == True


# --- 7.2 zone 완전 외부 bbox → False ---


class TestOutsideZone:
    def test_foot_point_clearly_outside(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # bbox: x1=85, y1=85, x2=95, y2=95 → foot=(90, 95), zone 밖
        detections = _make_detections([[85, 85, 95, 95]])
        result = zone.trigger(detections)
        assert result[0] == False


# --- 7.3 상반신 안/발 밖 → BOTTOM_CENTER False ---


class TestBodyInsideFootOutside:
    def test_upper_body_inside_foot_outside(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # bbox: x1=30, y1=50, x2=60, y2=90 → foot=(45, 90), zone 밖 (>80)
        detections = _make_detections([[30, 50, 60, 90]])
        result = zone.trigger(detections)
        assert result[0] == False


# --- 7.4 상반신 밖/발 안 → BOTTOM_CENTER True ---


class TestBodyOutsideFootInside:
    def test_upper_body_outside_foot_inside(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # bbox: x1=30, y1=5, x2=60, y2=50 → foot=(45, 50), zone 안
        detections = _make_detections([[30, 5, 60, 50]])
        result = zone.trigger(detections)
        assert result[0] == True


# --- 7.5 BOTTOM_CENTER vs CENTER anchor 판정 차이 ---


class TestAnchorDifference:
    def test_center_inside_but_foot_outside(self):
        # bbox: x1=30, y1=40, x2=60, y2=90
        # center=(45, 65) → zone 안
        # foot=(45, 90)   → zone 밖 (>80)
        bbox = [[30, 40, 60, 90]]

        zone_bottom = _make_zone_sv(SQUARE_ZONE_COORDS, Position.BOTTOM_CENTER)
        zone_center = _make_zone_sv(SQUARE_ZONE_COORDS, Position.CENTER)

        result_bottom = zone_bottom.trigger(_make_detections(bbox))
        result_center = zone_center.trigger(_make_detections(bbox))

        assert result_bottom[0] == False, "BOTTOM_CENTER: foot(90) > zone(80) → False"
        assert result_center[0] == True, "CENTER: center(65) in zone(20-80) → True"


# --- 7.6 경계선 안쪽/바깥 판정 ---


class TestBoundaryBehavior:
    def test_foot_just_inside_boundary(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # foot=(50, 79) → zone 안 (y=79 < 80)
        detections = _make_detections([[40, 60, 60, 79]])
        result = zone.trigger(detections)
        assert result[0] == True

    def test_foot_just_outside_boundary(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        # foot=(50, 81) → zone 밖 (y=81 > 80)
        detections = _make_detections([[40, 60, 60, 81]])
        result = zone.trigger(detections)
        assert result[0] == False


# --- 7.7 여러 사람 중 일부만 zone 안 ---


class TestMultipleDetections:
    def test_mixed_inside_outside(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        detections = _make_detections([
            [85, 85, 95, 95],   # 밖
            [30, 30, 60, 70],   # 안
            [0, 0, 10, 10],     # 밖
        ])
        result = zone.trigger(detections)
        assert list(result) == [False, True, False]


# --- 7.8 빈 detections ---


class TestEmptyDetections:
    def test_empty_detections_returns_empty(self):
        zone = _make_zone_sv(SQUARE_ZONE_COORDS)
        detections = _make_detections([])
        result = zone.trigger(detections)
        assert len(result) == 0


# --- 7.9 오목 polygon ---


class TestConcavePolygon:
    def test_point_inside_concave_polygon(self):
        # L자형 오목 polygon
        l_shape = [
            [0, 0], [50, 0], [50, 50], [25, 50], [25, 25], [0, 25],
        ]
        zone = _make_zone_sv(l_shape)
        # foot=(10, 10) → L의 왼쪽 상단 부분, 안쪽
        detections = _make_detections([[5, 5, 15, 10]])
        result = zone.trigger(detections)
        assert result[0] == True

    def test_point_in_concave_notch(self):
        # L자형에서 오목한 부분 (우하단)
        l_shape = [
            [0, 0], [50, 0], [50, 50], [25, 50], [25, 25], [0, 25],
        ]
        zone = _make_zone_sv(l_shape)
        # foot=(10, 40) → 오목 부분, 밖
        detections = _make_detections([[5, 30, 15, 40]])
        result = zone.trigger(detections)
        assert result[0] == False


# --- 7.10 정규화→픽셀 좌표 변환 ---


class TestNormalizedToPixelConversion:
    def _make_zone_def(self, coords: list[list[float]]) -> ZoneDefinition:
        return ZoneDefinition(
            zone_id="test",
            zone_name="테스트",
            zone_type=ZoneType.DANGER,
            geometry=GeoJSONPolygon(coordinates=[coords]),
        )

    def test_conversion_1920x1080(self):
        zone_def = self._make_zone_def(
            [[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0]]
        )
        pz = zone_def.to_polygon_zone(1920, 1080)
        assert pz.polygon[0][0] == 960.0
        assert pz.polygon[0][1] == 540.0

    def test_conversion_3840x2160(self):
        zone_def = self._make_zone_def(
            [[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0]]
        )
        pz = zone_def.to_polygon_zone(3840, 2160)
        assert pz.polygon[0][0] == 1920.0
        assert pz.polygon[0][1] == 1080.0

    def test_origin_maps_to_zero(self):
        zone_def = self._make_zone_def(
            [[0.0, 0.0], [0.5, 0.0], [0.5, 0.5], [0.0, 0.5]]
        )
        pz = zone_def.to_polygon_zone(1920, 1080)
        assert pz.polygon[0][0] == 0.0
        assert pz.polygon[0][1] == 0.0
