"""Watch Tower 환경 설정 스크립트.

ultralytics 설정을 프로젝트에 맞게 구성한다.
최초 1회 실행 또는 설정 초기화 시 사용.
"""

from ultralytics import settings

from watch_tower.config import DATASET_DIR


def setup() -> None:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    settings.update({"datasets_dir": str(DATASET_DIR)})
    print(f"datasets_dir: {settings['datasets_dir']}")
    print("설정 완료.")


if __name__ == "__main__":
    setup()
