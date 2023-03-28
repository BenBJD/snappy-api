from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import settings
from .database.user import load as user_load
from .database.friend import load as load_friends
from .models import TokenData, UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = UserInDB(**user_load(user_id=token_data.user_id))
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def check_user_is_friend(user_id: str, friend_id: str, confirmed: bool):
    # Get the user's confirmed friends
    friends = load_friends(user_id, confirmed)
    # Get the friend ids, excluding the users own id
    friend_ids = []
    for i in friends:
        if not i["friend_id"] == user_id:
            friend_ids.append(i["friend_id"])
    # Return true if they are friends
    return friend_id in friend_ids
