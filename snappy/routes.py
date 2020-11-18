# Imports
from flask import jsonify, request, send_from_directory

from . import app, database

### Friends ###
"""
URL: /api/v1/friends/load
Methods: GET
Required form data: login_token (string), user_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, load the rows of the user's friends with database.friends.load() and return the rows
If login token is invalid, return a json response where result = "permission denied"
"""
@app.route("/api/v1/friends/load", methods=["GET"])
def load_friends():
    # Load request data
    login_token = request.form.get("login_token")
    user_ID = request.form.get("user_ID")
    # Check login token
    return jsonify(database.friends.load(user_ID))


"""
URL: /api/v1/friends/add
Methods: POST
Required form data: login_token (string), user_ID (string), friend_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, adds the friend with database.friends.add() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@app.route("/api/v1/friends/add", methods=["POST"])
def add_friend():
    # Load request data
    login_token = request.form["login_token"]
    user_ID = request.form["user_ID"]
    friend_id = request.form["friend_id"]
    # Check login token
    if database.user.login_token_valid(user_ID, login_token):
        # return json response of the result
        return jsonify({
            "result": database.friends.add(user_ID, friend_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/friends/remove
Methods: POST
Required form data: login_token (string), user_ID (string), friend_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, remove the friend with database.friends.remove() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@app.route("/api/v1/friends/remove", methods=["POST"])
def remove_friend():
    login_token = request.form["login_token"]
    user_ID = request.form["user_ID"]
    friend_id = request.form["friend_id"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.friends.remove(user_ID, friend_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


### User ###
"""
URL: /api/v1/users/add
Methods: POST
Required form data: email (string), password (string), dark_mode (int), user_name (string)

Description:
Get email, password, dark_mode and user_name from the request then add the user with database.user.add() and return the result
"""
@app.route("/api/v1/user/add", methods=["POST"])
def add_user():
    email = request.form["email"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    return jsonify({
        "result": database.user.add(email, password, dark_mode, user_name)
    })


"""
URL: /api/v1/user/delete
Methods: POST
Required form data: login_token (string), user_ID (string)

Description:
Gets the login_token and user_ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, remove the user with database.user.remove() and return the result
If login token is invalid, return result = "permission denied"
"""
@app.route("/api/v1/user/delete", methods=["POST"])
def delete_user():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.user.delete(user_ID)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/user/login
Methods: GET
Required form data: user_name (string), email (string), password (string)

Description:
Get the user_name, email and password from the request and attempt a login with database.user.login().
If the login failed e.g. wrong password then return result = "permission denied"
If the login was successful, a login token for the user will be returned
"""
@app.route("/api/v1/user/login", methods=["GET"])
def login_user():
    user = request.form["user"]
    password = request.form["password"]
    return jsonify({
        "result": database.user.login(user, password)
    })


"""
URL: /api/v1/user/logout
Methods: POST
Required form data: login_token (string), user_ID (string)

Description:
Gets the login_token and user_ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, logout the user with database.user.remove() and return the result
If login token is invalid, return result = "permission denied"
"""
@app.route("/api/v1/user/logout", methods=["POST"])
def logout_user():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.user.logout(user_ID)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/user/load
Methods: GET
Required form data: login_token (string), user_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, load the data of the user with database.user.load() and return the result
If login token is invalid, return result = "permission denied"
"""
@app.route("/api/v1/user/load", methods=["GET"])
def load_user():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify(database.user.load(user_ID))
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/user/save
Methods: POST
Required form data: login_token (string), user_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, save the user's new data to  with database.user.save() and return the result
If login token is invalid, return result = "permission denied"
"""
@app.route("/api/v1/user/save", methods=["POST"])
def save_user():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.user.save(user_ID, password, dark_mode, user_name)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


# Snap
"""
URL: /api/v1/snaps/send
Methods: POST
Required form data: login_token (string), user_ID (string), to_user_ID (string), image (file)

Description:
Gets the login token, user ID, recieving user ID and the image from the request then checks if login token is valid with database.user.login_token_valid().
If login token is valid, save the image and make add a row to database with database.snaps.send() then return the result
If login token is invalid, return result = "permission denied"
"""
@app.route("/api/v1/snaps/send", methods=["POST"])
def send_snap():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    to_user_ID = request.form["to_user_ID"]
    image = request.files["image"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify({
            "result": database.snaps.send(user_ID, to_user_ID, image)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/snaps/load
Methods: GET
Required form data: login_token (string), user_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, get a list of incoming snaps for the user database.snaps.load() and return the result
If login token is invalid, return a json response where result = "permission denied"
"""
@app.route("/api/v1/snaps/load", methods=["GET"])
def load_snaps():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_ID, login_token):
        return jsonify(database.snaps.load(user_ID))
    else:
        return jsonify({
            "result": "permission denied"
        })


"""
URL: /api/v1/snaps/download
Methods: GET
Required form data: login_token (string), user_ID (string), snap_ID (string)

Description:
Gets the login token and user ID from the request then checks if it is valid with database.user.login_token_valid().
If login token is valid, 
If login token is invalid, return a json response where result = "permission denied"
"""
@app.route("/api/v1/snaps/download", methods=["GET"])
def download_snap():
    user_ID = request.form["user_ID"]
    login_token = request.form["login_token"]
    snap_id = request.form["snap_id"]
    if database.user.login_token_valid(user_ID, login_token):
        return send_from_directory(directory="./uploads", filename=(snap_id + ".jpg"))
    else:
        return jsonify({
            "result": "permission denied"
        })
