"""File Pydantic schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    """Schema for file response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    location_url: str
    topic: str
    size: int
    format: str
    chapters: list[str] | None = None
    pages: list[str] | None = None
    created_at: datetime
    updated_at: datetime
