import pytest
from app.database import get_db
from app.orm import Base
from app.main import app
from fastapi.testclient import TestClient

from tests.db import testing_get_db, engine

app.dependency_overrides[get_db] = testing_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_create_user(client):
    result = client.post(
        "/users/", json={"email": "test@example.com", "password": "password123"}
    )
    assert result.status_code == 201
    assert result.json().get("email") == "test@example.com"
