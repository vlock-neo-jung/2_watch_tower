## ADDED Requirements

### Requirement: SODA 데이터셋 다운로드 및 변환

SODA 데이터셋을 다운로드하고 VOC XML에서 Person 클래스만 YOLO 포맷으로 변환해야 한다.

#### Scenario: 다운로드 및 변환

- **WHEN** 변환 스크립트를 실행하면
- **THEN** SODA test set의 Person 어노테이션이 YOLO 포맷으로 변환되어 저장된다

#### Scenario: Person 클래스 필터링

- **WHEN** VOC XML에 person 이외의 클래스가 포함되어 있으면
- **THEN** person 클래스만 추출하고 나머지는 무시한다

### Requirement: SODA 기반 모델 벤치마크

SODA test set의 정답 대비 각 모델의 Person Detection Recall/Precision을 비교할 수 있어야 한다.

#### Scenario: 벤치마크 실행

- **WHEN** 모델과 SODA 데이터 경로를 지정하여 벤치마크를 실행하면
- **THEN** IoU ≥ 0.5 기준으로 TP/FP/FN 및 Recall/Precision이 출력된다

#### Scenario: 다중 모델 비교

- **WHEN** hazard, COCO, VisDrone 3개 모델을 순차 실행하면
- **THEN** 모델별 비교 테이블이 출력된다
