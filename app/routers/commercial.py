from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.license import verify_pro_license
from app.services.guardrails import evaluate_guardrails

router = APIRouter(prefix="/api/v1/pro", tags=["Commercial Pro"])

class AdvancedAuditRequest(BaseModel):
    text_content: str
    ruleset: str = "strict"

@router.post("/advanced-audit")
async def advanced_audit(
    payload: AdvancedAuditRequest, 
    license_data: dict = Depends(verify_pro_license)
):
    # Aplica os guardrails de segurança
    if not evaluate_guardrails(payload.text_content):
        raise HTTPException(
            status_code=400,
            detail="Conteúdo bloqueado pelos filtros de segurança do Aegis Gate (Guardrails)."
        )
        
    return {
        "status": "success",
        "tier": license_data["tier"],
        "audit_report": {
            "ruleset": payload.ruleset,
            "threats_detected": 0,
            "compliance": "approved",
            "message": "Conteúdo auditado com sucesso pela camada corporativa do Aegis Gate."
        }
    }
