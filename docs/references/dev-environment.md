# 개발 환경 설정

**작성일:** 2026-03-17
**대상:** FWY-43 (P1-1: 프로젝트 초기화 + GPU 환경 구성)

---

## 1. 하드웨어

| 항목 | 값 |
|------|-----|
| OS | WSL2 / Ubuntu 22.04.3 LTS |
| GPU | NVIDIA GeForce RTX 3080 Ti (12GB VRAM) |
| GPU Driver | 560.94 |
| CUDA (nvcc) | 12.1 |

## 2. 소프트웨어 환경

| 항목 | 값 |
|------|-----|
| Python | 3.12.9 (.python-version으로 고정) |
| 패키지 관리 | uv 0.6.3 |
| 가상환경 | .venv/ (uv 자동 관리) |
| Git | 2.53.0 |
| Docker | 28.0.1 (현 단계에서 미사용) |

## 3. 핵심 패키지 버전

| 패키지 | 버전 | 용도 |
|--------|------|------|
| torch | 2.10.0+cu128 | GPU 연산, 모델 학습/추론 |
| ultralytics | 8.4.23 | YOLO 모델 학습/추론/변환 |
| supervision | 0.27.0 | Zone 감지, 카운팅, bbox 시각화 |
| opencv-python-headless | 4.13.0 | 영상 처리 |
| huggingface-hub | 1.7.1 | 모델 다운로드/관리 |
| pytest | 9.0.2 | 테스트 |
| ruff | 0.15.6 | Linter/Formatter |

## 4. 설계 결정

| # | 결정 | 이유 |
|---|------|------|
| 1 | Python 3.12 | PyTorch, ultralytics, supervision 공식 지원 범위. 시스템 3.13과 uv로 분리 |
| 2 | PyTorch cu128 | 설계 시 cu121 목표였으나 uv가 PyPI에서 최신 호환 빌드 설치. GPU 동작 정상 확인 |
| 3 | uv 인덱스 통합 | pyproject.toml [tool.uv]에 PyTorch CUDA 인덱스 설정. `uv sync` 한 번으로 완결 |
| 4 | 의존성 2그룹 | core+gpu 통합 / dev 분리. 항상 GPU 사용하는 1인 개발 환경에 적합 |
| 5 | src layout | src/watch_tower/ 구조. 모듈은 필요할 때 추가 (현재: detection/, utils/) |

## 5. 프로젝트 구조

```
watch-tower/                          ← git repo (코드만)
├── .python-version
├── pyproject.toml
├── src/watch_tower/
│   ├── __init__.py
│   ├── config.py                     # DATA_ROOT 환경변수 기반 경로 관리
│   ├── detection/
│   └── utils/
├── scripts/                          # 실행 스크립트
├── tests/
├── models/README.md                  # 모델 목록 문서 (가중치는 외부)
├── docs/
└── .venv/                            # 가상환경 (gitignore)

/home/neo/share/watch-tower_data/     ← 대용량 데이터 (프로젝트 외부)
├── samples/                          # PoC 영상/이미지
├── models/                           # 모델 가중치
├── outputs/                          # 추론 결과
├── dataset/                          # ultralytics 데이터셋
└── experiments/                      # 실험 결과
```

경로 설정: 환경변수 `WATCH_TOWER_DATA_ROOT` (기본값: `/home/neo/share/watch-tower_data`)

## 6. 환경 설정 방법

```bash
# 1. uv 설치 (이미 있으면 생략)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 의존성 설치 (Python 3.12 자동 다운로드 + .venv 생성 + 패키지 설치)
uv sync --extra dev

# 3. GPU 확인
uv run python -c "import torch; print(torch.cuda.is_available())"
# → True

# 4. YOLO 추론 확인
uv run python -c "
from ultralytics import YOLO
model = YOLO('yolo11n.pt')
results = model.predict(source='https://ultralytics.com/images/bus.jpg', device='cuda', verbose=False)
print(f'감지 객체: {len(results[0].boxes)}개')
"
# → 감지 객체: 5개
```

## 7. GPU 검증 결과

| 테스트 | 결과 |
|--------|------|
| torch.cuda.is_available() | True |
| torch.cuda.get_device_name(0) | NVIDIA GeForce RTX 3080 Ti |
| YOLO11n GPU 추론 | 5객체 감지 (bus 1, person 4) |
| GPU 메모리 사용 | 42.1 MB |
