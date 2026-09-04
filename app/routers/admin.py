from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.metrics import get_metrics_summary

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Observability"])

ADMIN_SECRET_KEY = "AEGIS-ADMIN-MASTER-2026"

@router.get("/metrics")
async def get_system_metrics(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Chave de administração inválida ou ausente."
        )
    
    return {
        "status": "healthy",
        "system": "Aegis Gate V2.1",
        "metrics": get_metrics_summary()
    }
