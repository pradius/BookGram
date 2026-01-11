"""add test user

Revision ID: 12a33139df0f
Revises: 26a311441e93
Create Date: 2026-01-11 16:27:24.055777+00:00

"""

from collections.abc import Sequence
from typing import Union
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "12a33139df0f"
down_revision: Union[str, None] = "26a311441e93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - insert test user if not exists."""
    # Check if test user already exists
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT COUNT(*) FROM users WHERE email = 'test@bookgram.com'")
    )
    count = result.scalar()

    # Only insert if user doesn't exist
    if count == 0:
        users_table = sa.table(
            "users",
            sa.column("email", sa.String),
            sa.column("username", sa.String),
            sa.column("subscribed_topics", sa.ARRAY(sa.String)),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        )

        op.bulk_insert(
            users_table,
            [
                {
                    "email": "test@bookgram.com",
                    "username": "testuser",
                    "subscribed_topics": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            ],
        )


def downgrade() -> None:
    """Downgrade schema - remove test user."""
    op.execute("DELETE FROM users WHERE email = 'test@bookgram.com'")

