import sqlite3
import os
def seed_user_db():
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute('''
create table IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            redirect_prefix TEXT NOT NULL,
            allowed_scope TEXT NOT NULL
        )
''')
    cursor.execute('insert into user ()')