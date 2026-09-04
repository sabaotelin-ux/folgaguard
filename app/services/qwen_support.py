import os
import httpx

async def get_qwen_support_response(query: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Aegis Gate"
    }
    payload = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {"role": "system", "content": "Você é um assistente técnico especialista no Aegis Gate."},
            {"role": "user", "content": query}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        if response.status_code != 200:
            return f"Erro OpenRouter ({response.status_code}): {response.text}"
        data = response.json()
        return data["choices"][0]["message"]["content"]
