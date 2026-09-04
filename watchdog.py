# Licença MIT
# Copyright (c) 2026 Augusto Cezar de Almeida

import time
import subprocess
import requests

API_URL = "http://127.0.0.1:8000/decide"
CHECK_INTERVAL = 10

def check_health():
    try:
        response = requests.post(
            API_URL, 
            json={"company_size": "enterprise", "latency_ms": 10.0, "error_rate": 0.0},
            timeout=3
        )
        return response.status_code == 200
    except Exception:
        return False

def restart_api():
    print("[WATCHDOG] Falha detectada! Reiniciando cluster Uvicorn...")
    subprocess.run(["pkill", "-f", "uvicorn"])
    time.sleep(2)
    subprocess.Popen(["uvicorn", "main_api:app", "--host", "127.0.0.1", "--port", "8000", "--workers", "4"])

if __name__ == "__main__":
    print("[WATCHDOG] Aegis Gate Watchdog iniciado com sucesso.")
    while True:
        if not check_health():
            restart_api()
        time.sleep(CHECK_INTERVAL)
