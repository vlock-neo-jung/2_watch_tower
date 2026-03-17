## 1. 데이터 관리

- [x] 1.1 data/samples/ 디렉토리 생성 (.gitkeep 포함)
- [x] 1.2 ultralytics datasets_dir 설정 스크립트 작성 (scripts/setup_settings.py)
- [x] 1.3 .gitignore 보완 (experiments/, outputs/ 추가, data/samples/.gitkeep 예외)

## 2. 모델 관리

- [x] 2.1 models/ 디렉토리 생성
- [x] 2.2 models/README.md 작성 (모델 목록, 출처, 용도)
- [x] 2.3 scripts/download_models.py 작성 (huggingface_hub으로 yolo11m-construction-hazard.pt 다운로드)

## 3. 실험 기록

- [x] 3.1 experiments/ 디렉토리 생성 (.gitkeep 포함)
- [x] 3.2 experiments/README.md 작성 (기록 규칙: 디렉토리 명명, README 구조)

## 4. 테스트 인프라

- [x] 4.1 tests/ 디렉토리 생성
- [x] 4.2 tests/conftest.py 작성 (공통 fixture)
- [x] 4.3 tests/test_smoke.py 작성 (패키지 임포트 테스트)
- [x] 4.4 uv run pytest 실행하여 테스트 통과 확인 (4/4 passed)
