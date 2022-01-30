from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.orm import Base


engine = create_engine(
    "sqlite:///unittest.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def testing_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
