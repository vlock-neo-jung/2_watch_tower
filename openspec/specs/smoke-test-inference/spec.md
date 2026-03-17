## ADDED Requirements

### Requirement: 모델 다운로드 및 로드
download_models.py로 다운로드한 yolo11m-construction-hazard.pt 모델을 GPU에서 로드할 수 있어야 한다 (SHALL).

#### Scenario: 모델 다운로드
- **WHEN** `uv run python scripts/download_models.py`를 실행하면
- **THEN** models/yolo11m-construction-hazard.pt 파일이 생성되어야 한다

#### Scenario: 모델 GPU 로드
- **WHEN** 다운로드된 모델을 device="cuda"로 로드하면
- **THEN** 오류 없이 로드되어야 한다

### Requirement: 추론 스크립트 실행
scripts/run_inference.py가 샘플 데이터에 대해 GPU 추론을 실행하고 결과를 저장해야 한다 (SHALL).

#### Scenario: 이미지 추론
- **WHEN** `uv run python scripts/run_inference.py --source data/samples/construction_workers_01.jpg`를 실행하면
- **THEN** outputs/ 디렉토리에 bbox가 오버레이된 결과 이미지가 저장되어야 한다

#### Scenario: 영상 추론
- **WHEN** `uv run python scripts/run_inference.py --source data/samples/construction_helmets.mp4`를 실행하면
- **THEN** outputs/ 디렉토리에 bbox가 오버레이된 결과 영상이 저장되어야 한다

#### Scenario: 콘솔 요약 출력
- **WHEN** 추론이 완료되면
- **THEN** 감지 객체 수, 클래스별 분포, 추론 속도가 콘솔에 출력되어야 한다

### Requirement: 건설 현장 객체 감지
construction-hazard 모델이 건설 현장 샘플에서 Person 및 PPE 관련 객체를 감지해야 한다 (SHALL).

#### Scenario: Person 감지
- **WHEN** 건설 현장 영상에 대해 추론을 실행하면
- **THEN** Person 클래스가 1개 이상 감지되어야 한다
