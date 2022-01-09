from typing import Any, Dict
from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello, world"}


@app.get("/posts")
async def get_posts() -> dict:
    return {"data": "Here's the post"}


@app.post("/createpost")
async def create_post(payload: Dict[str, Any] = Body(...)) -> dict:
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
