"""Grounding DINO로 Person 정답 bbox를 생성하여 YOLO 포맷으로 저장한다.

사용법:
    uv run python scripts/generate_ground_truth.py
    uv run python scripts/generate_ground_truth.py --threshold 0.2
    uv run python scripts/generate_ground_truth.py --visualize
"""

import argparse
import json
from pathlib import Path

import cv2
import torch
from PIL import Image
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

IMAGES_DIR = Path("/home/neo/share/watch-tower_data/ground_truth/images")
LABELS_DIR = Path("/home/neo/share/watch-tower_data/ground_truth/labels")
VIS_DIR = Path("/home/neo/share/watch-tower_data/ground_truth/visualized")

MODEL_ID = "IDEA-Research/grounding-dino-base"
PROMPT = "person."  # Grounding DINO는 마침표로 클래스 구분


def load_model() -> tuple:
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(MODEL_ID).to("cuda")
    return processor, model


def detect_persons(
    image_path: Path,
    processor,
    model,
    threshold: float,
) -> list[dict]:
    """이미지에서 Person bbox를 감지한다."""
    image = Image.open(image_path).convert("RGB")
    w, h = image.size

    inputs = processor(images=image, text=PROMPT, return_tensors="pt").to("cuda")

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=threshold,
        text_threshold=threshold,
        target_sizes=[(h, w)],
    )[0]

    detections = []
    for box, score, label in zip(results["boxes"], results["scores"], results["labels"]):
        x1, y1, x2, y2 = box.tolist()
        detections.append({
            "bbox": [x1, y1, x2, y2],
            "score": float(score),
            "label": label,
        })

    return detections


def save_yolo_labels(image_path: Path, detections: list[dict]) -> Path:
    """bbox를 YOLO 포맷(class x_center y_center w h)으로 저장한다."""
    image = cv2.imread(str(image_path))
    img_h, img_w = image.shape[:2]

    label_path = LABELS_DIR / f"{image_path.stem}.txt"

    lines = []
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        x_center = ((x1 + x2) / 2) / img_w
        y_center = ((y1 + y2) / 2) / img_h
        w = (x2 - x1) / img_w
        h = (y2 - y1) / img_h
        lines.append(f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    label_path.write_text("\n".join(lines) + "\n" if lines else "")
    return label_path


def visualize(image_path: Path, detections: list[dict]) -> Path:
    """bbox를 그린 이미지를 저장한다."""
    VIS_DIR.mkdir(parents=True, exist_ok=True)
    image = cv2.imread(str(image_path))

    for det in detections:
        x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
        score = det["score"]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"person {score:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    output_path = VIS_DIR / f"{image_path.stem}_gt.jpg"
    cv2.imwrite(str(output_path), image)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Grounding DINO 정답 생성")
    parser.add_argument("--threshold", type=float, default=0.25, help="감지 임계값")
    parser.add_argument("--visualize", action="store_true", help="시각화 이미지 저장")
    args = parser.parse_args()

    LABELS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"모델: {MODEL_ID}")
    print(f"프롬프트: {PROMPT}")
    print(f"임계값: {args.threshold}")
    print()

    processor, model = load_model()
    print("모델 로드 완료\n")

    images = sorted(IMAGES_DIR.glob("*.jpg"))
    total_persons = 0
    metadata = []

    for img_path in images:
        detections = detect_persons(img_path, processor, model, args.threshold)
        save_yolo_labels(img_path, detections)

        if args.visualize:
            visualize(img_path, detections)

        count = len(detections)
        total_persons += count
        metadata.append({
            "image": img_path.name,
            "person_count": count,
            "detections": [{"bbox": d["bbox"], "score": d["score"]} for d in detections],
        })
        print(f"  {img_path.name}: {count}명")

    # 메타데이터 저장
    meta_path = LABELS_DIR.parent / "metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    print(f"\n총 {len(images)}장, {total_persons}명 감지")
    print(f"라벨: {LABELS_DIR}")
    if args.visualize:
        print(f"시각화: {VIS_DIR}")


if __name__ == "__main__":
    main()
