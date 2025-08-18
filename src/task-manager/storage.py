import sqlite3

def db_connection():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()

    return con, cur

def db_close_connection(con):
    con.close()