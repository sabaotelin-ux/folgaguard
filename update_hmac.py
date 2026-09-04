with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

if "import hmac" not in content:
    imports = "import hmac\nimport hashlib\nfrom fastapi import Header, HTTPException, Request\n"
    content = imports + content

target_sig = 'async def chat_completions(payload: dict):'
new_sig = '''async def chat_completions(payload: dict, x_signature: str = Header(None), request: Request = None):
    SECRET_KEY = b"aegis-secret-sovereign-key"
    if x_signature:
        body = await request.body()
        expected = hmac.new(SECRET_KEY, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, x_signature):
            return {"erro": "Assinatura HMAC inválida"}, 403'''

if target_sig in content and "x_signature" not in content:
    content = content.replace(target_sig, new_sig)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] HMAC integrado com sucesso!")
else:
    print("[*] HMAC já presente ou rota modificada.")
