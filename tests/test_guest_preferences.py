from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_preferences():
    response = client.post(
        "/preferences/",
        json={
            "name": "Samuel",
            "email": "samuel@example.com",
            "language": "English",
            "room_preference": "Suite",
            "requests": "High floor"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Samuel"
    assert data["email"] == "samuel@example.com"
    assert data["language"] == "English"
    assert data["room_preference"] == "Suite"


def test_invalid_email():
    response = client.post(
        "/preferences/",
        json={
            "name": "Samuel",
            "email": "invalid-email",
            "language": "English",
            "room_preference": "Suite",
            "requests": ""
        }
    )

    assert response.status_code == 422


def test_name_required():
    response = client.post(
        "/preferences/",
        json={
            "name": "",
            "email": "samuel@example.com",
            "language": "English",
            "room_preference": "Suite",
            "requests": ""
        }
    )

    assert response.status_code == 422