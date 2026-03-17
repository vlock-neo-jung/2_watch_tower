"""공통 테스트 fixture."""

from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """프로젝트 루트 디렉토리."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def models_dir(project_root: Path) -> Path:
    """모델 가중치 디렉토리."""
    return project_root / "models"


@pytest.fixture
def data_dir(project_root: Path) -> Path:
    """데이터 디렉토리."""
    return project_root / "data"
