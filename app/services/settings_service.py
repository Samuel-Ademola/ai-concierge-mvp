from sqlalchemy import select

from app.database import SessionLocal
from app.models.guest import Guest


def _user_pk(user_id: str) -> int | None:
    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None


def _guest_preferences_response(guest: Guest):
    return {
        "id": guest.id,
        "name": guest.name,
        "email": guest.email,
        "language": guest.language,
        "roomPreference": guest.room_preference,
        "requests": guest.requests,
    }


def save_guest_preferences(user_id: str, preferences: dict):
    user_pk = _user_pk(user_id)

    if user_pk is None:
        return None

    db = SessionLocal()

    try:
        guest = db.execute(
            select(Guest).where(Guest.user_pk == user_pk)
        ).scalar_one_or_none()

        if guest is None:
            guest = Guest(
                user_id=user_id,
                user_pk=user_pk,
                name=preferences["name"],
                email=preferences["email"],
                language=preferences["language"],
                room_preference=preferences["roomPreference"],
                requests=preferences.get("requests", ""),
            )
            db.add(guest)
        else:
            guest.name = preferences["name"]
            guest.email = preferences["email"]
            guest.language = preferences["language"]
            guest.room_preference = preferences["roomPreference"]
            guest.requests = preferences.get("requests", "")

        db.commit()
        db.refresh(guest)

        return _guest_preferences_response(guest)

    finally:
        db.close()


def get_guest_preferences(user_id: str):
    user_pk = _user_pk(user_id)

    if user_pk is None:
        return None

    db = SessionLocal()

    try:
        guest = db.execute(
            select(Guest).where(Guest.user_pk == user_pk)
        ).scalar_one_or_none()

        if guest is None:
            return None

        return _guest_preferences_response(guest)

    finally:
        db.close()


def clear_guest_preferences(user_id: str):
    user_pk = _user_pk(user_id)

    if user_pk is None:
        return

    db = SessionLocal()

    try:
        guest = db.execute(
            select(Guest).where(Guest.user_pk == user_pk)
        ).scalar_one_or_none()

        if guest:
            db.delete(guest)
            db.commit()

    finally:
        db.close()
