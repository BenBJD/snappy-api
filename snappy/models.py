import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str
    snappy_score: int


class UserInDB(User):
    id: str
    password_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None


class Snap(BaseModel):
    id: str
    from_user_id: str
    to_user_id: str
    date: str
    time: str
    seen: bool
