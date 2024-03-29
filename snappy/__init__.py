# imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import snap, friend, user

origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(snap.api)
app.include_router(friend.api)
app.include_router(user.api)
