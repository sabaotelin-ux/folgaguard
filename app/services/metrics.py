import sqlite3

DB_PATH = "aegis_licenses.db"

def init_metrics_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_request(endpoint: str, status_code: int):
    try:
        init_metrics_table()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO metrics (endpoint, status_code) VALUES (?, ?)', (endpoint, status_code))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_metrics_summary():
    try:
        init_metrics_table()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM metrics')
        total_requests = cursor.fetchone()[0]
        cursor.execute('SELECT endpoint, COUNT(*) FROM metrics GROUP BY endpoint')
        by_endpoint = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return {
            "total_requests": total_requests,
            "requests_by_endpoint": by_endpoint
        }
    except Exception:
        return {"total_requests": 0, "requests_by_endpoint": {}}
