"""FastAPI 라우트 통합 테스트.

Zone CRUD, Annotation CRUD, Video 목록 API에 대한 TestClient 기반 테스트.
경로 순회 방어, 에러 응답, CRUD 동작을 검증한다.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Zone CRUD API
# ---------------------------------------------------------------------------

class TestZoneList:
    def test_list_returns_empty_when_dir_missing(self, tmp_path: Path):
        with patch("api.routes.zones.ZONES_DIR", tmp_path / "nonexistent"):
            resp = client.get("/api/zones/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_yaml_files(self, tmp_path: Path):
        (tmp_path / "a.yaml").write_text("zones: []")
        (tmp_path / "b.yaml").write_text("zones: []")
        (tmp_path / "c.json").write_text("{}")  # 무시됨
        with patch("api.routes.zones.ZONES_DIR", tmp_path):
            resp = client.get("/api/zones/")
        assert resp.status_code == 200
        assert resp.json() == ["a.yaml", "b.yaml"]


class TestZoneCRUD:
    @pytest.fixture()
    def zones_dir(self, tmp_path: Path):
        d = tmp_path / "zones"
        d.mkdir()
        with patch("api.routes.zones.ZONES_DIR", d):
            yield d

    def test_save_and_get(self, zones_dir: Path):
        config = {
            "zones": [{
                "zone_id": "z1",
                "zone_name": "Test",
                "zone_type": "danger",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0.1, 0.1], [0.9, 0.1], [0.9, 0.9], [0.1, 0.1]]],
                },
                "triggering_anchor": "BOTTOM_CENTER",
                "target_classes": [0],
                "min_consecutive_frames": 3,
                "cooldown_ms": 30000,
            }],
        }
        # POST
        resp = client.post("/api/zones/test.yaml", json=config)
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

        # GET
        resp = client.get("/api/zones/test.yaml")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["zones"]) == 1
        assert data["zones"][0]["zone_id"] == "z1"

    def test_get_not_found(self, zones_dir: Path):
        resp = client.get("/api/zones/missing.yaml")
        assert resp.status_code == 404

    def test_delete(self, zones_dir: Path):
        (zones_dir / "del.yaml").write_text("zones: []")
        resp = client.delete("/api/zones/del.yaml")
        assert resp.status_code == 200
        assert not (zones_dir / "del.yaml").exists()

    def test_delete_not_found(self, zones_dir: Path):
        resp = client.delete("/api/zones/missing.yaml")
        assert resp.status_code == 404


class TestZonePathTraversal:
    def test_traversal_blocked(self, tmp_path: Path):
        with patch("api.routes.zones.ZONES_DIR", tmp_path):
            resp = client.get("/api/zones/../../../etc/passwd")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Annotation CRUD API
# ---------------------------------------------------------------------------

class TestAnnotationList:
    def test_list_empty(self, tmp_path: Path):
        with patch("api.routes.annotations.GT_DIR", tmp_path / "nonexistent"):
            resp = client.get("/api/annotations/")
        assert resp.status_code == 200
        assert resp.json() == []


class TestAnnotationCRUD:
    @pytest.fixture()
    def gt_dir(self, tmp_path: Path):
        d = tmp_path / "gt"
        d.mkdir()
        with patch("api.routes.annotations.GT_DIR", d):
            yield d

    def _sample_data(self) -> dict:
        return {
            "video": "test.mp4",
            "video_fps": 25.0,
            "video_width": 1920,
            "video_height": 1080,
            "total_frames": 500,
            "zones": [{
                "zone_id": "z1",
                "zone_name": "Test",
                "zone_type": "danger",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0.1, 0.1], [0.9, 0.1], [0.9, 0.9], [0.1, 0.1]]],
                },
                "triggering_anchor": "BOTTOM_CENTER",
                "target_classes": [0],
                "min_consecutive_frames": 3,
                "cooldown_ms": 30000,
            }],
            "events": [{"zone_id": "z1", "start_frame": 10, "end_frame": 50}],
        }

    def test_save_and_get(self, gt_dir: Path):
        data = self._sample_data()
        resp = client.post("/api/annotations/test.json", json=data)
        assert resp.status_code == 200

        resp = client.get("/api/annotations/test.json")
        assert resp.status_code == 200
        result = resp.json()
        assert result["video"] == "test.mp4"
        assert len(result["events"]) == 1

    def test_get_not_found(self, gt_dir: Path):
        resp = client.get("/api/annotations/missing.json")
        assert resp.status_code == 404

    def test_ignores_extra_fields(self, gt_dir: Path):
        """extra 필드는 조용히 무시되어 저장되지 않는다."""
        data = self._sample_data()
        data["malicious_field"] = "injected"
        resp = client.post("/api/annotations/test.json", json=data)
        assert resp.status_code == 200

        saved = json.loads((gt_dir / "test.json").read_text())
        assert "malicious_field" not in saved

    def test_rejects_missing_required_fields(self, gt_dir: Path):
        resp = client.post("/api/annotations/test.json", json={"video": "x.mp4"})
        assert resp.status_code == 422


class TestAnnotationPathTraversal:
    def test_traversal_blocked(self, tmp_path: Path):
        with patch("api.routes.annotations.GT_DIR", tmp_path):
            resp = client.get("/api/annotations/../../../etc/passwd")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Video API
# ---------------------------------------------------------------------------

class TestVideoList:
    def test_list_empty(self, tmp_path: Path):
        with patch("api.routes.videos.SAMPLES_DIR", tmp_path / "nonexistent"):
            resp = client.get("/api/videos/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_multiple_extensions(self, tmp_path: Path):
        (tmp_path / "a.mp4").write_text("")
        (tmp_path / "b.avi").write_text("")
        (tmp_path / "c.txt").write_text("")  # 무시됨
        with patch("api.routes.videos.SAMPLES_DIR", tmp_path):
            resp = client.get("/api/videos/")
        result = resp.json()
        assert "a.mp4" in result
        assert "b.avi" in result
        assert "c.txt" not in result


class TestVideoGet:
    def test_not_found(self, tmp_path: Path):
        with patch("api.routes.videos.SAMPLES_DIR", tmp_path):
            resp = client.get("/api/videos/missing.mp4")
        assert resp.status_code == 404

    def test_path_traversal(self, tmp_path: Path):
        with patch("api.routes.videos.SAMPLES_DIR", tmp_path):
            resp = client.get("/api/videos/../../../etc/passwd")
        assert resp.status_code == 404
