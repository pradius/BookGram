"""Tests for user service."""

from unittest.mock import AsyncMock, MagicMock
import pytest

from app.db.models.user import User
from app.services.user_service import UserService


class TestUserService:
    """Test UserService class."""

    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test creating a new user."""
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        
        user = await UserService.create_user(
            db=mock_db,
            email="newuser@example.com",
            username="newuser",
        )

        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.subscribed_topics == []
        mock_db.add.assert_called_once()
        mock_db.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user(self):
        """Test getting a user by ID."""
        mock_db = AsyncMock()
        mock_user = User(
            id=1,
            email="test@example.com",
            username="testuser",
            subscribed_topics=[],
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        user = await UserService.get_user(db=mock_db, user_id=1)

        assert user is not None
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_not_found(self):
        """Test getting non-existent user returns None."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        user = await UserService.get_user(db=mock_db, user_id=99999)

        assert user is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_subscribe_user_to_topic(self):
        """Test subscribing user to a topic."""
        mock_db = AsyncMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        mock_user = User(
            id=1,
            email="subscriber@example.com",
            username="subscriber",
            subscribed_topics=[],
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        updated_user = await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="python_basics",
        )

        assert updated_user is not None
        assert "python_basics" in updated_user.subscribed_topics
        mock_db.flush.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_subscribe_user_to_multiple_topics(self):
        """Test subscribing user to multiple topics."""
        mock_db = AsyncMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        mock_user = User(
            id=1,
            email="multi@example.com",
            username="multiuser",
            subscribed_topics=[],
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        # Subscribe to multiple topics
        await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="python",
        )
        await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="javascript",
        )
        updated_user = await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="rust",
        )

        assert updated_user is not None
        assert len(updated_user.subscribed_topics) == 3
        assert "python" in updated_user.subscribed_topics
        assert "javascript" in updated_user.subscribed_topics
        assert "rust" in updated_user.subscribed_topics

    @pytest.mark.asyncio
    async def test_subscribe_to_same_topic_twice(self):
        """Test subscribing to same topic twice doesn't duplicate."""
        mock_db = AsyncMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        mock_user = User(
            id=1,
            email="duplicate@example.com",
            username="duplicateuser",
            subscribed_topics=[],
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        # Subscribe to same topic twice
        await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="python",
        )
        updated_user = await UserService.subscribe_user_to_topic(
            db=mock_db,
            user_id=1,
            topic="python",
        )

        assert updated_user is not None
        assert len(updated_user.subscribed_topics) == 1
        assert updated_user.subscribed_topics.count("python") == 1

    @pytest.mark.asyncio
    async def test_subscribe_user_not_found(self):
        """Test subscribing non-existent user raises error."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(ValueError, match="User with id 99999 not found"):
            await UserService.subscribe_user_to_topic(
                db=mock_db,
                user_id=99999,
                topic="python",
            )
