"""Watch Tower 경로 설정.

모든 대용량 데이터 경로를 WATCH_TOWER_DATA_ROOT 환경변수로 제어한다.
환경변수 미설정 시 기본값 사용.

디렉토리 구조:
    DATA_ROOT/
    ├── samples/       # PoC 영상, 테스트 이미지
    ├── models/        # 모델 가중치 (.pt, .onnx, .engine)
    ├── outputs/       # 추론 결과
    ├── dataset/       # ultralytics 데이터셋
    └── experiments/   # 실험 결과 (YYYY-MM-DD-주제/)
"""

import os
from pathlib import Path

DATA_ROOT = Path(
    os.environ.get("WATCH_TOWER_DATA_ROOT", "/home/neo/share/watch-tower_data")
)

SAMPLES_DIR = DATA_ROOT / "samples"
MODELS_DIR = DATA_ROOT / "models"
OUTPUTS_DIR = DATA_ROOT / "outputs"
DATASET_DIR = DATA_ROOT / "dataset"
EXPERIMENTS_DIR = DATA_ROOT / "experiments"
