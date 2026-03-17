## Why

P2-1에서 Person Detection 정량 평가(mAP@50=78.7%, Recall=79.5%)를 완료했다. 이제 건설 현장 영상에서 Detection + ByteTrack을 함께 실행하여 실제 환경에서의 감지/추적 품질을 시각적으로 검증해야 한다. 정량 수치로는 알 수 없는 "어떤 상황에서 실패하는지"를 파악하는 것이 목적이다.

## What Changes

- Detection + ByteTrack 추적 스크립트 추가 (`scripts/run_tracking.py`)
- supervision 시각화 (bbox + track ID + 궤적) 결과 영상 생성
- Detection 실패 케이스 및 Tracking 안정성 분석
- Go/No-Go 정성 판단 및 문서화

## Capabilities

### New Capabilities

- `detection-tracking-eval`: 건설 현장 영상에서 Detection + Tracking을 실행하고 결과 영상을 생성하여 정성 평가한다

### Modified Capabilities

(없음)

## Impact

- `scripts/`: 추적 스크립트 추가
- `outputs/`: 결과 영상 저장
- `experiments/`: 정성 평가 결과 기록
- 의존성 변경 없음 (ultralytics, supervision 기존 설치)
