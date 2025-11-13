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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            url TEXT PRIMARY KEY,
            depth INTEGER
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

def enqueue_url(url, depth):
    with lock:
        conn = sqlite3.connect("crawler_state.sqlite")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO queue (url, depth) VALUES (?, ?)",
            (url, depth)
        )
        conn.commit()
        conn.close()

def dequeue_url():
    with lock:
        conn = sqlite3.connect("crawler_state.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT url, depth FROM queue LIMIT 1")
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None, None
        url, depth = row
        cursor.execute("DELETE FROM queue WHERE url = ?", (url,))
        conn.commit()
        conn.close()
        return url, depth

def get_queue_count():
    conn = sqlite3.connect("crawler_state.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM queue")
    (count,) = cursor.fetchone()
    conn.close()
    return count
