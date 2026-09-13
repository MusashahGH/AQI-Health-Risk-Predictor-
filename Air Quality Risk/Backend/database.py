import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            city TEXT,
            age INTEGER,
            has_asthma INTEGER,
            activity_level TEXT,
            aqi_index INTEGER,
            risk TEXT,
            summary TEXT,
            checked_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_check(name, city, age, has_asthma, activity_level, aqi_index, risk, summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (name, city, age, has_asthma, activity_level, aqi_index, risk, summary, checked_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, city, age, int(has_asthma), activity_level, aqi_index, risk, summary, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, city, age, aqi_index, risk, checked_at
        FROM history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows