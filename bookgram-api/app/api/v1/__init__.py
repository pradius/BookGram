"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import files

router = APIRouter()

router.include_router(files.router)
