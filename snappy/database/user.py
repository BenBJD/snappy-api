from passlib.context import CryptContext
from . import open_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add(username: str, password: str):
    db = open_db()
    cursor = db.cursor()
    password_hash: str = pwd_context.hash(password)
    cursor.execute("INSERT INTO user (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    db.commit()
    db.close()
    return {"result": "success"}


def delete(user_id: str):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM user WHERE id = %s", user_id)
    db.commit()
    db.close()
    return {"result": "success"}


def load(user_id: str = None, username: str = None):
    if user_id is not None:
        db = open_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user where id = %s", user_id)
        db.close()
    elif username is not None:
        db = open_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE id = %s", user_id)
        db.close()
    else:
        return {"result": "username or user_id not specified"}
    return {"result": "success", "data": cursor.fetchone()}


def save(user_id, username=None, password=None):
    db = open_db()
    cursor = db.cursor()
    if username is not None:
        cursor.execute("UPDATE user SET username = %s WHERE id = %s", (username, user_id))
    elif password is not None:
        password_hash = pwd_context.hash(password)
        cursor.execute("UPDATE user SET password_hash = %s WHERE id = %s", (password_hash, user_id))
    else:
        db.close()
        return {"result": "username or user_id not specified"}
    db.commit()
    db.close()
    return {"result": "success"}
