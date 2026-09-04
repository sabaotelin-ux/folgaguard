#!/bin/bash
pkill -f uvicorn
nohup uvicorn main:app --host 127.0.0.1 --port 8000 > uvicorn.log 2>&1 &
echo "[+] Aegis Gate rodando estavel em background! PID: $!"
echo "[+] Para ver os logs do uvicorn: tail -f uvicorn.log"
echo "[+] Para ver os logs de failover: cat gateway.log"
