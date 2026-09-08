import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
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

    yield TestingSessionLocal

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


def test_get_requests_uses_authenticated_user(client):
    first = signup(client, "request-one@example.com")
    second = signup(client, "request-two@example.com")

    assert first.status_code == 201
    assert second.status_code == 201

    first_token = first.json()["access_token"]
    second_token = second.json()["access_token"]

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