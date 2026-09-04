from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.db import create_pro_license

router = APIRouter(prefix="/api/v1/webhook", tags=["Webhooks"])

class PaymentNotification(BaseModel):
    status: str
    customer_email: str
    tier: str = "pro_enterprise"

@router.post("/payment")
async def payment_webhook(payload: PaymentNotification):
    if payload.status.lower() in ["approved", "succeeded", "paid"]:
        new_key = create_pro_license(payload.tier)
        return {
            "status": "success",
            "message": "Pagamento confirmado. Licença Pro gerada com sucesso.",
            "license_key": new_key,
            "customer": payload.customer_email
        }
    
    raise HTTPException(
        status_code=400,
        detail="Status de pagamento inválido ou não aprovado."
    )
