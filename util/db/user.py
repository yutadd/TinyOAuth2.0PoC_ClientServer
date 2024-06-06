import sqlite3
from datetime import datetime, timedelta
import os
def migrate_user_db():
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute('''
create table IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            token_type TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            refresh_token TEXT NOT NULL,
            scope TEXT NOT NULL,
            session_id TEXT NOT NULL
        )
''')
    # attention: expires_at can calculated from expires_in
def register_user(token:str,tokentype:str,expires_in:str,refresh_token:str,scope:str,sessionID:str):
    expires_at = datetime.now() + timedelta(seconds=int(expires_in))
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute('insert into clients (token, token_type, expires_at, refresh_token, scope, session_id) values (?, ?, ?, ?, ?, ?)', (token, tokentype, expires_at, refresh_token, scope, sessionID))
    conn.commit()
def get_user_by_(session_id:str):
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    user=cursor.execute("select * from clients where session_id=?",(session_id))
    #TODO: ユーザーモデルにして返却