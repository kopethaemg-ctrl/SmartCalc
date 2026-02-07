# database.py
import sqlite3

DB_FILE = "smartcalc.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    price REAL
                )""")
    
    # Data မရှိမှသာ Default Data ထည့်မယ်
    c.execute("SELECT count(*) FROM materials")
    if c.fetchone()[0] == 0:
        initial_data = [
            ("Vinyl (Outdoor)", 800),
            ("Vinyl (Indoor)", 1200),
            ("Sticker (Glossy)", 1500),
            ("Sticker (Clear)", 1800),
        ]
        c.executemany("INSERT INTO materials (name, price) VALUES (?, ?)", initial_data)
        conn.commit()
    conn.close()

def get_all_materials():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, price FROM materials ORDER BY name")
    data = c.fetchall()
    conn.close()
    return data

def get_material_price(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT price FROM materials WHERE name=?", (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def upsert_material(name, price):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO materials (name, price) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET price=excluded.price", (name, price))
    conn.commit()
    conn.close()

def delete_material(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM materials WHERE name=?", (name,))
    conn.commit()
    conn.close()

init_db()