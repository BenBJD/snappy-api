# imports
from fastapi import FastAPI

from .routers import snap, friend, user

app = FastAPI()

app.include_router(snap.api)
app.include_router(friend.api)
app.include_router(user.api)
