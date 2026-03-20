## Context

SODA 벤치마크 결과:
- COCO baseline: Recall 36.7%
- SAHI + COCO: Recall 57.8%
- 여전히 42% 누락

SODA train set 17,861장이 확보되어 있고, 3개 모델 모두 SODA로 학습하지 않았으므로 독립성 보장.

## Goals / Non-Goals

**Goals:**
- SODA train set으로 COCO pretrained yolo11m 파인튜닝
- Person 단일 클래스 학습 (건설현장 사람 감지에 집중)
- SODA test set 기준 Recall 60% 이상 달성 (baseline 36.7% 대비)
- 파인튜닝 모델 + SAHI 조합 효과 확인

**Non-Goals:**
- 15개 전체 클래스 학습 (Person만)
- P2 탐지 헤드 등 아키텍처 수정 (표준 yolo11m 구조 유지)
- NWD 손실 함수 등 고급 최적화 (기본 설정으로 시작)
- 멀티 GPU 학습

## Decisions

### 1. 베이스 모델: yolo11m.pt (COCO pretrained)

SODA 벤치마크에서 COCO가 최고 Recall(36.7%)이었으므로 COCO 가중치에서 출발.
hazard 모델(35.7%)보다 나은 출발점.

### 2. 학습 해상도: imgsz=1280

리서치에서 권장하는 소형 객체 최적 해상도.
"학습과 추론에서 동일한 imgsz 사용" 원칙 준수 — 1280으로 학습하고 1280으로 추론.
RTX 3080Ti 12GB에서 batch=4로 가능.

### 3. 학습 전략: 2단계

**Stage 1 — 헤드만 학습 (50 epochs)**
- `freeze=10`으로 백본 동결
- lr0=0.01 (기본값)
- 과적합 방지하면서 탐지 헤드가 Person 패턴 학습

**Stage 2 — 전체 학습 (200 epochs)**
- freeze 해제
- lr0=0.001 (낮은 학습률)
- 백본까지 건설현장 도메인에 적응

### 4. Person 단일 클래스

SODA 15개 클래스 중 Person만 사용. 다른 클래스는 라벨에서 제거.
이미 convert_soda_to_yolo.py에서 Person만 추출하도록 구현됨.

### 5. 데이터 증강

- mosaic=1.0 (소형 객체에 필수, 다양한 스케일 강제 학습)
- close_mosaic=20 (마지막 20 epoch은 모자이크 비활성화)
- flipud=0.5 (오버헤드 뷰는 회전 불변)
- scale=0.9 (공격적 스케일 변형)
- copy_paste=0.3 (소형 인물 인스턴스 증강)

### 6. 결과 저장

- 가중치: `models/yolo11m-soda-person.pt`
- 학습 로그: ultralytics runs/ 디렉토리
- 벤치마크 결과: `experiments/`

## Risks / Trade-offs

- **과적합 리스크**: Person 단일 클래스에 17,861장이면 충분하지만, SODA 도메인에 과적합될 수 있음 → 2단계 학습 + 낮은 lr로 완화
- **학습 시간**: RTX 3080Ti에서 imgsz=1280, 250 epochs 총 40~60시간 → 백그라운드 실행
- **VRAM 제한**: batch=4가 최대. 더 큰 배치는 OOM 발생 가능
- **SODA ≠ 실제 현장**: SODA로 학습해도 고객 현장 CCTV와는 차이 있을 수 있음 → 후속 파인튜닝(FWY-59) 필요할 수 있음
