## Context

P2-1에서 Construction-PPE 데이터셋으로 Person Detection 정량 평가를 완료했다(조건부 Go). 이제 건설 현장 CCTV 영상 3개에 Detection + ByteTrack을 적용하여 정성 평가를 수행한다.

샘플 영상:
- `construction_helmets.avi` — PoC 기존 영상
- `construction_subway_cctv.mp4` — 지하철 건설현장 CCTV
- `construction_tower_crane_cctv.mp4` — 타워 크레인 건설현장 CCTV

## Goals / Non-Goals

**Goals:**
- `model.track()` + ByteTrack으로 영상에서 사람 감지 + 추적
- supervision으로 bbox, track ID, 궤적을 오버레이한 결과 영상 생성
- Detection 실패 케이스 파악 (어떤 사람을 놓치는지)
- Tracking 안정성 확인 (ID 유지, 가림 복귀, 교차 시 스왑)
- Go/No-Go 정성 판단

**Non-Goals:**
- 정량 Tracking 벤치마크 (MOTA/IDF1)
- FiftyOne 도구 사용
- 파인튜닝, 모델 개선

## Decisions

### 1. 추적 방식: `model.track(source, tracker="bytetrack.yaml")`

ultralytics 내장 ByteTrack을 사용. 별도 라이브러리 설치 불필요.

대안: BoT-SORT → ByteTrack이 No-Go일 때 대안으로 시도.

### 2. 시각화: supervision 라이브러리

- `BoundingBoxAnnotator` — bbox
- `LabelAnnotator` — track ID + 클래스명
- `TraceAnnotator` — 이동 궤적

대안: ultralytics 내장 plot() → 궤적 표시 불가, 커스터마이징 제한적.

### 3. 결과 저장: `outputs/tracking/`

결과 영상과 실패 케이스 기록을 함께 저장.

### 4. Detection 실패 케이스도 함께 분석

P2-1에서 Recall 79.5%로 경계선이었으므로, 영상에서 놓치는 사람의 패턴을 시각적으로 확인한다. 별도 스크립트 없이 결과 영상을 눈으로 확인.

## Risks / Trade-offs

- **영상에 사람이 적을 수 있음**: 샘플 영상 3개 중 사람이 잘 안 보이는 영상이 있을 수 있음 → 해당 영상은 평가 대상에서 제외
- **ByteTrack 파라미터**: 기본값으로 시작, 불안정하면 파라미터 튜닝 시도
