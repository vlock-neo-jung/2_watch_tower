# 실시간 멀티카메라 파이프라인 아키텍처 리서치

**작성일:** 2026-02-26
**목적:** Watch Tower 시스템의 실시간 멀티카메라 처리, 객체 추적, 엣지 배포, 알림 파이프라인 아키텍처 조사

---

## 목차

1. [현재 상태 요약](#1-현재-상태-요약)
2. [객체 추적(Tracking) 알고리즘](#2-객체-추적tracking-알고리즘)
3. [엣지 배포 최적화](#3-엣지-배포-최적화)
4. [멀티카메라 아키텍처](#4-멀티카메라-아키텍처)
5. [알림 파이프라인](#5-알림-파이프라인)
6. [추천 아키텍처](#6-추천-아키텍처)
7. [구현 로드맵](#7-구현-로드맵)

---

## 1. 현재 상태 요약

### 구현 완료

| 모듈 | 모델 | 추론 속도 (MacBook CPU) | 비고 |
|------|------|------------------------|------|
| PPE 감지 | yolo11m-construction-hazard (39MB) | 84ms/frame (12 FPS) | Person/Hardhat/Vest 고신뢰도 |
| 쓰러짐 감지 | yolo11s-pose (19MB) | 40ms/frame (25 FPS) | 명확한 쓰러짐 정확 감지, 정상 자세 오탐 0건 |
| 두 모델 순차 실행 | - | 124ms/frame (7.4 FPS) | 1카메라 기준 |

### 현재 문제점

| 문제 | 영향 | 우선순위 |
|------|------|---------|
| 파일 입력만 지원 | RTSP/IP카메라 연동 불가 | 높음 |
| 프레임 단위 독립 감지 | "누가 위반했는지" 식별 불가 | 높음 |
| 단일 카메라만 처리 | 멀티카메라 미지원 | 높음 |
| PPE + 쓰러짐 순차 실행 | 7.4 FPS (느림) | 중간 |
| 알림 시스템 미구현 | 감지만 수행, 알림 없음 | 높음 |
| 엣지 디바이스 미검증 | Jetson 등 배포 미테스트 | 중간 |

---

## 2. 객체 추적(Tracking) 알고리즘

### 2.1 알고리즘 비교

| 항목 | ByteTrack | BoT-SORT | OC-SORT |
|------|-----------|----------|---------|
| **핵심 원리** | 2단계 매칭: 고신뢰 → 저신뢰 감지 순차 연결 | ByteTrack + ReID + 카메라 모션 보정(CMC) | 관측 중심 SORT, 비선형 운동 처리 |
| **외형 특징(ReID)** | 없음 (모션만 사용) | 있음 (ReID 모델 사용) | 없음 (모션만 사용) |
| **추적 속도** | 매우 빠름 (업데이트 ~0.8ms/frame) | 느림 (ReID 추론 추가) | 매우 빠름 (700+ FPS on CPU) |
| **가림(Occlusion) 처리** | 저신뢰 감지로 복구 | ReID로 재식별 | 궤적 외삽으로 유지 |
| **MOT17 MOTA** | 80.3 | **80.5** | 78.0 |
| **MOT17 IDF1** | 77.3 | **80.2** | 77.5 |
| **적합 시나리오** | 고정 카메라, 실시간 우선 | 복잡한 장면, 정확도 우선 | 카메라 이동, 비선형 운동 |
| **구현 난이도** | 낮음 | 중간 (ReID 모델 필요) | 낮음 |
| **라이선스** | MIT | - | Apache 2.0 |

### 2.2 Ultralytics 내장 Tracker (model.track())

Ultralytics YOLO는 **BoT-SORT**와 **ByteTrack**을 내장 지원한다.

```python
from ultralytics import YOLO

model = YOLO("yolo11m-construction-hazard.pt")

# ByteTrack 사용 (기본: BoT-SORT)
results = model.track(source="rtsp://camera_ip/stream", tracker="bytetrack.yaml", persist=True)

# 결과에서 트래킹 ID 접근
for result in results:
    boxes = result.boxes
    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
        # track_ids: [1, 2, 3, ...] — 각 감지 객체의 고유 ID
```

**설정 파일 (bytetrack.yaml):**
```yaml
tracker_type: bytetrack
track_high_thresh: 0.5    # 1차 매칭 임계값
track_low_thresh: 0.1     # 2차 매칭 임계값
new_track_thresh: 0.6     # 새 트랙 생성 임계값
track_buffer: 30          # 트랙 유지 프레임 수
match_thresh: 0.8         # 매칭 거리 임계값
```

**추적 추가 지연:**
- ByteTrack: **~1-2ms/frame** (칼만 필터 + 헝가리안 매칭만 수행)
- BoT-SORT (ReID 없이): **~2-3ms/frame**
- BoT-SORT (ReID 포함): **~10-20ms/frame** (별도 분류 모델 추론 추가)

### 2.3 추적 알고리즘 추천

**건설현장 시나리오에 ByteTrack 추천:**

1. **고정 카메라** 환경 → 카메라 모션 보정(CMC) 불필요 → BoT-SORT의 장점이 줄어듦
2. **실시간 우선** → ByteTrack의 ~1ms 오버헤드가 가장 유리
3. **Ultralytics 내장** → `model.track(tracker="bytetrack.yaml")` 한 줄로 적용
4. 가림이 심한 경우 BoT-SORT로 전환 가능 (설정 파일만 변경)

**추적 + 감지 통합 시 예상 지연:**
```
PPE 감지 + 추적:   84ms + 2ms = 86ms  (11.6 FPS)
쓰러짐 감지 + 추적: 40ms + 2ms = 42ms  (23.8 FPS)
```
→ 추적 추가 시 성능 저하 무시 가능

---

## 3. 엣지 배포 최적화

### 3.1 추론 엔진 비교

| 항목 | TensorRT | ONNX Runtime | CoreML | OpenVINO |
|------|----------|-------------|--------|----------|
| **대상 하드웨어** | NVIDIA GPU (Jetson, dGPU) | 크로스 플랫폼 (CPU/GPU) | Apple Silicon (M시리즈) | Intel CPU/GPU/VPU |
| **최적화 기법** | 레이어 퓨전, 커널 오토튜닝, INT8/FP16 | 그래프 최적화, EP 선택 | ANE/GPU/CPU 자동 배분 | 레이어 퓨전, INT8 |
| **속도 향상** | GPU 기준 5-6x (vs PyTorch) | CPU 기준 2-3x | M시리즈에서 네이티브 최적 | Intel CPU 기준 2-3x |
| **양자화** | FP16, INT8, FP8 | FP16, INT8 | FP16, INT8 | FP16, INT8 |
| **Ultralytics export** | `model.export(format="engine")` | `model.export(format="onnx")` | `model.export(format="coreml")` | `model.export(format="openvino")` |
| **라이선스** | 독점 (NVIDIA HW 무료) | MIT | Apple 독점 | Apache 2.0 |
| **적합 시나리오** | 프로덕션 배포 (Jetson) | 개발/테스트, 멀티플랫폼 | macOS/iOS 개발 | Intel 엣지 디바이스 |

### 3.2 YOLO11 Jetson Orin TensorRT 벤치마크

Jetson Orin NX 16GB, 입력 640x640 기준:

| 모델 | FP32 | FP16 | INT8 | FP16 대비 PyTorch 향상 |
|------|------|------|------|----------------------|
| yolo11n | 8.6ms (116 FPS) | 5.3ms (189 FPS) | 4.5ms (222 FPS) | ~5x |
| yolo11s | 14.5ms (69 FPS) | 7.9ms (127 FPS) | 6.1ms (164 FPS) | ~4x |
| **yolo11m** | **32.1ms (31 FPS)** | **15.6ms (64 FPS)** | **10.4ms (96 FPS)** | **~5x** |
| yolo11l | 39.7ms (25 FPS) | 19.9ms (50 FPS) | 13.6ms (73 FPS) | ~4x |

**핵심 발견:**
- 현재 MacBook CPU에서 84ms인 yolo11m이 Jetson Orin NX에서 **FP16: 15.6ms, INT8: 10.4ms**
- **INT8 양자화 시 MacBook 대비 8배 빠름** (84ms → 10.4ms)
- yolo11m FP16 기준 64 FPS → 1카메라라면 PPE+쓰러짐 동시 실행도 충분

### 3.3 INT8/FP16 양자화 효과 (속도 vs 정확도)

| 정밀도 | 속도 향상 (FP32 대비) | 정확도 손실 (mAP) | 비고 |
|--------|---------------------|------------------|------|
| FP16 | ~2x | < 0.5% | **거의 무손실. 기본 권장.** |
| INT8 | ~3x | 1-3% | 캘리브레이션 필요. 대부분의 경우 허용 가능. |

YOLO26 논문에 따르면, YOLO 모델은 양자화(FP16, INT8) 시에도 일관된 정확도를 유지하며, 엣지 디바이스 배포에 적합하다.

### 3.4 Ultralytics Export 활용

```python
from ultralytics import YOLO

model = YOLO("yolo11m-construction-hazard.pt")

# TensorRT (Jetson 배포용)
model.export(format="engine", half=True)  # FP16
model.export(format="engine", int8=True, data="calibration.yaml")  # INT8

# ONNX (크로스플랫폼)
model.export(format="onnx", dynamic=True)

# CoreML (개발/테스트용)
model.export(format="coreml", nms=True)

# OpenVINO (Intel 디바이스)
model.export(format="openvino", half=True)
```

### 3.5 엣지 배포 추천

| 시나리오 | 추천 엔진 | 추천 정밀도 | 이유 |
|---------|----------|-----------|------|
| **프로덕션 (Jetson)** | TensorRT | FP16 (기본), INT8 (고밀도) | 최고 성능, 네이티브 최적화 |
| **개발/테스트 (MacBook)** | CoreML 또는 PyTorch | FP32 | 편의성 우선 |
| **프로토타입 (범용)** | ONNX Runtime | FP16 | 크로스플랫폼 호환 |
| **Intel 엣지** | OpenVINO | FP16/INT8 | Intel HW 최적화 |

---

## 4. 멀티카메라 아키텍처

### 4.1 프레임 샘플링 전략

건설현장 안전 모니터링에서 매 프레임(25-30fps) 처리는 불필요하다.

| 샘플링 FPS | 분석 주기 | 적합성 | 비고 |
|-----------|----------|--------|------|
| 25 fps | 40ms | 과잉 | 자원 낭비 |
| 10 fps | 100ms | 좋음 | 빠른 움직임 추적에 적합 |
| **5 fps** | **200ms** | **충분** | **PPE 위반은 수초간 지속. 추적 연속성 유지 가능.** |
| 3 fps | 333ms | 최소 | 쓰러짐 감지 시 빠른 낙상 순간 놓칠 수 있음 |
| 1 fps | 1000ms | 부족 | 추적 ID 유지 어려움 |

**추천: PPE 감지 5fps, 쓰러짐 감지 5-10fps**
- PPE 위반은 지속적 상태 → 낮은 FPS로 충분
- 쓰러짐은 순간 이벤트 → 상대적으로 높은 FPS 필요
- 5fps로 통일하면 카메라당 200ms 주기, 충분히 실시간

### 4.2 카메라별 독립 프로세스 vs 중앙 배치 처리

| 전략 | 장점 | 단점 | 적합 규모 |
|------|------|------|----------|
| **독립 프로세스** (카메라당 1 프로세스) | 단순, 격리, 장애 전파 없음 | GPU 공유 비효율, 메모리 중복 | 1-5대 |
| **중앙 배치 처리** (프레임 모아서 배치 추론) | GPU 효율 극대화, 처리량 최적 | 복잡, 동기화 필요 | 10-50대 |
| **하이브리드** (그룹별 배치) | 균형 잡힌 접근 | 설계 복잡 | 5-20대 |

### 4.3 프레임 교대 처리 전략 (PPE ↔ 쓰러짐)

두 모델을 매 프레임 모두 실행하는 대신 교대 실행:

```
프레임 1: PPE 감지     (84ms → TensorRT FP16: 15.6ms)
프레임 2: 쓰러짐 감지   (40ms → TensorRT FP16: ~8ms)
프레임 3: PPE 감지
프레임 4: 쓰러짐 감지
...
```

- 순차 실행: 84 + 40 = 124ms/frame (7.4 FPS) → TensorRT: 15.6 + 8 = 23.6ms (42 FPS)
- 교대 실행: max(84, 40) = 84ms/frame (12 FPS) → TensorRT: max(15.6, 8) = 15.6ms (64 FPS)
- 교대 실행 시 각 모델은 **실질 절반 FPS**로 동작하지만, PPE는 6fps면 충분

### 4.4 멀티카메라 확장 시나리오

**소규모 (1-5대) — Jetson Orin NX 1대**

```
카메라 5대 × 5fps = 25 frames/sec
yolo11m FP16: 15.6ms/frame → 64 FPS 처리 가능
→ 5대 카메라 교대 처리 시 5fps 유지 여유
```

| 처리 방식 | 카메라 수 | 모델 | FPS/카메라 | GPU 사용률 |
|----------|----------|------|-----------|-----------|
| 교대 (PPE/Fall) | 5대 | yolo11m FP16 | 5fps | ~39% |
| 순차 (PPE+Fall) | 5대 | yolo11m FP16 | 5fps | ~78% |
| 교대 (PPE/Fall) | 5대 | yolo11m INT8 | 5fps | ~26% |

**중규모 (10-50대) — DeepStream 배치 추론**

DeepStream의 `nvstreammux`로 여러 카메라 프레임을 배치화:

```
카메라 50대 × 3fps = 150 frames/sec
Jetson AGX Orin: 배치 추론으로 ~200+ FPS 가능
→ 50대 카메라 처리 가능 (여유 있음)
```

DeepStream 스트림 처리 능력 (공식 벤치마크):
- Jetson AGX Orin: 최대 16 스트림 (FP16, 1080p, 30fps)
- Jetson Orin NX: 최대 8 스트림 (FP16, 1080p, 30fps)
- Jetson Orin Nano: 최대 4 스트림 (FP16, 1080p, 30fps)
- dGPU 서버 (T4/A100): 30+ 스트림/GPU

**50대 카메라 시 권장 구성:**
- Jetson AGX Orin 3-4대 (각 12-16대 카메라 담당)
- 또는 dGPU 서버 2대 (각 25대 카메라)

### 4.5 DeepStream 기반 멀티카메라 파이프라인

```
[IP Camera x16] --RTSP--> [nvstreammux (배치 형성)]
                                  |
                          [nvinfer: PPE 감지 (TensorRT)]
                                  |
                          [nvtracker: ByteTrack 추적]
                                  |
                          [nvinfer: Pose 추정 (TensorRT)]  (2차 추론)
                                  |
                          [Python Probe: 쓰러짐 판정 + 이벤트 생성]
                                  |
                    +-------------+-------------+
                    |                           |
              [nvosd: 시각화]            [메타데이터 출력]
                    |                           |
              [RTSP 출력]               [Python 서비스]
                    |                    (알림, 로깅, API)
              [go2rtc]
                    |
              [브라우저 WebRTC]
```

DeepStream의 `nvtracker`는 배치 모드로 동작하며, 여러 카메라의 프레임을 동시에 추적한다. 멀티카메라 추적(MCT) 플러그인은 겹치는 카메라 간 3D 추적과 글로벌 ID를 지원한다.

---

## 5. 알림 파이프라인

### 5.1 이벤트 큐 아키텍처

| 솔루션 | 적합 규모 | 장점 | 단점 | 라이선스 |
|--------|----------|------|------|---------|
| **Python asyncio.Queue** | 1-5대 | 가장 단순, 의존성 없음 | 프로세스 간 공유 불가, 영속성 없음 | - |
| **Redis Pub/Sub + Streams** | 5-50대 | 빠름, 영속성, 다양한 패턴 | 외부 서비스 필요 | BSD-3 |
| **RabbitMQ** | 20-100대+ | 보장 전달, 복잡한 라우팅 | 무거움, 운영 복잡 | MPL 2.0 |
| **Apache Kafka** | 100대+ | 대규모 스트리밍, 리플레이 | 과잉 설계 | Apache 2.0 |

**추천:**
- **소규모 (1-5대):** `asyncio.Queue` 또는 Redis Pub/Sub (Redis가 이미 go2rtc와 함께 운용 가능)
- **중규모 (10-50대):** Redis Streams (영속성 + 소비자 그룹으로 안정적 전달)

### 5.2 이벤트 처리 흐름

```
[AI 감지 결과] → [이벤트 판정 엔진] → [이벤트 큐 (Redis)] → [알림 디스패처]
                      |                                            |
                 N프레임 연속 위반?                          +------+------+
                 동일 인물 추적 ID?                          |      |      |
                 구역별 규칙 매칭?                     웹소켓   카카오   SMS
                                                   대시보드  알림톡  문자
```

### 5.3 이벤트 판정 규칙 엔진

```python
# 이벤트 판정 예시
class EventRule:
    min_consecutive_frames: int = 15     # 최소 연속 프레임 (5fps × 3초)
    cooldown_seconds: float = 60.0       # 동일 인물 재알림 방지
    zone_rules: dict                     # 구역별 필수 PPE 목록

# PPE 위반 이벤트 판정
if (track_id가 15프레임 연속 NO-Hardhat) and (해당 구역에서 안전모 필수):
    → PPE_VIOLATION 이벤트 생성

# 쓰러짐 이벤트 판정
if (track_id가 10프레임 연속 FALLEN) and (쿨다운 기간 경과):
    → FALL_DETECTED 이벤트 생성 (긴급)
```

### 5.4 웹소켓 기반 실시간 대시보드

```
[Python 백엔드 (FastAPI)]
         |
    [WebSocket 서버]
         |
    +----+----+
    |         |
[대시보드]  [모바일 앱]

# FastAPI WebSocket 예시
@app.websocket("/ws/events")
async def event_stream(websocket: WebSocket):
    await websocket.accept()
    async for event in redis.subscribe("safety_events"):
        await websocket.send_json(event)
```

**기술 스택:**
- **백엔드:** FastAPI (Python, 비동기 WebSocket 지원)
- **실시간 통신:** WebSocket (양방향, 저지연)
- **메시지 브로커:** Redis Pub/Sub (이벤트 배포)
- **프론트엔드:** React + WebSocket 클라이언트

### 5.5 외부 알림 채널

| 채널 | 서비스/API | 비용 | 지연 | 적합 용도 |
|------|-----------|------|------|----------|
| **카카오 알림톡** | NHN Cloud / CoolSMS / Sendbird | ~8원/건 | 1-3초 | 기본 알림 (PPE 위반) |
| **SMS** | CoolSMS / NHN Cloud | ~20원/건 | 1-5초 | 알림톡 실패 시 폴백 |
| **모바일 Push** | Firebase Cloud Messaging (FCM) | 무료 | <1초 | 앱 사용자 즉시 알림 |
| **웹 Push** | Web Push API | 무료 | <1초 | 대시보드 사용자 알림 |

**카카오 알림톡 연동:**
```python
# CoolSMS Python SDK 활용
from coolsms_python_sdk import Message

message = Message(api_key="KEY", api_secret="SECRET")
message.send({
    "to": "01012345678",
    "from": "01000000000",
    "kakaoOptions": {
        "pfId": "SENDER_KEY",
        "templateId": "TEMPLATE_001",
        "variables": {
            "worker_name": "김철수",
            "violation_type": "안전모 미착용",
            "zone": "A구역 크레인",
            "time": "14:23:15",
            "dashboard_url": "https://watchtower.example.com/event/12345"
        }
    }
})
```

### 5.6 에스컬레이션 규칙

```
레벨 1 (즉시):     현장 안전관리자에게 알림톡 발송
                   ↓ 30초 이내 미확인
레벨 2 (30초):     현장소장에게 추가 알림톡 + SMS 동시 발송
                   ↓ 2분 이내 미확인
레벨 3 (2분):      본사 안전관리팀에게 전화 발신 (긴급)
                   ↓ 쓰러짐의 경우
레벨 0 (즉시):     119 신고 안내 + 모든 관리자에게 동시 알림
```

**구현 패턴:**
- 각 이벤트에 `acknowledged_at` 타임스탬프 필드
- Redis Sorted Set으로 미확인 이벤트 관리 (score = 발생 시간)
- 주기적 워커가 미확인 이벤트 스캔 → 경과 시간에 따라 에스컬레이션

---

## 6. 추천 아키텍처

### 6.1 소규모 (1-5대 카메라) — Python-First

```
[IP Camera 1~5]
      |
      | RTSP
      v
[go2rtc] ─────────────────────────────────────────────┐
      |                                                 |
      | RTSP (내부)                                     | WebRTC
      v                                                 v
[Python Worker]                                   [브라우저 대시보드]
  ├─ OpenCV RTSP 수신                               (React + WebSocket)
  ├─ 프레임 샘플링 (5fps)
  ├─ yolo11m PPE 감지 + ByteTrack 추적
  ├─ yolo11s-pose 쓰러짐 감지 (교대 실행)
  ├─ 이벤트 판정 엔진
  └─ annotated 프레임 → go2rtc 재발행
           |
           v
     [Redis Pub/Sub]
           |
     +-----+-----+
     |     |      |
  WebSocket 카카오  SMS
  대시보드  알림톡  문자
```

**하드웨어:** Jetson Orin NX 1대 또는 GPU 서버 1대
**예상 성능:** 카메라당 5fps, PPE+쓰러짐 교대 감지, 추적 ID 부여
**구현 난이도:** 중간 (4-6주)
**비용:** Jetson Orin NX ~$500 + go2rtc 무료 + Redis 무료

### 6.2 중규모 (10-50대 카메라) — DeepStream 하이브리드

```
[IP Camera 10~50]
      |
      | RTSP
      v
[NVIDIA DeepStream Pipeline]
  ├─ nvstreammux (다중 스트림 배치)
  ├─ nvinfer: PPE 감지 (TensorRT FP16/INT8)
  ├─ nvtracker: ByteTrack (배치 추적)
  ├─ nvinfer: Pose 추정 (TensorRT, 2차 추론)
  ├─ Python Probe: 쓰러짐 판정 + 이벤트 생성
  └─ nvosd: 바운딩박스/스켈레톤 오버레이
      |                              |
      | RTSP 출력                    | 메타데이터 (JSON)
      v                              v
  [go2rtc]                    [Python 서비스 (FastAPI)]
      |                         ├─ Redis 이벤트 큐
      | WebRTC                  ├─ WebSocket 대시보드
      v                         ├─ 알림 디스패처
  [브라우저]                     ├─ 에스컬레이션 엔진
                                └─ DB 로깅 (PostgreSQL)
```

**하드웨어:** Jetson AGX Orin 2-4대 또는 dGPU 서버 1-2대
**예상 성능:** 카메라당 3-5fps, 배치 추론으로 GPU 효율 극대화
**구현 난이도:** 높음 (8-12주, DeepStream 학습 곡선 포함)
**비용:** Jetson AGX Orin ~$2,000 × 3 = $6,000 또는 dGPU 서버

### 6.3 아키텍처 비교

| 항목 | 소규모 (Python-First) | 중규모 (DeepStream) |
|------|---------------------|-------------------|
| **카메라 수** | 1-5대 (최대 8대) | 10-50대 |
| **GPU 활용** | Ultralytics 직접 추론 | TensorRT 배치 추론 |
| **추적** | Ultralytics model.track() | DeepStream nvtracker |
| **스트리밍** | go2rtc + OpenCV | DeepStream + go2rtc |
| **알림** | Redis Pub/Sub + FastAPI | Redis Streams + FastAPI |
| **코드 복잡도** | 순수 Python | Python + GStreamer + DeepStream config |
| **구현 기간** | 4-6주 | 8-12주 |
| **확장성** | 제한적 | 우수 |
| **디버깅** | 쉬움 | 어려움 |

---

## 7. 구현 로드맵

### 7.1 Phase 1: 추적 + RTSP 연동 (2-3주)

| 작업 | 설명 | 예상 기간 |
|------|------|----------|
| ByteTrack 추적 통합 | `model.track()` 적용, 트랙 ID 관리 | 3일 |
| go2rtc 설정 | RTSP 프록시 + WebRTC 출력 구성 | 2일 |
| RTSP 입력 연동 | OpenCV → go2rtc RTSP 읽기 | 3일 |
| 프레임 샘플링 | 5fps 샘플링 + 프레임 교대 처리 | 2일 |
| annotated 스트림 재발행 | 감지 결과 시각화 → go2rtc로 발행 | 3일 |

### 7.2 Phase 2: 이벤트 + 알림 (2-3주)

| 작업 | 설명 | 예상 기간 |
|------|------|----------|
| 이벤트 판정 엔진 | 연속 프레임 + 구역 규칙 기반 판정 | 4일 |
| Redis 이벤트 큐 | Redis Pub/Sub + Streams 설정 | 2일 |
| WebSocket 대시보드 | FastAPI + WebSocket 이벤트 스트리밍 | 4일 |
| 카카오 알림톡 연동 | CoolSMS/NHN Cloud API 통합 | 3일 |
| 에스컬레이션 규칙 | 미확인 이벤트 자동 상위 알림 | 2일 |

### 7.3 Phase 3: 엣지 최적화 (2-3주)

| 작업 | 설명 | 예상 기간 |
|------|------|----------|
| TensorRT 변환 | yolo11m + yolo11s-pose FP16 export | 2일 |
| Jetson 배포 테스트 | Jetson Orin NX에서 성능 검증 | 3일 |
| INT8 양자화 | 캘리브레이션 + 정확도 검증 | 3일 |
| 멀티카메라 부하 테스트 | 3-5대 카메라 동시 처리 성능 측정 | 3일 |

### 7.4 Phase 4: 중규모 확장 (4-6주, 선택)

| 작업 | 설명 | 예상 기간 |
|------|------|----------|
| DeepStream 파이프라인 | GStreamer + nvinfer + nvtracker 구성 | 2주 |
| 배치 추론 최적화 | nvstreammux 배치 사이즈 튜닝 | 1주 |
| 멀티노드 구성 | 여러 Jetson/서버 분산 처리 | 1-2주 |

---

## 부록: 참고 자료

### 객체 추적
- [Ultralytics YOLO Tracking 문서](https://docs.ultralytics.com/modes/track/)
- [ByteTrack YAML 설정](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/bytetrack.yaml)
- [BoT-SORT GitHub](https://github.com/NirAharon/BoT-SORT)
- [OC-SORT GitHub](https://github.com/noahcao/OC_SORT)
- [YOLOv8 ByteTrack vs BoT-SORT 비교](https://medium.com/pixelmindx/ultralytics-yolov8-object-trackers-botsort-vs-bytetrack-comparison-d32d5c82ebf3)
- [Object Tracking with YOLO and ByteTrack/BoT-SORT](https://visionbrick.com/object-tracking-with-yolo-and-bytetrack-bot-sort-trackers/)

### 엣지 배포
- [Ultralytics YOLO Export 문서](https://docs.ultralytics.com/modes/export/)
- [Ultralytics YOLO Jetson 가이드](https://docs.ultralytics.com/guides/nvidia-jetson/)
- [NVIDIA Jetson 벤치마크](https://developer.nvidia.com/embedded/jetson-benchmarks)
- [YOLO11 Jetson Orin Nano 성능](https://www.ultralytics.com/blog/ultralytics-yolo11-on-nvidia-jetson-orin-nano-super-fast-and-efficient)
- [YOLO26 양자화 벤치마크](https://arxiv.org/html/2509.25164v3)
- [추론 엔진 비교 연구 (2025)](https://www.mdpi.com/2079-9292/14/15/2977)
- [CoreML YOLO11 배포](https://www.ultralytics.com/blog/bringing-ultralytics-yolo11-to-apple-devices-via-coreml)

### 멀티카메라
- [NVIDIA DeepStream SDK](https://developer.nvidia.com/deepstream-sdk)
- [DeepStream 멀티카메라 IVA](https://developer.nvidia.com/blog/multi-camera-large-scale-iva-deepstream-sdk/)
- [DeepStream nvtracker 문서](https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_plugin_gst-nvtracker.html)
- [NVIDIA AI 멀티카메라 추적](https://www.nvidia.com/en-us/use-cases/ai-powered-multi-camera-tracking/)
- [DeepStream + Ultralytics YOLO Jetson 가이드](https://docs.ultralytics.com/guides/deepstream-nvidia-jetson/)
- [Ray 배치 비디오 추론](https://docs.ray.io/en/latest/ray-overview/examples/object-detection/3.video_processing_batch_inference.html)

### 알림 파이프라인
- [Redis 알림 서비스 구축](https://redis.io/blog/how-to-create-notification-services-with-redis-websockets-and-vue-js/)
- [Django + WebSocket + Redis 실시간 알림](https://medium.com/@yogeshkrishnanseeniraj/real-time-notifications-at-scale-django-websockets-redis-pub-sub-s3-event-pipelines-191a9305299b)
- [CoolSMS Python SDK (카카오 알림톡)](https://pypi.org/project/coolsms_python_sdk/)
- [카카오 알림톡 API 문서](https://docs.kakaoi.ai/kakao_i_connect_message/bizmessage_eng/api/api_reference/at/)
- [NHN Cloud 카카오 알림톡](https://docs.nhncloud.com/en/Notification/KakaoTalk%20Bizmessage/en/alimtalk-overview/)

### 영상 스트리밍 (별도 문서)
- [video-streaming-framework.md](./video-streaming-framework.md) — go2rtc, MediaMTX, DeepStream, LiveKit 등 상세 비교
