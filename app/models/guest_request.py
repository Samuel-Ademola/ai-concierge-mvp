from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GuestRequest(Base):
    __tablename__ = "guest_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    request_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    user_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    # Canonical User relationship.
    # Nullable so existing legacy demo requests remain intact.
    user_pk: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    request_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    details: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )