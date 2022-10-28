from . import open_db


# Load users
# set confirmed=True to get only confirmed friends
def load(user_id: str, confirmed: bool = False):
    db = open_db()
    cursor = db.cursor()
    if confirmed:
        cursor.execute(
            "SELECT * FROM friend where confirmed = true and (user_1_id = %s or user_2_id = %s)",
            (user_id, user_id),
        )
    else:
        cursor.execute(
            "SELECT * FROM friend where (user_1_id = %s or user_2_id = %s)",
            (user_id, user_id),
        )
    db.close()
    return {"result": "success", "data": cursor.fetchall()}


def add(user_id, friend_user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO friend (user_1_id, user_2_id) VALUES (%s, %s)",
        (user_id, friend_user_id),
    )
    db.commit()
    db.close()
    return {"result": "success"}


def confirm(user_id, friend_user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        """UPDATE friend SET confirmed = true 
        where (user_1_id = %s and user_2_id = %s) 
        or (user_2_id = %s and user_1_id = %s)""",
        (user_id, friend_user_id, friend_user_id, user_id),
    )
    db.commit()
    db.close()
    return {"result": "success"}


def remove(user_id, friend_user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        """delete from friend 
        where (user_1_id = %s and user_2_id = %s) 
        or (user_2_id = %s and user_1_id = %s)""",
        (user_id, friend_user_id, friend_user_id, user_id),
    )
    db.commit()
    db.close()
    return {"result": "success"}
