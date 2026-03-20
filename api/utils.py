"""API 공용 유틸리티."""

from pathlib import Path

from fastapi import HTTPException


def safe_path(base: Path, user_input: str) -> Path:
    """base 디렉토리 내부 경로만 허용. 경로 순회 시 404 반환."""
    resolved = (base / user_input).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise HTTPException(status_code=404, detail="잘못된 경로")
    return resolved
