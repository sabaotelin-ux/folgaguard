import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

old_log = '''def log_metric(event_type):
    import sqlite3
    conn = sqlite3.connect("cache.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO metrics (event_type) VALUES (?)", (event_type,))
    conn.commit()
    conn.close()'''

new_log = '''def log_metric(event_type):
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
    conn.close()'''

if old_log in content:
    content = content.replace(old_log, new_log)
else:
    content += "\n\n" + new_log

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[+] log_metric corrigido com auto-criação de tabela!")
