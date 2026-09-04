# Licença MIT - Aegis Gate Teste Unificado
import sqlite3

DB_NAME = "aegis_unified.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS cache (prompt_hash TEXT PRIMARY KEY, response TEXT)")
        # Inserindo um dado simulado de "swarm" ou remoto
        conn.execute("INSERT OR REPLACE INTO cache (prompt_hash, response) VALUES (?, ?)", 
                     ("p2p_chave_99", "Dado recuperado com sucesso pelo Aegis Gate!"))
        conn.commit()

def resolve_cache(prompt_hash):
    # 1. Tenta cache local
    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute("SELECT response FROM cache WHERE prompt_hash = ?", (prompt_hash,)).fetchone()
        if row:
            return {"response": row[0], "source": "local"}
            
    # 2. Simula busca na malha P2P (Swarm) caso falhe localmente
    # (Aqui entra a lógica de consulta aos peers vizinhos)
    return {"error": "not_found_in_swarm"}

if __name__ == "__main__":
    init_db()
    print("Banco inicializado.")
    
    # Testando consulta de chave existente
    resultado = resolve_cache("p2p_chave_99")
    print("Resultado da consulta:", resultado)
