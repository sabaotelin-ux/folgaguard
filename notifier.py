import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_alerta(mensagem):
    if not TOKEN or not CHAT_ID:
        print("[-] Telegram Bot Token ou Chat ID não configurados no .env")
        return False
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🛡️ *Aegis Gate Alert*\n\n{mensagem}",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print("[+] Alerta enviado para o Telegram com sucesso!")
            return True
        else:
            print(f"[-] Erro ao enviar alerta: {response.text}")
            return False
    except Exception as e:
        print(f"[-] Falha na conexão com o Telegram: {e}")
        return False

if __name__ == "__main__":
    enviar_alerta("Sistema Aegis Gate operando normalmente e rotina de backup executada com sucesso.")
