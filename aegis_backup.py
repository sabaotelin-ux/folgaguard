import shutil
import datetime
import os

def run_backup():
    db_file = "aegis_unified.db"
    if not os.path.exists(db_file):
        print("[Backup] Banco de dados não encontrado.")
        return

    backup_dir = "./backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"aegis_backup_{timestamp}.db")

    shutil.copy2(db_file, backup_path)
    print(f"[Backup] Cópia de segurança criada com sucesso em: {backup_path}")

if __name__ == "__main__":
    run_backup()
