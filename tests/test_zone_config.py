"""Zone 설정 모듈 테스트."""

import pytest

from watch_tower.zone import (
    GeoJSONPolygon,
    ZoneConfig,
    ZoneDefinition,
    ZoneType,
    load_zone_config,
    save_zone_config,
)


def _make_geometry(coords: list[list[float]] | None = None) -> GeoJSONPolygon:
    if coords is None:
        coords = [[0.2, 0.3], [0.8, 0.3], [0.8, 0.9], [0.2, 0.9], [0.2, 0.3]]
    return GeoJSONPolygon(coordinates=[coords])


def _make_zone(zone_id: str = "test_zone", **kwargs) -> ZoneDefinition:
    defaults = {
        "zone_id": zone_id,
        "zone_name": "테스트 구역",
        "zone_type": ZoneType.DANGER,
        "geometry": _make_geometry(),
    }
    defaults.update(kwargs)
    return ZoneDefinition(**defaults)


# --- 6.1 유효한 ZoneDefinition 생성 ---


class TestZoneDefinitionCreation:
    def test_valid_zone_definition(self):
        zone = _make_zone()
        assert zone.zone_id == "test_zone"
        assert zone.zone_name == "테스트 구역"
        assert zone.zone_type == ZoneType.DANGER

    def test_default_values(self):
        zone = _make_zone()
        assert zone.triggering_anchor == "BOTTOM_CENTER"
        assert zone.target_classes == [0]
        assert zone.min_consecutive_frames == 3
        assert zone.cooldown_ms == 30000


# --- 6.2 zone_id 빈 문자열 거부 ---


class TestZoneIdValidation:
    def test_empty_zone_id_rejected(self):
        with pytest.raises(ValueError, match="zone_id는 비어있을 수 없습니다"):
            _make_zone(zone_id="")

    def test_whitespace_zone_id_rejected(self):
        with pytest.raises(ValueError, match="zone_id는 비어있을 수 없습니다"):
            _make_zone(zone_id="   ")


# --- 6.3 ZoneType 유효/무효 값 ---


class TestZoneType:
    def test_valid_zone_types(self):
        for zt in ("danger", "warning", "entry"):
            zone = _make_zone(zone_type=zt)
            assert zone.zone_type == zt

    def test_invalid_zone_type_rejected(self):
        with pytest.raises(ValueError):
            _make_zone(zone_type="unknown")


# --- 6.4 좌표 범위 초과 거부 ---


class TestCoordinateRange:
    def test_coordinate_exceeds_upper_bound(self):
        with pytest.raises(ValueError, match="좌표가 0-1 범위를 벗어났습니다"):
            _make_geometry([[0.0, 0.0], [1.5, 0.0], [1.5, 1.0], [0.0, 1.0]])

    def test_coordinate_below_lower_bound(self):
        with pytest.raises(ValueError, match="좌표가 0-1 범위를 벗어났습니다"):
            _make_geometry([[0.0, 0.0], [-0.1, 0.0], [0.5, 0.5]])


# --- 6.5 꼭짓점 부족 거부 ---


class TestVertexCount:
    def test_two_vertices_rejected(self):
        with pytest.raises(ValueError, match="최소 3개 꼭짓점"):
            _make_geometry([[0.0, 0.0], [1.0, 1.0]])

    def test_one_vertex_rejected(self):
        with pytest.raises(ValueError, match="최소 3개 꼭짓점"):
            _make_geometry([[0.5, 0.5]])


# --- 6.6 closing point 자동 추가 ---


class TestClosingPoint:
    def test_auto_close_polygon(self):
        geom = _make_geometry([[0.2, 0.3], [0.8, 0.3], [0.8, 0.9], [0.2, 0.9]])
        ring = geom.coordinates[0]
        assert ring[0] == ring[-1], "첫 점과 마지막 점이 같아야 한다"
        assert len(ring) == 5  # 4 vertices + closing point

    def test_already_closed_polygon_unchanged(self):
        geom = _make_geometry(
            [[0.2, 0.3], [0.8, 0.3], [0.8, 0.9], [0.2, 0.9], [0.2, 0.3]]
        )
        ring = geom.coordinates[0]
        assert len(ring) == 5


# --- 6.7 zone_id 중복 거부 ---


