from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import requests
import json
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "sua_chave_aqui")

class SuporteRequest(BaseModel):
    texto: str
    provedor_forcado: Optional[str] = None

@app.post("/suporte/stream")
async def suporte_stream(request: SuporteRequest):
    system_prompt = (
        "Você é o Assistente Técnico Especializado do ecossistema Aegis Gate e Folgaguard. "
        "Sua função é orientar clientes e desenvolvedores sobre a instalação no Termux, "
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
