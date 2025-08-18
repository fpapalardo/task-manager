import sqlite3

def db_connection():
    con = sqlite3.connect("tasks_manager.db")
    cur = con.cursor()

    return con, cur

def db_close_connection(con):
    con.close()

def initial_setup():
    con, cur = db_connection()
    cur.executescript("""
        BEGIN;
        CREATE TABLE IF NOT EXISTS task_lists(
                    id INTEGER PRIMARY KEY
                    name TEXT UNIQUE NOT NULL
                    );
        CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY
                    name TEXT NOT NULL
                    task_list_id INTEGER REFERENCES task_lists(id)
                    due_date TEXT
                    priority TEXT
                    status TEXT DEFAULT 'pending'
                    );
        COMMIT;
    """)
    db_close_connection(con)
