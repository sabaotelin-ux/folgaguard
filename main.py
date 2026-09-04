import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.qwen_support import get_qwen_support_response
from app.routers import commercial

app = FastAPI(title="Aegis Gate", version="2.0.0")

# Garante que a pasta static existe e a monta
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui as rotas comerciais protegidas por chave de licença
app.include_router(commercial.router)

class SupportQuery(BaseModel):
    query: str

@app.get("/")
async def read_index():
    index_path = "app/static/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "online", "message": "Aegis Gate API ativa."}

@app.post("/support/qwen")
async def qwen_support(payload: SupportQuery):
    try:
        response_text = await get_qwen_support_response(payload.query)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
