from typing import Any, Dict, Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root() -> dict:
    return {"message": "Hello, world"}


@app.get("/posts")
async def get_posts() -> dict:
    return {"data": "Here's the post"}


@app.post("/createpost")
async def create_post(post: Post) -> dict:
    return {"new_post": f"data: {post}"}
