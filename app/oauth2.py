import datetime
from jose import jwt, JWTError

SECRET_KEY = "aaaaaaa"  # for testing purposes
ALGORITHM = jwt.ALGORITHMS.HS256
ACCESS_TOKEN_EXPIRATION_MINUTES = 30


def create_access_token(payload: dict) -> str:
    claims = payload.copy()
    expiration_time = datetime.datetime.now() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRATION_MINUTES
    )

    claims["exp"] = expiration_time
    token = jwt.encode(claims, SECRET_KEY, ALGORITHM)
    return token
