# imports
from fastapi import FastAPI

from .routers import snap, friend, user

app = FastAPI()

app.include_router(api)
