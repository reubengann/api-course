import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from . import schemas, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.settings.secret_key
ALGORITHM = jwt.ALGORITHMS.HS256
ACCESS_TOKEN_EXPIRATION_MINUTES = 30


BadToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(payload: dict) -> str:
    claims = payload.copy()
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRATION_MINUTES
    )

    claims["exp"] = expiration_time
    token = jwt.encode(claims, SECRET_KEY, ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme)) -> schemas.Token:
    try:
        claims = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise BadToken
    if claims.get("id") is None:
        raise BadToken
    return schemas.Token(**claims)
