import sqlite3

def init_db():
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        query TEXT,
        message_sent INTEGER DEFAULT 0
    )""")
    conn.commit()
    return conn
