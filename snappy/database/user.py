from passlib.context import CryptContext

from . import open_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add(username: str, password: str):
    db = open_db()
    cursor = db.cursor()
    password_hash: str = pwd_context.hash(password)
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
        (username, password_hash),
    )
    user_id = cursor.fetchone[0]
    db.commit()
    db.close()
    return user_id


def delete(user_id: str):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    db.close()
    return


def load(user_id=None, username=None):
    if user_id is not None:
        db = open_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users where id = %s", (user_id,))
        result = cursor.fetchone()
        db.close()
        return result
    elif username is not None:
        db = open_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        db.close()
        return result
    else:
        return


def save(user_id, username=None, password=None):
    db = open_db()
    cursor = db.cursor()
    if username is not None:
        cursor.execute(
            "UPDATE users SET username = %s WHERE id = %s", (username, user_id)
        )
    elif password is not None:
        password_hash = pwd_context.hash(password)
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, user_id),
        )
    else:
        db.close()
        return
    db.commit()
    db.close()
    return


def increment_score(user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET snappy_score = snappy_score + 1 WHERE id = %s", (user_id,)
    )
    db.commit()
    db.close()
    return

