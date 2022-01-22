from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..utils import verify_password
from .. import schemas, orm, oauth2
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=schemas.UserLoginResponse)
async def login(request: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(orm.User).filter(orm.User.email == request.email).first()
    if user is None or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Username or password is incorrect",
        )
    token = oauth2.create_access_token({"id": user.id, "email": user.email})
    return {"access_token": token}
