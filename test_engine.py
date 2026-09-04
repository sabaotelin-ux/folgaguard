# Licença MIT
# Copyright (c) 2026 Augusto Cezar de Almeida

system_metrics = {
    "total_requests": 0,
    "overload_events": 0,
    "adaptive_threshold": 5.0,
    "learning_rate": 0.1
}

def simulate_request(company_size, latency_ms, error_rate):
    system_metrics["total_requests"] += 1
    latency_sec = latency_ms / 1000.0
    current_threshold = system_metrics["adaptive_threshold"]
    
    is_overloaded = latency_sec > current_threshold or error_rate > 0.05
    
    if is_overloaded:
        system_metrics["overload_events"] += 1
        system_metrics["adaptive_threshold"] -= system_metrics["learning_rate"] * 0.2
        decision = "FALLBACK_MODE: Roteando para processamento local isolado"
    else:
        system_metrics["adaptive_threshold"] += system_metrics["learning_rate"] * 0.05
        decision = "NORMAL_MODE: Operação integrada padrão"
        
    system_metrics["adaptive_threshold"] = max(1.0, min(system_metrics["adaptive_threshold"], 10.0))
    
    print(f"--- Empresa: {company_size} | Latência: {latency_sec}s ---")
    print(f"Decisão do Motor: {decision}")
    print(f"Limiar Atual: {system_metrics['adaptive_threshold']:.2f}\n")

print("Iniciando simulação do motor adaptativo...\n")
simulate_request("Pequena", 2000, 0.01)
simulate_request("Média", 6500, 0.02)
simulate_request("Grande", 1500, 0.08)
simulate_request("Média", 3000, 0.01)
