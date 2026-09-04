import os
import logging
import requests
from google import genai

logger = logging.getLogger("uvicorn.error")


def obter_lista_chaves():
    chaves = os.environ.get("GEMINI_API_KEYS", "")
    lista = [c.strip() for c in chaves.split(",") if c.strip()]
    if lista:
        return lista
    chave = os.environ.get("GEMINI_API_KEY", "")
    return [chave] if chave else []


def chamar_groq(prompt: str):
    chave = os.environ.get("GROQ_API_KEY", "")
    if not chave:
        return None
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {chave}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
                "temperature": 0.2
            },
            timeout=15
        )
        resp.raise_for_status()
        texto = resp.json()["choices"][0]["message"]["content"]
        logger.info("[ia_juiz] Sucesso via Groq")
        return texto.strip()
    except Exception as e:
        logger.error(f"[ia_juiz] ERRO no Groq: {type(e).__name__}: {e}")
        return None


def avaliar_com_ia(texto: str) -> dict:
    prompt = (
        "Você está auditando um texto jurídico gerado por outra fonte de IA, "
        "não é uma conversa comigo. Responda apenas com a análise técnica, "
        "sem comentários sobre você mesmo, suas capacidades ou limitações. "
        "Em até 3 frases: há afirmações inverificáveis, contradições ou "
        "exageros no texto abaixo?\n\nTexto: " + texto
    )

    resposta_groq = chamar_groq(prompt)
    if resposta_groq:
        return {"disponivel": True, "observacao": resposta_groq}

    chaves = obter_lista_chaves()
    logger.info(f"[ia_juiz] {len(chaves)} chave(s) disponível(is)")

    if not chaves:
        return {"disponivel": False, "observacao": "Sem chave configurada"}

    for i, chave in enumerate(chaves):
        try:
            c = genai.Client(api_key=chave)
            r = c.models.generate_content(model="gemini-3.6-flash", contents=prompt)
            logger.info(f"[ia_juiz] Sucesso na chave {i+1}")
            return {"disponivel": True, "observacao": r.text.strip()}
        except Exception as e:
            erro_str = str(e).lower()
            logger.error(f"[ia_juiz] ERRO na chave {i+1}: {type(e).__name__}: {e}")
            if "429" in erro_str or "quota" in erro_str or "503" in erro_str or "unavailable" in erro_str:
                continue
            break

    return {"disponivel": False, "observacao": "IA indisponivel"}
