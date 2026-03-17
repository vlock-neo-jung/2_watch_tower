"""Construction-PPE 데이터셋 라벨을 모델 클래스 인덱스에 맞춰 리매핑한다.

yolo11m-construction-hazard 모델의 클래스 인덱스와 Construction-PPE 데이터셋의
클래스 인덱스가 다르므로, 라벨 파일을 변환하여 정확한 평가를 가능하게 한다.

사용법:
    uv run python scripts/remap_construction_ppe.py
"""

from pathlib import Path

from watch_tower.config import DATASET_DIR

SOURCE_DIR = DATASET_DIR / "construction-ppe"
TARGET_DIR = DATASET_DIR / "construction-ppe-remapped"

# 데이터셋 클래스 → 모델 클래스 인덱스 매핑
# 매핑 불가능한 클래스는 None (라벨에서 제거)
DATASET_TO_MODEL = {
    0: 0,     # helmet → Hardhat
    1: None,  # gloves → (모델에 없음)
    2: 7,     # vest → Safety Vest
    3: None,  # boots → (모델에 없음)
    4: None,  # goggles → (모델에 없음)
    5: None,  # none → (모델에 없음)
    6: 5,     # Person → Person
    7: 2,     # no_helmet → NO-Hardhat
    8: None,  # no_goggle → (모델에 없음)
    9: None,  # no_gloves → (모델에 없음)
    10: None, # no_boots → (모델에 없음)
}


def remap_label_file(src_path: Path, dst_path: Path) -> dict:
    """라벨 파일의 클래스 인덱스를 리매핑한다."""
    stats = {"total": 0, "kept": 0, "dropped": 0}

    lines = src_path.read_text().strip().split("\n")
    remapped_lines = []

    for line in lines:
        if not line.strip():
            continue
        stats["total"] += 1
        parts = line.strip().split()
        cls_idx = int(parts[0])
        new_idx = DATASET_TO_MODEL.get(cls_idx)

        if new_idx is not None:
            parts[0] = str(new_idx)
            remapped_lines.append(" ".join(parts))
            stats["kept"] += 1
        else:
            stats["dropped"] += 1

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text("\n".join(remapped_lines) + "\n" if remapped_lines else "")

    return stats


def remap_split(split: str) -> dict:
    """train/val/test 중 하나의 split을 리매핑한다."""
    src_labels = SOURCE_DIR / "labels" / split
    dst_labels = TARGET_DIR / "labels" / split

    # 이미지는 파일 단위 심볼릭 링크로 연결
    # (디렉토리 심볼릭 링크를 쓰면 YOLO가 resolve하여 원본 labels를 읽음)
    src_images = SOURCE_DIR / "images" / split
    dst_images = TARGET_DIR / "images" / split
    dst_images.mkdir(parents=True, exist_ok=True)

    if not any(dst_images.iterdir()):
        for img_file in src_images.iterdir():
            link = dst_images / img_file.name
            if not link.exists():
                link.symlink_to(img_file.resolve())

    total_stats = {"total": 0, "kept": 0, "dropped": 0, "files": 0}

    if not src_labels.exists():
        return total_stats

    for label_file in sorted(src_labels.glob("*.txt")):
        stats = remap_label_file(label_file, dst_labels / label_file.name)
        total_stats["total"] += stats["total"]
        total_stats["kept"] += stats["kept"]
        total_stats["dropped"] += stats["dropped"]
        total_stats["files"] += 1

    return total_stats


def create_yaml() -> Path:
    """리매핑된 데이터셋용 yaml을 생성한다."""
    yaml_content = f"""# Construction-PPE (remapped to yolo11m-construction-hazard classes)
path: {TARGET_DIR}
train: images/train
val: images/val
test: images/test

# Model class names (matching yolo11m-construction-hazard)
names:
  0: Hardhat
  1: Mask
  2: NO-Hardhat
  3: NO-Mask
  4: NO-Safety Vest
  5: Person
  6: Safety Cone
  7: Safety Vest
  8: machinery
  9: utility pole
  10: vehicle
"""
    yaml_path = TARGET_DIR / "construction-ppe-remapped.yaml"
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path.write_text(yaml_content)
    return yaml_path


def main() -> None:
    print("Construction-PPE 라벨 리매핑 시작")
    print(f"원본: {SOURCE_DIR}")
    print(f"대상: {TARGET_DIR}")
    print()

    for split in ["train", "val", "test"]:
        stats = remap_split(split)
        print(f"[{split}] 파일: {stats['files']}, "
              f"어노테이션: {stats['total']} → 유지: {stats['kept']}, 제거: {stats['dropped']}")

    yaml_path = create_yaml()
    print(f"\nYAML 생성: {yaml_path}")
    print("리매핑 완료!")


if __name__ == "__main__":
    main()
