from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qwen_support import get_qwen_support_response

router = APIRouter(prefix="/support", tags=["Technical Support"])

class SupportRequest(BaseModel):
    query: str

@router.post("/qwen")
async def qwen_support_endpoint(request: SupportRequest):
    try:
        response = await get_qwen_support_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
