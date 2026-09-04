from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Existing identity field.
    # Keep this for backward compatibility with the current application.
    user_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    # New canonical User relationship.
    # Nullable so existing guest records are not broken during Phase 1.
    user_pk: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    # New hotel relationship.
    # Nullable because existing guests may not yet belong to a hotel.
    hotel_id: Mapped[int | None] = mapped_column(
        ForeignKey("hotels.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    room_preference: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    requests: Mapped[str] = mapped_column(
        String(200),
        default="",
        nullable=False,
    )

    # New User relationship
    user = relationship(
        "User",
        back_populates="guest_profile",
    )

    # New Hotel relationship
    hotel = relationship(
        "Hotel",
        back_populates="guests",
    )

    # New Stay relationship
    stays = relationship(
        "Stay",
        back_populates="guest",
        cascade="all, delete-orphan",
    )
