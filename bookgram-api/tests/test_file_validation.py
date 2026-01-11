"""Tests for file validation in the SaveFile endpoint."""

import io
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.db.models.user import User


class TestFileValidation:
    """Test file validation logic."""

    @pytest.mark.asyncio
    async def test_file_without_extension_rejected(self, client: AsyncClient):
        """Test that files without extension are rejected."""
        file_content = b"Test content"
        files = {"file": ("testfile", io.BytesIO(file_content), "text/plain")}
        data = {"title": "Test File", "user_id": "1"}

        with patch("app.api.v1.files.UserService.get_user", new_callable=AsyncMock) as mock_get_user:
            mock_user = User(
                id=1,
                email="test@example.com",
                username="testuser",
                subscribed_topics=[],
            )
            mock_get_user.return_value = mock_user

            response = await client.post("/api/v1/files/save", files=files, data=data)

            assert response.status_code == 400
            assert "must have a valid extension" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_file_with_valid_extension_accepted(self, client: AsyncClient):
        """Test that files with valid extensions are accepted."""
        file_content = b"Test content"
        files = {"file": ("testfile.txt", io.BytesIO(file_content), "text/plain")}
        data = {"title": "Test File", "user_id": "1"}

        with patch("app.api.v1.files.UserService.get_user", new_callable=AsyncMock) as mock_get_user, \
             patch("app.api.v1.files.UserService.subscribe_user_to_topic", new_callable=AsyncMock) as mock_subscribe, \
             patch("app.api.v1.files.FileService.save_file_to_disk", new_callable=AsyncMock) as mock_save, \
             patch("app.api.v1.files.FileService.create_file_record", new_callable=AsyncMock) as mock_create:
            
            mock_user = User(
                id=1,
                email="test@example.com",
                username="testuser",
                subscribed_topics=[],
            )
            mock_get_user.return_value = mock_user
            mock_save.return_value = "uploads/test_file.txt"
            
            # Create a mock file record with the topic attribute
            from app.db.models.file import File
            mock_file_record = File(
                id=1,
                location_url="uploads/test_file.txt",
                topic="test_file",
                size=len(file_content),
                format="txt",
            )
            mock_create.return_value = mock_file_record

            response = await client.post("/api/v1/files/save", files=files, data=data)

            assert response.status_code == 201
            assert response.json() == "test_file"
