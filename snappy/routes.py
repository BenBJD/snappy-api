# Imports
from snappy.database import user
from flask import jsonify, request, send_from_directory

from snappy import app, database


# Friends
@app.route("/api/v1/friends/load", methods=["GET"])
def load_friends():
    login_token = request.form.get("login_token")
    user_id = request.form.get("user_id")
    if database.user.login_token_valid(user_id, login_token):
        return jsonify(database.friends.load(user_id))
    else:
        return jsonify({
            "result": "permission denied"
        })


@app.route("/api/v1/friends/add", methods=["POST"])
def add_friend():
    login_token = request.form["login_token"]
    user_id = request.form["user_id"]
    friend_id = request.form["friend_id"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.friends.add(user_id, friend_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


@app.route("/api/v1/friends/remove", methods=["DELETE"])
def remove_friend():
    login_token = request.form["login_token"]
    user_id = request.form["user_id"]
    friend_id = request.form["friend_id"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.friends.remove(user_id, friend_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


# User
@app.route("/api/v1/user/add", methods=["POST"])
def add_user():
    email = request.form["email"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    return jsonify({
        "result": database.user.add(email, password, dark_mode, user_name)
    })


@app.route("/api/v1/user/delete", methods=["DELETE"])
def delete_user():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.user.delete(user_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


@app.route("/api/v1/user/login", methods=["GET"])
def login_user():
    user_name = request.form["user_name"]
    email = request.form["email"]
    password = request.form["password"]
    return jsonify({
        "result": database.user.login(user_name, email, password)
    })


@app.route("/api/v1/user/logout", methods=["PUT"])
def logout_user():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.user.logout(user_id)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


@app.route("/api/v1/user/load", methods=["GET"])
def load_user():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify(database.user.load(user_id))
    else:
        return jsonify({
            "result": "permission denied"
        })


@app.route("/api/v1/user/save", methods=["PUT"])
def save_user():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    password = request.form["password"]
    dark_mode = request.form["dark_mode"]
    user_name = request.form["user_name"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.user.save(user_id, password, dark_mode, user_name)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })


# Snap
@app.route("/api/v1/snaps/send", methods=["POST"])
def send_snap():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    to_user_id = request.form["to_user_id"]
    image = request.files["image"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify({
            "result": database.snaps.send(user_id, to_user_id, image)
        })
    else:
        return jsonify({
            "result": "permission denied"
        })

@app.route("/api/v1/snaps/load", methods=["GET"])
def load_snaps():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    if database.user.login_token_valid(user_id, login_token):
        return jsonify(database.snaps.load(user_id))
    else:
        return jsonify({
            "result": "permission denied"
        })

@app.route("/api/v1/snaps/download", methods=["GET"])
def download_snap():
    user_id = request.form["user_id"]
    login_token = request.form["login_token"]
    snap_id = request.form["snap_id"]
    if database.user.login_token_valid(user_id, login_token):
        return send_from_directory(directory="./uploads", filename=(snap_id + ".jpg"))
    else:
        return jsonify({
            "result": "permission denied"
        })
