import sqlite3
import os

DB_PATH = "aegis_licenses.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            tier TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insere a chave de teste padrão se ela não existir
    cursor.execute('''
        INSERT OR IGNORE INTO licenses (key, tier, active)
        VALUES ('AEGIS-PRO-TEST-KEY-2026', 'pro_enterprise', 1)
    ''')
    conn.commit()
    conn.close()

def check_license_db(api_key: str):
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT tier, active FROM licenses WHERE key = ?', (api_key,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[1] == 1:
        return {"valid": True, "tier": row[0]}
    return {"valid": False, "tier": None}
