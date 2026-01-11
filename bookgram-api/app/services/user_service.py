"""User service for handling user operations."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserService:
    """Service for user-related operations."""

    @staticmethod
    async def subscribe_user_to_topic(
        db: AsyncSession,
        user_id: int,
        topic: str,
    ) -> User:
        """
        Subscribe a user to a topic.

        Args:
            db: Database session
            user_id: User ID
            topic: Topic to subscribe to

        Returns:
            Updated User instance
        """
        # Get user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        # Initialize subscribed_topics if None
        if user.subscribed_topics is None:
            user.subscribed_topics = []

        # Add topic if not already subscribed
        if topic not in user.subscribed_topics:
            user.subscribed_topics = [*user.subscribed_topics, topic]

        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User | None:
        """Get a user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        username: str,
    ) -> User:
        """Create a new user."""
        db_user = User(email=email, username=username, subscribed_topics=[])
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return db_user
