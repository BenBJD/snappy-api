from . import open_db


# Load users
# set confirmed=True to get only confirmed friends
def load(user_id: str, confirmed: bool = False):
    db = open_db()
    cursor = db.cursor()
    results = []
    if confirmed:
        cursor.execute(
            "SELECT friend.user_1_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_1_id = users.id where confirmed = true and user_2_id = %s", (user_id,)
        )
        cursor.execute(
            "SELECT friend.user_2_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_2_id = users.id where confirmed = true and user_1_id = %s", (user_id,)
        )
    else:
        cursor.execute(
            "SELECT friend.user_1_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_1_id = users.id where user_2_id = %s ", (user_id,)
        )
        cursor.execute(
            "SELECT friend.user_2_id, friend.confirmed, users.username, users.snappy_score from friend inner join "
            "users on friend.user_2_id = users.id where user_1_id = %s ", (user_id,)
        )
    results = cursor.fetchall()
    formatted_friends = []
    for i in range(0, len(results)):
        friend = {
            "confirmed": results[i]["confirmed"],
            "username": results[i]["username"],
            "snappy_score": results[i]["snappy_score"]
        }
        if "user_1_id" in results[i].keys():
            friend["friend_id"] = results[i]['user_1_id']
        if "user_2_id" in results[i].keys():
            friend["friend_id"] = results[i]['user_2_id']
        formatted_friends.append(friend)
    print(formatted_friends)
    db.close()
    return formatted_friends


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
