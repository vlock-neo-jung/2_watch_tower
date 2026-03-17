## Why

지금까지 모델 비교가 "Person 3회 vs 4회" 같은 정답 없는 비교였다. 실제 프레임에 사람이 몇 명인지 모르니 Recall/Precision을 정량적으로 측정할 수 없었다. Grounding DINO로 정답(Ground Truth) bbox를 생성하고, 이를 기준으로 모델별 성능을 정량 비교한다.

## What Changes

- CCTV 영상에서 대표 프레임 추출 (20~30장)
- Grounding DINO로 Person 정답 bbox 생성 → YOLO 포맷 저장
- 정답 대비 모델별 Recall/Precision 비교 스크립트 추가
- hazard, COCO, VisDrone 3개 모델 정량 비교

## Capabilities

### New Capabilities

- `ground-truth-benchmark`: CCTV 프레임에서 정답 bbox를 생성하고 모델별 Person Detection 정량 비교를 수행한다

### Modified Capabilities

(없음)

## Impact

- `data/ground_truth/`: 정답 프레임 + YOLO 라벨 저장
- `scripts/`: 정답 생성 스크립트, 벤치마크 비교 스크립트 추가
- 의존성: groundingdino (dev)
- `experiments/`: 벤치마크 결과 기록
