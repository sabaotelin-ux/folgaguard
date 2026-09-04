with open('main.py', 'r') as f:
    content = f.read()

old = '''def call_primary_provider(prompt: str):
    if random.random() < 0.15:
        raise ConnectionError("Primary-LLM indisponivel")
    time.sleep(0.08)
    return f"Aegis Secure Processed (Primary): {prompt}..."

def call_secondary_provider(prompt: str):
    time.sleep(0.12)
    return f"Aegis Secure Processed (Fallback): {prompt}..."'''

new = '''def call_primary_provider(prompt: str):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ConnectionError("MISTRAL_API_KEY nao configurada")
    resp = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]},
        timeout=15
    )
    if resp.status_code != 200:
        raise ConnectionError(f"Mistral retornou status {resp.status_code}")
    return resp.json()["choices"][0]["message"]["content"]

def call_secondary_provider(prompt: str):
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise ConnectionError("CEREBRAS_API_KEY nao configurada")
    resp = requests.post(
        "https://api.cerebras.ai/v1/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        json={"model": "llama3.1-8b", "messages": [{"role": "user", "content": prompt}]},
        timeout=15
    )
    if resp.status_code != 200:
        raise ConnectionError(f"Cerebras retornou status {resp.status_code}")
    return resp.json()["choices"][0]["message"]["content"]'''

if old not in content:
    print("ERRO: bloco original nao encontrado, nada foi alterado.")
else:
    content = content.replace(old, new)
    with open('main.py', 'w') as f:
        f.write(content)
    print("Substituicao feita com sucesso!")
