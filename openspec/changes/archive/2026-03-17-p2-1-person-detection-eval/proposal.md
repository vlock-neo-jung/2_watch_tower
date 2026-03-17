## Why

Phase 1에서 Smoke Test로 모델이 "동작한다"는 것을 확인했다. 이제 yolo11m-construction-hazard 모델의 Person Detection 성능을 정량적으로 측정하여 Phase 2 이후 작업(Tracking, Zone, PPE)의 기반이 되는 탐지 품질을 검증해야 한다.

## What Changes

- Construction-PPE 데이터셋 기반 `model.val()` 평가 스크립트 추가
- Person 클래스 mAP@50, Recall 수치 확보 및 Go/No-Go 판단
- 평가 결과를 experiments/에 기록하는 구조 확립
- 데이터 leakage 의심 시(mAP > 95%) SODA 데이터셋 독립 검증 경로 마련

## Capabilities

### New Capabilities

- `person-detection-eval`: Construction-PPE 데이터셋으로 Person Detection 정량 평가를 실행하고 결과를 기록한다

### Modified Capabilities

(없음)

## Impact

- `scripts/`: 평가 스크립트 추가
- `experiments/`: 평가 결과 기록 디렉토리 사용 시작
- 의존성: ultralytics (기존), Construction-PPE 데이터셋 (자동 다운로드)
- Go/No-Go 결과에 따라 Phase 2 후속 작업(FWY-48, FWY-49) 진행 여부 결정
