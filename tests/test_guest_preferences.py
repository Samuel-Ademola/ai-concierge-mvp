from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def valid_payload():
    return {
        "guest_name": "Samuel",
        "email": "samuel@example.com",
        "language": "English",
        "room_preference": "Ocean View",
        "requests": "Extra pillows"
    }


def test_successful_creation():

    response = client.post(
        "/guest-preferences/",
        json=valid_payload()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["guest_name"] == "Samuel"
    assert "id" in data


def test_missing_required_fields():

    payload = valid_payload()

    del payload["language"]

    response = client.post(
        "/guest-preferences/",
        json=payload
    )

    assert response.status_code == 422


def test_invalid_email():

    payload = valid_payload()

    payload["email"] = "wrong-email"

    response = client.post(
        "/guest-preferences/",
        json=payload
    )

    assert response.status_code == 422


def test_requests_max_length():

    payload = valid_payload()

    payload["requests"] = "a" * 501

    response = client.post(
        "/guest-preferences/",
        json=payload
    )

    assert response.status_code == 422