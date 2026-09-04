from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Stay(Base):
    __tablename__ = "stays"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    guest_id: Mapped[int] = mapped_column(
        ForeignKey("guests.id"),
        nullable=False,
        index=True,
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False,
        index=True,
    )

    check_in: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    check_out: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    guest = relationship(
        "Guest",
        back_populates="stays",
    )

    room = relationship(
        "Room",
        back_populates="stays",
    )
