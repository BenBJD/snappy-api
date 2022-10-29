from fastapi import APIRouter, Depends

from ..database import friend as friend_database
from ..dependencies import get_current_user
from ..models import UserInDB

api = APIRouter(prefix="/api/friend")


@api.get("", status_code=200)
def load_friends(current_user: UserInDB = Depends(get_current_user)):
    friends = friend_database.load(current_user.id)
    return friends


@api.put("", status_code=201)
def add_friend(friend_id: str, current_user: UserInDB = Depends(get_current_user)):
    friend_database.add(current_user.id, friend_id)


@api.delete("")
def remove_friend(friend_id: str, current_user: UserInDB = Depends(get_current_user)):
    friend_database.remove(current_user.id, friend_id)


@api.post("/")
def confirm_friend(friend_id: str, current_user: UserInDB = Depends(get_current_user)):
    friend_database.confirm(current_user.id, friend_id)
