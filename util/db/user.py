import sqlite3
from datetime import datetime, timedelta
import os

from util.model.user import User


def migrate_user_db():
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
create table IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            token_type TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            refresh_token TEXT NOT NULL,
            refresh_expires_at TEXT NOT NULL,
            scope TEXT NOT NULL,
            session_id TEXT NOT NULL,
            username TEXT NOT NULL
        )
''')
    # attention: expires_at can calculated from expires_in


def register_user(token: str, tokentype: str, token_expires_in: int,refresh_expires_in, refresh_token: str, scope: str, sessionID: str, username: str):
    print("register_user start")
    token_expires_at = datetime.now() + timedelta(seconds=int(token_expires_in))
    refresh_expires_at=datetime.now() + timedelta(seconds=int(refresh_expires_in))
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    print("starting db connection")
    conn = sqlite3.connect(db_path)
    print("connected to db")
    cursor = conn.cursor()
    print("registering user")
    cursor.execute('insert into clients (token, token_type, expires_at, refresh_token,refresh_expires_at, scope, session_id,username) values \
                   (?, ?, ?, ?, ?, ?,?,?)',
                   (token, tokentype, token_expires_at, refresh_token,refresh_expires_at, scope, sessionID, username))
    conn.commit()
    print("user registered")

def get_user_by_sessionid(session_id: str) -> User:
    db_path = './db/users.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("select id,token, token_type, expires_at, refresh_token,refresh_expires_at, scope, session_id,username from clients where session_id=?", (session_id,))
    user = cursor.fetchone()
    return User(id=user[0], token=user[1], token_type=user[2], expires_at=user[3], refresh_token=user[4],refresh_expires_at=user[5], scope=user[6], session_id=user[7],username=user[8])
migrate_user_db()