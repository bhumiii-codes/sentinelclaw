import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'decisions.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            ticker TEXT,
            quantity INTEGER,
            value REAL,
            decision TEXT,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_decision(action, ticker, quantity, value, decision, reason):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisions (timestamp, action, ticker, quantity, value, decision, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), action, ticker, quantity, value, decision, reason))
    conn.commit()
    conn.close()
    
    color = "\033[92m" if decision == "ALLOWED" else "\033[91m"
    reset = "\033[0m"
    print(f"{color}[{decision}]{reset} {action.upper()} {quantity}x {ticker} @ ${value:.2f} — {reason}")

def get_all_decisions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM decisions')
    rows = c.fetchall()
    conn.close()
    return rows