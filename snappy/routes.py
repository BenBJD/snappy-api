# Imports
from uuid import uuid1
from fastapi import APIRouter, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from . import database

api = APIRouter(prefix="/api/v1")
api.mount("/static", StaticFiles(directory="./static"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

### Friends ###
"""
URL: /api/v1/friends/load
Required form data: login_token (string), user_id (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, load the rows of the user's friends with database.friends.load() and return the rows
If login token is invalid, return a json response where result = "permission denied"
"""
class Login(BaseModel):
    login_token: str
    user_ID: str
@api.post("/friends/load")
def load_friends(user_id: str, token: str = Depends(oauth2_scheme)):
    # Check login token
    if database.user.login_token_valid(user_id, login_token):
        # return json response of the result
        return database.friends.load(user_id)
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/friends/add
Required form data: login_token (string), user_id (string), friend_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, adds the friend with database.friends.add() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@api.post("/friends/add")
def add_friend():
    # Load request data
    login_token = request.form["login_token"]
    user_ID = request.form["user_id"]
    friend_ID = request.form["friend_ID"]
    # Check login token
    if database.user.login_token_valid(user_ID, login_token):
        # return json response of the result
        return {
            "result": database.friends.add(user_ID, friend_ID)
        }
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/friends/remove
Required form data: login_token (string), user_id (string), friend_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, remove the friend with database.friends.remove() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@api.post("/friends/remove")
def remove_friend():
    login_token = request.form["login_token"]
    user_ID = request.form["user_id"]
    friend_ID = request.form["friend_ID"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.friends.remove(user_ID, friend_ID)
        })
    else:
        return {
            "result": "permission denied"
        }


### User ###
"""
URL: /api/v1/users/add
Required form data: email (string), password (string), dark_mode (int), user_name (string)

Description:
Get email, password, dark_mode and user_name from the request then add the user with database.user.add() and return the result
"""
@api.post("/user/add")
def add_user():
    email = request.form["email"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    return {
        "result": database.user.add(email, password, dark_mode, user_name)
    }


"""
URL: /api/v1/user/delete
Methods: POST
Required form data: login_token (string), user_id (string)

Description:
Gets the login_token and user_id from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, remove the user with database.user.remove() and return the result
If login token is invalid, return result = "permission denied"
"""
@api.post("/user/delete")
def delete_user():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return {
            "result": database.user.delete(user_ID)
        }
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/user/login
Required form data: user (string), password (string)

Description:
Get the user_name or email and password from the request and attempt a login with database.user.login().
If the login failed e.g. wrong password then return result = "permission denied"
If the login was successful, a login token for the user will be returned
"""
@api.post("/user/login")
def login_user(form_data: OAuth2PasswordRequestForm= Depends()):
    token = ""
    return {
        "access_token": token,
        "token_type": "bearer"
    }


"""
URL: /api/v1/user/logout
Required form data: login_token (string), user_id (string)

Description:
Gets the login_token and user_id from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, logout the user with database.user.remove() and return the result
If login token is invalid, return result = "permission denied"
"""
@api.post("/user/logout")
def logout_user():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return {
            "result": database.user.logout(user_ID)
        }
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/user/load
Required form data: login_token (string), user_id (string), search_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, load the data of the user specified with search_ID with database.user.load() and return the result.
If the search ID is 'all' then a list of all the users will be returned sans some private details.
If login token is invalid, return result = "permission denied"
"""
@api.post("/user/load")
def load_user():
    user_ID = request.form["user_id"]
    search_ID = request.form["search_ID"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return database.user.load(user_ID, search_ID)
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/user/save
Required form data: login_token (string), user_id (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, save the user's new data to  with database.user.save() and return the result
If login token is invalid, return result = "permission denied"
"""
@api.post("/user/save")
def save_user():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    if database.user.login_token_valid(user_ID, login_token):
        return {
            "result": database.user.save(user_ID, password, dark_mode, user_name)
        }
    else:
        return {
            "result": "permission denied"
        }


# Snap
"""
URL: /api/v1/snaps/send
Required form data: login_token (string), user_id (string), to_user_ID (string), image (file)

Description:
Gets the login token, user ID, recieving user ID and the image from the request then checks if login token is valid with database.user.login_token_valid().
If login token is valid, save the image and make add a row to database with database.snaps.send() then return the result
If login token is invalid, return result = "permission denied"
"""
@api.post("/snaps/send")
def send_snap():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    to_user_ID = request.form["to_user_ID"]
    image = request.files["image"]
    if database.user.login_token_valid(user_ID, login_token):
        snap_ID = uuid1()
        image.save(f"./uploads/{snap_ID}")
        return {
            "result": database.snaps.send(user_ID, to_user_ID, snap_ID)
        }
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/snaps/load
Required form data: login_token (string), user_id (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, get a list of incoming snaps for the user database.snaps.load() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@api.post("/snaps/load")
def load_snaps():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return database.snaps.load(user_ID)
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/snaps/download
Required form data: login_token (string), user_id (string), snap_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, 
If login token is invalid, return a json response where result = "permission denied"
"""
@api.post("/snaps/download")
def download_snap():
    user_ID = request.form["user_id"]
    login_token = request.form["login_token"]
    snap_ID = request.form["snap_ID"]
    if database.user.login_token_valid(user_ID, login_token):
        database.snaps.delete(snap_ID)
        return name=(snap_ID + ".png")
    else:
        return {
            "result": "permission denied"
        }
