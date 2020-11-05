from mysql import connector
from .. import app
from flask import g
from . import friends, user, snap


# Opening and closing connection
def open_db():
    g.db = connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )


def close_db():
    g.db.close()
