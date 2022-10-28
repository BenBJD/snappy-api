from fastapi import APIRouter

api = APIRouter(prefix="/api/friend")

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
def load_friends(id: str, token: str = Depends(oauth2_scheme)):
    # Check login token
    if database.user.login_token_valid(id, token):
        # return json response of the result
        return database.friends.load(id)
    else:
        return {
            "result": "permission denied"
        }


"""
URL: /api/v1/friends/add
Required form data: login_token (string), user_id (string), friend_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, adds the friend.py with database.friends.add() and return the result
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
If login token is valid, remove the friend.py with database.friends.remove() and return the result
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
