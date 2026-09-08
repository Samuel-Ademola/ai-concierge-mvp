"""link guest requests to users

Revision ID: f95520ab98f5
Revises: ef60349e4397
Create Date: 2026-09-07 21:17:16.463830

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f95520ab98f5"
down_revision: Union[str, Sequence[str], None] = "ef60349e4397"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("guest_requests", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_pk", sa.Integer(), nullable=True)
        )
        batch_op.create_index(
            "ix_guest_requests_user_pk",
            ["user_pk"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_guest_requests_user_pk_users",
            "users",
            ["user_pk"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("guest_requests", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_guest_requests_user_pk_users",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_guest_requests_user_pk")
        batch_op.drop_column("user_pk")
