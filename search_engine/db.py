import sqlite3
from .config import DB_PATH

def connect():
    db = sqlite3.connect(DB_PATH)
    db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(
        url UNINDEXED,
        title,
        text,
        tokenize='unicode61'
    )""")
    return db

def add_document(db, url, title, text):
    db.execute("INSERT INTO documents(url,title,text) VALUES(?,?,?)",
               (url, title, text))

def search(query, limit=20):
    db = connect()
    rows = db.execute(
        "SELECT url,title,snippet(documents,2,'<mark>','</mark>','…',20) "
        "FROM documents WHERE documents MATCH ? LIMIT ?",
        (query, limit)
    ).fetchall()
    db.close()
    return [{"url":u,"title":t or u,"snippet":s} for u,t,s in rows]
