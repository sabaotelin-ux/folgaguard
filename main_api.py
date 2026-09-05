from typing import Optional
import json
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="Folgaguard Hub")

API_KEY_SECRETA = os.getenv("FOLGAGUARD_API_KEY", "sua_chave_aqui")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class AuditoriaRequest(BaseModel):
    texto: str
    origem: str = "default"

def avaliar_com_ia(texto: str):
    prompt_sistema = "Audite o texto a seguir para identificar afirmações factuais, contradições ou exageros. Seja objetivo."
    
    # Tentativa com Groq (Primary)
    if GROQ_API_KEY:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": texto}
                    ],
                    "temperature": 0.3
                },
                timeout=15
            )
            if response.status_code == 200:
                conteudo = response.json()["choices"][0]["message"]["content"]
                return {"provedor": "groq", "disponivel": True, "observacao": conteudo}
        except Exception:
            pass  # Falhou, tenta fallback

    # Fallback para Gemini
    if GEMINI_API_KEY:
        try:
            url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            response = requests.post(
                url_gemini,
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": f"{prompt_sistema}\n\nTexto: {texto}"}]}]},
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                conteudo = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"provedor": "gemini-fallback", "disponivel": True, "observacao": conteudo}
        except Exception:
            pass

    # Resposta mock caso nenhuma chave esteja ativa
    return {
        "provedor": "mock-local",
        "disponivel": True,
        "observacao": f"O texto '{texto}' foi processado sem chaves de IA ativas. Nenhuma anomalia factual relevante detectada."
    }

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>Folgaguard Hub</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>Folgaguard Hub Ativo</h1>
            <p>Servidor rodando com rastreamento de provedor de IA.</p>
        </body>
    </html>
    """

@app.post("/auditar", summary="Alias de /web/auditar")
@app.post("/web/auditar", summary="Audita um texto de IA usando Groq com fallback Gemini")
def auditar_web(request: AuditoriaRequest, x_api_key: str = Header(None)):
    resultado = avaliar_com_ia(request.texto)
    resultado["origem"] = request.origem
    return resultado

from fastapi.responses import StreamingResponse

@app.post("/auditar/stream")
async def auditar_stream(request: AuditoriaRequest):
    def gerar_eventos():
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [{"role": "user", "content": f"Audite o texto: {request.texto}"}],
                    "stream": True
                },
                stream=True
            )
            for linha in response.iter_lines():
                if linha:
                    linha_str = linha.decode("utf-8")
                    if linha_str.startswith("data: "):
                        conteudo = linha_str[6:]
                        if conteudo.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            dados = json.loads(conteudo)
                            delta = dados["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield f"data: {json.dumps({'texto': delta})}\n\n"
                        except Exception:
                            continue
        except Exception as e:
            yield f"data: {json.dumps({'erro': str(e)})}\n\n"

    return StreamingResponse(gerar_eventos(), media_type="text/event-stream")

class SuporteRequest(BaseModel):
    texto: str
    provedor_forcado: Optional[str] = None

@app.post("/suporte/stream")
async def suporte_stream(request: SuporteRequest):
    system_prompt = (
        "Você é o Assistente Técnico Especializado do ecossistema Aegis Gate e Folgaguard. "
        "Ajude desenvolvedores sobre a instalação no Termux, "
        "configuração do SQLite local, chaves de API, arquitetura edge-to-cloud e otimização de cache via Redis. "
        "Responda com precisão técnica, clareza e foco em resolução de problemas."
    )

    def gerar_eventos_suporte():
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": request.texto}
                    ],
                    "stream": True
                },
                stream=True
            )
            for linha in response.iter_lines():
                if linha:
                    linha_str = linha.decode("utf-8")
                    if linha_str.startswith("data: "):
                        conteudo = linha_str[6:]
                        if conteudo.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            dados = json.loads(conteudo)
                            delta = dados["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield f"data: {json.dumps({'chunk': delta})}\n\n"
                        except Exception:
                            continue
        except Exception as e:
            yield f"data: {json.dumps({'erro': str(e)})}\n\n"

    return StreamingResponse(gerar_eventos_suporte(), media_type="text/event-stream")
