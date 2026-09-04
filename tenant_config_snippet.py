import psycopg2
import psycopg2.extras

def get_tenant_config(tenant_id: str):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT motor_padrao, threshold_confianca, regras_prompt_guard FROM tenant_config WHERE tenant_id = %s",
            (tenant_id,)
        )
        row = cur.fetchone()
        if row:
            return dict(row)
        return {"motor_padrao": "groq", "threshold_confianca": 0.7, "regras_prompt_guard": {}}
    finally:
        conn.close()

