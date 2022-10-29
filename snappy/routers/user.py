from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..config import settings
from ..database import user as user_database
from ..dependencies import get_current_user, create_access_token
from ..models import UserInDB, Token

api = APIRouter(prefix="/api/user")


@api.put("/", status_code=201)
def add_user(username: str, password: str):
    user_database.add(username, password)


@api.delete("/", status_code=200)
def delete_user(current_user: UserInDB = Depends(get_current_user)):
    user_database.delete(current_user.id)


# Authentication and token creation endpoint
@api.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Get user
    user_data = user_database.load(username=form_data.username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserInDB(**user_data)
    # Exception if password wrong
    if not user_database.pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api.get("/")
def load_user(username: str, current_user: UserInDB = Depends(get_current_user)):
    # If it's the logged-in user, just return current_user
    if username == current_user.username:
        del current_user.password_hash
        return current_user
    else:
        pass
    # For everyone else just return the id
    user_data = user_database.load(username=username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username",
        )
    user = UserInDB(**user_data)
    return user.id


@api.post("/", status_code=200)
def change_password(password: str, current_user: UserInDB = Depends(get_current_user)):
    user_database.save(current_user.id, password=password)
