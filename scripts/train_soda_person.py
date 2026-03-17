"""SODA Person Detection 파인튜닝 스크립트.

COCO pretrained yolo11m을 SODA 건설현장 데이터로 파인튜닝한다.
2단계 학습: Stage 1(헤드만) → Stage 2(전체).

사용법:
    # Stage 1: 헤드만 학습 (약 5~8시간)
    uv run python scripts/train_soda_person.py --stage 1

    # Stage 2: 전체 학습 (약 30~50시간)
    uv run python scripts/train_soda_person.py --stage 2

    # 한 번에 Stage 1 → Stage 2 순차 실행
    uv run python scripts/train_soda_person.py --stage all
"""

import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO

from watch_tower.config import DATASET_DIR, EXPERIMENTS_DIR, MODELS_DIR

DATA_YAML = DATASET_DIR / "soda" / "yolo" / "soda-person.yaml"
BASE_MODEL = "yolo11m.pt"  # COCO pretrained (자동 다운로드)
PROJECT_DIR = EXPERIMENTS_DIR / "soda-finetune"
FINAL_MODEL = MODELS_DIR / "yolo11m-soda-person.pt"


def stage1() -> Path:
    """Stage 1: 백본 동결, 헤드만 학습."""
    print("=" * 60)
    print("Stage 1: 헤드만 학습 (freeze=10, 50 epochs)")
    print("=" * 60)

    model = YOLO(BASE_MODEL)
    model.train(
        data=str(DATA_YAML),
        imgsz=1280,
        epochs=50,
        batch=4,
        freeze=10,
        project=str(PROJECT_DIR),
        name="stage1",
        exist_ok=True,
        # 증강
        mosaic=1.0,
        close_mosaic=10,
        flipud=0.5,
        scale=0.9,
        copy_paste=0.3,
    )

    best = PROJECT_DIR / "stage1" / "weights" / "best.pt"
    print(f"\nStage 1 완료: {best}")
    return best


def stage2(stage1_weights: Path | None = None) -> Path:
    """Stage 2: 전체 네트워크 학습."""
    if stage1_weights is None:
        stage1_weights = PROJECT_DIR / "stage1" / "weights" / "best.pt"

    if not stage1_weights.exists():
        print(f"Stage 1 가중치를 찾을 수 없음: {stage1_weights}")
        print("먼저 --stage 1을 실행하세요.")
        raise SystemExit(1)

    print("=" * 60)
    print("Stage 2: 전체 학습 (lr0=0.001, 200 epochs)")
    print(f"시작 가중치: {stage1_weights}")
    print("=" * 60)

    model = YOLO(str(stage1_weights))
    model.train(
        data=str(DATA_YAML),
        imgsz=1280,
        epochs=200,
        batch=4,
        lr0=0.001,
        cos_lr=True,
        patience=50,
        project=str(PROJECT_DIR),
        name="stage2",
        exist_ok=True,
        # 증강
        mosaic=1.0,
        close_mosaic=20,
        flipud=0.5,
        scale=0.9,
        copy_paste=0.3,
    )

    best = PROJECT_DIR / "stage2" / "weights" / "best.pt"
    print(f"\nStage 2 완료: {best}")
    return best


def save_final(weights_path: Path) -> None:
    """최종 가중치를 models/에 복사한다."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(weights_path, FINAL_MODEL)
    print(f"최종 모델 저장: {FINAL_MODEL}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SODA Person Detection 파인튜닝")
    parser.add_argument("--stage", default="all", choices=["1", "2", "all"],
                        help="학습 단계 (1: 헤드만, 2: 전체, all: 순차 실행)")
    args = parser.parse_args()

    if args.stage == "1":
        stage1()
    elif args.stage == "2":
        best = stage2()
        save_final(best)
    else:  # all
        stage1_best = stage1()
        stage2_best = stage2(stage1_best)
        save_final(stage2_best)


if __name__ == "__main__":
    main()
