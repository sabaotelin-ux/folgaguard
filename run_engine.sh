#!/bin/bash
echo "=== Inicializando Aegis Gate Autonomous Engine ==="
python db_query.py
echo "=== Subindo Servidor FastAPI via Uvicorn ==="
uvicorn main_api:app --host 127.0.0.1 --port 8000 --reload
