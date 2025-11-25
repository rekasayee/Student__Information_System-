# db.py
import sqlite3
from flask import g
import os

DB_PATH = r"C:\Users\HP\Downloads\SIS\SIS\student_info.db"  # uploaded DB path

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False   # IMPORTANT FIX
        )
        g.db.row_factory = sqlite3.Row

        # Enable WAL mode (allows simultaneous read/write)
        g.db.execute("PRAGMA journal_mode=WAL;")

    return g.db

def query(sql, args=(), one=False):
    cur = get_db().execute(sql, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    cur.close()

def init_users_table():
    """
    Create a simple users table if not exists:
    users(id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)
    role: 'admin' or 'user'
    """
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """
    execute(sql)
