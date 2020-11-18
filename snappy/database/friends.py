from . import open_db

def load(user_ID):
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    sql = f"SELECT * FROM friendsTable WHERE userID = '{user_ID}'"
    cursor.execute(sql)
    db.close()
    return cursor.fetchall()

def add(user_ID, friend_ID):
    db = open_db()
    cursor = db.cursor(buffered=True)
    sql = f"INSERT INTO friendsTable (userID, friendID) VALUES ('{user_ID}', '{friend_ID}')"
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"

def remove(user_ID, friend_ID):
    db = open_db()
    cursor = db.cursor(buffered=True)
    sql = f"DELETE FROM friendsTable WHERE userID = '{user_ID}' AND friendID = '{friend_ID}'"
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"

