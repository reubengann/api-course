import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    published = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    owner_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
