# lib/db/connection.py

import sqlite3
from contextlib import contextmanager

def get_connection(db_path="lib/db/database.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_connection_cm(db_path="lib/db/database.db"):
    conn = get_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()
