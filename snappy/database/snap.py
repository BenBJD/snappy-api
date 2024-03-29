from uuid import uuid1

from . import open_db
from ..models import Snap


def send(from_user_id, to_user_id):
    db = open_db()
    cursor = db.cursor()
    snap_id = str(uuid1())
    cursor.execute(
        "INSERT INTO snap (id, from_user_id, to_user_id) VALUES (%s, %s, %s) RETURNING date, time, from_user_id",
        (snap_id, from_user_id, to_user_id),
    )
    result = cursor.fetchone()
    db.commit()
    db.close()
    return {"id": snap_id, "from_user_id": result[2], "date": result[0], "time": result[1]}


def load_received(user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM snap WHERE to_user_id = %s", (user_id,))
    result = cursor.fetchall()
    db.close()
    return result


def load_sent(user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM snap WHERE from_user_id = %s", (user_id,))
    result = cursor.fetchall()
    db.close()
    return result


def load(snap_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM snap WHERE id = %s", (snap_id,))
    result: Snap = cursor.fetchone()
    db.close()
    return result


def delete(snap_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM snap WHERE id = %s", (snap_id,))
    db.commit()
    db.close()
    return


def mark_read(snap_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute("UPDATE snap SET seen = true WHERE id = %s", (snap_id,))
    db.commit()
    db.close()
    return
