from . import open_db
from uuid import uuid1
import time
from werkzeug.security import check_password_hash, generate_password_hash


def add(email, password, dark_mode, user_name):
    user_ID = uuid1()
    password_hash = generate_password_hash(password)
    sql = f"INSERT INTO userTable (userID, email, userName, password, darkMode, snapScore) VALUES ('{user_ID}', '{email}', '{user_name}', '{password_hash}', '{dark_mode}', 0)"
    db = open_db()
    cursor = db.cursor(buffered=True)
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"


def delete(user_ID):
    sql1 = f"DELETE * FROM usersTable WHERE userID = '{user_ID}'"
    sql2 = f"DELETE * FROM userTokenTable WHERE userID = '{user_ID}'"
    sql3 = f"DELETE * FROM snapTable WHERE userID = '{user_ID}'"
    sql4 = f"DELETE * FROM friendTable WHERE userID = '{user_ID}'"
    db = open_db()
    cursor = db.cursor(buffered=True)
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    db.commit()
    db.close()
    return "success"


def login(user, password):
    db = open_db()
    cursor = db.cursor(dictionary=True, buffered=True)
    # Get user data
    if "@" in user:
        cursor.execute(f"SELECT * FROM userTable WHERE email = '{user}'")
    else:
        cursor.execute(f"SELECT * FROM userTable WHERE userName = '{user}'")
    if cursor.rowcount == 0:
        return "failed"
    else:
        user_data = cursor.fetchone()
    # Check if password is correct
    if check_password_hash(user_data["password"], password) == False:
        return "failed"
    # Get user id and login token and return
    login_token = uuid1()
    expires_time = time.time() + 2592000
    user_ID = user_data["userID"]
    sql = f"INSERT INTO userTokenTable (loginToken, userID, expireTime) VALUES ('{login_token}', '{user_ID}', '{expires_time}')"
    cursor.execute(sql)
    db.commit()
    db.close()
    result = {
        "login_token": login_token,
        "user_ID": user_ID
    }
    return result


def logout(user_ID):
    sql = f"DELETE * FROM userTokenTable WHERE userID = '{user_ID}'"
    db = open_db()
    cursor = db.cursor(buffered=True)
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"


def load(user_ID, search_ID):
    if search_ID == all:
        sql = f"SELECT userID, userName, snapScore FROM userTable"
    elif user_ID == search_ID:
        sql = f"SELECT * FROM userTable WHERE userID = '{user_ID}'"
    else: 
        return "permission denied"
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    cursor.execute(sql)
    db.close()
    return cursor.fetchall


def save(user_ID, email=None, user_name=None, password=None, dark_mode=None):
    db = open_db()
    cursor = db.cursor(buffered=True)
    if email != None:
        cursor.execute(f"UPDATE userTable SET email = '{email}' WHERE userID = '{user_ID}'")
    if user_name != None:
        cursor.execute(f"UPDATE userTable SET userName = '{user_name}' WHERE userID = '{user_ID}'")
    if password != None:
        cursor.execute(f"UPDATE userTable SET password = '{password}' WHERE userID = '{user_ID}'")
    if dark_mode != None:
        cursor.execute(f"UPDATE userTable SET darkMode = '{dark_mode}' WHERE userID = '{user_ID}'")    
    db.commit()
    db.close()
    return "success"
    
def login_token_valid(user_ID, login_token):
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    sql = f"SELECT * FROM userTokenTable WHERE userID = '{user_ID}'"
    cursor.execute(sql)
    tokens = cursor.fetchall()
    for i in tokens:
        print(i)
        if i["loginToken"] == login_token:
            db.close()
            return True
    db.close()
    return False

