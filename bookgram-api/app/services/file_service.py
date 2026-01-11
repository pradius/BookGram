"""File service for handling file operations."""

from __future__ import annotations

import re
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file import File


class FileService:
    """Service for file-related operations."""

    UPLOAD_DIR = Path("uploads")

    @staticmethod
    def normalize_topic(title: str) -> str:
        """
        Normalize title to create a valid topic/filename.

        Args:
            title: Raw title string

        Returns:
            Normalized topic string (lowercase, alphanumeric with underscores)
        """
        # Remove special characters and replace spaces with underscores
        normalized = re.sub(r"[^\w\s-]", "", title.lower())
        normalized = re.sub(r"[-\s]+", "_", normalized)
        return normalized.strip("_")

    @staticmethod
    async def save_file_to_disk(
        file_content: bytes,
        topic: str,
        file_extension: str,
    ) -> str:
        """
        Save file to disk and return the location URL.

        Args:
            file_content: File content as bytes
            topic: Normalized topic/filename
            file_extension: File extension (e.g., 'txt', 'pdf')

        Returns:
            Location URL (relative path to the file)
        """
        # Ensure upload directory exists
        FileService.UPLOAD_DIR.mkdir(exist_ok=True)

        # Create filename
        filename = f"{topic}.{file_extension}"
        file_path = FileService.UPLOAD_DIR / filename

        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Return relative path as location_url
        return str(file_path)

    @staticmethod
    async def create_file_record(
        db: AsyncSession,
        location_url: str,
        topic: str,
        size: int,
        file_format: str,
    ) -> File:
        """
        Create a file record in the database.

        Args:
            db: Database session
            location_url: Path to file on disk
            topic: Normalized topic
            size: File size in bytes
            file_format: File extension/type

        Returns:
            Created File instance
        """
        db_file = File(
            location_url=location_url,
            topic=topic,
            size=size,
            format=file_format,
            chapters=None,
            pages=None,
        )
        db.add(db_file)
        await db.flush()
        await db.refresh(db_file)
        return db_file

    @staticmethod
    async def get_file_by_topic(db: AsyncSession, topic: str) -> File | None:
        """Get a file by its topic."""
        result = await db.execute(select(File).where(File.topic == topic))
        return result.scalar_one_or_none()

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Extract file extension from filename."""
        return Path(filename).suffix.lstrip(".").lower()
