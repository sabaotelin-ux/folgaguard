with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

if "from pydantic import BaseModel" not in content:
    content = "from pydantic import BaseModel, Field\n" + content

model_def = """class ChatRequest(BaseModel):
    motor: str
    prompt: str = "Teste de failover"

"""

if "class ChatRequest" not in content:
    content = content.replace("import hmac", model_def + "import hmac")

content = content.replace("async def chat_completions(payload: dict", "async def chat_completions(payload: ChatRequest")
content = content.replace('motor = payload.get("motor")', 'motor = payload.motor')
content = content.replace('ultimo_prompt = payload.get("prompt") or payload.get("message") or "Teste de failover"', 'ultimo_prompt = payload.prompt or "Teste de failover"')

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)
print("[+] Pydantic v2 integrado com sucesso!")
