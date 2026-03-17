"""YouTube 영상 다운로드 스크립트.

P2-2 평가용 건설 현장 영상을 YouTube에서 다운로드하여 samples/에 저장한다.

사용법:
    uv run python scripts/download_video.py --url "https://youtube.com/watch?v=..." --name "site_01"
    uv run python scripts/download_video.py --url "URL" --name "site_02" --section "1:30-3:00"
    uv run python scripts/download_video.py --url "URL" --name "site_03" --resolution 720
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from watch_tower.config import SAMPLES_DIR


def check_ffmpeg() -> bool:
    """ffmpeg 설치 여부를 확인한다."""
    return shutil.which("ffmpeg") is not None


def download(url: str, name: str, resolution: int, section: str | None) -> Path:
    """YouTube 영상을 다운로드한다."""
    output_path = SAMPLES_DIR / f"{name}.mp4"
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        "yt-dlp",
        url,
        "-f", f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[height<={resolution}][ext=mp4]/best[height<={resolution}]",
        "--merge-output-format", "mp4",
        "-o", str(output_path),
        "--no-playlist",
    ]

    if section:
        if not check_ffmpeg():
            print("경고: ffmpeg가 설치되어 있지 않습니다. 구간 추출이 실패할 수 있습니다.")
        cmd += ["--download-sections", f"*{section}"]

    print(f"다운로드 시작: {url}")
    print(f"저장 경로: {output_path}")
    print(f"해상도: {resolution}p")
    if section:
        print(f"구간: {section}")
    print(flush=True)

    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        print(f"\n다운로드 실패 (exit code: {result.returncode})", file=sys.stderr)
        sys.exit(1)

    print(f"\n다운로드 완료: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="YouTube 영상 다운로드")
    parser.add_argument("--url", required=True, help="YouTube URL")
    parser.add_argument("--name", required=True, help="저장할 파일명 (확장자 제외)")
    parser.add_argument("--resolution", type=int, default=1080, help="최대 해상도 (기본: 1080)")
    parser.add_argument("--section", default=None, help="구간 추출 (예: '1:30-3:00')")
    args = parser.parse_args()

    download(url=args.url, name=args.name, resolution=args.resolution, section=args.section)


if __name__ == "__main__":
    main()
