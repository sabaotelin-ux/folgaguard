import time
import hashlib
import json
from datetime import datetime, timedelta
from fastapi import Response

CACHE_MEMORIA = {}
TTL_CACHE = 300

METRICAS = {
    "requisicoes_total": 0,
    "ameacas_bloqueadas": 0,
    "latencia_acumulada_ms": 0.0
}

def verificar_cache(payload_str: str):
    hash_key = hashlib.sha256(payload_str.encode()).hexdigest()
    if hash_key in CACHE_MEMORIA:
        dados, timestamp = CACHE_MEMORIA[hash_key]
        if datetime.now() - timestamp < timedelta(seconds=TTL_CACHE):
            return {"origem": "Cache", "dados": dados}
        else:
            del CACHE_MEMORIA[hash_key]
    return None

def salvar_cache(payload_str: str, dados):
    hash_key = hashlib.sha256(payload_str.encode()).hexdigest()
    CACHE_MEMORIA[hash_key] = (dados, datetime.now())
