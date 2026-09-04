import os
import requests

def send_notification(message):
    webhook_url = os.getenv("AEGIS_WEBHOOK_URL")
    if not webhook_url:
        print(f"[Aegis Alerta]: {message}")
        return
    
    payload = {"content": message}
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        print(f"[Erro de Disparo]: {e}")

if __name__ == "__main__":
    send_notification("✨ Novo ativo processado, renderizado em 9:16 e integrado à malha P2P com sucesso!")
