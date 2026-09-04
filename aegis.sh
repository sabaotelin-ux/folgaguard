#!/bin/bash
case "$1" in
    start)
        echo "[*] Iniciando Aegis Gate..."
        nohup python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 > aegis.log 2>&1 &
        echo "[+] Aegis Gate rodando em segundo plano. Logs em aegis.log"
        ;;
    stop)
        echo "[*] Parando Aegis Gate..."
        pkill -f uvicorn
        echo "[+] Servidor encerrado."
        ;;
    status)
        if pgrep -f uvicorn > /dev/null; then
            echo "[+] Aegis Gate está ATIVO."
        else
            echo "[-] Aegis Gate está INATIVO."
        fi
        ;;
    logs)
        tail -n 20 aegis.log
        ;;
    *)
        echo "Uso: ./aegis.sh {start|stop|status|logs}"
        ;;
esac
