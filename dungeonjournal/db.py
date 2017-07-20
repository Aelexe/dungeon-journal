import sqlite3

from flask import g, current_app

def connect_db():
    db_connection = sqlite3.connect(current_app.config["DATABASE"])
    db_connection.row_factory = sqlite3.Row
    return db_connection

def get_db():
    if not hasattr(g, "db_connection"):
        g.db_connection = connect_db()
    return g.db_connection

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
