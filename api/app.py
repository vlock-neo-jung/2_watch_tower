"""FastAPI 앱 진입점."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import annotations, videos, zones

app = FastAPI(title="Watch Tower API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(zones.router, prefix="/api/zones", tags=["zones"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["annotations"])
