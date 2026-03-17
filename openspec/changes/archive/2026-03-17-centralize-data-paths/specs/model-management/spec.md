## MODIFIED Requirements

### Requirement: 모델 다운로드 스크립트
huggingface_hub을 사용하여 필요한 모델을 config.MODELS_DIR에 다운로드하는 스크립트가 존재해야 한다 (SHALL).

#### Scenario: 스크립트 실행
- **WHEN** `uv run python scripts/download_models.py`를 실행하면
- **THEN** config.MODELS_DIR/yolo11m-construction-hazard.pt 파일이 생성되어야 한다

### Requirement: 모델 목록 문서
models/README.md에 사용 중인 모델 목록, 출처, 용도, 다운로드 경로가 기록되어야 한다 (SHALL).

#### Scenario: README 확인
- **WHEN** models/README.md를 확인하면
- **THEN** config.MODELS_DIR 경로와 다운로드 방법이 포함되어 있어야 한다
