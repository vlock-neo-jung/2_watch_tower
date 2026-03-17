# 쓰러짐 감지 모듈 PoC 결과 보고서

**작성일:** 2026-02-24
**목적:** YOLO11-Pose 사전학습 모델 + 규칙 기반 분석으로 쓰러짐(낙상) 감지 가능성 검증

---

## 1. PoC 개요

### 목표
- 사전학습된 포즈 추정 모델로 사람의 쓰러짐을 감지할 수 있는지 확인
- 정상 자세(직립/보행)에서 오탐이 발생하지 않는지 확인
- 추론 속도가 실시간 처리에 충분한지 측정

### 접근 방식
- **YOLO11s-Pose** 사전학습 모델로 인물 감지 + 17개 키포인트(관절) 추출
- 키포인트 좌표로 3가지 특성(몸통 각도, 높이 비율, bbox 비율) 계산
- 가중 합산 점수로 쓰러짐 판정 (추가 학습 없이 규칙 기반)

### 기술 스택
- **Python 3.12** + uv (패키지 관리)
- **Ultralytics** (YOLO11-Pose 프레임워크)
- **OpenCV** (영상 처리)

### 프로젝트 구조 (추가분)
```
watch-tower/
├── src/watch_tower/
│   ├── detection/
│   │   ├── ppe_detector.py          # (기존) PPE 감지기
│   │   └── fall_detector.py         # [NEW] 쓰러짐 감지기
│   └── utils/visualize.py           # 스켈레톤 시각화 함수 추가
├── scripts/
│   └── run_fall_detection.py        # [NEW] 쓰러짐 감지 실행
├── tests/
│   └── test_fall_detector.py        # [NEW] 14개 단위 테스트
├── models/
│   └── yolo11s-pose.pt              # [NEW] 포즈 추정 모델 (19MB)
└── samples/
    ├── fall_person.mp4              # [NEW] 쓰러짐 테스트 영상
    └── fall_snow.mp4                # [NEW] 눈밭 쓰러짐 영상
```

---

## 2. 쓰러짐 판정 규칙

### 2.1 COCO 17 키포인트

YOLO11-Pose는 한 번의 추론으로 인물 감지 + 17개 관절 키포인트를 추출한다.

```
        nose(0)
       /      \
 l_eye(1)    r_eye(2)
 l_ear(3)    r_ear(4)
l_shoulder(5)  r_shoulder(6)
  l_elbow(7)    r_elbow(8)
  l_wrist(9)    r_wrist(10)
   l_hip(11)     r_hip(12)
  l_knee(13)    r_knee(14)
 l_ankle(15)   r_ankle(16)
```

### 2.2 3가지 판정 특성

| 특성 | 계산 방법 | 임계값 | 가중치 |
|------|----------|--------|--------|
| **몸통 각도** | nose → hip 중점 벡터의 수직 대비 각도 | ≥ 60° (직립=0°, 수평=90°) | 0.4 |
| **키포인트 높이 비율** | 유효 키포인트의 세로 범위 / 가로 범위 | ≤ 0.8 (직립 > 1, 수평 < 1) | 0.3 |
| **Bbox 가로세로 비율** | bbox 가로 / bbox 세로 | ≥ 1.3 (직립 < 1, 수평 > 1) | 0.3 |

### 2.3 판정 로직

1. 각 특성이 임계값을 넘으면 해당 가중치만큼 점수 부여
2. 키포인트 신뢰도가 낮은 경우(< 0.5) 해당 특성 건너뛰고 나머지로 정규화
3. **정규화 점수 ≥ 0.6 → 쓰러짐(fallen) 판정**

### 2.4 연속 프레임 에피소드

- 단일 프레임의 쓰러짐 판정은 오탐 가능성이 있음
- **10프레임 이상 연속 쓰러짐** 시 "쓰러짐 에피소드 1회"로 집계
- ~0.4초(@ 25fps) 이상 쓰러진 상태로 판단

---

## 3. 사용 모델: yolo11s-pose

| 항목 | 값 |
|------|------|
| 아키텍처 | YOLO11 Small (Pose) |
| 출처 | Ultralytics 공식 (COCO-Pose 사전학습) |
| 키포인트 | 17개 (COCO 포맷) |
| 파일 크기 | 19MB |
| 파라미터 | 9.9M |
| 추론 속도 | **40~43ms/frame (23~25 FPS)** — MacBook CPU, 720p |
| person 감지 신뢰도 | 기본 0.50 |

---

## 4. 테스트 결과

### 4.1 테스트 영상

| 영상 | 해상도 | FPS | 길이 | 내용 |
|------|--------|-----|------|------|
| fall_person.mp4 | 1280x720 | 25fps | 13.6초 (340프레임) | 사람이 쓰러지는 장면 |
| fall_snow.mp4 | 1280x720 | 25fps | 21.7초 (542프레임) | 눈밭에서 사람이 쓰러지는 장면 |
| construction_helmets.mp4 | 1280x720 | 25fps | 8.3초 (207프레임) | 건설현장 보행 작업자 (쓰러짐 없음) |
| construction_blueprint.mp4 | 1280x720 | 25fps | 15.4초 (386프레임) | 도면 확인 작업자 3명 (쓰러짐 없음) |

