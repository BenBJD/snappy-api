from .. import app
import mysql.connector

def open_db():
    return mysql.connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )

from . import friends, user, snaps