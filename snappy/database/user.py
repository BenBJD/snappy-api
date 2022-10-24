from . import open_db
from uuid import uuid1
import time


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


# def new_token(user, password):
#     db = open_db()
#     cursor = db.cursor(dictionary=True, buffered=True)
#     # Get user data
#     if "@" in user:
#         cursor.execute(f"SELECT (id) FROM userTable WHERE email = '{user}'")
#     else:
#         cursor.execute(f"SELECT (id) FROM userTable WHERE userName = '{user}'")
#     if cursor.rowcount == 0:
#         return "failed"
#     else:
#         user_data = cursor.fetchone()
#     # Get user id and login token and return
#     login_token = uuid1()
#     expires_time = time.time() + 2592000
#     user_ID = user_data["userID"]
#     cursor.execute(sql)
#     db.commit()
#     db.close()
#     result = {
#         "login_token": login_token,
#         "user_id": user_ID
#     }
#     return result


def logout(user_ID):
    sql = f"DELETE * FROM userTokenTable WHERE userID = '{user_ID}'"
    db = open_db()
    cursor = db.cursor(buffered=True)
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"


def load(term, form):
    sql = ""
    if form == "id":
        sql = f"SELECT * FROM userTable where id = '{term}'"
    elif form == "email":
        sql = f"SELECT * FROM userTable WHERE id = '{term}'"
    elif form == "username":
        sql = f"SELECT * FROM userTable WHERE id = '{term}'"
    else:
        print("invalid option: expects id, email or username")
        return {"error": "invalid option"}
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    cursor.execute(sql)
    db.close()
    return cursor.fetchone()


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

