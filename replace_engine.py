with open('main.py', 'r') as f:
    content = f.read()

old = '''def query_llm_engine(prompt: str):
    start_time = time.time()
    time.sleep(0.08)
    latency = (time.time() - start_time) * 1000

    return {
        "source": "Primary-LLM",
        "response": f"Processado com segurança: {prompt}...",
        "latency_ms": round(latency, 2),
        "threat_guard": "passed"
    }'''

new = '''def query_llm_engine(prompt: str):
    start_time = time.time()
    mistral_key = os.environ.get("MISTRAL_API_KEY")
    cerebras_key = os.environ.get("CEREBRAS_API_KEY")

    try:
        if not mistral_key:
            raise ConnectionError("MISTRAL_API_KEY nao configurada")
        resp = httpx.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {mistral_key}"},
            json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]},
            timeout=15
        )
        resp.raise_for_status()
        texto = resp.json()["choices"][0]["message"]["content"]
        source = "Mistral"
    except Exception:
        try:
            if not cerebras_key:
                raise ConnectionError("CEREBRAS_API_KEY nao configurada")
            resp = httpx.post(
                "https://api.cerebras.ai/v1/chat/completions",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {cerebras_key}"},
                json={"model": "llama3.1-8b", "messages": [{"role": "user", "content": prompt}]},
                timeout=15
            )
            resp.raise_for_status()
            texto = resp.json()["choices"][0]["message"]["content"]
            source = "Cerebras-Fallback"
        except Exception as e:
            texto = f"Erro: ambos os provedores falharam ({e})"
            source = "Error"

    latency = (time.time() - start_time) * 1000
    return {
        "source": source,
        "response": texto,
        "latency_ms": round(latency, 2),
        "threat_guard": "passed"
    }'''

if old not in content:
    print("ERRO: bloco original nao encontrado, nada foi alterado.")
else:
    content = content.replace(old, new)
    with open('main.py', 'w') as f:
        f.write(content)
    print("Substituicao feita com sucesso!")
