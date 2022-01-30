import pytest
from jose import jwt
from app.settings import settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    result = client.post("/users/", json=user_data).json()
    result["password"] = user_data["password"]
    return result


def test_create_user(client):
    result = client.post(
        "/users/", json={"email": "test2@example.com", "password": "password123"}
    )
    assert result.status_code == 201
    assert result.json().get("email") == "test2@example.com"


def test_login_user(client, test_user):
    result = client.post(
        "/login/", json={"email": test_user["email"], "password": test_user["password"]}
    )
    token = result.json().get("access_token")
    token = jwt.decode(token, settings.secret_key, ["HS256"])
    assert token.get("id") == test_user["id"]
    assert result.json().get("token_type") == "bearer"
    assert result.status_code == 200
