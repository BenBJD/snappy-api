from fastapi import APIRouter

api = APIRouter(prefix="/api/user")
api.mount("/static", StaticFiles(directory="./static"))

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
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
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
