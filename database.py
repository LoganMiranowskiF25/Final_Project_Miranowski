import sqlite3

def connect_db():
    return sqlite3.connect("inventory.db", check_same_thread=False)

def create_table():
    conn = connect_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT UNIQUE,
                name TEXT,
                quantity INTEGER,
                category TEXT,
                price REAL,
                expiration TEXT,
                reorder_level INTEGER,
                time_sensitive INTEGER
                )""")
    
    conn.commit()
    conn.close()