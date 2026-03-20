"""GT 어노테이션 CRUD API."""

import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.utils import safe_path
from watch_tower.config import DATA_ROOT

router = APIRouter()

GT_DIR = DATA_ROOT / "zone_gt"


class AnnotationData(BaseModel, extra="allow"):
    """GT JSON. video, events 필드 필수. 나머지 필드는 유연하게 허용."""

    video: str
    events: list[dict]


class StatusResponse(BaseModel):
    status: str
    path: str


@router.get("/", response_model=list[str])
def list_annotations() -> list[str]:
    if not GT_DIR.exists():
        return []
    return sorted(f.name for f in GT_DIR.glob("*.json"))


@router.get("/{annotation_name}", response_model=AnnotationData)
def get_annotation(annotation_name: str) -> AnnotationData:
    path = safe_path(GT_DIR, annotation_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"GT 파일 없음: {annotation_name}")
    with open(path) as f:
        data = json.load(f)
    return AnnotationData.model_validate(data)


@router.post("/{annotation_name}", response_model=StatusResponse)
def save_annotation(annotation_name: str, data: AnnotationData) -> StatusResponse:
    GT_DIR.mkdir(parents=True, exist_ok=True)
    path = safe_path(GT_DIR, annotation_name)
    with open(path, "w") as f:
        json.dump(data.model_dump(), f, indent=2, ensure_ascii=False)
    return StatusResponse(status="ok", path=str(path))
