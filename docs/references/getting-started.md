# 시작하기

상세 환경 정보는 [dev-environment.md](dev-environment.md) 참조.

## 전제 조건

- Python 3.12 (uv가 자동 설치)
- NVIDIA GPU + CUDA 12.x
- uv ([설치 안내](https://docs.astral.sh/uv/getting-started/installation/))

## 설치 & 실행

```bash
# 1. 의존성 설치 (Python 3.12 + .venv + 패키지)
uv sync --extra dev

# 2. GPU 확인
uv run python -c "import torch; print(torch.cuda.is_available())"
# → True

# 3. 추론 테스트
uv run python scripts/run_inference.py
```

## 확인

- [ ] `uv sync` 정상 완료
- [ ] `torch.cuda.is_available()` → True
- [ ] `scripts/run_inference.py` 실행 시 감지 결과 출력
