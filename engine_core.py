import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Motor Híbrido Adaptativo - Aegis Core")

system_metrics = {
    "total_requests": 0,
    "overload_events": 0,
    "adaptive_threshold": 5.0,
    "learning_rate": 0.1
}

class SystemPayload(BaseModel):
    company_size: str
    latency_ms: float
    error_rate: float

@app.post("/analyze")
def analyze_and_adapt(payload: SystemPayload):
    system_metrics["total_requests"] += 1
    latency_sec = payload.latency_ms / 1000.0
    current_threshold = system_metrics["adaptive_threshold"]
    
    is_overloaded = latency_sec > current_threshold or payload.error_rate > 0.05
    
    if is_overloaded:
        system_metrics["overload_events"] += 1
        system_metrics["adaptive_threshold"] -= system_metrics["learning_rate"] * 0.2
        decision = "FALLBACK_MODE: Roteando para processamento local isolado"
    else:
        system_metrics["adaptive_threshold"] += system_metrics["learning_rate"] * 0.05
        decision = "NORMAL_MODE: Operação integrada padrão"
        
    system_metrics["adaptive_threshold"] = max(1.0, min(system_metrics["adaptive_threshold"], 10.0))
    
    return {
        "status": "success",
        "company_size": payload.company_size,
        "decision": decision,
        "metrics": system_metrics
    }

@app.get("/status")
def get_engine_status():
    return system_metrics
