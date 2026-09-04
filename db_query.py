# Licença MIT
# Copyright (c) 2026 Augusto Cezar de Almeida

import sqlite3

# Conecta ao banco de dados autônomo existente
conn = sqlite3.connect("autonomous_engine.db")
cursor = conn.cursor()

# Busca todos os registros salvos pelas simulações anteriores
cursor.execute("SELECT id, company_size, latency_sec, error_rate, decision, threshold FROM engine_logs")
rows = cursor.fetchall()

print("=== HISTÓRICO DE DECISÕES AUTÔNOMAS DO MOTOR ===\n")
for row in rows:
    print(f"ID: {row[0]} | Empresa: {row[1]} | Latência: {row[2]}s | Limiar: {row[5]:.2f}")
    print(f"  -> Decisão: {row[4]}\n")

conn.close()
