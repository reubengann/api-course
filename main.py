from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

my_posts = [
    {
        "id": 1,
        "title": "A well thought out englilsh paper",
        "content": "Eating 5 batteries",
        "published": True,
        "rating": None,
    }
]


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
    return {"posts": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    new_post = post.dict()
    new_post["id"] = len(my_posts) + 1
    my_posts.append(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return find_post(post_id)


def find_post(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {post_id} not found",
    )


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    post = find_post(post_id)
    my_posts.remove(post)
    return {"detail": f"Removed post with id {post_id}"}


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int, post: Post):
    old_post = find_post(post_id)
    post = post.dict()
    for k in post:
        old_post[k] = post[k]
    return {"detail": f"Updated post with id {post_id}"}
