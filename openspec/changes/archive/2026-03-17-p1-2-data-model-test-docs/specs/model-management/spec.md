## ADDED Requirements

### Requirement: 모델 다운로드 스크립트
huggingface_hub을 사용하여 필요한 모델을 다운로드하는 스크립트가 존재해야 한다 (SHALL).

#### Scenario: 스크립트 실행
- **WHEN** `uv run python scripts/download_models.py`를 실행하면
- **THEN** yolo11m-construction-hazard.pt가 models/ 디렉토리에 다운로드되어야 한다

### Requirement: 모델 목록 문서
models/README.md에 사용 중인 모델 목록, 출처, 용도가 기록되어야 한다 (SHALL).

#### Scenario: README 확인
- **WHEN** models/README.md를 확인하면
- **THEN** 모델명, HuggingFace 출처 URL, 용도가 포함되어 있어야 한다

### Requirement: 모델 가중치 gitignore
models/ 내 가중치 파일(.pt, .onnx, .engine)은 git에서 추적하지 않아야 한다 (SHALL).

#### Scenario: gitignore 확인
- **WHEN** .gitignore를 확인하면
- **THEN** *.pt, *.onnx, *.engine 패턴이 포함되어 있어야 한다
