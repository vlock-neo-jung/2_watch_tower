"""영상 파일 서빙 + 메타데이터."""

import json
import subprocess

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from api.utils import safe_path
from watch_tower.config import SAMPLES_DIR

router = APIRouter()


class VideoInfo(BaseModel):
    filename: str
    fps: float
    width: int
    height: int
    duration: float
    total_frames: int


@router.get("/", response_model=list[str])
def list_videos() -> list[str]:
    if not SAMPLES_DIR.exists():
        return []
    return sorted(f.name for f in SAMPLES_DIR.glob("*.mp4"))


@router.get("/{filename}")
def get_video(filename: str) -> FileResponse:
    path = safe_path(SAMPLES_DIR, filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"영상 파일 없음: {filename}")
    return FileResponse(path, media_type="video/mp4")


@router.get("/{filename}/info", response_model=VideoInfo)
def get_video_info(filename: str) -> VideoInfo:
    path = safe_path(SAMPLES_DIR, filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"영상 파일 없음: {filename}")

    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                "-show_format",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        probe = json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail=f"ffprobe 타임아웃: {filename}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise HTTPException(status_code=500, detail=f"ffprobe 실행 실패: {e}")

    video_stream = next(
        (s for s in probe.get("streams", []) if s["codec_type"] == "video"),
        None,
    )
    if video_stream is None:
        raise HTTPException(status_code=400, detail="영상 스트림을 찾을 수 없습니다")

    # fps 계산: r_frame_rate (예: "25/1")
    fps = 0.0
    r_rate = video_stream.get("r_frame_rate", "")
    if "/" in r_rate:
        try:
            num, den = map(int, r_rate.split("/"))
            fps = round(num / den, 2) if den > 0 else 0.0
        except (ValueError, ZeroDivisionError):
            fps = 0.0

    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    duration = float(probe.get("format", {}).get("duration", 0))
    total_frames = int(video_stream.get("nb_frames", 0))

    if total_frames == 0 and fps > 0 and duration > 0:
        total_frames = int(duration * fps)

    return VideoInfo(
        filename=filename,
        fps=fps,
        width=width,
        height=height,
        duration=duration,
        total_frames=total_frames,
    )
