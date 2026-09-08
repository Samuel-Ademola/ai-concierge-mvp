"""add hotel memberships

Revision ID: 7dd2ec6d8e9b
Revises: f95520ab98f5
Create Date: 2026-09-08 13:29:44.991393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7dd2ec6d8e9b"
down_revision: Union[str, Sequence[str], None] = "f95520ab98f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the hotel memberships table."""
    op.create_table(
        "hotel_memberships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "hotel_id",
            name="uq_hotel_membership_user_hotel",
        ),
    )

    op.create_index(
        "ix_hotel_memberships_id",
        "hotel_memberships",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_hotel_memberships_user_id",
        "hotel_memberships",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_hotel_memberships_hotel_id",
        "hotel_memberships",
        ["hotel_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the hotel memberships table."""
    op.drop_index(
        "ix_hotel_memberships_hotel_id",
        table_name="hotel_memberships",
    )
    op.drop_index(
        "ix_hotel_memberships_user_id",
        table_name="hotel_memberships",
    )
    op.drop_index(
        "ix_hotel_memberships_id",
        table_name="hotel_memberships",
    )
    op.drop_table("hotel_memberships")
