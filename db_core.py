
# Licença MIT
# Copyright (c) 2026 Augusto Cezar de Almeida

import sqlite3

# Inicializa ou conecta ao banco de dados SQLite local
conn = sqlite3.connect("autonomous_engine.db")
cursor = conn.cursor()

# Cria a tabela de histórico de decisões autônomas
cursor.execute("""
CREATE TABLE IF NOT EXISTS engine_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_size TEXT,
    latency_sec REAL,
    error_rate REAL,
    decision TEXT,
    threshold REAL
)
""")
conn.commit()

system_metrics = {
    "total_requests": 0,
    "overload_events": 0,
    "adaptive_threshold": 5.0,
    "learning_rate": 0.1
}

def simulate_and_save(company_size, latency_ms, error_rate):
    system_metrics["total_requests"] += 1
    latency_sec = latency_ms / 1000.0
    current_threshold = system_metrics["adaptive_threshold"]
    
    is_overloaded = latency_sec > current_threshold or error_rate > 0.05
    
    if is_overloaded:
        system_metrics["overload_events"] += 1
        system_metrics["adaptive_threshold"] -= system_metrics["learning_rate"] * 0.2
        decision = "FALLBACK_MODE: Roteando para processamento local isolado"
    else:
        system_metrics["adaptive_threshold"] += system_metrics["learning_rate"] * 0.05
        decision = "NORMAL_MODE: Operação integrada padrão"
        
    system_metrics["adaptive_threshold"] = max(1.0, min(system_metrics["adaptive_threshold"], 10.0))
    
    # Salva os dados de forma autônoma no banco SQLite
    cursor.execute("""
        INSERT INTO engine_logs (company_size, latency_sec, error_rate, decision, threshold)
        VALUES (?, ?, ?, ?, ?)
    """, (company_size, latency_sec, error_rate, decision, system_metrics["adaptive_threshold"]))
    conn.commit()
    
    print(f"Gravado no BD -> Empresa: {company_size} | Limiar: {system_metrics['adaptive_threshold']:.2f}")

print("Iniciando gravação autônoma no banco de dados...\n")
simulate_and_save("Pequena", 2000, 0.01)
simulate_and_save("Média", 6500, 0.02)
simulate_and_save("Grande", 1500, 0.08)

conn.close()
print("\nSimulação concluída e dados salvos com sucesso!")
