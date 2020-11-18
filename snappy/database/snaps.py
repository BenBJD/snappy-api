from . import open_db

def send(user_ID, friend_ID, snap_ID):
    db = open_db()
    cursor = db.cursor(buffered=True)
    sql = f"INSERT INTO snapTable (snapID, userID, friendID) VALUES ({snap_ID}, {user_ID}, {friend_ID})"
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"

def load(user_ID):
    db = open_db()
    cursor = db.cursor(buffered=True, dictionary=True)
    sql = f"SELECT * FROM snapTable WHERE toUserID = {user_ID}"
    cursor.execute(sql)
    db.close()
    return cursor.fetchall()

def delete(snap_ID):
    db = open_db()
    cursor = db.cursor(buffered=True)
    sql = f"DELETE FROM snapTable WHERE snapID = {snap_ID}"
    cursor.execute(sql)
    db.commit()
    db.close()
    return "success"