### 4.2 결과 요약

| 영상 | 프레임 | 인물 감지 | 쓰러짐 판정 | 에피소드 | 추론 속도 | 평가 |
|------|--------|----------|-----------|---------|----------|------|
| **fall_person.mp4** | 340 | 336 (1.0/f) | **267 (78.5%)** | **1회** | 43ms (23.5 FPS) | **쓰러짐 정확히 감지** |
| fall_snow.mp4 | 542 | 315 (0.6/f) | 6 (1.9%) | 0회 | 40ms (24.8 FPS) | 미감지 (두꺼운 옷 → 키포인트 부정확) |
| construction_helmets.mp4 | 207 | 414 (2.0/f) | **0 (0%)** | **0회** | 42ms (23.9 FPS) | **오탐 없음** |
| construction_blueprint.mp4 | 386 | 1,158 (3.0/f) | **0 (0%)** | **0회** | 40ms (24.9 FPS) | **오탐 없음** |

### 4.3 상세 분석

#### fall_person.mp4 (쓰러짐 영상)

- 340프레임 중 267프레임에서 쓰러짐 판정 (78.5%)
- **253프레임 연속 쓰러짐** 감지 → 에피소드 1회로 정확히 집계
- 영상 초반 직립 상태에서는 쓰러짐 미판정 → 쓰러지는 순간부터 감지 시작
- 결과 영상에서 빨간색 bbox + 스켈레톤 + "FALLEN" 라벨 표시 확인

#### fall_snow.mp4 (눈밭 쓰러짐)

- 542프레임 중 6프레임에서만 쓰러짐 판정 (1.9%), 최대 연속 5프레임
- **미감지 원인**: 두꺼운 겨울 옷으로 키포인트 추출 정확도 저하
- 에피소드 기준(10프레임 연속) 미달 → 0회
- **한계 사례**: 의복/PPE로 인한 키포인트 감지 어려움

#### 건설현장 영상 2개 (오탐 테스트)

- **593프레임, 총 1,572명 인물 감지에서 쓰러짐 판정 0건**
- 보행, 직립, 대화 등 정상 자세에서 오탐 없음
- 건설현장 환경에서 규칙 엔진이 정상 동작하는 것으로 확인

---

## 5. 성능 측정

### 추론 속도

| 측정 항목 | 값 |
|----------|------|
| 모델 | yolo11s-pose (19MB) |
| 디바이스 | MacBook (M시리즈 CPU) |
| 해상도 | 1280x720 |
| 평균 추론 시간 | **40~43ms/frame** |
| 평균 FPS | **23~25 FPS** |

### PPE 감지 대비 성능 비교

| | PPE 감지 (yolo11m) | 쓰러짐 감지 (yolo11s-pose) |
|---|---|---|
| 추론 시간 | 84ms | 40ms |
| FPS | 12 | 25 |
| 모델 크기 | 39MB | 19MB |

→ 포즈 추정 모델이 더 작고 빨라서, 두 모델을 동시에 실행해도 실시간 처리 가능.

### 두 모델 동시 실행 시 예상 지연

```
카메라 프레임 캡처     ~10ms
PPE 감지 (yolo11m)    ~84ms
쓰러짐 감지 (yolo11s) ~40ms   (순차 실행 시)
이벤트 판정 로직       ~1ms
────────────────────────────
합계                  ~135ms → 7.4 FPS (1카메라 기준)
```

프레임 교대 처리 전략(짝수 프레임은 PPE, 홀수 프레임은 낙상)을 사용하면 ~12 FPS로 향상 가능.

---

## 6. 확인된 이슈 및 한계

### 동작하는 것 (Validated)

- **명확한 쓰러짐 감지**: 배경이 깨끗하고 사람이 잘 보이는 환경에서 쓰러짐 정확히 포착
- **정상 자세 오탐 없음**: 직립/보행 작업자 1,572건에서 오탐 0건
- **실시간 성능**: 40ms/frame (25 FPS)으로 실시간 처리 여유 충분

### 미검증 사항 (Not Yet Validated)

| 항목 | 설명 | 리스크 |
|------|------|--------|
| **쪼그림/구부림 구분** | 쪼그려 작업하는 영상 미테스트. 오탐 가능성 존재 | 높음 |
| **카메라 각도** | 정면/측면만 테스트. 높은 곳에서 내려다보는 CCTV 각도 미검증 | 높음 |
| **두꺼운 옷/PPE** | fall_snow 실패 사례. 건설현장 동절기에 같은 문제 예상 | 높음 |
| **가림(Occlusion)** | 자재/장비에 가려진 상태에서의 감지 미검증 | 중간 |
| **원거리 인물** | 카메라에서 먼 작업자의 키포인트 정확도 미확인 | 중간 |
| **다양한 쓰러짐 패턴** | 높이 추락, 비계 전도, 미끄러짐 등 실제 사고 패턴 미테스트 | 높음 |

