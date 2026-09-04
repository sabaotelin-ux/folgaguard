import os
import shutil
import zipfile
from datetime import datetime

# Configuração de diretórios
backup_dir = "backups"
os.makedirs(backup_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = os.path.join(backup_dir, f"aegis_backup_{timestamp}.zip")

files_to_backup = ["folgaguard.db", "autonomous_engine.db", ".env"]

print("Iniciando rotina de backup seguro...")

with zipfile.ZipFile(backup_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files_to_backup:
        if os.path.exists(file):
            zipf.write(file)
            print(f"[+] Arquivo incluído: {file}")
        else:
            print(f"[-] Aviso: {file} não encontrado.")

print(f"\nBackup concluído com sucesso! Salvo em: {backup_filename}")

# Notificação via Telegram
try:
    from notifier import enviar_alerta
    enviar_alerta(f"Backup realizado com sucesso:\n`{backup_filename}`")
except Exception as e:
    print(f"Não foi possível enviar o alerta: {e}")
