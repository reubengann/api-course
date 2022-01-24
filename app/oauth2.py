import datetime
import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.environ.get("SECRET_KEY")
if SECRET_KEY is None:
    raise Exception("SECRET_KEY must be set as an environment variable")
ALGORITHM = jwt.ALGORITHMS.HS256
ACCESS_TOKEN_EXPIRATION_MINUTES = 30


class BadToken(Exception):
    pass


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
