from flask import g
from mysql import connector
from .. import app

def open_db():
    g.db = connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )


def close_db():
    g.db.close()


def load(user_id):
    g.open_db()
    