"""Smoke Test 추론 스크립트.

건설 현장 이미지/영상에 대해 YOLO 모델로 GPU 추론을 실행하고 결과를 저장한다.

사용법:
    uv run python scripts/run_inference.py --source /home/neo/share/watch-tower_data/samples/construction_workers_01.jpg
    uv run python scripts/run_inference.py --source /home/neo/share/watch-tower_data/samples/construction_helmets.mp4
"""

import argparse
from collections import Counter
from pathlib import Path

from ultralytics import YOLO

from watch_tower.config import MODELS_DIR, OUTPUTS_DIR

DEFAULT_MODEL = MODELS_DIR / "yolo11m-construction-hazard.pt"


def run(source: str, model_path: Path, output_dir: Path, conf: float) -> None:
    model_name = model_path.stem
    model_output_dir = output_dir / model_name
    model_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"모델: {model_path}")
    print(f"입력: {source}")
    print(f"출력: {model_output_dir}")
    print()

    model = YOLO(str(model_path))
    results = model.predict(
        source=source,
        device="cuda",
        conf=conf,
        save=True,
        project=str(model_output_dir),
        name="inference",
        exist_ok=True,
    )

    # 결과 요약
    class_counts: Counter[str] = Counter()
    total_frames = 0
    total_time_ms = 0.0

    for r in results:
        total_frames += 1
        total_time_ms += r.speed.get("inference", 0)
        for cls_id in r.boxes.cls:
            class_name = r.names[int(cls_id)]
            class_counts[class_name] += 1

    avg_ms = total_time_ms / total_frames if total_frames else 0

    print()
    print("=" * 50)
    print(f"프레임 수: {total_frames}")
    print(f"평균 추론 속도: {avg_ms:.1f}ms/frame ({1000/avg_ms:.1f} FPS)" if avg_ms > 0 else "")
    print()
    print("클래스별 감지 횟수:")
    for cls_name, count in class_counts.most_common():
        print(f"  {cls_name}: {count}")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(description="Watch Tower 추론 스크립트")
    parser.add_argument("--source", required=True, help="입력 이미지/영상 경로")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="모델 가중치 경로")
    parser.add_argument("--output", default=str(OUTPUTS_DIR), help="출력 디렉토리")
    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")
    args = parser.parse_args()

    run(
        source=args.source,
        model_path=Path(args.model),
        output_dir=Path(args.output),
        conf=args.conf,
    )


if __name__ == "__main__":
    main()
