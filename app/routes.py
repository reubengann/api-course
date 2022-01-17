from fastapi import Depends, FastAPI, HTTPException, Response, status
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas
from . import orm

app = FastAPI()
orm.Base.metadata.create_all(engine)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello, world"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)) -> dict:
    result = db.query(orm.Post).all()
    return {"posts": result}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)) -> dict:
    new_post = orm.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    post = db.query(orm.Post).filter(orm.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"post-detail": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(orm.Post).filter(orm.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(orm.Post).filter(orm.Post.id == post_id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
