"""FastAPI 앱 진입점."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import annotations, videos, zones

app = FastAPI(title="Watch Tower API")

_cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3031")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(zones.router, prefix="/api/zones", tags=["zones"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["annotations"])
