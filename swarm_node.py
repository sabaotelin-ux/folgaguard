# Licença MIT
import asyncio
import json
import sqlite3
import time
import socket
from aiohttp import web

PORT_API = 50006
NODE_ID = f"node_{socket.gethostname()}"

class SwarmNode:
    def __init__(self):
        self.db_path = "aegis_swarm.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    prompt_hash TEXT PRIMARY KEY,
                    response TEXT,
                    timestamp REAL
                )
            """)
            conn.commit()

    def get_local_cache(self, prompt_hash):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT response FROM cache WHERE prompt_hash = ?", (prompt_hash,))
            row = cursor.fetchone()
            return row[0] if row else None

    async def handle_cache_request(self, request):
        prompt_hash = request.match_info.get("hash")
        cached = self.get_local_cache(prompt_hash)
        if cached:
            return web.json_response({"response": cached})
        return web.json_response({"error": "not_found"}, status=404)

    async def start(self):
        app = web.Application()
        app.router.add_get("/cache/{hash}", self.handle_cache_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT_API)
        await site.start()
        print(f"[{NODE_ID}] Servidor de cache P2P rodando na porta {PORT_API}...")
        await asyncio.Event().wait()

if __name__ == "__main__":
    node = SwarmNode()
    try:
        asyncio.run(node.start())
    except KeyboardInterrupt:
        print(f"\n[{NODE_ID}] Encerrado.")
