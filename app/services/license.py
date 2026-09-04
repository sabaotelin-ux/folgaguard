from fastapi import Header, HTTPException

async def verify_commercial_license(x_license_key: str = Header(..., description="Chave de licença comercial do Aegis Gate")):
    # Validação de licença comercial (pode ser integrada a banco de dados ou gateway de pagamento)
    valid_keys = ["AEGIS-PRO-TEST-KEY-2026"]
    if x_license_key not in valid_keys:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: Chave de licença inválida, expirada ou inexistente para recursos pagos."
        )
    return {"license_key": x_license_key, "tier": "pro_enterprise"}
