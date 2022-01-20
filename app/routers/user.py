from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from ..utils import hash_password
from ..database import get_db
from .. import schemas, orm

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse,
)
async def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = orm.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
