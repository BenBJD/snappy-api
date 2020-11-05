# Imports
from flask import redirect, render_template, request, session, url_for, Response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from snappy import database


# Friends
@app.route("/api/v1/<user_id>/friends/load", methods=["GET"])
def load_friends():
    login_token = request.form.get("login_token")
    if login_token_valid(user_id, login_token):
        return jsonify(database.friends.load(login_token, user_id))
    else:
        return Response(status=401)
    
@app.route("/api/v1/<user_id>/friends/add" methods=["GET"])
def add_friend():
    request_data = request.form.get("login_token")

@app.route("/api/v1/<user_id>/friends/remove" methods=["GET"])
def remove_friend():
    request_data = request.form.get("login_token")
