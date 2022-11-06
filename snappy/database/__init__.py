import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor


from ..config import settings


def open_db():
    db = psycopg2.connect(
        database=settings.db_name,
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        port=settings.db_port,
        cursor_factory=RealDictCursor,
    )
    return db
