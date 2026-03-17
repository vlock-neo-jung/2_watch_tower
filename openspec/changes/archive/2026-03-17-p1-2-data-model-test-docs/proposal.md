## Why

FWY-43에서 프로젝트 구조와 GPU 환경이 구축되었으나, 데이터/모델/실험 관리 체계와 테스트 인프라가 없다. Phase 2(모델 검증) 진입 전에 이 체계를 갖춰야 검증 결과를 구조적으로 기록하고 재현할 수 있다.

## What Changes

- 데이터 관리: `data/samples/` 디렉토리 구조, ultralytics 데이터셋 경로 설정
- 모델 관리: `models/` 디렉토리 + 다운로드 스크립트 (`scripts/download_models.py`)
- 실험 기록: `experiments/` 디렉토리 구조 및 기록 규칙
- 테스트: pytest 인프라 (`tests/conftest.py`, `tests/test_smoke.py`)
- .gitignore 보완 (models/, experiments/, outputs/ 등)

## Capabilities

### New Capabilities
- `data-management`: 데이터 디렉토리 구조, ultralytics 데이터셋 경로 설정, 샘플 데이터 관리
- `model-management`: 모델 가중치 다운로드 스크립트, models/ 디렉토리 관리
- `experiment-tracking`: 실험 결과 디렉토리 구조 및 기록 규칙
- `test-infrastructure`: pytest 인프라, 기본 smoke test

### Modified Capabilities

(없음)

## Impact

- 신규 파일: scripts/download_models.py, tests/conftest.py, tests/test_smoke.py, models/README.md
- 신규 디렉토리: data/samples/, models/, experiments/, tests/
- 설정 변경: ultralytics datasets_dir → /home/neo/toy-project/workspace_watch-tower/dataset/
- .gitignore 보완
