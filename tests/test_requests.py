import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.guest import Guest
from app.models.guest_request import GuestRequest
from app.models.hotel import Hotel
from app.models.user import User
from app.services import auth_service, request_service


@pytest.fixture()
def test_db(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    monkeypatch.setattr(
        auth_service,
        "SessionLocal",
        TestingSessionLocal,
    )

    monkeypatch.setattr(
        request_service,
        "SessionLocal",
        TestingSessionLocal,
    )

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def client(test_db):
    return TestClient(app)


def signup(client, email):
    return client.post(
        "/auth/signup",
        json={
            "name": "Request Test User",
            "email": email,
            "password": "TestPassword123!",
        },
    )


def assign_guest_to_hotel(test_db, user_id, hotel_id):
    db = test_db()

    try:
        guest = db.execute(
            select(Guest).where(
                Guest.user_pk == int(user_id),
            )
        ).scalar_one()

        guest.hotel_id = hotel_id

        db.commit()
    finally:
        db.close()


def create_hotel(test_db, name):
    db = test_db()

    try:
        hotel = Hotel(
            name=name,
            address=f"{name} address",
            timezone="Africa/Lagos",
            is_active=True,
        )

        db.add(hotel)
        db.commit()
        db.refresh(hotel)

        return hotel.id
    finally:
        db.close()

def create_staff_membership(test_db, user_id, hotel_id):
    from app.models.hotel_membership import HotelMembership

    db = test_db()
    try:
        membership = HotelMembership(
            user_id=int(user_id),
            hotel_id=hotel_id,
            role="staff",
            is_active=True,
        )
        db.add(membership)
        db.commit()
    finally:
        db.close()

def promote_user_to_staff(test_db, user_id):
    db = test_db()
    try:
        user = db.execute(
            select(User).where(User.id == int(user_id))
        ).scalar_one()
        user.role = "staff"
        db.commit()
    finally:
        db.close()

def test_get_requests_uses_authenticated_user(client, test_db):
    hotel_a_id = create_hotel(
        test_db,
        "Hotel A",
    )

    first = signup(
        client,
        "request-one@example.com",
    )

    second = signup(
        client,
        "request-two@example.com",
    )

    assert first.status_code == 201
    assert second.status_code == 201

    first_token = first.json()["access_token"]
    second_token = second.json()["access_token"]

    assign_guest_to_hotel(
        test_db,
        first.json()["user_id"],
        hotel_a_id,
    )

    assign_guest_to_hotel(
        test_db,
        second.json()["user_id"],
        hotel_a_id,
    )

    create_response = client.post(
        "/requests",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
        json={
            "request_type": "dining",
            "details": "Italian dinner",
        },
    )

    assert create_response.status_code == 200

    response = client.get(
        "/requests",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["user_id"] == first.json()["user_id"]

    second_response = client.get(
        "/requests",
        headers={
            "Authorization": f"Bearer {second_token}",
        },
    )

    assert second_response.status_code == 200
    assert second_response.json() == []


def test_get_requests_requires_authentication(client):
    response = client.get("/requests")

    assert response.status_code == 401

def test_guest_cannot_see_requests_from_another_hotel(client, test_db):
    hotel_a_id = create_hotel(test_db, "Hotel A")
    hotel_b_id = create_hotel(test_db, "Hotel B")

    first = signup(client, "hotel-a-guest@example.com")
    second = signup(client, "hotel-b-guest@example.com")

    assert first.status_code == 201
    assert second.status_code == 201

    first_token = first.json()["access_token"]
    second_token = second.json()["access_token"]

    assign_guest_to_hotel(test_db, first.json()["user_id"], hotel_a_id)
    assign_guest_to_hotel(test_db, second.json()["user_id"], hotel_b_id)

    create_response = client.post(
        "/requests",
        headers={"Authorization": f"Bearer {first_token}"},
        json={
            "request_type": "maintenance",
            "details": "Air conditioner issue",
        },
    )

    assert create_response.status_code == 200

    response = client.get(
        "/requests",
        headers={"Authorization": f"Bearer {second_token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_staff_cannot_update_request_from_another_hotel(client, test_db):
    hotel_a_id = create_hotel(test_db, "Hotel A")
    hotel_b_id = create_hotel(test_db, "Hotel B")

    guest = signup(client, "guest-a@example.com")
    staff = signup(client, "staff-b@example.com")

    assert guest.status_code == 201
    assert staff.status_code == 201

    guest_token = guest.json()["access_token"]

    assign_guest_to_hotel(
        test_db,
        guest.json()["user_id"],
        hotel_a_id,
    )

    create_staff_membership(
        test_db,
        staff.json()["user_id"],
        hotel_b_id,
    )

    promote_user_to_staff(
        test_db,
        staff.json()["user_id"],
    )

    staff_login = client.post(
        "/auth/login",
        json={
            "email": "staff-b@example.com",
            "password": "TestPassword123!",
        },
    )

    assert staff_login.status_code == 200

    staff_token = staff_login.json()["access_token"]

    create_response = client.post(
        "/requests",
        headers={"Authorization": f"Bearer {guest_token}"},
        json={
            "request_type": "maintenance",
            "details": "Broken AC",
        },
    )

    assert create_response.status_code == 200

    request_id = create_response.json()["request_id"]

    response = client.patch(
        f"/requests/{request_id}",
        headers={"Authorization": f"Bearer {staff_token}"},
        json={"status": "confirmed"},
    )

    assert response.status_code == 404


def test_request_creation_uses_authenticated_hotel(client, test_db):
    hotel_a_id = create_hotel(test_db, "Hotel A")
    hotel_b_id = create_hotel(test_db, "Hotel B")

    guest = signup(client, "hotel-owner-guest@example.com")

    assert guest.status_code == 201

    token = guest.json()["access_token"]

    assign_guest_to_hotel(
        test_db,
        guest.json()["user_id"],
        hotel_a_id,
    )

    response = client.post(
        "/requests",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "request_type": "dining",
            "details": "Dinner reservation",
        },
    )

    assert response.status_code == 200

    data = response.json()
    request_id = data["request_id"]

    db = test_db()

    try:
        request = db.execute(
            select(GuestRequest).where(
                GuestRequest.request_id == request_id
            )
        ).scalar_one()

        assert request.hotel_id == hotel_a_id
        assert request.hotel_id != hotel_b_id

    finally:
        db.close()