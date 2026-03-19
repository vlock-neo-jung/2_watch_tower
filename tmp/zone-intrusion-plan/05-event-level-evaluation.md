# Step 5: Event-level 정량 평가

## 이 단계가 왜 필요한가

Step 4에서 PoC가 동작하면 결과 영상을 볼 수 있다.
하지만 "보니까 잘 되는 것 같다"는 정성 평가일 뿐이다.

Phase 2에서 Person Detection을 평가할 때도 처음에는 결과 영상을 보는 정성 평가로 시작했지만,
결국 SODA 벤치마크를 돌려서 Recall 36.7%, F1 50.9% 같은 **숫자**를 얻어야 판단이 가능했다.

Zone 침입 감지도 마찬가지다. **"몇 건의 침입 중 몇 건을 감지했는가"** 를 숫자로 알아야
파인튜닝 모델을 적용했을 때 "이전보다 나아졌는가"를 비교할 수 있다.

## 평가 방법

### 입력

1. **시스템 출력**: Step 4의 이벤트 로그 (`events.json`)
   - 시스템이 감지한 침입 이벤트 목록 (zone_id, start_frame, end_frame)

2. **Ground Truth**: Step 3에서 만든 GT 파일
   - 사람이 직접 기록한 실제 침입 구간 목록

### 매칭 규칙

시스템 이벤트와 GT 이벤트를 어떻게 대응시킬 것인가:

```
GT 이벤트:     |----침입 1----|        |---침입 2---|     |--침입 3--|
시스템 이벤트:    |--감지 A--|           (없음)         |감지 C|  |감지 D|

매칭 결과:
  GT 침입 1 ↔ 감지 A → 겹침 있음 → TP
  GT 침입 2 ↔ (없음)  → 미감지   → FN
  GT 침입 3 ↔ 감지 C  → 겹침 있음 → TP (감지 D도 같은 GT에 매칭 → 중복 무시)
```

**규칙**:
- 시스템 이벤트의 구간이 GT 이벤트 구간과 **1프레임이라도 겹치면** 매칭 성공 (TP)
- 하나의 GT 이벤트에 여러 시스템 이벤트가 매칭될 수 있음 (1개라도 있으면 TP)
- GT 이벤트와 매칭되지 않는 시스템 이벤트는 FP (오탐)
- 시스템 이벤트가 없는 GT 이벤트는 FN (미탐)

### 메트릭

| 메트릭 | 계산 | 의미 |
|--------|------|------|
| **Event Detection Rate (EDR)** | TP / (TP + FN) | GT 침입 중 시스템이 감지한 비율 |
| **False Alarm Count** | FP 개수 | GT에 없는 침입을 시스템이 감지한 횟수 |
| **Event Precision** | TP / (TP + FP) | 시스템이 감지한 것 중 실제 침입인 비율 |
| **Event F1** | 2 × P × R / (P + R) | Precision과 EDR의 조화평균 |
| **Response Time** | 시스템 감지 시작 - GT 침입 시작 | 침입 후 감지까지 걸리는 시간 |

### 구체적 예시

```
GT 이벤트 5건, 시스템 이벤트 6건

TP = 4 (GT 5건 중 4건 감지)
FN = 1 (GT 5건 중 1건 놓침)
FP = 2 (시스템 6건 중 2건은 GT에 없음)

EDR (Recall)  = 4/5 = 80%
Precision     = 4/6 = 67%
F1            = 2 × 0.80 × 0.67 / (0.80 + 0.67) = 73%

Response Time (TP 이벤트 평균):
  이벤트 1: GT 시작 프레임 150, 시스템 감지 프레임 155 → 5프레임 (1초@5fps)
  이벤트 2: GT 시작 프레임 520, 시스템 감지 프레임 528 → 8프레임 (1.6초)
  평균 응답 시간: 6.5프레임 (1.3초)
```

## 스크립트 구조

기존 `eval_person_detection.py`의 패턴을 따른다:

```bash
uv run python scripts/eval_zone_intrusion.py \
  --events outputs/zone_detection/construction_subway_cctv_events.json \
  --gt /home/neo/share/watch-tower_data/zone_gt/test_zone_01.json
```

### 핵심 함수

```python
def match_events(system_events, gt_events) -> dict:
    """시스템 이벤트와 GT 이벤트를 매칭하여 TP/FP/FN 계산"""

def compute_metrics(match_result) -> dict:
    """EDR, Precision, F1, Response Time 계산"""

def judge(metrics) -> dict:
    """Go/No-Go 임계값 대비 판정"""

def save_report(metrics, judgment, output_dir) -> Path:
    """Markdown + JSON 리포트 저장"""
```

### 출력 리포트 예시

```markdown
# Zone Intrusion 평가 리포트

## 요약
| 메트릭 | 값 | 목표 | 판정 |
|--------|-----|------|------|
| Event Detection Rate | 80% | ≥ 80% | PASS |
| False Alarm Count | 2건 | ≤ 2건/zone | PASS |
| Event F1 | 73% | ≥ 75% | FAIL |
| 평균 Response Time | 1.3초 | ≤ 2초 | PASS |

## Go/No-Go: Conditional
- EDR, Response Time은 목표 달성
- F1이 목표 미달 → FP(오탐) 감소 필요
- 권장: min_consecutive_frames를 3→5로 올려서 재측정

## 이벤트별 상세
| GT # | GT 구간 | 시스템 감지 | 결과 | 응답 시간 |
|------|---------|-----------|------|----------|
| 1 | 150-300 | 155-295 | TP | 5프레임 |
| 2 | 520-580 | - | FN | - |
| 3 | 820-950 | 825-940 | TP | 5프레임 |
```

## 파인튜닝 모델 도착 후

이 평가 스크립트의 가장 큰 가치는 **모델을 바꿔 끼우고 재측정**할 수 있다는 것이다:

```bash
# 1. baseline 모델로 PoC 실행
uv run python scripts/run_zone_detection.py --model yolo11m.pt ...

# 2. 평가
uv run python scripts/eval_zone_intrusion.py --events baseline_events.json --gt gt.json

# 3. 파인튜닝 모델로 같은 PoC 실행
uv run python scripts/run_zone_detection.py --model yolo11m-soda-finetuned.pt ...

# 4. 같은 평가
uv run python scripts/eval_zone_intrusion.py --events finetuned_events.json --gt gt.json

# 5. 비교: EDR 80% → 90%? 파인튜닝 효과 확인!
```

## 완료 기준

- [ ] `eval_zone_intrusion.py` 작성
- [ ] GT와 이벤트 로그를 매칭하여 메트릭 산출
- [ ] Markdown + JSON 리포트 생성
- [ ] Go/No-Go 판정 로직 동작 확인

## 이 단계의 산출물

- `scripts/eval_zone_intrusion.py` — 평가 스크립트
- `DATA_ROOT/experiments/{date}-zone-intrusion-eval/report.md` — 평가 리포트
- `DATA_ROOT/experiments/{date}-zone-intrusion-eval/results.json` — 수치 결과
