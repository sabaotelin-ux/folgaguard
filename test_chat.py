import requests
import json

url = "http://127.0.0.1:8000/v1/chat/completions"
headers = {
    "x-api-key": "cliente_alpha_key_123",
    "Content-Type": "application/json"
}
payload = {
    "motor": "groq",
    "messages": [{"role": "user", "content": "Olá, teste do sistema Aegis Gate via Groq"}]
}

print("Enviando requisição usando o motor Groq...")
try:
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    print(f"Status Code: {response.status_code}")
    print(f"Resposta: {response.text}")
except Exception as e:
    print(f"Erro na execução: {e}")