class TestZoneConfigDuplicateIds:
    def test_duplicate_zone_ids_rejected(self):
        z1 = _make_zone(zone_id="same_id")
        z2 = _make_zone(zone_id="same_id")
        with pytest.raises(ValueError, match="zone_id 중복"):
            ZoneConfig(zones=[z1, z2])

    def test_unique_zone_ids_accepted(self):
        z1 = _make_zone(zone_id="zone_a")
        z2 = _make_zone(zone_id="zone_b")
        config = ZoneConfig(zones=[z1, z2])
        assert len(config.zones) == 2

    def test_empty_zones_accepted(self):
        config = ZoneConfig(zones=[])
        assert len(config.zones) == 0


# --- 6.8 to_polygon_zone 좌표 변환 정확성 ---


class TestToPolygonZone:
    def test_coordinate_conversion_1920x1080(self):
        zone = _make_zone(
            geometry=_make_geometry(
                [[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0]]
            )
        )
        pz = zone.to_polygon_zone(1920, 1080)
        # 첫 점 [0.5, 0.5] → [960, 540]
        assert pz.polygon[0][0] == pytest.approx(960.0)
        assert pz.polygon[0][1] == pytest.approx(540.0)

    def test_coordinate_conversion_3840x2160(self):
        zone = _make_zone(
            geometry=_make_geometry(
                [[0.5, 0.5], [1.0, 0.5], [1.0, 1.0], [0.5, 1.0]]
            )
        )
        pz = zone.to_polygon_zone(3840, 2160)
        assert pz.polygon[0][0] == pytest.approx(1920.0)
        assert pz.polygon[0][1] == pytest.approx(1080.0)

    def test_triggering_anchor_applied(self):
        zone = _make_zone(triggering_anchor="CENTER")
        pz = zone.to_polygon_zone(1920, 1080)
        from supervision.geometry.core import Position

        assert pz.triggering_anchors == [Position.CENTER]


# --- 6.9 YAML 로드/저장 왕복 ---


class TestYamlRoundTrip:
    def test_save_and_load(self, tmp_path):
        original = ZoneConfig(
            zones=[
                _make_zone(zone_id="zone_a"),
                _make_zone(zone_id="zone_b", zone_type=ZoneType.WARNING),
            ]
        )
        yaml_path = tmp_path / "test_config.yaml"
        save_zone_config(original, yaml_path)

        loaded = load_zone_config(yaml_path)
        assert len(loaded.zones) == 2
        assert loaded.zones[0].zone_id == "zone_a"
        assert loaded.zones[1].zone_type == ZoneType.WARNING

    def test_save_creates_parent_directory(self, tmp_path):
        config = ZoneConfig(zones=[_make_zone()])
        nested_path = tmp_path / "deep" / "nested" / "config.yaml"
        save_zone_config(config, nested_path)
        assert nested_path.exists()

    def test_round_trip_preserves_geometry(self, tmp_path):
        original_coords = [[0.1, 0.2], [0.9, 0.2], [0.9, 0.8], [0.1, 0.8], [0.1, 0.2]]
        zone = _make_zone(geometry=_make_geometry(original_coords))
        config = ZoneConfig(zones=[zone])

        yaml_path = tmp_path / "config.yaml"
        save_zone_config(config, yaml_path)
        loaded = load_zone_config(yaml_path)

        loaded_coords = loaded.zones[0].geometry.coordinates[0]
        assert loaded_coords == original_coords


# --- 6.10 존재하지 않는 파일 로드 시 에러 ---


class TestLoadErrors:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError, match="zone 설정 파일이 존재하지 않습니다"):
            load_zone_config("/nonexistent/path/config.yaml")

    def test_invalid_yaml_structure(self, tmp_path):
        yaml_path = tmp_path / "invalid.yaml"
        yaml_path.write_text("zones:\n  - zone_id: test\n    zone_type: danger\n")
        with pytest.raises(Exception) as exc_info:
            load_zone_config(yaml_path)
        assert "zone_name" in str(exc_info.value) or "Field required" in str(exc_info.value)

    def test_sample_yaml_loads(self):
        config = load_zone_config(
            "/home/neo/share/watch-tower_data/configs/zones/sample.yaml"
        )
        assert len(config.zones) >= 2
