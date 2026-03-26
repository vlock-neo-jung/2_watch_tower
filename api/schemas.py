"""API 공통 Pydantic 스키마."""

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str
    path: str
