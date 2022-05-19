from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from .. import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
