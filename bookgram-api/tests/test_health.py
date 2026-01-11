"""Test health check endpoint."""

from unittest.mock import AsyncMock
import pytest
from httpx import AsyncClient


async def mock_get_db():
    """Mock database session for health check test."""
    mock_db = AsyncMock()
    mock_db.execute = AsyncMock()
    yield mock_db


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test health check endpoint returns healthy status."""
    from app.main import app
    from app.db import get_db
    
    # Override the dependency
    app.dependency_overrides[get_db] = mock_get_db
    
    try:
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert data["database"] == "healthy"
    finally:
        # Clean up the override
        app.dependency_overrides.clear()
