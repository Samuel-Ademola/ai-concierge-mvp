from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id"),
        nullable=False,
        index=True,
    )

    room_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    room_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="available",
        nullable=False,
    )

    hotel = relationship(
        "Hotel",
        back_populates="rooms",
    )

    stays = relationship(
        "Stay",
        back_populates="room",
    )
