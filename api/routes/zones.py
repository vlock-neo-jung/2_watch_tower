"""Zone 설정 CRUD API."""

from fastapi import APIRouter, HTTPException

from api.schemas import StatusResponse
from api.utils import safe_path
from watch_tower.config import DATA_ROOT
from watch_tower.zone import ZoneConfig, load_zone_config, save_zone_config

router = APIRouter()

ZONES_DIR = DATA_ROOT / "configs" / "zones"


@router.get("/", response_model=list[str])
def list_zone_configs() -> list[str]:
    if not ZONES_DIR.exists():
        return []
    return sorted(f.name for f in ZONES_DIR.glob("*.yaml"))


@router.get("/{config_name}", response_model=ZoneConfig)
def get_zone_config(config_name: str) -> ZoneConfig:
    path = safe_path(ZONES_DIR, config_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"설정 파일 없음: {config_name}")
    return load_zone_config(path)


@router.post("/{config_name}", response_model=StatusResponse)
def save_zone_config_api(config_name: str, config: ZoneConfig) -> StatusResponse:
    ZONES_DIR.mkdir(parents=True, exist_ok=True)
    path = safe_path(ZONES_DIR, config_name)
    save_zone_config(config, path)
    return StatusResponse(status="ok", path=str(path))


@router.delete("/{config_name}", response_model=StatusResponse)
def delete_zone_config(config_name: str) -> StatusResponse:
    path = safe_path(ZONES_DIR, config_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"설정 파일 없음: {config_name}")
    path.unlink()
    return StatusResponse(status="ok", path=str(path))
