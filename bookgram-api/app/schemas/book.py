"""Book Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    """Base book schema with common attributes."""

    title: str = Field(..., min_length=1, max_length=255, description="Book title")
    author: str = Field(..., min_length=1, max_length=255, description="Book author")
    isbn: str | None = Field(None, min_length=10, max_length=13, description="ISBN number")
    description: str | None = Field(None, description="Book description")
    published_year: int | None = Field(None, ge=1000, le=9999, description="Publication year")


class BookCreate(BookBase):
    """Schema for creating a new book."""

    pass


class BookUpdate(BaseModel):
    """Schema for updating an existing book."""

    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    isbn: str | None = Field(None, min_length=10, max_length=13)
    description: str | None = None
    published_year: int | None = Field(None, ge=1000, le=9999)


class BookResponse(BookBase):
    """Schema for book response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class BookListResponse(BaseModel):
    """Schema for paginated book list response."""

    items: list[BookResponse]
    total: int
    page: int
    size: int
    pages: int
