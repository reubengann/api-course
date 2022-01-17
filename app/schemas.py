import datetime
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass


class PostResponse(Post):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
