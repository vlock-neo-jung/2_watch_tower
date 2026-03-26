# Watch Tower - 아키텍처

## 시스템 개요

건설 현장 실시간 AI 안전 모니터링 시스템. 카메라 영상을 YOLO 기반 모델로 분석하여 위험 상황을 감지하고 이벤트를 생성한다.

## 주요 컴포넌트

### 영상 수집 레이어
- 웹캠(USB) / IP카메라(RTSP) 입력
- 멀티 카메라 동시 처리

### AI 추론 레이어
- **Person Detection** — YOLO11 기반 사람 검출 + ByteTrack 추적
- **Zone 감지** (`src/watch_tower/zone/`) — PolygonZone 기반 위험구역 침입 감지, 구역 내 인원 카운팅
- **PPE 감지** (`src/watch_tower/ppe/`) — 보호구 착용 여부 판정, Zone×PPE 이중 판정 로직

### 이벤트 처리 레이어
- 이벤트 생성 및 저장
- 실시간 알림 (Push, SMS, 카카오 알림톡)

### 프레젠테이션 레이어
- 중앙 모니터링 대시보드 (웹 기반)
- 라이브 영상 + AI 오버레이
- 이벤트 타임라인 및 통계

## 데이터 흐름

```
카메라 → 영상 수집 → YOLO 추론 → Tracking → Zone/PPE 규칙 판정 → 이벤트 → 알림/대시보드
```

## 기술 스택

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.12 |
| 패키지 관리 | uv |
| 객체 검출 | ultralytics (YOLO11) |
| 후처리/시각화 | supervision (Zone, Counting, Annotator) |
| 영상 처리 | OpenCV |
| 모델 관리 | huggingface-hub |
| 데이터 모델 | Pydantic v2 |
| API (선택) | FastAPI + Uvicorn |
| 프론트엔드 | React (어노테이션 도구) |
| 테스트 | pytest + pytest-cov |
| 린터 | ruff |

## 배포 구조

> 추후 확정 예정. 현재는 로컬 WSL2 + RTX 3080 Ti 단일 머신에서 개발/검증 중.
