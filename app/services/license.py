from fastapi import Header, HTTPException
from app.services.db import check_license_db, init_db

# Garante que o banco seja inicializado na carga do serviço
init_db()

async def verify_pro_license(x_license_key: str = Header(None)):
    if not x_license_key:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Cabeçalho 'x-license-key' ausente."
        )
    
    license_info = check_license_db(x_license_key)
    
    if not license_info["valid"]:
        raise HTTPException(
            status_code=403, 
            detail="Licença comercial inválida, expirada ou inexistente."
        )
        
    return {"tier": license_info["tier"], "status": "authorized"}
