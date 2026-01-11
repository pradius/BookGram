"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import books

router = APIRouter()

router.include_router(books.router)
