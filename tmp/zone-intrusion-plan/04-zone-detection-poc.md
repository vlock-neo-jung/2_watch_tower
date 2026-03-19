# Step 4: Zone 침입 감지 PoC 스크립트

## 이 단계가 왜 필요한가

Step 1~3은 개별 조각을 준비한 것이다.
이 단계에서 **모든 조각을 조립**하여 실제로 영상에서 zone 침입을 감지하는 파이프라인을 만든다.

```
영상 입력 → YOLO 사람 감지 → ByteTrack 추적 → Zone 판정 → 이벤트 판정 → 결과 출력
             (Layer 1)        (Layer 2)       (Layer 3)    (Layer 4)
```

기존 `run_tracking.py`가 Layer 1+2까지 하고 있으므로, 여기에 Layer 3+4를 추가하는 것이다.

## 파이프라인 상세

### Layer 3: Zone 판정 (PolygonZone)

매 프레임마다:
1. YOLO가 사람 bbox를 반환한다
2. ByteTrack이 각 사람에게 track_id를 부여한다
3. **PolygonZone.trigger()** 로 각 사람의 foot point가 zone 안인지 판정한다

```python
# 프레임당 처리 (핵심 로직)
detections = sv.Detections.from_ultralytics(results)
is_in_zone = polygon_zone.trigger(detections)
# is_in_zone = [False, True, False]  ← 3명 중 2번째만 zone 안
```

이 시점에서 "프레임 N에서 track_id 7이 zone 안에 있다"는 정보가 나온다.

### Layer 4: 이벤트 판정 (Temporal Logic)

**단일 프레임 판정만으로는 실제 알림을 보내면 안 된다.**
이유:

1. **감지 깜빡임**: 같은 사람이 프레임마다 감지됐다 안 됐다 할 수 있다
2. **경계선 흔들림**: foot point가 경계 근처에서 안/밖을 오갈 수 있다
3. **순간 통과**: 사람이 zone 모서리를 스치고 지나가는 것은 실제 침입이 아닐 수 있다

따라서 **track_id별로 상태를 누적**한다:

```
track_id 7의 상태 추적:

프레임 100: zone 밖 → 상태: outside
프레임 101: zone 안 → 연속 1프레임
프레임 102: zone 안 → 연속 2프레임
프레임 103: zone 안 → 연속 3프레임 → ★ 이벤트 발생! (min_consecutive_frames=3)
프레임 104: zone 안 → 이벤트 진행 중 (추가 알림 없음, cooldown)
...
프레임 200: zone 밖 → 상태: outside, 이벤트 종료
```

이 로직을 담당하는 `ZoneTracker` 클래스가 필요하다.

### ZoneTracker의 역할

```python
class ZoneTracker:
    """track_id별 zone 체류 상태를 관리한다."""

    def update(self, track_id, is_in_zone, frame_number) -> Event | None:
        """
        매 프레임마다 호출.
        연속 프레임 조건을 만족하면 Event를 반환한다.
        """
```

각 track_id에 대해:
- `consecutive_count`: zone 안에 연속으로 있었던 프레임 수
- `last_event_frame`: 마지막 이벤트 발생 프레임 (cooldown 계산용)
- `state`: `outside` / `entering` / `inside`

### 시각화

결과 영상에 다음을 오버레이한다:
- zone 경계선 (polygon)
- zone 이름과 현재 인원 수
- zone 밖의 사람: 초록색 bbox
- zone 안의 사람: 빨간색 bbox
- 이벤트 발생 시: 경고 텍스트

```
   ┌─────────────────────────────────────┐
   │                                     │
   │    ┌──┐ Person #3                   │
   │    │녹│ (zone 밖)                   │
   │    └──┘                             │
   │         ╔══════════════════╗        │
   │         ║  크레인 작업 반경  ║        │
   │         ║  (위험구역)       ║        │
   │         ║   ┌──┐           ║        │
   │         ║   │적│ Person #7 ║        │
   │         ║   └──┘ ⚠ 침입!   ║        │
   │         ╚══════════════════╝        │
   └─────────────────────────────────────┘
```

## 스크립트 인터페이스

기존 스크립트(`run_tracking.py`, `eval_person_detection.py`)의 패턴을 따른다:

```bash
uv run python scripts/run_zone_detection.py \
  --source /home/neo/share/watch-tower_data/samples/construction_subway_cctv.mp4 \
  --model /home/neo/share/watch-tower_data/models/yolo11m.pt \
  --zone-config /home/neo/share/watch-tower_data/configs/zones/sample.yaml \
  --conf 0.25
```

### 출력물

1. **결과 영상**: `outputs/zone_detection/{영상명}_zone.mp4`
   - zone 오버레이, 침입 표시가 포함된 영상
   - 육안으로 "제대로 동작하는가" 확인 가능

2. **이벤트 로그**: `outputs/zone_detection/{영상명}_events.json`
   ```json
   {
     "events": [
       {
         "zone_id": "crane_area",
         "track_id": 7,
         "start_frame": 103,
         "end_frame": 200,
         "duration_frames": 97,
         "event_type": "intrusion"
       }
     ],
     "summary": {
       "crane_area": {"total_events": 3, "avg_duration_frames": 85}
     }
   }
   ```

3. **터미널 요약**:
   ```
   Zone: 크레인 작업 반경 (danger)
     이벤트: 3건
     평균 체류: 3.4초

   Zone: 굴착 주의 구역 (warning)
     이벤트: 1건
     평균 체류: 1.2초
   ```

## 파일 구조

```
scripts/
└── run_zone_detection.py    ← 메인 스크립트 (신규)
src/watch_tower/zone/
├── __init__.py
├── config.py                ← Step 2에서 작성
└── tracker.py               ← ZoneTracker 클래스 (신규)
```

## 완료 기준

- [ ] 샘플 영상에서 zone 오버레이가 포함된 결과 영상 생성
- [ ] zone 안의 사람이 빨간색으로 표시됨
- [ ] 이벤트 로그 JSON 생성
- [ ] min_consecutive_frames 설정이 동작함 (단일 프레임 감지는 이벤트가 아님)

## 이 단계의 산출물

- `scripts/run_zone_detection.py` — PoC 스크립트
- `src/watch_tower/zone/tracker.py` — ZoneTracker 클래스
- 결과 영상 + 이벤트 로그 JSON
