from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import schemas, orm, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> dict:
    result = db.query(orm.Post).all()
    return result


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(
    post: schemas.Post,
    db: Session = Depends(get_db),
    token: schemas.Token = Depends(oauth2.verify_token),
) -> dict:
    new_post = orm.Post(owner_id=token.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)) -> orm.Post:
    post = db.query(orm.Post).filter(orm.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    token: schemas.Token = Depends(oauth2.verify_token),
):
    post_query = db.query(orm.Post).filter(orm.Post.id == post_id)
    post_result = post_query.first()
    if post_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_result.owner_id != token.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(
    post_id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    token: schemas.Token = Depends(oauth2.verify_token),
):
    post_query = db.query(orm.Post).filter(orm.Post.id == post_id)
    post_result = post_query.first()
    if post_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_result.owner_id != token.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
