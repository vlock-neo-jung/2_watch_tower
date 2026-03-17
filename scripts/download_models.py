"""모델 가중치 다운로드 스크립트.

HuggingFace에서 프로젝트에 필요한 모델 가중치를 다운로드한다.
"""

from pathlib import Path

from huggingface_hub import hf_hub_download

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

MODELS = [
    {
        "repo_id": "yihong1120/Construction-Hazard-Detection",
        "filename": "models/yolo11/pt/yolo11m.pt",
        "local_name": "yolo11m-construction-hazard.pt",
    },
]


def download_all() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    for model in MODELS:
        local_path = MODELS_DIR / model["local_name"]
        if local_path.exists():
            print(f"이미 존재: {local_path}")
            continue

        print(f"다운로드 중: {model['repo_id']} / {model['filename']}")
        downloaded = hf_hub_download(
            repo_id=model["repo_id"],
            filename=model["filename"],
            local_dir=MODELS_DIR,
            local_dir_use_symlinks=False,
        )
        # HuggingFace 캐시 구조에서 실제 파일을 프로젝트 이름으로 복사
        downloaded_path = Path(downloaded)
        if downloaded_path != local_path:
            downloaded_path.rename(local_path)

        print(f"완료: {local_path}")


if __name__ == "__main__":
    download_all()
