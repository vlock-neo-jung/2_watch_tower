## ADDED Requirements

### Requirement: CCTV 영상에서 프레임 추출

영상에서 대표 프레임을 균등 간격으로 추출하여 이미지로 저장할 수 있어야 한다.

#### Scenario: 프레임 추출

- **WHEN** 영상 경로와 추출 수를 지정하여 스크립트를 실행하면
- **THEN** 균등 간격으로 프레임이 추출되어 `data/ground_truth/images/`에 jpg로 저장된다

### Requirement: Grounding DINO로 정답 bbox 생성

추출된 프레임에서 Grounding DINO 모델로 Person bbox를 자동 생성하여 YOLO 포맷으로 저장해야 한다.

#### Scenario: 정답 생성

- **WHEN** 프레임 이미지 디렉토리를 지정하여 스크립트를 실행하면
- **THEN** 각 이미지에서 "person" 프롬프트로 bbox가 감지되고, YOLO 포맷(class x_center y_center w h)으로 `data/ground_truth/labels/`에 저장된다

### Requirement: 모델별 정량 비교

정답 bbox 대비 각 모델의 Person Detection Recall/Precision을 비교할 수 있어야 한다.

#### Scenario: 벤치마크 실행

- **WHEN** 모델 경로와 정답 데이터 경로를 지정하여 비교 스크립트를 실행하면
- **THEN** IoU ≥ 0.5 기준으로 TP/FP/FN을 계산하고 Recall/Precision을 출력한다

#### Scenario: 다중 모델 비교

- **WHEN** 여러 모델을 순차적으로 실행하면
- **THEN** 모델별 Recall/Precision 비교 테이블이 출력된다
