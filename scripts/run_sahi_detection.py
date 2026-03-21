"""SAHI (Slicing Aided Hyper Inference) 적용 Detection 스크립트.

기존 YOLO 모델에 SAHI를 적용하여 소형 객체 탐지 성능을 검증한다.
이미지를 타일로 분할하여 각 타일에서 독립적으로 추론 후 NMS로 결과를 병합한다.

사용법:
    uv run python scripts/run_sahi_detection.py --source 영상.mp4
    uv run python scripts/run_sahi_detection.py --source 이미지.jpg --slice 640
    uv run python scripts/run_sahi_detection.py --source 영상.mp4 --model yolo11m.pt --no-sahi
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from sahi import AutoDetectionModel
from sahi.predict import get_prediction, get_sliced_prediction

from watch_tower.config import MODELS_DIR, OUTPUTS_DIR

DEFAULT_MODEL = MODELS_DIR / "yolo11m-construction-hazard.pt"
OUTPUT_DIR = OUTPUTS_DIR / "sahi"

PERSON_CLASS_NAMES = {"person", "Person"}


def create_model(model_path: Path, conf: float) -> AutoDetectionModel:
    return AutoDetectionModel.from_pretrained(
        model_type="ultralytics",
        model_path=str(model_path),
        confidence_threshold=conf,
        device="cuda:0",
    )


def run_on_image(
    image_path: str,
    model: AutoDetectionModel,
    output_dir: Path,
    slice_size: int,
    overlap: float,
    use_sahi: bool,
) -> dict:
    """단일 이미지에 SAHI 적용 후 결과를 저장한다."""
    if use_sahi:
        result = get_sliced_prediction(
            image=image_path,
            detection_model=model,
            slice_height=slice_size,
            slice_width=slice_size,
            overlap_height_ratio=overlap,
            overlap_width_ratio=overlap,
            perform_standard_pred=True,
            postprocess_type="GREEDYNMM",
            postprocess_match_threshold=0.5,
            postprocess_class_agnostic=False,
        )
    else:
        result = get_prediction(image=image_path, detection_model=model)

    # 결과 분석
    total = len(result.object_prediction_list)
    person_count = sum(
        1 for p in result.object_prediction_list
        if p.category.name in PERSON_CLASS_NAMES
    )

    # 결과 이미지 저장
    output_dir.mkdir(parents=True, exist_ok=True)
    name = Path(image_path).stem
    suffix = "sahi" if use_sahi else "normal"
    output_path = output_dir / f"{name}_{suffix}.jpg"
    result.export_visuals(export_dir=str(output_dir), file_name=f"{name}_{suffix}")

    return {"total": total, "person": person_count, "output": str(output_path)}


def run_on_video(
    video_path: str,
    model: AutoDetectionModel,
    output_dir: Path,
    slice_size: int,
    overlap: float,
    use_sahi: bool,
) -> None:
    """영상에 SAHI 적용 후 결과 영상을 저장한다."""
    output_dir.mkdir(parents=True, exist_ok=True)
    name = Path(video_path).stem
    suffix = "sahi" if use_sahi else "normal"
    output_path = output_dir / f"{name}_{suffix}.mp4"

    cap = cv2.VideoCapture(video_path)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"해상도: {w}x{h}, FPS: {fps:.1f}, 프레임: {total_frames}")
    print(f"SAHI: {'ON' if use_sahi else 'OFF'} (slice={slice_size}, overlap={overlap})")
    print(f"출력: {output_path}")
    print()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (w, h))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # SAHI는 numpy array도 받을 수 있음
        if use_sahi:
            result = get_sliced_prediction(
                image=frame,
                detection_model=model,
                slice_height=slice_size,
                slice_width=slice_size,
                overlap_height_ratio=overlap,
                overlap_width_ratio=overlap,
                perform_standard_pred=True,
                postprocess_type="GREEDYNMM",
                postprocess_match_threshold=0.5,
                postprocess_class_agnostic=False,
            )
        else:
            result = get_prediction(image=frame, detection_model=model)

        # 결과 시각화
        annotated = frame.copy()
        person_count = 0
        for pred in result.object_prediction_list:
            bbox = pred.bbox
            x1, y1, x2, y2 = int(bbox.minx), int(bbox.miny), int(bbox.maxx), int(bbox.maxy)
            label = pred.category.name
            score = pred.score.value

            if label in PERSON_CLASS_NAMES:
                color = (0, 255, 0)  # 초록
                person_count += 1
            else:
                color = (255, 165, 0)  # 주황

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                annotated, f"{label} {score:.2f}",
                (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
            )

        writer.write(annotated)
        frame_idx += 1

        if frame_idx % 100 == 0 or frame_idx == 1:
            total = len(result.object_prediction_list)
            print(f"  프레임 {frame_idx}/{total_frames} — 감지: {total}, Person: {person_count}")

    cap.release()
    writer.release()
    print(f"\n결과 영상 저장: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SAHI Detection 테스트")
    parser.add_argument("--source", required=True, help="입력 이미지/영상 경로")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="모델 가중치 경로")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="출력 디렉토리")
    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")
    parser.add_argument("--slice", type=int, default=640, help="SAHI 타일 크기")
    parser.add_argument("--overlap", type=float, default=0.2, help="SAHI 타일 오버랩 비율")
    parser.add_argument("--no-sahi", action="store_true", help="SAHI 없이 일반 추론")
    args = parser.parse_args()

    model_path = Path(args.model)
    model_name = model_path.stem
    output_dir = Path(args.output) / model_name
    use_sahi = not args.no_sahi

    print(f"모델: {model_path.name}")
    print(f"입력: {args.source}")
    print(f"출력: {output_dir}")
    print(f"신뢰도: {args.conf}")

    model = create_model(model_path, args.conf)

    source = Path(args.source)
    if source.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
        stats = run_on_image(args.source, model, output_dir, args.slice, args.overlap, use_sahi)
        print(f"\n감지: {stats['total']}, Person: {stats['person']}")
        print(f"결과: {stats['output']}")
    else:
        run_on_video(args.source, model, output_dir, args.slice, args.overlap, use_sahi)


if __name__ == "__main__":
    main()
