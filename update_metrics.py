import re

with open("main_api.py", "r") as f:
    code = f.read()

metrics_code = """
@app.get("/metrics")
def get_metrics():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM audit_logs")
        total_logs = cursor.fetchone()[0]
        conn.close()
        return {"total_decisions": total_logs, "status": "active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

if "/metrics" not in code:
    code += metrics_code
    with open("main_api.py", "w") as f:
        f.write(code)
    print("Endpoint /metrics adicionado com sucesso!")
else:
    print("Endpoint já existe.")
