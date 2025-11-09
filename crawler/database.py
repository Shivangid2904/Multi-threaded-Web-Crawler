import sqlite3
import threading

lock = threading.Lock()

def init_db():
    conn = sqlite3.connect("crawler_state.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visited (
            url TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

def save_url(url):
    with lock:
        conn = sqlite3.connect("crawler_state.sqlite")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO visited (url) VALUES (?)", (url,))
        conn.commit()
        conn.close()

def get_visited_urls():
    conn = sqlite3.connect("crawler_state.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM visited")
    urls = {row[0] for row in cursor.fetchall()}
    conn.close()
    return urls
