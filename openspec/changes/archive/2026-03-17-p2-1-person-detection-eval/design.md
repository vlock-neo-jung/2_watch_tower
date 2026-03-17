## Context

Phase 1에서 프로젝트 구조, GPU 환경, Smoke Test가 완료되었다. 이제 yolo11m-construction-hazard 모델의 Person Detection 성능을 Construction-PPE 데이터셋으로 정량 평가한다. 이 결과가 Phase 2 전체의 Go/No-Go 기준이 된다.

현재 상태:
- 모델: `models/yolo11m-construction-hazard.pt` (확보 완료)
- 추론 스크립트: `scripts/run_inference.py` (Smoke Test용, 평가용 아님)
- 실험 기록: `experiments/` 디렉토리 존재하나 미사용

## Goals / Non-Goals

**Goals:**
- `model.val()`로 Construction-PPE 데이터셋 대상 Person Detection mAP@50, Recall 측정
- 클래스별 성능 분석 결과 기록
- Go/No-Go 판단 근거 문서화

**Non-Goals:**
- 다른 모델과의 비교 평가 (PoC에서 완료)
- Tracking 평가 (FWY-48에서 별도 진행)
- 파인튜닝 또는 모델 개선
- FiftyOne 등 추가 도구 도입

## Decisions

### 1. 평가 방식: `model.val()` 단일 호출

ultralytics의 `model.val(data="Construction-PPE.yaml")` 한 줄로 mAP, precision, recall, 클래스별 분석이 모두 나온다. 별도 평가 파이프라인 구축 불필요.

대안: FiftyOne으로 시각적 분석 → Phase 2에서는 불필요. Phase 4(PPE 파인튜닝) 시점에 재검토.

### 2. 데이터셋: Construction-PPE (Ultralytics 제공)

`model.val()` 호출 시 자동 다운로드. 별도 다운로드 스크립트 불필요.
- 1,416장 (train 1,132 / val 143 / test 141)
- 11개 클래스 (Person 포함)

대안: SODA 데이터셋 → leakage 의심(mAP > 95%) 시에만 독립 검증용으로 사용.

### 3. 결과 저장 위치: `experiments/YYYY-MM-DD-person-detection-eval/`

기존 실험 기록 구조(P1-2에서 확정) 그대로 사용. `model.val()`의 결과 디렉토리(`runs/`)와 별도로, 정리된 결과 요약을 experiments/에 기록한다.

### 4. 평가 스크립트 위치: `scripts/eval_person_detection.py`

기존 `scripts/run_inference.py`와 분리. 역할이 다르다(추론 vs 평가).

## Risks / Trade-offs

- **데이터 leakage**: 모델 학습 데이터와 Construction-PPE가 겹칠 가능성 → mAP > 95%이면 SODA로 재검증
- **val set 크기**: 143장으로 적은 편 → 현 단계에서는 수용. 통계적 신뢰도가 낮을 수 있음을 인지
- **Person 클래스만 평가**: 11개 클래스 중 Person만 Go/No-Go 대상 → 전체 결과는 기록하되 판단은 Person에 집중
