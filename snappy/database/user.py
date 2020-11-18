from . import open_db
from uuid import uuid1
import time
from werkzeug.security import check_password_hash, generate_password_hash
from .. import app


def add(email, password, dark_mode, user_name):
    user_ID = uuid1()
    password_hash = generate_password_hash(password)
    sql = f"INSERT INTO user_ID (userID, email, userName, password, darkMode, snapScore) VALUES ({user_ID}, {email}, {user_name}, {password_hash}, {dark_mode}, 0)"
    db = open_db()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"


def delete(user_ID):
    sql1 = f"DELETE * FROM usersTable WHERE userID = {user_ID}"
    sql2 = f"DELETE * FROM userTokenTable WHERE userID = {user_ID}"
    db = open_db()
    cursor = db.cursor()
    cursor.execute(sql1)
    db.commit()
    cursor.execute(sql2)
    db.commit()
    db.close()
    return "success"


def login(user, password):
    if 
    
    login_token = uuid1()
    expires_time = time.time() + 2592000
    sql = f"INSERT INTO userTokenTable (loginToken, userID, expireTime) VALUES ({login_token}, {user_ID}, {expires_time}"
    db = open_db()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return login_token


def logout(user_ID):
    sql = f"DELETE * FROM userTokenTable WHERE userID = {user_ID}"
    db = open_db()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"


def load(user_ID):
    sql = f"SELECT * FROM usersTable WHERE userID = {user_ID}"
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    cursor.execute(sql)
    db.close()
    return cursor.fetchone()


def save(user_ID):
    sql = f"UPDATE usersTable SET "
    db = open_db()
    cursor = db.cursor()
    cursor.execute(sql)
    db.close()
    return cursor.fetchall()
    