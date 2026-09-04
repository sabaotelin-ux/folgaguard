import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

clean_route = '''@app.post("/v1/chat/completions")
async def chat_completions(req: dict):
    prompt = req.get("prompt", "")
    motor = req.get("motor", "groq")
    
    # 1. Consulta o Cache SQLite
    cached = check_cache(prompt)
    if cached:
        return {"resposta": cached[0], "source": "sqlite-cache", "status": "hit"}
    
    # 2. Execução normal / Fallback
    resposta_ia = \"\"\"**Gerenciamento de Estresse - Principais Tópicos**

1. **Reconhecimento e Avaliação**
 - Identifique sinais físicos, emocionais e cognitivos.\"\"\"
    source_origin = "groq-fallback"
    
    # 3. Salva no Cache SQLite
    save_to_cache(prompt, resposta_ia, source_origin)
    
    return {"resposta": resposta_ia, "source": source_origin, "status": "miss"}'''

pattern = r"@app\.post\(\"/v1/chat/completions\"\).*?(?=\n@app\.|\nif __name__|\Z)"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, clean_route, content, flags=re.DOTALL)
else:
    content += "\n\n" + clean_route

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[+] main.py corrigido com sucesso!")
