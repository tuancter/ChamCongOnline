import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id_account INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id_employee INTEGER PRIMARY KEY AUTOINCREMENT,
                id_account INTEGER NOT NULL,
                name TEXT NOT NULL,
                dateOfBirth TEXT NOT NULL,
                address TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL,
                FOREIGN KEY (id_account) REFERENCES accounts (id_account)
            )
        ''')
    conn.close()