### 현재 미지원 기능

- **작업자 추적(Tracking)**: "누가" 쓰러졌는지 식별 불가. 프레임 단위 독립 감지.
- **속도 기반 감지**: 키포인트의 시간축 이동 속도 미분석. 누워서 쉬는 것과 쓰러지는 것 구분 불가.
- **RTSP/IP카메라 연동**: 파일 입력만 지원.
- **알림 시스템**: 감지만 수행, 알림 발송 미구현.

---

## 7. 상용화까지의 로드맵

### 현재 위치: PoC 완료 — "원리 검증"

```
[현재] PoC 완료
  │   - YOLO11-Pose + 규칙 기반 쓰러짐 감지 동작 확인
  │   - 정상 자세 오탐 0건 확인
  │   - 실시간 성능 확인 (25 FPS)
  │
  ▼  2-3주
파일럿 (데이터 수집 + 튜닝)
  │   - 실제 현장 1곳에 카메라 설치
  │   - 쪼그림/구부림/보행/계단 등 다양한 자세 데이터 수집
  │   - 임계값 최적화 (현장별 카메라 각도 맞춤)
  │   - 오탐/미탐율 측정 및 개선
  │
  ▼  2-4주
알파 (핵심 기능 보강)
  │   - Tracking 추가 (동일 인물 ID 추적)
  │   - 시간축 속도 분석 (쓰러짐 vs 눕기 구분)
  │   - RTSP 입력 연동
  │   - 알림 파이프라인 연결
  │
  ▼  4-8주
베타 (현장 검증)
  │   - 다양한 현장/카메라 각도에서 검증
  │   - 필요시 LSTM 시계열 분류기 추가 (90%+ 정확도 목표)
  │   - 엣지 디바이스(Jetson) 배포 테스트
  │   - PPE 감지 모듈과 통합
  │
  ▼
상용
```

### 대안 검토: 상용 솔루션

PoC 수준의 직접 구현 대신 상용 플랫폼 활용도 가능:

| 서비스 | 비용 | 특징 |
|--------|------|------|
| Spot AI | ~$18/카메라/월 | 기존 카메라 활용, PPE+낙상 동시 지원 |
| Voxel AI | 엔터프라이즈 | 산업안전 전문, 80% 사고 감소 주장 |
| Azure Video Indexer | 엔터프라이즈 + GPU | 건설현장 명시 지원 (Preview) |

→ 상용 서비스 데모와 직접 구현을 병행 검토하는 것이 최적의 의사결정 방법.

---

## 8. 단위 테스트

```bash
uv run python -m pytest tests/test_fall_detector.py -v
# 14/14 통과
```

| 테스트 | 내용 | 결과 |
|--------|------|------|
| TestCalcTorsoAngle::test_standing | 직립 자세 → 작은 각도 | PASS |
| TestCalcTorsoAngle::test_fallen | 수평 자세 → 큰 각도 | PASS |
| TestCalcTorsoAngle::test_low_confidence | 낮은 신뢰도 → None | PASS |
| TestCalcHeightRatio::test_standing | 직립 → 높은 비율 | PASS |
| TestCalcHeightRatio::test_fallen | 수평 → 낮은 비율 | PASS |
| TestCalcBboxRatio::test_tall_bbox | 세로 bbox → < 1 | PASS |
| TestCalcBboxRatio::test_wide_bbox | 가로 bbox → > 1 | PASS |
| TestFallEvent::test_standing_not_fallen | 직립 데이터 → 정상 판정 | PASS |
| TestFallEvent::test_fallen_is_fallen | 수평 데이터 → 쓰러짐 판정 | PASS |
| TestFallDetector::test_model_loads | 모델 로드 성공 | PASS |
| TestFallDetector::test_detect_poses | 포즈 감지 리스트 반환 | PASS |
| TestFallDetector::test_empty_image | 빈 이미지 → 빈 결과 | PASS |
| TestFallDetector::test_analyze_standing | 직립 키포인트 → 정상 | PASS |
| TestFallDetector::test_analyze_fallen | 수평 키포인트 → 쓰러짐 | PASS |

전체 테스트 (PPE + 쓰러짐): **20/20 통과**

---

## 부록: 실행 방법

### 모델 다운로드
```bash
# YOLO11s-Pose (포즈 추정)
curl -L -o models/yolo11s-pose.pt \
  "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s-pose.pt"
```

### 쓰러짐 감지 실행
```bash
# 쓰러짐 영상 테스트
uv run python scripts/run_fall_detection.py --source samples/fall_person.mp4
# 결과: outputs/fall_fall_person.mp4

# 건설현장 영상 (오탐 확인)
uv run python scripts/run_fall_detection.py --source samples/construction_helmets.mp4
# 결과: outputs/fall_construction_helmets.mp4
```

### 실시간 화면 표시
```bash
uv run python scripts/run_fall_detection.py --source samples/fall_person.mp4 --show
```

### 테스트
```bash
uv run python -m pytest tests/test_fall_detector.py -v
# 14/14 통과
```
