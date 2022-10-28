from . import open_db


def send(from_user_id, to_user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO snap (from_user_id, to_user_id) VALUES (%s, %s)",
        (from_user_id, to_user_id),
    )
    db.commit()
    db.close()
    return "success"


def load_received(user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM snap WHERE to_user_id = %s", user_id)
    db.close()
    return {"result": "success", "data": cursor.fetchall()}


def load_sent(user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM snap WHERE from_user_id = %s", user_id)
    db.close()
    return {"result": "success", "data": cursor.fetchall()}


def delete(snap_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM snap WHERE id = %s", snap_id)
    db.commit()
    db.close()
    return {"result": "success"}


def mark_read(snap_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("UPDATE snap SET seen = true WHERE id = %s", snap_id)
    db.commit()
    db.close()
    return {"result": "success"}
