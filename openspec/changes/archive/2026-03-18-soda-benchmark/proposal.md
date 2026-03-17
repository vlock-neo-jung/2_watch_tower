## Why

이전 벤치마크(26장/96명)는 Grounding DINO로 생성한 불완전한 정답 + 소량 데이터여서 통계적 신뢰도가 낮았다. SODA 데이터셋은 건설현장 특화 + 사람이 직접 라벨링한 정확한 정답 + 약 2만장 규모로, 신뢰할 수 있는 벤치마크와 향후 파인튜닝 데이터를 동시에 확보할 수 있다.

## What Changes

- SODA 데이터셋 다운로드 및 VOC → YOLO 포맷 변환
- Person 클래스 매핑 (SODA의 person → 모델별 Person 인덱스)
- SODA val/test set으로 hazard/COCO/VisDrone 3개 모델 정량 벤치마크
- 대량 데이터 기반 Recall/Precision 확보

## Capabilities

### New Capabilities

- `soda-benchmark`: SODA 건설현장 데이터셋으로 모델별 Person Detection 정량 벤치마크를 수행한다

### Modified Capabilities

(없음)

## Impact

- `dataset/soda/`: SODA 데이터셋 저장 (DATASET_DIR)
- `scripts/`: VOC→YOLO 변환 스크립트, 벤치마크 스크립트 확장
- 3개 모델 모두 SODA로 학습하지 않았으므로 독립 검증 가능 확인 완료
- 향후 파인튜닝 시 동일 데이터셋 재사용 가능
