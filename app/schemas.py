import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass


class UserCreateResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class PostResponse(Post):
    id: int
    created_at: datetime.datetime
    owner: UserCreateResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    id: int
    email: EmailStr
