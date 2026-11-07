import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "sahaaya.db"

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            module TEXT, language TEXT, question TEXT, response TEXT
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            language TEXT, department TEXT, location TEXT, issue TEXT, draft TEXT
        )""")

def save_interaction(module, language, question, response):
    with _connect() as con:
        con.execute(
            "INSERT INTO interactions(module, language, question, response) VALUES(?,?,?,?)",
            (module, language, question, response)
        )

def save_grievance(language, department, location, issue, draft):
    with _connect() as con:
        con.execute(
            "INSERT INTO grievances(language, department, location, issue, draft) VALUES(?,?,?,?,?)",
            (language, department, location, issue, draft)
        )

def recent_interactions(limit=20):
    with _connect() as con:
        return con.execute(
            "SELECT id, created_at, module, question, response, language FROM interactions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
