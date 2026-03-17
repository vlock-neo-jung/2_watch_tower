## Context

FWY-43에서 Python 프로젝트 구조(pyproject.toml, src layout)와 GPU 환경이 구축된 상태. 다음 단계(FWY-45 Smoke Test, Phase 2 모델 검증)를 진행하려면 데이터/모델/실험 관리 체계와 테스트 인프라가 필요하다. 1인 개발이므로 과하지 않은 최소 구조를 목표로 한다.

## Goals / Non-Goals

**Goals:**
- Phase 2 모델 검증 결과를 구조적으로 기록할 수 있는 체계
- 모델 가중치를 재현 가능하게 관리
- pytest로 기본 테스트를 실행할 수 있는 인프라

**Non-Goals:**
- DVC, W&B, MLflow 등 외부 MLOps 도구 도입
- FiftyOne 설치/설정
- CI/CD 파이프라인
- 대규모 데이터셋 버전 관리

## Decisions

### 1. 데이터셋 경로: ultralytics 설정 변경
- 경로: `/home/neo/toy-project/workspace_watch-tower/dataset/`
- `ultralytics.settings.update({"datasets_dir": "..."})`로 설정
- 프로젝트 내 `data/samples/`는 PoC 영상/이미지 등 수동 관리 파일 전용
- 대안 검토: 프로젝트 내부(data/datasets/)에 두는 방식 → 불필요한 설정 변경 없이 기본 경로를 쓰되, 사용자가 workspace 경로를 원하므로 설정 변경 채택

### 2. 모델 관리: huggingface_hub 다운로드 스크립트
- `scripts/download_models.py`에서 `huggingface_hub.hf_hub_download()` 사용
- `models/` 디렉토리에 저장, `models/README.md`에 모델 목록/출처 기록
- ultralytics 기본 모델(yolo11n.pt 등)은 자동 다운로드되므로 스크립트 불포함
- 대안 검토: 수동 curl 명령 → 재현성이 떨어지므로 스크립트 채택

### 3. 실험 기록: 디렉토리 + README.md
- `experiments/YYYY-MM-DD-주제/README.md` 한 파일에 설정+결과+분석 통합
- `experiments/YYYY-MM-DD-주제/outputs/`에 결과 파일 저장
- 대안 검토: config.yaml 분리, 별도 메타데이터 → 1인 개발에 오버헤드

### 4. 테스트: pytest 인프라만 세팅
- `tests/conftest.py`에 공통 fixture (프로젝트 루트 경로 등)
- `tests/test_smoke.py`에 패키지 임포트 확인 테스트
- 실질적인 detection/tracking 테스트는 Phase 2 코드와 함께 추가
- 대안 검토: GPU 테스트 포함 → FWY-45(Smoke Test)에서 처리하므로 여기서는 제외

## Risks / Trade-offs

- **[ultralytics 설정이 전역]** → datasets_dir 변경이 다른 ultralytics 프로젝트에도 영향. 단, 현재 이 프로젝트만 사용하므로 문제 없음.
- **[experiments/ 구조가 느슨함]** → 기록 형식이 강제되지 않아 일관성이 깨질 수 있음. 1인 개발에서는 본인이 규칙을 지키면 충분.
