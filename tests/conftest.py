"""공통 테스트 fixture."""

from pathlib import Path

import pytest

from watch_tower import config


@pytest.fixture
def project_root() -> Path:
    """프로젝트 루트 디렉토리."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def data_root() -> Path:
    """데이터 루트 디렉토리."""
    return config.DATA_ROOT


@pytest.fixture
def models_dir() -> Path:
    """모델 가중치 디렉토리."""
    return config.MODELS_DIR


@pytest.fixture
def samples_dir() -> Path:
    """샘플 데이터 디렉토리."""
    return config.SAMPLES_DIR
