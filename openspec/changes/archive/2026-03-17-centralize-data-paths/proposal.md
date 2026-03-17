## Why

대용량 파일(모델 가중치, 샘플 데이터, 추론 결과, 데이터셋, 실험 결과)이 프로젝트 디렉토리 안에 있어서 git repo가 불필요하게 복잡하다. 모든 대용량 데이터를 share 디렉토리(/home/neo/share/watch-tower_data/)로 통합하고, 경로를 환경변수 기반 config 모듈로 관리하여 다양한 환경(로컬, Jetson, Docker)에서 경로만 바꾸면 동작하도록 한다.

## What Changes

- 신규: src/watch_tower/config.py (DATA_ROOT 환경변수 기반 경로 관리)
- 수정: scripts/download_models.py (config.MODELS_DIR 참조)
- 수정: scripts/run_inference.py (config.MODELS_DIR, config.OUTPUTS_DIR 참조)
- 수정: scripts/setup_settings.py (config.DATASET_DIR 참조)
- 수정: tests/conftest.py (config 모듈 참조)
- 수정: .gitignore (프로젝트 내 data/, experiments/ 관련 규칙 정리)
- **삭제**: data/samples/.gitkeep (git 추적 제거, 물리 파일은 share로 이동)
- **삭제**: experiments/README.md (git 추적 제거, share로 이동)
- 수정: models/README.md (경로 안내 업데이트)
- 수정: docs/references/dev-environment.md (프로젝트 구조 업데이트)

## Capabilities

### New Capabilities
- `config-module`: DATA_ROOT 환경변수 기반 중앙 경로 관리 모듈

### Modified Capabilities
- `data-management`: 데이터 경로가 프로젝트 내부에서 외부 share 디렉토리로 변경
- `model-management`: 모델 경로가 config 모듈 기반으로 변경
- `experiment-tracking`: 실험 경로가 config 모듈 기반으로 변경

## Impact

- 수정 파일 7개: config.py(신규), download_models.py, run_inference.py, setup_settings.py, conftest.py, .gitignore, models/README.md
- git 추적 제거 2개: data/samples/.gitkeep, experiments/README.md
- 물리 파일 이동: data/samples/* → /home/neo/share/watch-tower_data/samples/
- 물리 파일 이동: models/*.pt → /home/neo/share/watch-tower_data/models/
- 물리 파일 이동: outputs/* → /home/neo/share/watch-tower_data/outputs/
- 물리 파일 이동: experiments/* → /home/neo/share/watch-tower_data/experiments/
- ultralytics datasets_dir 변경: → /home/neo/share/watch-tower_data/dataset/
