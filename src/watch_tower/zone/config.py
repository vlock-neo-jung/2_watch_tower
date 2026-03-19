"""Zone 설정 YAML 파일 로드/저장."""

from pathlib import Path

import yaml

from watch_tower.zone.models import ZoneConfig


def load_zone_config(path: str | Path) -> ZoneConfig:
    """YAML 파일에서 zone 설정을 로드한다."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"zone 설정 파일이 존재하지 않습니다: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    return ZoneConfig.model_validate(data)


def save_zone_config(config: ZoneConfig, path: str | Path) -> None:
    """ZoneConfig를 YAML 파일로 저장한다."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.model_dump(mode="json")

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
