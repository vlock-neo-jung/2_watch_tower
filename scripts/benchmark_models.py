"""모델별 Person Detection 벤치마크.

Ground Truth bbox 대비 각 모델의 Recall/Precision을 IoU 기반으로 비교한다.

사용법:
    uv run python scripts/benchmark_models.py
    uv run python scripts/benchmark_models.py --gt-images /path/to/images --gt-labels /path/to/labels
    uv run python scripts/benchmark_models.py --iou 0.3
"""

import argparse
from pathlib import Path

import numpy as np
from ultralytics import YOLO

from watch_tower.config import MODELS_DIR

GT_IMAGES = Path("/home/neo/share/watch-tower_data/ground_truth/images")
GT_LABELS = Path("/home/neo/share/watch-tower_data/ground_truth/labels")

SODA_PERSON_MODEL = MODELS_DIR / "yolo11m-soda-person.pt"

MODELS = {
    "hazard (0.25)": (MODELS_DIR / "yolo11m-construction-hazard.pt", {"Person"}, 0.25),
    "hazard (0.15)": (MODELS_DIR / "yolo11m-construction-hazard.pt", {"Person"}, 0.15),
    "COCO (0.25)": (Path("yolo11m.pt"), {"person"}, 0.25),
    "VisDrone (0.25)": (MODELS_DIR / "yolov8m-visdrone.pt", {"pedestrian", "people"}, 0.25),
    "VisDrone (0.15)": (MODELS_DIR / "yolov8m-visdrone.pt", {"pedestrian", "people"}, 0.15),
    "VisDrone (0.10)": (MODELS_DIR / "yolov8m-visdrone.pt", {"pedestrian", "people"}, 0.10),
}

# 파인튜닝 모델이 있으면 추가
if SODA_PERSON_MODEL.exists():
    MODELS["SODA-ft (0.25)"] = (SODA_PERSON_MODEL, {"person"}, 0.25)
    MODELS["SODA-ft (0.15)"] = (SODA_PERSON_MODEL, {"person"}, 0.15)


def load_gt_boxes(label_path: Path, img_w: int, img_h: int) -> np.ndarray:
    """YOLO 포맷 라벨을 (x1, y1, x2, y2) 배열로 변환한다."""
    if not label_path.exists():
        return np.empty((0, 4))

    text = label_path.read_text().strip()
    if not text:
        return np.empty((0, 4))

    boxes = []
    for line in text.split("\n"):
        parts = line.split()
        xc, yc, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        x1 = (xc - w / 2) * img_w
        y1 = (yc - h / 2) * img_h
        x2 = (xc + w / 2) * img_w
        y2 = (yc + h / 2) * img_h
        boxes.append([x1, y1, x2, y2])

    return np.array(boxes)


def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """두 박스의 IoU를 계산한다."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter

    return inter / union if union > 0 else 0


def match_boxes(
    gt_boxes: np.ndarray,
    pred_boxes: np.ndarray,
    iou_threshold: float,
) -> tuple[int, int, int]:
    """GT와 예측 박스를 IoU 매칭하여 TP/FP/FN을 계산한다."""
    if len(gt_boxes) == 0 and len(pred_boxes) == 0:
        return 0, 0, 0
    if len(gt_boxes) == 0:
        return 0, len(pred_boxes), 0
    if len(pred_boxes) == 0:
        return 0, 0, len(gt_boxes)

    matched_gt = set()
    tp = 0
    fp = 0

    for pred in pred_boxes:
        best_iou = 0
        best_gt_idx = -1
        for i, gt in enumerate(gt_boxes):
            if i in matched_gt:
                continue
            iou = compute_iou(pred, gt)
            if iou > best_iou:
                best_iou = iou
                best_gt_idx = i

        if best_iou >= iou_threshold and best_gt_idx >= 0:
            tp += 1
            matched_gt.add(best_gt_idx)
        else:
            fp += 1

    fn = len(gt_boxes) - len(matched_gt)
    return tp, fp, fn


def run_model(
    model_path: Path,
    person_classes: set[str],
    conf: float,
    images: list[Path],
    iou_threshold: float,
    gt_labels_dir: Path = GT_LABELS,
) -> dict:
    """모델을 실행하고 GT 대비 TP/FP/FN을 집계한다."""
    model = YOLO(str(model_path))

    total_tp, total_fp, total_fn = 0, 0, 0
    total_gt = 0

    for img_path in images:
        # GT 로드
        label_path = gt_labels_dir / f"{img_path.stem}.txt"
        results = model.predict(str(img_path), device="cuda", conf=conf, imgsz=640, verbose=False)[0]
        img_h, img_w = results.orig_shape

        gt_boxes = load_gt_boxes(label_path, img_w, img_h)
        total_gt += len(gt_boxes)

        # 예측에서 Person 클래스만 추출
        pred_boxes = []
        for i, cls_id in enumerate(results.boxes.cls):
            cls_name = results.names[int(cls_id)]
            if cls_name in person_classes:
                pred_boxes.append(results.boxes.xyxy[i].cpu().numpy())

        pred_array = np.array(pred_boxes) if pred_boxes else np.empty((0, 4))

        tp, fp, fn = match_boxes(gt_boxes, pred_array, iou_threshold)
        total_tp += tp
        total_fp += fp
        total_fn += fn

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
        "gt_total": total_gt,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="모델별 Person Detection 벤치마크")
    parser.add_argument("--iou", type=float, default=0.5, help="IoU 매칭 임계값")
    parser.add_argument("--gt-images", default=str(GT_IMAGES), help="GT 이미지 디렉토리")
    parser.add_argument("--gt-labels", default=str(GT_LABELS), help="GT 라벨 디렉토리")
    args = parser.parse_args()

    gt_images_dir = Path(args.gt_images)
    gt_labels_dir = Path(args.gt_labels)

    images = sorted(gt_images_dir.glob("*.jpg")) + sorted(gt_images_dir.glob("*.jpeg")) + sorted(gt_images_dir.glob("*.png"))
    print(f"이미지: {len(images)}장")
    print(f"IoU 임계값: {args.iou}")
    print()

    print(f"{'모델':<20} {'TP':>4} {'FP':>4} {'FN':>4} {'GT':>4} {'Precision':>10} {'Recall':>8} {'F1':>6}")
    print("-" * 70)

    for name, (model_path, person_classes, conf) in MODELS.items():
        result = run_model(model_path, person_classes, conf, images, args.iou, gt_labels_dir)
        print(
            f"{name:<20} {result['tp']:>4} {result['fp']:>4} {result['fn']:>4} "
            f"{result['gt_total']:>4} {result['precision']:>9.1%} {result['recall']:>7.1%} "
            f"{result['f1']:>5.1%}"
        )


if __name__ == "__main__":
    main()
