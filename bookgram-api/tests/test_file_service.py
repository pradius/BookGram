"""Tests for file service."""

from unittest.mock import AsyncMock, MagicMock
import pytest
from pathlib import Path

from app.db.models.file import File
from app.services.file_service import FileService


class TestFileService:
    """Test FileService class."""

    def test_normalize_topic(self):
        """Test topic normalization."""
        assert FileService.normalize_topic("Hello World") == "hello_world"
        assert FileService.normalize_topic("Python 3.12!") == "python_3.12"
        assert FileService.normalize_topic("Test-Title") == "test_title"
        assert FileService.normalize_topic("  Spaces  ") == "spaces"
        assert FileService.normalize_topic("Special@#$Chars") == "special_chars"

    def test_get_file_extension(self):
        """Test file extension extraction."""
        assert FileService.get_file_extension("test.txt") == "txt"
        assert FileService.get_file_extension("file.PDF") == "pdf"
        assert FileService.get_file_extension("doc.tar.gz") == "gz"
        assert FileService.get_file_extension("no_extension") == ""

    @pytest.mark.asyncio
    async def test_save_file_to_disk(self, tmp_path, monkeypatch):
        """Test saving file to disk."""
        # Override UPLOAD_DIR to use tmp_path
        test_upload_dir = tmp_path / "uploads"
        monkeypatch.setattr(FileService, "UPLOAD_DIR", test_upload_dir)

        file_content = b"Test file content"
        topic = "test_topic"
        file_extension = "txt"

        location_url = await FileService.save_file_to_disk(
            file_content=file_content,
            topic=topic,
            file_extension=file_extension,
        )

        # Verify file was created
        assert Path(location_url).exists()
        assert Path(location_url).read_bytes() == file_content
        assert location_url.endswith("test_topic.txt")

    @pytest.mark.asyncio
    async def test_create_file_record(self):
        """Test creating file record in database."""
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()

        file_record = await FileService.create_file_record(
            db=mock_db,
            location_url="uploads/test.txt",
            topic="test_topic",
            size=1024,
            file_format="txt",
        )

        assert file_record.location_url == "uploads/test.txt"
        assert file_record.topic == "test_topic"
        assert file_record.size == 1024
        assert file_record.format == "txt"
        mock_db.add.assert_called_once()
        mock_db.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_file_by_topic(self):
        """Test retrieving file by topic."""
        mock_db = AsyncMock()
        mock_file = File(
            id=1,
            location_url="uploads/python.txt",
            topic="python_basics",
            size=2048,
            format="txt",
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_file
        mock_db.execute.return_value = mock_result

        # Retrieve it
        file_record = await FileService.get_file_by_topic(
            db=mock_db, topic="python_basics"
        )

        assert file_record is not None
        assert file_record.topic == "python_basics"
        assert file_record.size == 2048
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_file_by_topic_not_found(self):
        """Test retrieving non-existent file returns None."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        file_record = await FileService.get_file_by_topic(
            db=mock_db, topic="nonexistent"
        )

        assert file_record is None
        mock_db.execute.assert_called_once()
