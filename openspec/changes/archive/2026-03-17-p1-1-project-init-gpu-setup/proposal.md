## Why

Watch Tower 프로젝트에 코드가 아직 없다. 모델 검증 작업(Phase 2~)을 시작하려면 Python 프로젝트 구조, GPU 개발 환경, 핵심 의존성이 먼저 갖춰져야 한다.

## What Changes

- Python 3.12 기반 프로젝트 초기화 (pyproject.toml, src layout, uv)
- PyTorch cu121 + ultralytics + supervision + huggingface_hub 의존성 설치
- GPU/CUDA 환경 검증 (RTX 3080 Ti, CUDA 12.x)
- ultralytics GPU 추론 동작 확인

## Capabilities

### New Capabilities
- `project-structure`: Python 프로젝트 구조 (pyproject.toml, src/watch_tower/ layout, 의존성 그룹)
- `gpu-environment`: GPU/CUDA 개발 환경 (PyTorch cu121, ultralytics GPU 추론 검증)

### Modified Capabilities

(없음 - 신규 프로젝트)

## Impact

- 신규 파일: pyproject.toml, .python-version, .gitignore, src/watch_tower/__init__.py, src/watch_tower/detection/__init__.py, src/watch_tower/utils/__init__.py
- 의존성: ultralytics, supervision, opencv-python-headless, huggingface-hub, torch (cu121), torchvision, pytest, ruff, ipykernel
- uv 인덱스 설정: PyTorch CUDA 빌드를 위한 별도 인덱스 URL
