"""CCTV 영상에서 대표 프레임을 균등 간격으로 추출한다.

사용법:
    uv run python scripts/extract_frames.py
"""

from pathlib import Path

import cv2

from watch_tower.config import SAMPLES_DIR

OUTPUT_DIR = Path("/home/neo/share/watch-tower_data/ground_truth/images")

# 영상별 추출할 프레임 수
VIDEOS = [
    ("construction_subway_cctv.mp4", 8),
    ("construction_tower_crane_cctv.mp4", 8),
    ("construction_site_cctv.mp4", 6),
    ("construction_helmets.mp4", 4),
]


def extract(video_name: str, num_frames: int) -> list[Path]:
    """영상에서 균등 간격으로 프레임을 추출한다."""
    video_path = SAMPLES_DIR / video_name
    cap = cv2.VideoCapture(str(video_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total == 0:
        print(f"  건너뜀: {video_name} (프레임 없음)")
        cap.release()
        return []

    # 균등 간격으로 프레임 인덱스 계산 (처음과 끝 제외)
    step = total // (num_frames + 1)
    indices = [step * (i + 1) for i in range(num_frames)]

    stem = Path(video_name).stem
    saved = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue

        filename = f"{stem}_{idx:05d}.jpg"
        output_path = OUTPUT_DIR / filename
        cv2.imwrite(str(output_path), frame)
        saved.append(output_path)

    cap.release()
    return saved


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total_saved = 0

    for video_name, num_frames in VIDEOS:
        print(f"{video_name} ({num_frames}장 추출)")
        saved = extract(video_name, num_frames)
        print(f"  → {len(saved)}장 저장")
        total_saved += len(saved)

    print(f"\n총 {total_saved}장 추출 완료: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
