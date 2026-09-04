import requests
import json
import sqlite3
from datetime import datetime

URL_AUDIT = "https://folgaguard.onrender.com/auditar/stream"
URL_SUPORTE = "https://folgaguard.onrender.com/suporte/stream"

HEADERS = {
    "Content-Type": "application/json",
    "X-Api-Key": "sua_chave_aqui"
}
DB_FILE = "aegis_local.db"

def inicializar_banco():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            texto_enviado TEXT,
            status_code INTEGER,
            provedor TEXT,
            cache_hit BOOLEAN,
            observacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_historico(registro: dict):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    resp = registro.get("resposta", {})
    cursor.execute("""
        INSERT INTO auditorias (timestamp, texto_enviado, status_code, provedor, cache_hit, observacao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        registro.get("timestamp"),
        registro.get("texto_enviado"),
        registro.get("status_code"),
        resp.get("provedor"),
        resp.get("cache_hit", False),
        resp.get("observacao", "")
    ))
    conn.commit()
    conn.close()

def exibir_historico():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, texto_enviado, provedor, cache_hit, status_code FROM auditorias ORDER BY id DESC LIMIT 20")
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        print("\n[i] Nenhum registro no banco de dados local.\n")
        return
    
    print(f"\n=== Histórico Local (Últimos {len(registros)}) ===")
    for i, reg in enumerate(registros, 1):
        ts, texto, prov, cache, status = reg
        print(f"[{i}] Data: {ts}")
        print(f"    Texto: {texto}")
        print(f"    Provedor: {prov} | Cache Hit: {cache} | Status: {status}")
        print("-" * 40)
    print()

def consultar_suporte():
    texto_suporte = input("\nQual a sua dúvida técnica ou de configuração? ").strip()
    if not texto_suporte:
        print("A pergunta não pode estar vazia.\n")
        return

    payload = {"texto": texto_suporte}
    print("\nConectando ao Assistente Técnico do Aegis Gate...")
    try:
        response = requests.post(URL_SUPORTE, json=payload, headers=HEADERS, stream=True, timeout=30)
        if response.status_code == 200:
            print("\n--- Resposta do Suporte Técnico ---")
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data: "):
                    data_str = line.split("data: ", 1)[1]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data_json = json.loads(data_str)
                        chunk = data_json.get("chunk", "")
                        print(chunk, end="", flush=True)
                    except Exception:
                        pass
            print("\n------------------------------------\n")
        else:
            print(f"Erro no servidor de suporte. Status: {response.status_code}\n")
    except Exception as e:
        print(f"Erro de conexão: {e}\n")

inicializar_banco()
print("=== Folgaguard Edge Agent (SSE Streaming Ativo) ===")

while True:
    print("\nO que você deseja fazer?")
    print("1. Enviar texto para auditoria (Streaming SSE)")
    print("2. Consultar Suporte Técnico Aegis Gate")
    print("3. Ver histórico local")
    print("4. Sair")
    
    opcao = input("Escolha uma opção (1-4): ").strip()
    
    if opcao == "1":
        texto = input("\nDigite o texto para auditoria: ").strip()
        if not texto:
            print("O texto não pode estar vazio.\n")
            continue

        print("\nEscolha o provedor de IA:")
        print("0. Automático (Groq com fallback para Gemini)")
        print("1. Groq")
        print("2. Gemini")
        escolha_prov = input("Opção de provedor [0]: ").strip()
        
        provedor_forcado = None
        if escolha_prov == "1":
            provedor_forcado = "groq"
        elif escolha_prov == "2":
            provedor_forcado = "gemini"

        payload = {"texto": texto, "origem": "termux-node"}
        if provedor_forcado:
            payload["provedor_forcado"] = provedor_forcado

        print("\nConectando ao stream de auditoria...")
        try:
            response = requests.post(URL_AUDIT, json=payload, headers=HEADERS, stream=True, timeout=30)
            status = response.status_code
            
            if status == 200:
                meta_info = {}
                observacao_completa = ""
                current_event = "message"
                
                print("\n--- Resposta em Tempo Real ---")
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    if line.startswith("event: "):
                        current_event = line.split("event: ")[1].strip()
                        continue
                    if line.startswith("data: "):
                        data_str = line.split("data: ", 1)[1]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            if current_event == "meta":
                                meta_info = data_json
                            elif current_event == "message":
                                chunk = data_json.get("chunk", data_json.get("texto", ""))
                                print(chunk, end="", flush=True)
                                observacao_completa += chunk
                        except Exception:
                            pass
                print("\n------------------------------\n")

                registro = {
                    "timestamp": datetime.now().isoformat(),
                    "texto_enviado": texto,
                    "status_code": status,
                    "resposta": {
                        "provedor": meta_info.get("provedor", "groq"),
                        "cache_hit": meta_info.get("cache_hit", False),
                        "observacao": observacao_completa
                    }
                }
                salvar_historico(registro)
                print("[✓] Salvo no banco de dados local com sucesso.\n")
            else:
                print(f"Erro no servidor. Resposta: {response.text}\n")
                
        except Exception as e:
            print(f"Erro de conexão: {e}\n")

    elif opcao == "2":
        consultar_suporte()

    elif opcao == "3":
        exibir_historico()

    elif opcao in ["4", "sair", "exit"]:
        print("Encerrando agente de borda...")
        break
    else:
        print("Opção inválida. Tente novamente.\n")
