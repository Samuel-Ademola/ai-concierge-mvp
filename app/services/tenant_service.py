from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.guest import Guest
from app.models.hotel import Hotel
from app.models.hotel_membership import HotelMembership


def _get_active_hotel(
    db: Session,
    hotel_id: int,
) -> Hotel:
    hotel_result = db.execute(
        select(Hotel).where(
            Hotel.id == hotel_id,
            Hotel.is_active.is_(True),
        )
    )

    hotel = hotel_result.scalar_one_or_none()

    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hotel is not active",
        )

    return hotel


def get_user_hotel(
    db: Session,
    user_id: int,
) -> Hotel:
    membership_result = db.execute(
        select(HotelMembership)
        .where(
            HotelMembership.user_id == user_id,
            HotelMembership.is_active.is_(True),
        )
        .order_by(HotelMembership.id.asc())
    )

    membership = membership_result.scalars().first()

    if membership is not None:
        return _get_active_hotel(
            db=db,
            hotel_id=membership.hotel_id,
        )

    guest_result = db.execute(
        select(Guest).where(
            Guest.user_pk == user_id,
            Guest.hotel_id.is_not(None),
        )
    )

    guest = guest_result.scalar_one_or_none()

    if guest is not None and guest.hotel_id is not None:
        return _get_active_hotel(
            db=db,
            hotel_id=guest.hotel_id,
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not associated with an active hotel",
        )