import sqlite3
import time
import hmac
import hashlib
import requests
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

DB_NAME = "aegis_unified.db"
PORT = 8080
SHARED_SECRET = b"aegis_secure_mesh_key_2026"

def sign_payload(data: bytes) -> str:
    return hmac.new(SHARED_SECRET, data, hashlib.sha256).hexdigest()

def verify_payload(data: bytes, signature: str) -> bool:
    expected = sign_payload(data)
    return hmac.compare_digest(expected, signature)

class SecureP2PHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        signature = self.headers.get('X-Aegis-Signature', '')
        
        if not verify_payload(post_data, signature):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized: Invalid E2EE Signature")
            return
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Sync Accepted Securely")

def start_secure_server():
    server = HTTPServer(('0.0.0.0', PORT), SecureP2PHandler)
    print(f"[P2P E2EE] Servidor criptografado ativo na porta {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    t_server = threading.Thread(target=start_secure_server, daemon=True)
    t_server.start()
    print("[P2P E2EE] Módulo inicializado e pronto para validação de nós.")
    while True:
        time.sleep(3600)
