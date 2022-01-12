from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
import os


app = FastAPI()
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
    cursor.execute("SELECT * FROM posts")
    return {"posts": cursor.fetchall()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (?, ?, ?) RETURNING *",
        (post.title, post.content, post.published),
    )
    new_post = dict(cursor.fetchone())
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id = ? RETURNING *", (post_id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return {"removed": deleted_post}


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = ?, content = ?, published = ? WHERE id = ? RETURNING *",
        (post.title, post.content, post.published, post_id),
    )
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return {"updated_post": updated_post}
