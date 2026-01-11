"""Books CRUD endpoints."""

import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.book import BookCreate, BookListResponse, BookResponse, BookUpdate
from app.services.book import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=BookListResponse)
async def list_books(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
) -> BookListResponse:
    """
    List all books with pagination.

    - **page**: Page number (starts at 1)
    - **size**: Number of items per page (max 100)
    """
    skip = (page - 1) * size
    books, total = await BookService.get_books(db, skip=skip, limit=size)

    return BookListResponse(
        items=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BookResponse:
    """
    Get a specific book by ID.

    - **book_id**: Book ID
    """
    book = await BookService.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return BookResponse.model_validate(book)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BookResponse:
    """
    Create a new book.

    - **title**: Book title (required)
    - **author**: Book author (required)
    - **isbn**: ISBN number (optional)
    - **description**: Book description (optional)
    - **published_year**: Publication year (optional)
    """
    db_book = await BookService.create_book(db, book)
    return BookResponse.model_validate(db_book)


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BookResponse:
    """
    Update an existing book.

    - **book_id**: Book ID
    - Fields to update (all optional)
    """
    db_book = await BookService.update_book(db, book_id, book_update)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return BookResponse.model_validate(db_book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """
    Delete a book.

    - **book_id**: Book ID
    """
    deleted = await BookService.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
