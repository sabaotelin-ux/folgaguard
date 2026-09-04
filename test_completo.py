import requests, json
BASE_URL = "http://127.0.0.1:8000"
print("--- 1. Health Check ---")
print(requests.get(f"{BASE_URL}/health").json())
print("\n--- 2. Motor Local (Llama) ---")
r = requests.post(f"{BASE_URL}/local/analisar", json={"prompt": "Oi", "max_tokens": 20})
print("Status:", r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
print("\n--- 3. Nuvem (Groq) ---")
r2 = requests.post(f"{BASE_URL}/v1/chat/completions", json={"messages": [{"role": "user", "content": "Oi"}], "motor": "groq"})
print("Status:", r2.status_code)
print(json.dumps(r2.json(), indent=2, ensure_ascii=False))
