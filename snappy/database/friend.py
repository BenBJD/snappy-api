from . import open_db


# Load users
# set confirmed=True to get only confirmed friends
def load(user_id: str, confirmed: bool = False):
    db = open_db()
    cursor = db.cursor()
    results = []
    if confirmed:
        # cursor.execute(
        #     "SELECT * FROM friend where confirmed = true and (user_1_id = %s or user_2_id = %s)",
        #     (user_id, user_id),
        # )
        cursor.execute(
            "SELECT friend.user_1_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_1_id = users.id where confirmed = true and user_1_id = %s "
        )
        results.append(cursor.fetchall())
        cursor.execute(
            "SELECT friend.user_2_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_2_id = users.id where confirmed = true and user_2_id = %s "
        )
        results.append(cursor.fetchall())
    else:
        ccursor.execute(
            "SELECT friend.user_1_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_1_id = users.id where user_1_id = %s "
        )
        results.append(cursor.fetchall())
        cursor.execute(
            "SELECT friend.user_2_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_2_id = users.id where user_2_id = %s "
        )
        results.append(cursor.fetchall())
    results.append(cursor.fetchall())
    # Change to only contain the friend's ids
    friends = []
    for result in results:
        if not result.user_1_id == user_id:
            friends.append(
                {"friend_id": result.user_1_id, "confirmed": result.confirmed}
            )
        if not result.user_2_id == user_id:
            friends.append(
                {"friend_id": result.user_2_id, "confirmed": result.confirmed}
            )
    db.close()
    return friends


def add(user_id, friend_user_id):
    db = open_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO friend (user_1_id, user_2_id) VALUES (%s, %s)",
        (user_id, friend_user_id),
    )
    db.commit()
    db.close()
    return


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
    return


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
    return
