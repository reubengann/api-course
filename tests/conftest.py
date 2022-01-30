import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app import orm
from app.database import get_db
from app.orm import Base
from app.main import app
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient

from app.orm import Base


engine = create_engine(
    "sqlite:///unittest.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client(session):
    def testing_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = testing_get_db
    yield TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    result = client.post("/users/", json=user_data).json()
    result["password"] = user_data["password"]
    return result


@pytest.fixture
def token(test_user):
    return create_access_token({"id": test_user.get("id"), "email": test_user["email"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers["Authorization"] = "Bearer " + token
    return client


@pytest.fixture
def example_posts(test_user, session):
    posts_data = [
        {"title": "1st title", "content": "content", "owner_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
    ]
    session.add_all([orm.Post(**d) for d in posts_data])
    session.commit()
    return session.query(orm.Post).all()
