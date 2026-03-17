## 1. Python 프로젝트 초기화

- [x] 1.1 .python-version 파일 생성 (3.12 지정)
- [x] 1.2 ~~uv python install 3.12 실행~~ (uv sync에서 자동 처리)
- [x] 1.3 pyproject.toml 작성 (메타데이터, 기본 의존성, dev 의존성, [tool.uv] PyTorch cu121 인덱스)
- [x] 1.4 src/watch_tower/__init__.py 생성
- [x] 1.5 src/watch_tower/detection/__init__.py 생성
- [x] 1.6 src/watch_tower/utils/__init__.py 생성

## 2. 의존성 설치 및 환경 구성

- [x] 2.1 uv sync --extra dev 실행하여 전체 의존성 설치
- [x] 2.2 설치 오류 발생 시 해결 (hatchling.backends → hatchling.build 수정)

## 3. GPU/CUDA 환경 검증

- [x] 3.1 torch.cuda.is_available() → True 확인
- [x] 3.2 torch.cuda.get_device_name(0) → RTX 3080 Ti 확인
- [x] 3.3 ultralytics YOLO 모델 로드 (yolo11n.pt) + device="cuda" 추론 테스트
- [x] 3.4 GPU 추론 결과 정상 반환 (5객체 감지, GPU 메모리 42.1MB 사용)
