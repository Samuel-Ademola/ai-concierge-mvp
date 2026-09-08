from app.dependencies.tenant import get_current_hotel
from datetime import datetime, timezone


import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.database import Base
from app.models.guest import Guest
from app.models.hotel import Hotel
from app.models.hotel_membership import HotelMembership
from app.models.user import User
from app.services.tenant_service import get_user_hotel


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def create_user(db, name, email):
    user = User(
        name=name,
        email=email,
        password_hash="test-hash",
        role="staff",
        is_active=True,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )

    db.add(user)
    db.flush()

    return user


def create_hotel(db, name):
    hotel = Hotel(
        name=name,
        address=f"{name} address",
        timezone="Africa/Lagos",
        is_active=True,
    )

    db.add(hotel)
    db.flush()

    return hotel


def create_membership(db, user, hotel):
    membership = HotelMembership(
        user_id=user.id,
        hotel_id=hotel.id,
        role="staff",
        is_active=True,
    )

    db.add(membership)
    db.flush()

    return membership


def test_user_resolves_to_their_active_hotel(db):
    hotel_a = create_hotel(db, "Hotel A")
    hotel_b = create_hotel(db, "Hotel B")

    user_a = create_user(
        db,
        "User A",
        "user-a@example.com",
    )

    user_b = create_user(
        db,
        "User B",
        "user-b@example.com",
    )

    create_membership(db, user_a, hotel_a)
    create_membership(db, user_b, hotel_b)

    db.commit()

    resolved_a = get_user_hotel(
        db=db,
        user_id=user_a.id,
    )

    resolved_b = get_user_hotel(
        db=db,
        user_id=user_b.id,
    )

    assert resolved_a.id == hotel_a.id
    assert resolved_b.id == hotel_b.id
    assert resolved_a.id != resolved_b.id


def test_user_without_active_membership_is_forbidden(db):
    user = create_user(
        db,
        "Unassigned User",
        "unassigned@example.com",
    )

    db.commit()

    with pytest.raises(HTTPException) as exc_info:
        get_user_hotel(
            db=db,
            user_id=user.id,
        )

    assert exc_info.value.status_code == 403


def test_inactive_membership_is_forbidden(db):
    hotel = create_hotel(db, "Inactive Membership Hotel")

    user = create_user(
        db,
        "Inactive Member",
        "inactive-member@example.com",
    )

    membership = create_membership(db, user, hotel)
    membership.is_active = False

    db.commit()

    with pytest.raises(HTTPException) as exc_info:
        get_user_hotel(
            db=db,
            user_id=user.id,
        )

    assert exc_info.value.status_code == 403


def test_inactive_hotel_is_forbidden(db):
    hotel = create_hotel(db, "Inactive Hotel")
    hotel.is_active = False

    user = create_user(
        db,
        "Hotel User",
        "hotel-user@example.com",
    )

    create_membership(db, user, hotel)

    db.commit()

    with pytest.raises(HTTPException) as exc_info:
        get_user_hotel(
            db=db,
            user_id=user.id,
        )

    assert exc_info.value.status_code == 403

def test_guest_resolves_to_their_active_hotel(db):
    hotel = create_hotel(db, "Guest Hotel")

    user = create_user(
        db,
        "Guest User",
        "guest-user@example.com",
    )

    guest = Guest(
        user_id=str(user.id),
        user_pk=user.id,
        hotel_id=hotel.id,
        name=user.name,
        email=user.email,
        language="English",
        room_preference="Single",
        requests="",
    )

    db.add(guest)
    db.commit()

    resolved_hotel = get_user_hotel(
        db=db,
        user_id=user.id,
    )

    assert resolved_hotel.id == hotel.id

def test_current_hotel_dependency_resolves_authenticated_user(db):
    hotel = create_hotel(db, "Dependency Hotel")

    user = create_user(
        db,
        "Dependency User",
        "dependency-user@example.com",
    )

    create_membership(db, user, hotel)
    db.commit()

    resolved_hotel = get_current_hotel(
        db=db,
        current_user={"user_id": str(user.id)},
    )

    assert resolved_hotel.id == hotel.id