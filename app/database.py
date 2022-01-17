import os
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_created():
    if not os.path.exists("test.db"):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute(
            """create table posts (
    id integer primary key autoincrement,
    title varchar(255) not null,
    content text not null,
    published bool not null,
    rating int null
    )"""
        )
        conn.commit()
    else:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

    cursor.row_factory = sqlite3.Row
    return conn, cursor


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
