from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, orm, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote_data: schemas.Vote,
    db: Session = Depends(get_db),
    token: schemas.Token = Depends(oauth2.verify_token),
) -> dict:
    if db.query(orm.Post).filter(orm.Post.id == vote_data.post_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist"
        )
    vote_query = db.query(orm.Vote).filter(
        orm.Vote.post_id == vote_data.post_id, orm.Vote.user_id == token.id
    )
    vote_row = vote_query.first()
    if vote_data.vote_direction == 1:
        if vote_row is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted for that post",
            )
        vote_row = orm.Vote(user_id=token.id, post_id=vote_data.post_id)
        db.add(vote_row)
        db.commit()
        return {"message": "success"}
    if vote_row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No vote to undo"
        )
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Vote successfully undone"}
