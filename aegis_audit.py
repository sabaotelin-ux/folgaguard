import os
import shutil
import sqlite3

DB_NAME = 'aegis_unified.db'

def run_system_audit():
    print('=== Aegis Auditoria de Telemetria e Desempenho ===')
    total, used, free = shutil.disk_usage('.')
    print(f'[Armazenamento] Total: {total // (2**20)} MB | Usado: {used // (2**20)} MB | Livre: {free // (2**20)} MB')
    try:
        with open('/proc/meminfo', 'r') as mf:
            for line in mf:
                if 'MemTotal' in line or 'MemAvailable' in line:
                    print(f'[Memória] {line.strip()}')
    except Exception:
        print('[Memória] Informação indisponível.')
    load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0)
    print(f'[Load Average] 1m, 5m, 15m: {load_avg}')
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        print(f'[Banco de Dados] Tabelas: {tables}')
    else:
        print('[Banco de Dados] Não encontrado.')
    print('==================================================')

if __name__ == '__main__':
    run_system_audit()
