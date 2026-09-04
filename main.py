import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.routers import commercial
from app.services.qwen_support import get_qwen_support_response

app = FastAPI(title="Aegis Gate", version="2.0.0")

app.include_router(commercial.router)

class SupportQuery(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aegis Gate - Open-Core AI Gateway</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 100%; max-width: 500px; box-sizing: border-box; }
        h1 { font-size: 1.5rem; margin-bottom: 10px; color: #38bdf8; text-align: center; }
        p.sub { font-size: 0.9rem; color: #94a3b8; text-align: center; margin-bottom: 20px; }
        textarea { width: 100%; height: 100px; background: #0f172a; border: 1px solid #334155; color: #fff; padding: 10px; border-radius: 6px; resize: none; margin-bottom: 10px; box-sizing: border-box; }
        button { background: #0284c7; color: white; border: none; padding: 10px 15px; width: 100%; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        .response-box { margin-top: 15px; background: #0f172a; padding: 10px; border-radius: 6px; border: 1px solid #334155; font-size: 0.9rem; min-height: 50px; white-space: pre-wrap; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Aegis Gate</h1>
        <p class="sub">Interface de Suporte Qwen (Open-Core)</p>
        <textarea id="queryInput" placeholder="Digite sua dúvida técnica para a Secretária Qwen..."></textarea>
        <button onclick="sendQuery()">Enviar Consulta</button>
        <div id="responseBox" class="response-box">Aguardando consulta...</div>
    </div>
    <script>
        async function sendQuery() {
            const query = document.getElementById('queryInput').value;
            const box = document.getElementById('responseBox');
            if (!query.trim()) return;
            box.innerText = "Processando...";
            try {
                const res = await fetch('/support/qwen', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                box.innerText = data.response || JSON.stringify(data);
            } catch (err) {
                box.innerText = "Erro ao conectar com o servidor: " + err;
            }
        }
    </script>
</body>
</html>"""

@app.post("/support/qwen")
async def qwen_support(payload: SupportQuery):
    try:
        response_text = await get_qwen_support_response(payload.query)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
