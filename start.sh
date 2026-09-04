#!/bin/bash
echo "Iniciando o Aegis Gate..."
uvicorn main_api:app --host 127.0.0.1 --port 8000 --reload
