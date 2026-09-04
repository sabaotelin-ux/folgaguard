import requests

url = "http://127.0.0.1:8000/v1/chat/completions"

print("Enviando requisições para estourar o limite do Circuit Breaker (threshold=3)...")
for i in range(1, 5):
    payload = {"motor": "local_invalido", "prompt": f"Teste estresse CB {i}"}
    response = requests.post(url, json=payload)
    print(f"[{i}] Status: {response.status_code} | Resposta: {response.json().get('source')} | Erro/Info: {response.json().get('resposta', response.json())}")

print("\nVerificando as últimas linhas do arquivo de auditoria (gateway.log):")
