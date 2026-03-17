## Context

Watch Tower 프로젝트는 현재 문서만 존재하고 코드가 없는 상태이다. 개발 환경은 WSL2 / Ubuntu 22.04 / RTX 3080 Ti (12GB VRAM) / CUDA 12.x이며, 1인 개발로 진행한다. 이 change에서 Python 프로젝트 구조와 GPU 개발 환경을 구축하여 Phase 2(모델 검증) 진입이 가능한 상태를 만든다.

## Goals / Non-Goals

**Goals:**
- pyproject.toml 기반 프로젝트 구조 확립
- GPU에서 ultralytics YOLO 추론이 동작하는 환경 확보
- 후속 Phase에서 모듈을 점진적으로 추가할 수 있는 구조

**Non-Goals:**
- 데이터/모델/실험 관리 체계 (FWY-44에서 처리)
- 테스트 프레임워크 구성 (FWY-44에서 처리)
- Smoke Test (FWY-45에서 처리)
- Docker 컨테이너화
- CI/CD 파이프라인
- MLOps 도구 (DVC, W&B 등)

## Decisions

### 1. Python 3.12
- PyTorch, ultralytics, supervision 모두 3.12까지 공식 지원
- 시스템 Python은 3.13이지만 uv가 프로젝트별 Python 버전을 관리하므로 충돌 없음
- `.python-version` 파일로 고정

### 2. PyTorch cu121
- 로컬 nvcc 12.1과 일치
- 드라이버 560.94는 CUDA 12.6까지 지원하므로 하위 호환 OK
- cu124도 가능하지만, nvcc와 일치하는 cu121이 가장 안정적

### 3. pyproject.toml에 uv 인덱스 통합 (방식 A)
- `[tool.uv]` 섹션에 PyTorch CUDA 인덱스 URL 지정
- `uv sync` 한 번으로 GPU 환경 완결
- 별도 설치 스크립트 불필요 (1인 개발이므로)

### 4. 의존성 2그룹 (core+gpu / dev)
- 항상 GPU를 사용하므로 torch를 기본 의존성에 포함
- dev 그룹: pytest, ruff, ipykernel
- CI CPU-only 환경이 필요해지면 그때 그룹 분리

### 5. src layout + 필요할 때 모듈 추가
- `src/watch_tower/` 구조 채택
- FWY-43에서는 `detection/`, `utils/`만 생성
- `tracking/`, `zones/`는 Phase 2-3에서 추가

## Risks / Trade-offs

- **[Python 3.12 별도 설치 필요]** → uv python install 3.12로 해결. uv가 자동 관리.
- **[PyTorch CUDA 인덱스 의존]** → PyTorch 공식 인덱스가 안정적이므로 리스크 낮음. 오프라인 시 wheel 캐시 활용.
- **[ultralytics AGPL 라이선스]** → 현 단계(모델 검증)에서는 문제 없음. 상용화 시 Enterprise 라이선스 또는 대안 모델 검토 필요 (Phase 6에서 판단).
