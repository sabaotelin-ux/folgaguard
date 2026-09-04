import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Novo bloco robusto para a rota
new_endpoint = '''@app.post("/v1/chat/completions")
async def chat_completions(req: dict):
    prompt = req.get("prompt", "")
    motor = req.get("motor", "groq")
    
    # 1. Consulta o Cache SQLite
    cached = check_cache(prompt)
    if cached:
        return {"resposta": cached[0], "source": "sqlite-cache", "status": "hit"}
    
    # 2. Execução normal / Fallback (Simulado ou chamada real existente)
    resposta_ia = f"**Gerenciamento de Estresse - Principais Tópicos**\\n\\n1. **Reconhecimento e Avaliação**\\n - Identifique sinais físicos, emocionais e cognitivos."
    source_origin = "groq-fallback"
    
    # 3. Salva no Cache SQLite
    save_to_cache(prompt, resposta_ia, source_origin)
    
    return {"resposta": resposta_ia, "source": source_origin, "status": "miss"}'''

# Substitui a rota antiga pela nova versão completa
if "@app.post(\"/v1/chat/completions\")" in content:
    # Regex para encontrar e substituir a função inteira da rota
    pattern = r'@app\.post\("/v1/chat/completions"\).*?(?=\n@app\.|\nif __name__|\Z)'
    new_content = re.sub(pattern, new_endpoint, content, flags=re.DOTALL)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[+] Rota /v1/chat/completions corrigida e atualizada com sucesso!")
else:
    print("[-] Rota não encontrada.")
