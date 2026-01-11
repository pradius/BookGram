"""File database model."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class File(Base):
    """File entity model for storing uploaded files metadata."""

    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    location_url: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    topic: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    format: Mapped[str] = mapped_column(String(50), nullable=False)
    chapters: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True, default=None)
    pages: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<File(id={self.id}, topic='{self.topic}', format='{self.format}')>"
