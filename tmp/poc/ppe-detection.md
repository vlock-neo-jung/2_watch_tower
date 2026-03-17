# PPE 감지 모듈 PoC 결과 보고서

**작성일:** 2026-02-24
**목적:** 사전학습 모델을 활용한 PPE(개인보호구) 감지 가능성 검증

---

## 1. PoC 개요

### 목표
- 사전학습된 객체 감지 모델로 건설현장 안전모/조끼 감지가 즉시 가능한지 확인
- 이미지 및 영상에서의 감지 정확도와 처리 속도 측정
- 상용화 가능한 모델 후보 선정

### 기술 스택
- **Python 3.12** + uv (패키지 관리)
- **Ultralytics** (YOLO 프레임워크)
- **OpenCV** (영상 처리)

### 프로젝트 구조
```
watch-tower/
├── src/watch_tower/
│   ├── detection/ppe_detector.py   # PPE 감지기 클래스
│   └── utils/visualize.py          # 바운딩박스 시각화
├── scripts/
│   ├── run_detection.py            # 이미지 감지 실행
│   ├── run_video_detection.py      # 영상 감지 실행
│   └── compare_models.py           # 모델 비교
├── models/                         # 사전학습 가중치 (.pt)
├── samples/                        # 테스트용 이미지/영상
├── outputs/                        # 감지 결과 출력
└── tests/                          # 단위 테스트 (6/6 통과)
```

---

## 2. 모델 비교

### 2.1 아키텍처별 비교 (이미지 테스트)

건설현장 샘플 이미지 3장에 대해 동일 조건(confidence=0.25)으로 3개 모델 비교.

| 모델 | 아키텍처 | 클래스 수 | 크기 | 출처 |
|------|---------|----------|------|------|
| yolov8n-hardhat | YOLOv8 Nano | 2 (Hardhat, NO-Hardhat) | 5.9MB | HuggingFace (keremberke) |
| yolov8s-construction-ppe-11cls | YOLOv8 Small | 11 (Gloves, Hardhat, Mask 등 착용/미착용 쌍) | 21MB | GitHub (ftnabil97) |
| yolo11s-construction-hazard | YOLO11 Small | 11 (Hardhat, Safety Vest, Person 등) | 18MB | HuggingFace (yihong1120) |

**결과 요약:**

| 모델 | 이미지01 (근접) | 이미지02 (원거리) | 이미지03 (역광) | 평가 |
|------|---------------|-----------------|---------------|------|
| yolov8n-hardhat | 1개 감지 | 7개 감지 | 1개 감지 | 안전모만 감지. 단순하지만 안정적. |
| yolov8s-ppe-11cls | 3개 감지 | 19개 감지 | **0개 (실패)** | 신뢰도 낮음. **부적합.** |
| **yolo11-hazard** | **6개 감지** | **22개 감지** | **3개 감지** | **Person/Hardhat/Vest 고신뢰도. 가장 견고. 채택.** |

→ **yolo11-hazard 계열(yihong1120/Construction-Hazard-Detection)을 기본 모델로 선정.**

### 2.2 모델 사이즈별 비교 (영상 테스트)

yolo11-hazard 계열의 s/m/x 3개 사이즈를 동일 영상(construction_helmets.mp4, 8.3초 207프레임)으로 비교.

| | **yolo11s** (Small) | **yolo11m** (Medium) | **yolo11x** (XLarge) |
|---|---|---|---|
| **파일 크기** | 18MB | 39MB | 109MB |
| **추론 속도** | 40ms (25 FPS) | 84ms (12 FPS) | 185ms (5.4 FPS) |
| **프레임당 감지** | 12.2개 | 10.1개 | 8.5개 |
| **위반 감지** | 726회 | 749회 | 637회 |
| **NO-Mask 오탐** | 23회 | **2회** | 65회 |
| **실시간 가능** | O (여유) | **O (충분)** | X (5.4 FPS) |

**핵심 발견:**
- 모델이 크다고 무조건 좋지 않음 — yolo11x는 속도만 느리고 정확도 이득 미미
- **yolo11m이 오탐(NO-Mask)을 가장 잘 억제** (s 대비 91% 감소)
- yolo11m의 12 FPS는 1카메라 기준 실시간 충분

→ **yolo11m을 최종 기본 모델로 채택.**

---

## 3. 최종 선정 모델: yolo11m-construction-hazard

| 항목 | 값 |
|------|------|
| 아키텍처 | YOLO11 Medium |
| 출처 | yihong1120/Construction-Hazard-Detection (HuggingFace) |
| 클래스 (11개) | Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, utility pole, vehicle |
| 파일 크기 | 39MB |
| 추론 속도 | **84ms/frame (12 FPS)** — MacBook CPU, 720p |
| 주요 감지 정확도 | Person ~90%, Hardhat ~80-88%, Safety Vest ~80-88% |
| 오탐 수준 | NO-Mask 2회/207프레임 (s 대비 91% 감소) |

---

## 4. 영상 테스트 상세 (yolo11m)

### 테스트 영상

| 영상 | 해상도 | FPS | 길이 | 내용 |
|------|--------|-----|------|------|
| construction_helmets.mp4 | 1280x720 | 25fps | 8.3초 (207프레임) | 건설현장 이동하는 작업자들 |
| construction_blueprint.mp4 | 1280x720 | 25fps | 15.4초 (386프레임) | 도면 확인하는 작업자 3명 |

