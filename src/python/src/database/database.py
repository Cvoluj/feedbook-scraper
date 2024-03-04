import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from utils import mysql_connection_string


def get_db() -> Engine:
    """
    Database connetion from settings.py
    """
    db_uri = mysql_connection_string()
    return create_engine(url=db_uri, echo=False)

if __name__ == '__main__':
    """
    Run to check connection (it wont work if run from file directory, because it doesnt see utils module)
    """
    with get_db().connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")