with open("main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = [line for line in lines if "def log_metric" not in line]

log_metric_code = '''
def log_metric(event_type):
    import sqlite3
    conn = sqlite3.connect("cache.db")
    cursor = conn.cursor()
    cursor.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    \'\'\')
    cursor.execute("INSERT INTO metrics (event_type) VALUES (?)", (event_type,))
    conn.commit()
    conn.close()
'''

with open("main.py", "w", encoding="utf-8") as f:
    f.write(log_metric_code + "\n\n" + "".join(clean_lines))

print("[+] log_metric posicionado no escopo global com sucesso!")
