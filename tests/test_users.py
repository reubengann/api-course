from jose import jwt
import pytest
from app.settings import settings


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


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test2@example.com", "incorrect", 403),
        ("testwrong2@example.com", "password123", 403),
        ("testwrong@example.com", "incorrect", 403),
        (None, "password123", 422),
        ("test2@example.com", None, 422),
    ],
)
def test_bad_login(client, test_user, email, password, status_code):
    result = client.post("/login/", json={"email": email, "password": password})
    assert result.status_code == status_code
