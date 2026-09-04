import time
from fastapi import HTTPException, Request

REQUEST_WINDOW = 60  # Janela de 1 minuto
MAX_REQUESTS = 10    # Máximo de 10 requisições por minuto por IP
clients_ip_tracker = {}

async def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    
    if client_ip in clients_ip_tracker:
        clients_ip_tracker[client_ip] = [
            t for t in clients_ip_tracker[client_ip] if current_time - t < REQUEST_WINDOW
        ]
    else:
        clients_ip_tracker[client_ip] = []
        
    if len(clients_ip_tracker[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Muitas requisições. Limite de taxa excedido. Tente novamente mais tarde."
        )
        
    clients_ip_tracker[client_ip].append(current_time)
