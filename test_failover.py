import requests

url = "http://127.0.0.1:8000/v1/chat/completions"
headers = {
    "x-api-key": "cliente_alpha_key_123",
    "Content-Type": "application/json"
}
payload = {
    "motor": "local",
    "messages": [{"role": "user", "content": "Teste de failover: se o local falhar, responda via nuvem."}]
}

print("Enviando requisição forçando motor local para testar o failover...")
response = requests.post(url, headers=headers, json=payload, timeout=15)
print(f"Status Code: {response.status_code}")
print(f"Resposta: {response.text}")
