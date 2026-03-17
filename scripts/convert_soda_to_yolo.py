"""SODA 데이터셋 VOC → YOLO 변환 스크립트.

VOC XML에서 Person 클래스만 추출하여 YOLO 포맷(class x_center y_center w h)으로 변환한다.

사용법:
    uv run python scripts/convert_soda_to_yolo.py
    uv run python scripts/convert_soda_to_yolo.py --split test
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from watch_tower.config import DATASET_DIR

SODA_ROOT = DATASET_DIR / "soda"
PERSON_CLASS = "person"
YOLO_CLASS_ID = 0  # Person = class 0 in output


def convert_voc_to_yolo(xml_path: Path, output_path: Path) -> int:
    """VOC XML을 YOLO 포맷으로 변환한다. Person만 추출."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    if img_w == 0 or img_h == 0:
        return 0

    lines = []
    for obj in root.findall("object"):
        name = obj.find("name").text.strip().lower()
        if name != PERSON_CLASS:
            continue

        bbox = obj.find("bndbox")
        x1 = float(bbox.find("xmin").text)
        y1 = float(bbox.find("ymin").text)
        x2 = float(bbox.find("xmax").text)
        y2 = float(bbox.find("ymax").text)

        # YOLO 포맷: 정규화된 중심 좌표 + 크기
        x_center = ((x1 + x2) / 2) / img_w
        y_center = ((y1 + y2) / 2) / img_h
        w = (x2 - x1) / img_w
        h = (y2 - y1) / img_h

        lines.append(f"{YOLO_CLASS_ID} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n" if lines else "")

    return len(lines)


def find_soda_structure(soda_root: Path) -> tuple[Path, Path]:
    """SODA 디렉토리 구조를 탐색하여 Annotations, JPEGImages 경로를 반환한다."""
    # VOCv1.zip 해제 후 구조에 따라 탐색
    candidates = [
        soda_root,
        soda_root / "VOCv1",
        soda_root / "VOC2007",
    ]

    for base in candidates:
        ann_dir = base / "Annotations"
        img_dir = base / "JPEGImages"
        if ann_dir.exists() and img_dir.exists():
            return ann_dir, img_dir

    # 재귀 탐색
    for ann_dir in soda_root.rglob("Annotations"):
        img_dir = ann_dir.parent / "JPEGImages"
        if img_dir.exists():
            return ann_dir, img_dir

    raise FileNotFoundError(f"SODA Annotations/JPEGImages not found in {soda_root}")


def convert_split(
    ann_dir: Path,
    img_dir: Path,
    split_file: Path | None,
    output_images: Path,
    output_labels: Path,
) -> dict:
    """지정된 split의 이미지를 변환한다."""
    # split 파일이 있으면 해당 이미지만, 없으면 전체
    if split_file and split_file.exists():
        image_ids = split_file.read_text(encoding="utf-8", errors="ignore").strip().split("\n")
    else:
        image_ids = [f.stem for f in sorted(ann_dir.glob("*.xml"))]

    stats = {"total_images": 0, "images_with_person": 0, "total_persons": 0}

    for img_id in image_ids:
        img_id = img_id.strip()
        xml_path = ann_dir / f"{img_id}.xml"
        if not xml_path.exists():
            continue

        label_path = output_labels / f"{img_id}.txt"
        person_count = convert_voc_to_yolo(xml_path, label_path)

        # 이미지 심볼릭 링크 생성
        src_img = None
        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG"]:
            candidate = img_dir / f"{img_id}{ext}"
            if candidate.exists():
                src_img = candidate
                break

        if src_img:
            link = output_images / src_img.name
            if not link.exists():
                link.symlink_to(src_img.resolve())

        stats["total_images"] += 1
        if person_count > 0:
            stats["images_with_person"] += 1
        stats["total_persons"] += person_count

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="SODA VOC→YOLO 변환")
    parser.add_argument("--split", default="test", help="변환할 split (train/test, 기본: test)")
    args = parser.parse_args()

    print(f"SODA 루트: {SODA_ROOT}")

    ann_dir, img_dir = find_soda_structure(SODA_ROOT)
    print(f"Annotations: {ann_dir}")
    print(f"JPEGImages: {img_dir}")

    # split 파일 탐색
    split_dir = ann_dir.parent / "ImageSets" / "Main"
    split_file = split_dir / f"{args.split}.txt" if split_dir.exists() else None

    output_base = SODA_ROOT / "yolo" / args.split
    output_images = output_base / "images"
    output_labels = output_base / "labels"
    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    print(f"Split: {args.split}")
    print(f"Split 파일: {split_file}")
    print(f"출력: {output_base}")
    print()

    stats = convert_split(ann_dir, img_dir, split_file, output_images, output_labels)

    print(f"변환 완료:")
    print(f"  이미지: {stats['total_images']}장")
    print(f"  Person 포함: {stats['images_with_person']}장")
    print(f"  Person 어노테이션: {stats['total_persons']}개")


if __name__ == "__main__":
    main()
