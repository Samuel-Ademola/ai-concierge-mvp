from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.models.guest import Guest
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.services import auth_service


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

    yield TestingSessionLocal

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def client(test_db):
    return TestClient(app)


def signup(client, email="test@example.com", password="TestPassword123!"):
    return client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
        },
    )


def login(client, email="test@example.com", password="TestPassword123!"):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def test_signup_creates_user_and_guest(client, test_db):
    response = signup(client)

    assert response.status_code == 201

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["role"] == "guest"
    assert data["user_id"].isdigit()
    assert data["access_token"]

    db = test_db()

    user = db.execute(
        select(User).where(User.email == "test@example.com")
    ).scalar_one()

    guest = db.execute(
        select(Guest).where(Guest.user_pk == user.id)
    ).scalar_one()

    assert user.name == "Test User"
    assert user.role == "guest"
    assert guest.user_pk == user.id
    assert guest.user_id == str(user.id)
    assert guest.email == user.email

    db.close()


def test_duplicate_email_is_rejected(client):
    first = signup(client)

    assert first.status_code == 201

    duplicate = signup(client)

    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == (
        "An account with this email already exists"
    )


def test_signup_rejects_short_password(client):
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "short@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422


def test_signup_rejects_invalid_email(client):
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "not-an-email",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422


def test_login_succeeds(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    response = login(client)

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["role"] == "guest"
    assert data["user_id"].isdigit()
    assert data["access_token"]


def test_login_rejects_wrong_password(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    response = login(
        client,
        password="WrongPassword123!",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_me_returns_authenticated_user(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    token = signup_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == signup_response.json()["user_id"]
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "guest"


def test_me_rejects_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
    )

    assert response.status_code == 401


def test_me_rejects_expired_token(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user_id"]

    now = datetime.now(timezone.utc)

    expired_token = jwt.encode(
        {
            "sub": user_id,
            "role": "guest",
            "iat": now - timedelta(hours=2),
            "exp": now - timedelta(hours=1),
        },
        auth_service.SECRET_KEY,
        algorithm=auth_service.ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Authentication token has expired"
    )


def test_accounts_are_isolated(client):
    first = signup(
        client,
        email="first@example.com",
    )

    second = signup(
        client,
        email="second@example.com",
    )

    assert first.status_code == 201
    assert second.status_code == 201

    first_token = first.json()["access_token"]
    second_user_id = second.json()["user_id"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["user_id"] != second_user_id
    assert response.json()["email"] == "first@example.com"


def test_forgot_password_creates_reset_token(client, test_db):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "test@example.com",
        },
    )

    assert response.status_code == 200

    message = response.json()["message"]

    assert message.startswith("Password reset token: ")

    raw_token = message.replace(
        "Password reset token: ",
        "",
        1,
    )

    assert raw_token

    db = test_db()

    reset_token = db.execute(
        select(PasswordResetToken)
    ).scalar_one()

    assert reset_token.token_hash != raw_token
    assert reset_token.user_id == int(
        signup_response.json()["user_id"]
    )
    assert reset_token.used_at is None

    db.close()


def test_reset_password_changes_password(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    reset_response = client.post(
        "/auth/forgot-password",
        json={
            "email": "test@example.com",
        },
    )

    reset_message = reset_response.json()["message"]

    token = reset_message.replace(
        "Password reset token: ",
        "",
        1,
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Password has been reset successfully."
    )

    old_login = login(client)

    assert old_login.status_code == 401

    new_login = login(
        client,
        password="NewPassword123!",
    )

    assert new_login.status_code == 200


def test_reset_token_cannot_be_reused(client):
    signup_response = signup(client)

    assert signup_response.status_code == 201

    reset_response = client.post(
        "/auth/forgot-password",
        json={
            "email": "test@example.com",
        },
    )

    token = reset_response.json()["message"].replace(
        "Password reset token: ",
        "",
        1,
    )

    first_reset = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!",
        },
    )

    assert first_reset.status_code == 200

    second_reset = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "AnotherPassword123!",
        },
    )

    assert second_reset.status_code == 400
    assert second_reset.json()["detail"] == (
        "Invalid or expired password reset token"
    )


def test_reset_rejects_invalid_token(client):
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "not-a-real-reset-token",
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid or expired password reset token"
    )


def test_forgot_password_does_not_reveal_unknown_email(client):
    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "does-not-exist@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "If an account exists for that email, "
        "a password reset link has been requested."
    )
