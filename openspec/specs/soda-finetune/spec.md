## ADDED Requirements

### Requirement: SODA train set 학습 데이터 준비

SODA train set을 YOLO 학습에 사용할 수 있도록 변환해야 한다.

#### Scenario: train set 변환

- **WHEN** `convert_soda_to_yolo.py --split train`을 실행하면
- **THEN** Person 클래스만 추출된 YOLO 포맷 라벨이 `dataset/soda/yolo/train/`에 생성된다

### Requirement: COCO 기반 파인튜닝 실행

COCO pretrained yolo11m을 SODA train set으로 파인튜닝해야 한다.

#### Scenario: Stage 1 학습 (헤드만)

- **WHEN** freeze=10, epochs=50으로 학습을 실행하면
- **THEN** 백본이 동결된 상태에서 탐지 헤드만 Person 패턴을 학습한다

#### Scenario: Stage 2 학습 (전체)

- **WHEN** Stage 1 가중치에서 freeze 해제, lr0=0.001, epochs=200으로 학습하면
- **THEN** 전체 네트워크가 건설현장 도메인에 적응한다

### Requirement: 벤치마크 비교

파인튜닝 전후 성능을 SODA test set으로 정량 비교해야 한다.

#### Scenario: 파인튜닝 모델 단독 벤치마크

- **WHEN** 파인튜닝 모델로 SODA test set 벤치마크를 실행하면
- **THEN** Recall/Precision이 COCO baseline(36.7%) 대비 유의미하게 개선된다

#### Scenario: 파인튜닝 모델 + SAHI 조합

- **WHEN** 파인튜닝 모델에 SAHI를 적용하여 벤치마크를 실행하면
- **THEN** 파인튜닝 단독 대비 추가 Recall 개선이 확인된다
