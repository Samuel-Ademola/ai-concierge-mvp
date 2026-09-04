from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        default="",
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(80),
        default="Africa/Lagos",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    rooms = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete-orphan",
    )

    guests = relationship(
        "Guest",
        back_populates="hotel",
    )
