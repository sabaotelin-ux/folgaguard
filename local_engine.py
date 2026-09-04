import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("AEGIS_MODEL_NAME", "qwen2.5:1.5b")


def get_local_runtime():
    """Verifica se o servidor Ollama esta disponivel."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e:
        print(f"[Aegis Engine] Ollama indisponivel: {e}")
    return None


def generate_local_response(prompt):
    """Executa a inferencia localmente via API do Ollama (Qwen)."""
    runtime = get_local_runtime()

    if runtime is None:
        return "[Aegis Gate] Modelo local indisponivel."

    try:
        full_prompt = (
            "Voce e o assistente inteligente do FolgaGuard. "
            "Responda de forma direta e curta.\n\n"
            f"Usuario: {prompt}\nAssistente:"
        )
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512
                }
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[Erro na inferencia local]: {str(e)}"
