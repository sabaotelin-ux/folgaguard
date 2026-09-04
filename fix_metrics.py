import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_metrics_route = '''@app.get("/v1/metrics")
async def get_metrics():
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
    conn.commit()
    cursor.execute("SELECT event_type, COUNT(*) FROM metrics GROUP BY event_type")
    rows = cursor.fetchall()
    conn.close()
    
    stats = {row[0]: row[1] for row in rows}
    hits = stats.get("hit", 0)
    misses = stats.get("miss", 0)
    total = hits + misses
    hit_rate = (hits / total * 100) if total > 0 else 0.0
    latency_saved_ms = hits * 67.05
    
    return {
        "total_requests": total,
        "cache_hits": hits,
        "cache_misses": misses,
        "hit_rate_percent": round(hit_rate, 2),
        "estimated_latency_saved_ms": round(latency_saved_ms, 2)
    }'''

pattern = r"@app\.get\(\"/v1/metrics\"\).*?(?=\n@app\.|\nif __name__|\Z)"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_metrics_route, content, flags=re.DOTALL)
else:
    content += "\n\n" + new_metrics_route

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[+] Rota de métricas corrigida com auto-criação de tabela!")
