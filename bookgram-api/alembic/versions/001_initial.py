"""Initial migration - create files and users tables

Revision ID: 001
Revises:
Create Date: 2026-01-11

"""

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create files table
    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("location_url", sa.String(length=512), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("format", sa.String(length=50), nullable=False),
        sa.Column("chapters", sa.ARRAY(sa.Text()), nullable=True),
        sa.Column("pages", sa.ARRAY(sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_id"), "files", ["id"], unique=False)
    op.create_index(op.f("ix_files_topic"), "files", ["topic"], unique=False)
    op.create_index(op.f("ix_files_location_url"), "files", ["location_url"], unique=True)

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("subscribed_topics", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Insert test user
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
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop users table
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    # Drop files table
    op.drop_index(op.f("ix_files_location_url"), table_name="files")
    op.drop_index(op.f("ix_files_topic"), table_name="files")
    op.drop_index(op.f("ix_files_id"), table_name="files")
    op.drop_table("files")
