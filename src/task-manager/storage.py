import sqlite3
import os

# Default database name
DB_NAME = "tasks_manager.db"

def db_connection():
    con = sqlite3.connect(DB_NAME, timeout=30)
    cur = con.cursor()
    
    # Configure SQLite for better concurrent access
    cur.execute("PRAGMA journal_mode=WAL")
    cur.execute("PRAGMA busy_timeout=5000")
    cur.execute("PRAGMA foreign_keys=ON")
    
    return con, cur

def db_close_connection(con):
    if con:
        try:
            con.commit()
            con.close()
        except sqlite3.Error:
            pass

def reset_database():
    files_to_remove = [
        DB_NAME,
        f"{DB_NAME}-shm",
        f"{DB_NAME}-wal"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
            except OSError as e:
                print(f"Error removing {file}: {e}")

def initial_setup():
    """Initialize database tables"""
    con, cur = db_connection()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS task_lists(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                task_list_id INTEGER REFERENCES task_lists(id),
                due_date TEXT,
                priority TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        con.commit()
    finally:
        db_close_connection(con)