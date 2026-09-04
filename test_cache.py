import requests
import time
import hmac
import hashlib
import json

url = "http://127.0.0.1:8000/v1/chat/completions"
secret_key = b"aegis_secret_key"

payload = {
    "prompt": "Explique o gerenciamento de estresse em tópicos.",
    "motor": "groq"
}

body_bytes = json.dumps(payload).encode("utf-8")
signature = hmac.new(secret_key, body_bytes, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature": signature
}

print("[*] Disparando 1ª requisição (Cache Miss com Assinatura HMAC)...")
start_1 = time.time()
res_1 = requests.post(url, json=payload, headers=headers)
time_1 = (time.time() - start_1) * 1000
print(f"Tempo: {time_1:.2f} ms | Status: {res_1.status_code} | Resposta: {res_1.json()}")

print("\n[*] Disparando 2ª requisição idêntica (Cache Hit com Assinatura HMAC)...")
start_2 = time.time()
res_2 = requests.post(url, json=payload, headers=headers)
time_2 = (time.time() - start_2) * 1000
print(f"Tempo: {time_2:.2f} ms | Status: {res_2.status_code} | Resposta: {res_2.json()}")

if time_2 < time_1:
    print(f"\n[+] Sucesso! O cache SQLite economizou {time_1 - time_2:.2f} ms na resposta protegida por HMAC.")
