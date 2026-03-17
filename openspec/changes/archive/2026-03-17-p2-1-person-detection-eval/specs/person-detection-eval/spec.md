## ADDED Requirements

### Requirement: Person Detection 정량 평가 실행

시스템은 yolo11m-construction-hazard 모델을 Construction-PPE 데이터셋으로 평가하여 Person 클래스의 mAP@50과 Recall을 측정할 수 있어야 한다.

#### Scenario: 평가 스크립트 실행

- **WHEN** `scripts/eval_person_detection.py`를 실행하면
- **THEN** Construction-PPE 데이터셋이 자동 다운로드되고, `model.val()`이 GPU에서 실행되어 클래스별 성능 수치가 출력된다

#### Scenario: 결과 저장

- **WHEN** 평가가 완료되면
- **THEN** 전체 클래스별 mAP@50, Recall, Precision 수치와 Person 클래스 개별 수치가 `experiments/YYYY-MM-DD-person-detection-eval/`에 기록된다

### Requirement: Go/No-Go 판단 기준 적용

평가 결과에 대해 사전 정의된 Go/No-Go 기준을 적용하여 Phase 2 계속 진행 여부를 판단할 수 있어야 한다.

#### Scenario: Go 판단

- **WHEN** Person mAP@50 >= 75% AND Recall >= 80%
- **THEN** Go로 판단하고 결과 리포트에 "Go" 기록

#### Scenario: No-Go 판단 — mAP 미달

- **WHEN** Person mAP@50 < 75%
- **THEN** No-Go로 판단하고 SODA 데이터셋 독립 검증을 후속 작업으로 기록

#### Scenario: No-Go 판단 — Recall 미달

- **WHEN** Person Recall < 80%
- **THEN** No-Go로 판단하고 신뢰도 임계값 조정(0.25 → 0.15) 후 재평가를 후속 작업으로 기록

### Requirement: 데이터 Leakage 감지

평가 결과가 비정상적으로 높을 경우 데이터 leakage 가능성을 식별할 수 있어야 한다.

#### Scenario: Leakage 의심

- **WHEN** Person mAP@50 > 95%
- **THEN** 결과 리포트에 leakage 경고를 기록하고, SODA 데이터셋 독립 검증을 후속 작업으로 기록
