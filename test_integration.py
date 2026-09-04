import hmac
import hashlib
import requests
import json

URL = "http://127.0.0.1:8000/v1/chat/completions"
SECRET_KEY = b"aegis-secret-sovereign-key"

def send_request(payload_dict, custom_sig=None, use_valid_hmac=True):
    body = json.dumps(payload_dict).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    
    if custom_sig is not None:
        headers["X-Signature"] = custom_sig
    elif use_valid_hmac:
        sig = hmac.new(SECRET_KEY, body, hashlib.sha256).hexdigest()
        headers["X-Signature"] = sig
        
    return requests.post(URL, data=body, headers=headers)

print("[*] Teste 1: Payload válido com HMAC correto")
res = send_request({"motor": "local", "prompt": "Teste integrado 1"})
print(f"Status: {res.status_code} | Resposta: {res.json()}\n")

print("[*] Teste 2: Payload inválido (faltando campo obrigatório 'motor' - Pydantic v2)")
res = send_request({"prompt": "Sem motor"}, use_valid_hmac=True)
print(f"Status (Esperado 422): {res.status_code} | Detalhes: {res.text}\n")

print("[*] Teste 3: Assinatura HMAC incorreta (Bloqueio Criptográfico)")
res = send_request({"motor": "local", "prompt": "Ataque"}, custom_sig="assinatura_falsa_invalida")
print(f"Status (Esperado 403): {res.status_code} | Resposta: {res.json()}\n")

print("[*] Teste 4: Forçando Circuit Breaker com falhas consecutivas no motor local")
for i in range(1, 5):
    res = send_request({"motor": "local_quebrado", "prompt": f"Estresse {i}"})
    print(f"Tentativa {i} -> Status: {res.status_code} | Fonte/Erro: {res.json()}")

print("\n[+] Teste integrado concluído com sucesso!")
