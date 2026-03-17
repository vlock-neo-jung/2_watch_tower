## ADDED Requirements

### Requirement: pyproject.toml 기반 프로젝트 설정
프로젝트는 pyproject.toml을 사용하여 메타데이터, 의존성, 도구 설정을 관리해야 한다 (SHALL).

#### Scenario: 프로젝트 메타데이터 정의
- **WHEN** pyproject.toml을 확인하면
- **THEN** name은 "watch-tower"이고 requires-python은 ">=3.12,<3.13"이어야 한다

#### Scenario: 기본 의존성 설치
- **WHEN** `uv sync`를 실행하면
- **THEN** ultralytics, supervision, opencv-python-headless, huggingface-hub, torch (cu121), torchvision이 설치되어야 한다

#### Scenario: 개발 의존성 설치
- **WHEN** `uv sync --extra dev`를 실행하면
- **THEN** pytest, pytest-cov, ruff, ipykernel이 추가로 설치되어야 한다

### Requirement: src layout 프로젝트 구조
프로젝트는 src layout을 사용해야 한다 (SHALL).

#### Scenario: 패키지 구조 확인
- **WHEN** 프로젝트 디렉토리를 확인하면
- **THEN** src/watch_tower/__init__.py, src/watch_tower/detection/__init__.py, src/watch_tower/utils/__init__.py가 존재해야 한다

#### Scenario: 패키지 임포트
- **WHEN** `from watch_tower.detection import ...`을 실행하면
- **THEN** 정상적으로 임포트되어야 한다

### Requirement: Python 버전 고정
프로젝트는 Python 3.12를 사용해야 한다 (SHALL).

#### Scenario: Python 버전 파일
- **WHEN** .python-version 파일을 확인하면
- **THEN** 3.12가 지정되어 있어야 한다

#### Scenario: uv 환경 생성
- **WHEN** `uv sync`를 실행하면
- **THEN** Python 3.12 기반 가상환경이 생성되어야 한다

### Requirement: PyTorch CUDA 인덱스 설정
pyproject.toml의 [tool.uv] 섹션에서 PyTorch CUDA 빌드 인덱스를 설정해야 한다 (SHALL).

#### Scenario: CUDA 인덱스 설정 확인
- **WHEN** pyproject.toml의 [tool.uv] 섹션을 확인하면
- **THEN** PyTorch cu121 인덱스 URL이 지정되어 있어야 한다
