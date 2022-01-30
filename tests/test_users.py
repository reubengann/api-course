from .db import session, client


def test_create_user(client):
    result = client.post(
        "/users/", json={"email": "test@example.com", "password": "password123"}
    )
    assert result.status_code == 201
    assert result.json().get("email") == "test@example.com"
