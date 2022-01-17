from sqlalchemy import Boolean, Column, Integer, String, Text
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer)
