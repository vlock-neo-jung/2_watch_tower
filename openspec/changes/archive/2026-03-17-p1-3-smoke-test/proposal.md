## Why

Phase 1(개발환경 구성)의 마지막 검증 게이트. 프로젝트 모델(yolo11m-construction-hazard)로 건설 현장 영상에 대해 end-to-end 추론이 동작하는지 확인해야 Phase 2에 진입할 수 있다.

## What Changes

- 모델 다운로드 실행 (scripts/download_models.py)
- ultralytics 설정 실행 (scripts/setup_settings.py)
- 추론 스크립트 작성 (scripts/run_inference.py)
- 샘플 영상/이미지에 대해 GPU 추론 → 결과 저장

## Capabilities

### New Capabilities
- `smoke-test-inference`: 프로젝트 모델로 샘플 데이터에 대해 end-to-end GPU 추론을 실행하고 결과를 저장

### Modified Capabilities

(없음)

## Impact

- 신규 파일: scripts/run_inference.py
- 신규 디렉토리: outputs/
- 모델 다운로드: models/yolo11m-construction-hazard.pt (39MB, gitignore)
- 의존: scripts/download_models.py, scripts/setup_settings.py (FWY-44에서 생성)
