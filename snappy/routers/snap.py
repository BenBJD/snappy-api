from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles


api = APIRouter(prefix="/api/snap")
api.mount("/static", StaticFiles(directory="../../snaps"))

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
