from fastapi import FastAPI

from .database import engine
from . import orm
from .routers import user, post, auth, vote

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

orm.Base.metadata.create_all(engine)
