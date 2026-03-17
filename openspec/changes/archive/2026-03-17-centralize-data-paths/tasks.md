## 1. share 디렉토리 준비 + 물리 파일 이동

- [x] 1.1 /home/neo/share/watch-tower_data/ 하위 디렉토리 생성 (samples, models, outputs, dataset, experiments)
- [x] 1.2 data/samples/* → share/watch-tower_data/samples/ 이동 (7파일)
- [x] 1.3 models/*.pt → share/watch-tower_data/models/ 이동 (README.md는 프로젝트에 유지)
- [x] 1.4 outputs/* → share/watch-tower_data/outputs/ 이동
- [x] 1.5 experiments/README.md → share/watch-tower_data/experiments/ 복사
- [x] 1.6 workspace_watch-tower/dataset/ → 비어있음, 스킵

## 2. config 모듈 생성

- [x] 2.1 src/watch_tower/config.py 작성 (WATCH_TOWER_DATA_ROOT 환경변수 기반, 기본값 포함)

## 3. 스크립트 수정

- [x] 3.1 scripts/download_models.py → config.MODELS_DIR 참조로 변경
- [x] 3.2 scripts/run_inference.py → config.MODELS_DIR, config.OUTPUTS_DIR 참조로 변경
- [x] 3.3 scripts/setup_settings.py → config.DATASET_DIR 참조로 변경

## 4. 테스트 수정

- [x] 4.1 tests/conftest.py → config 모듈 참조로 변경

## 5. git 정리

- [x] 5.1 git rm data/samples/.gitkeep
- [x] 5.2 git rm experiments/README.md
- [x] 5.3 .gitignore 정리 (data/*, experiments/* 관련 규칙 제거)
- [x] 5.4 프로젝트 내 빈 experiments/ 디렉토리 제거 (data/, outputs/는 이미 없음)

## 6. 문서 업데이트

- [x] 6.1 models/README.md 경로 안내 업데이트
- [x] 6.2 docs/references/dev-environment.md 프로젝트 구조 업데이트

## 7. 검증

- [x] 7.1 uv run pytest 통과 확인 (4/4 passed)
- [x] 7.2 scripts/download_models.py 실행 → share/watch-tower_data/models/ 정상 참조
- [x] 7.3 scripts/run_inference.py 실행 → share/watch-tower_data/outputs/에 결과 저장 확인
