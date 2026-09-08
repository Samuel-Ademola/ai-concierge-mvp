from sqlalchemy import select

from app.database import SessionLocal
from app.models.guest_request import GuestRequest


def create_guest_request(
    user_id: str,
    hotel_id: int,
    request_type: str,
    details: str,
):
    db = SessionLocal()

    try:
        user_pk = int(user_id)

        # Prevent duplicate active requests within the same hotel.
        existing_result = db.execute(
            select(GuestRequest)
            .where(
                GuestRequest.user_pk == user_pk,
                GuestRequest.hotel_id == hotel_id,
                GuestRequest.request_type == request_type,
                GuestRequest.details == details,
                GuestRequest.status.in_(["pending", "confirmed"]),
            )
            .order_by(GuestRequest.created_at.desc())
        )

        existing = existing_result.scalars().first()

        if existing is not None:
            return existing

        request = GuestRequest(
            request_id="TEMP",
            user_id=user_id,
            user_pk=user_pk,
            hotel_id=hotel_id,
            request_type=request_type,
            details=details,
            status="pending",
        )

        db.add(request)
        db.flush()

        request.request_id = f"REQ-{request.id:04d}"

        db.commit()
        db.refresh(request)

        return request

    finally:
        db.close()


def get_guest_requests(
    user_id: str,
    hotel_id: int,
):
    db = SessionLocal()

    try:
        result = db.execute(
            select(GuestRequest)
            .where(
                GuestRequest.user_pk == int(user_id),
                GuestRequest.hotel_id == hotel_id,
            )
            .order_by(GuestRequest.created_at.desc())
        )

        return result.scalars().all()

    finally:
        db.close()


def update_guest_request_status(
    request_id: str,
    hotel_id: int,
    status: str,
):
    db = SessionLocal()

    try:
        result = db.execute(
            select(GuestRequest).where(
                GuestRequest.request_id == request_id,
                GuestRequest.hotel_id == hotel_id,
            )
        )

        request = result.scalar_one_or_none()

        if request is None:
            return None

        request.status = status

        db.commit()
        db.refresh(request)

        return request

    finally:
        db.close()