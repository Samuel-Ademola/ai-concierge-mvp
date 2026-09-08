"""add hotel tenant to guest requests

Revision ID: ec3af8fa40b8
Revises: 7dd2ec6d8e9b
Create Date: 2026-09-08 18:14:23.565772

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ec3af8fa40b8"
down_revision: Union[str, Sequence[str], None] = "7dd2ec6d8e9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The hotel_id column and index were already created before the
    # previous migration attempt failed on SQLite's FK ALTER operation.
    # Only add the missing foreign key using SQLite batch mode.
    with op.batch_alter_table("guest_requests") as batch_op:
        batch_op.create_foreign_key(
            "fk_guest_requests_hotel_id_hotels",
            "hotels",
            ["hotel_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("guest_requests") as batch_op:
        batch_op.drop_constraint(
            "fk_guest_requests_hotel_id_hotels",
            type_="foreignkey",
        )