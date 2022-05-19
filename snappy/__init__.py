# imports
from .app import app
from .database import db_session
from . import routes


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
