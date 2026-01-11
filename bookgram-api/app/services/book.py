"""Book service with business logic."""

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    """Service for book-related operations."""

    @staticmethod
    async def get_book(db: AsyncSession, book_id: int) -> Book | None:
        """Get a book by ID."""
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_books(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Book], int]:
        """Get all books with pagination."""
        # Get total count
        count_result = await db.execute(select(func.count(Book.id)))
        total = count_result.scalar_one()

        # Get paginated books
        result = await db.execute(select(Book).offset(skip).limit(limit))
        books = result.scalars().all()

        return books, total

    @staticmethod
    async def create_book(db: AsyncSession, book: BookCreate) -> Book:
        """Create a new book."""
        db_book = Book(**book.model_dump())
        db.add(db_book)
        await db.flush()
        await db.refresh(db_book)
        return db_book

    @staticmethod
    async def update_book(
        db: AsyncSession,
        book_id: int,
        book_update: BookUpdate,
    ) -> Book | None:
        """Update an existing book."""
        db_book = await BookService.get_book(db, book_id)
        if not db_book:
            return None

        update_data = book_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)

        await db.flush()
        await db.refresh(db_book)
        return db_book

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int) -> bool:
        """Delete a book."""
        db_book = await BookService.get_book(db, book_id)
        if not db_book:
            return False

        await db.delete(db_book)
        await db.flush()
        return True
