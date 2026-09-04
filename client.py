import sys
import json
import hmac
import hashlib
import requests
import time

URL = "http://127.0.0.1:8000/v1/chat/completions"
SECRET_KEY = b"aegis_secret_key"

def send_prompt(prompt_text):
    payload = {"prompt": prompt_text, "motor": "groq"}
    body_bytes = json.dumps(payload).encode("utf-8")
    signature = hmac.new(SECRET_KEY, body_bytes, hashlib.sha256).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "X-Signature": signature
    }
    
    start_time = time.time()
    try:
        response = requests.post(URL, json=payload, headers=headers)
        elapsed = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[+] Status: {response.status_code} | Tempo: {elapsed:.2f} ms")
            print(f"[+] Origem: {data.get('source')} (status: {data.get('status')})")
            print(f"\nResposta:\n{data.get('resposta')}\n")
        else:
            print(f"[-] Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[-] Falha na conexão com o gateway: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 client.py \"Seu prompt aqui\"")
    else:
        send_prompt(" ".join(sys.argv[1:]))
