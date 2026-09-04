"""phase1 hospitality schema

Revision ID: 2c2a3ee91c30
Revises:
Create Date: 2026-09-04 02:43:35.192805

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2c2a3ee91c30"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("guests", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_pk",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "hotel_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_index(
            "ix_guests_user_pk",
            ["user_pk"],
            unique=False,
        )

        batch_op.create_index(
            "ix_guests_hotel_id",
            ["hotel_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_guests_user_pk_users",
            "users",
            ["user_pk"],
            ["id"],
        )

        batch_op.create_foreign_key(
            "fk_guests_hotel_id_hotels",
            "hotels",
            ["hotel_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("guests", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_guests_hotel_id_hotels",
            type_="foreignkey",
        )

        batch_op.drop_constraint(
            "fk_guests_user_pk_users",
            type_="foreignkey",
        )

        batch_op.drop_index("ix_guests_hotel_id")
        batch_op.drop_index("ix_guests_user_pk")

        batch_op.drop_column("hotel_id")
        batch_op.drop_column("user_pk")