### 영상 1: 건설현장 이동 (8.3초)

| 클래스 | 감지 횟수 | 비고 |
|--------|----------|------|
| Person | 892 | 작업자 추적 안정적 |
| **NO-Safety Vest** | **747** | **조끼 미착용 작업자 정확히 감지 (위반)** |
| Hardhat | 426 | 안전모 착용 감지 |
| machinery | 20 | 배경 중장비 |
| NO-Mask | 2 | 오탐 거의 없음 (s 대비 91% 감소) |

### 영상 2: 도면 확인 (15.4초)

이전 yolo11s 측정값 참고 (yolo11m은 동일 패턴에서 오탐 감소 기대):

| 클래스 | yolo11s 감지 횟수 | 비고 |
|--------|-----------------|------|
| Person | 1,251 | 3명 작업자 안정 추적 |
| Hardhat | 1,166 | 3명 모두 안전모 감지 (84~88%) |
| Safety Vest | 1,132 | 3명 모두 조끼 감지 (80~88%) |
| NO-Mask | 1,159 → **yolo11m에서 대폭 감소 기대** | 오탐 필터링 효과 |

---

## 5. 확인된 이슈 및 한계

### 오탐 (False Positive)
- **NO-Mask**: yolo11m에서 크게 개선됨 (207프레임 중 2회). 추가로 구역별 규칙 엔진에서 필터링 가능.
- **NO-Safety Vest 간헐적 오감지**: 특정 각도/가림에서 미착용으로 판정되는 경우 있음. 연속 프레임 이벤트 로직으로 억제 가능.

### 미감지 (False Negative)
- **원거리 작업자**: ~15m 이상에서 감지율 하락.
- **가림(Occlusion)**: 자재/장비에 의해 몸이 가려진 경우 Person 감지 실패.

### 미지원 기능
- **장갑 감지**: 모델에 장갑 클래스 없음. 별도 2단계 파이프라인 또는 전용 모델 필요.
- **작업자 추적(Tracking)**: 프레임 단위 독립 감지. 동일 인물 ID 부여 미구현.

---

## 6. 실시간 처리 가능성 분석

### 요구사항
- 감지 → 알림 전달까지 **수초 이내** (overview.md)

### 전체 파이프라인 지연 추정 (yolo11m 기준)

```
카메라 프레임 캡처     ~10ms
AI 추론 (감지)        ~84ms   ← yolo11m 측정값 (MacBook CPU)
이벤트 판정 로직       ~1ms
알림 발송 (API 호출)   ~200~500ms
────────────────────────────
합계                  ~295~595ms → 1초 이내
```

### 디바이스별 예상 성능 (yolo11m, 1카메라, 720p 기준)

| 디바이스 | 추론 시간 | FPS | 실시간 가능 여부 |
|---------|----------|-----|----------------|
| MacBook (M시리즈 CPU) | 84ms | 12 | O (현재 측정값) |
| Jetson Orin Nano (INT8) | ~100-140ms | 7-10 | △ (프레임 스킵 권장) |
| Jetson AGX Orin (INT8) | ~30-50ms | 20-33 | O (멀티스트림 가능) |

### 멀티카메라 시 전략
- **1대**: 매 프레임 처리 가능 (12 FPS)
- **2~3대**: 프레임 스킵 (3~5fps 샘플링) → 카메라당 1초 이내 유지 가능
- **5대 이상**: GPU 가속(TensorRT) 또는 엣지 노드 분산 필수

---

## 7. 향후 구현 과제 (우선순위 순)

1. **구역별 PPE 규칙 엔진** — "이 구역은 안전모+조끼만 필수" 등 필터링 로직 (NO-Mask 오탐 해결)
2. **이벤트 생성 로직** — N프레임 연속 위반 시 이벤트 트리거 (단발성 오탐 억제)
3. **작업자 추적(Tracking)** — 동일 인물 ID 부여 → "누가 위반했는지" 추적
4. **쓰러짐 감지 모듈** — MediaPipe Pose 기반 포즈 추정 + 낙상 분류기
5. **장갑 감지** — 2단계 파이프라인 또는 근접 카메라 전용 모델
6. **RTSP 입력 지원** — IP카메라 실시간 스트림 연동
7. **성능 최적화** — TensorRT 변환, INT8 양자화, 프레임 스킵 전략

---

## 부록: 실행 방법

### 환경 설정
```bash
cd watch-tower
uv sync --extra dev
```

### 모델 다운로드
```bash
mkdir -p models
# 기본 모델 (yolo11m)
curl -L -o models/yolo11m-construction-hazard.pt \
  "https://huggingface.co/yihong1120/Construction-Hazard-Detection/resolve/main/models/yolo11/pt/yolo11m.pt"
```

### 이미지 감지
```bash
uv run python scripts/run_detection.py --source samples/
# 결과: outputs/result_*.jpg
```

### 영상 감지
```bash
uv run python scripts/run_video_detection.py --source samples/construction_helmets.mp4
# 결과: outputs/result_construction_helmets.mp4
```

### 모델 비교
```bash
uv run python scripts/compare_models.py --source samples/
# 결과: outputs/comparison/compare_*.jpg
```

### 테스트
```bash
uv run python -m pytest tests/ -v
# 6/6 통과
```
