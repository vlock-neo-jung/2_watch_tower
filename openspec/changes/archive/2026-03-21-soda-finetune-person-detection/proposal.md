## Why

SODA 벤치마크에서 최고 조합(SAHI + COCO)도 Recall 57.8% — 42%를 놓침.
공개 모델 교체와 추론 최적화의 한계가 확인됨. SODA train set(17,861장)이 이미 확보되어 있으므로, COCO 모델을 건설현장 데이터로 파인튜닝하여 Person Detection Recall을 근본적으로 개선한다.

## What Changes

- SODA train set VOC → YOLO 변환 (Person 클래스만)
- YOLO 학습 yaml 구성
- COCO pretrained yolo11m 기반 파인튜닝 실행
- SODA test set으로 벤치마크 비교 (before/after)
- 파인튜닝 모델 + SAHI 조합 테스트

## Capabilities

### New Capabilities

- `soda-finetune`: SODA 데이터셋으로 YOLO 모델을 파인튜닝하여 건설현장 Person Detection을 개선한다

### Modified Capabilities

(없음)

## Impact

- `dataset/soda/yolo/train/`: 학습용 데이터 (VOC→YOLO 변환)
- `models/`: 파인튜닝된 모델 가중치 저장
- `experiments/`: 학습 로그 및 벤치마크 결과
- GPU 점유: RTX 3080Ti VRAM 8~10GB, 2~3일 소요
