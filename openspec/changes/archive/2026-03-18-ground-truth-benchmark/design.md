## Context

Phase 2에서 3개 모델(hazard, COCO, VisDrone)을 테스트했지만, 정답 데이터 없이 감지 수만 비교했다. 정확한 Recall/Precision 측정을 위해 Ground Truth를 만들고 정량 벤치마크를 수행한다.

## Goals / Non-Goals

**Goals:**
- 4개 CCTV 영상에서 대표 프레임 20~30장 추출
- Grounding DINO로 Person bbox 자동 생성 → 수동 검증
- YOLO 포맷 라벨 파일 저장
- 모델별 Recall/Precision 정량 비교

**Non-Goals:**
- 완벽한 데이터셋 구축 (벤치마크용 소량)
- PPE 클래스 정답 (Person만)
- COCO mAP 스타일 평가 (단순 Recall/Precision으로 충분)

## Decisions

### 1. 정답 생성: Grounding DINO

텍스트 프롬프트("person")로 bbox를 정확히 찍어주는 오픈소스 모델. 로컬 GPU에서 실행 가능.

대안: Claude/GPT-4o 멀티모달 → bbox 좌표가 부정확. 사람 수 파악은 가능하나 위치 정밀도 부족.

### 2. 프레임 추출: 영상당 5~8장, 균등 간격 + 사람 있는 구간

총 20~30장. 모든 영상의 다양한 시점을 커버.

### 3. 저장 구조

```
data/ground_truth/
├── images/          # 추출된 프레임 (jpg)
├── labels/          # YOLO 포맷 라벨 (txt, class x_center y_center w h)
└── metadata.json    # 프레임별 출처 영상, 프레임 번호
```

### 4. 비교 방식: IoU 기반 매칭

정답 bbox와 예측 bbox의 IoU ≥ 0.5이면 TP, 아니면 FP/FN. Person 클래스만 비교.

## Risks / Trade-offs

- **Grounding DINO도 완벽하지 않음**: 매우 작은 사람을 놓칠 수 있음 → 생성 후 수동 검증 필요
- **소량 데이터**: 20~30장은 통계적 신뢰도가 낮음 → 경향 파악 목적
