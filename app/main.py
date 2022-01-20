from fastapi import FastAPI

from .database import engine
from . import orm
from .routers import user, post

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

orm.Base.metadata.create_all(engine)
