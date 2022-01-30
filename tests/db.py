import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.database import get_db
from app.orm import Base
from app.main import app
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
