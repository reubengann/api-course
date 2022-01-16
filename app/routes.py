from fastapi import FastAPI, HTTPException, status
from .database import ensure_created
from .models import Post

conn, cursor = ensure_created()
app = FastAPI()


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
