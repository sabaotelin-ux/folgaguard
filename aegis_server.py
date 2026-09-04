# Aegis Gate - Camada P2P Blindada com HMAC, TTL e LRU
import asyncio, sqlite3, socket, json, time, hmac, hashlib, aiohttp
from aiohttp import web

PORT_DISCOVERY, PORT_API = 50005, 50006
NODE_ID = f"node_{socket.gethostname()}"
DB_NAME = "aegis_unified.db"
SECRET_KEY = b"aegis_secure_swarm_key_2026"
CACHE_TTL = 3600
MAX_CACHE_ITEMS = 100

class AegisSecureServer:
    def __init__(self):
        self.peers = {}
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    prompt_hash TEXT PRIMARY KEY, 
                    response TEXT, 
                    created_at REAL, 
                    last_accessed REAL
                )
            """)
            conn.commit()

    def clean_cache(self):
        now = time.time()
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("DELETE FROM cache WHERE ? - created_at > ?", (now, CACHE_TTL))
            count = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            if count > MAX_CACHE_ITEMS:
                excess = count - MAX_CACHE_ITEMS
                conn.execute("""
                    DELETE FROM cache WHERE prompt_hash IN (
                        SELECT prompt_hash FROM cache ORDER BY last_accessed ASC LIMIT ?
                    )
                """, (excess,))
            conn.commit()

    def get_local(self, ph):
        self.clean_cache()
        now = time.time()
        with sqlite3.connect(DB_NAME) as conn:
            row = conn.execute("SELECT response FROM cache WHERE prompt_hash = ?", (ph,)).fetchone()
            if row:
                conn.execute("UPDATE cache SET last_accessed = ? WHERE prompt_hash = ?", (now, ph))
                conn.commit()
                return row[0]
        return None

    def set_local(self, ph, val):
        self.clean_cache()
        now = time.time()
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO cache (prompt_hash, response, created_at, last_accessed) 
                VALUES (?, ?, ?, ?)
            """, (ph, val, now, now))
            conn.commit()

    async def broadcast_presence(self):
        while True:
            try:
                data = {"node_id": NODE_ID, "api_port": PORT_API, "time": time.time()}
                raw_data = json.dumps(data).encode()
                sig = hmac.new(SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
                payload = json.dumps({"data": data, "sig": sig}).encode()
                
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(payload, ('255.255.255.255', PORT_DISCOVERY))
            except: pass
            await asyncio.sleep(5)

    async def listen_peers(self):
        class Proto(asyncio.DatagramProtocol):
            def __init__(self, outer): self.outer = outer
            def datagram_received(self, data, addr):
                try:
                    packet = json.loads(data.decode())
                    raw_data = json.dumps(packet["data"]).encode()
                    expected_sig = hmac.new(SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
                    
                    if hmac.compare_digest(expected_sig, packet.get("sig", "")):
                        msg = packet["data"]
                        pid = msg.get("node_id")
                        port = msg.get("api_port")
                        if pid and pid != NODE_ID and port:
                            self.outer.peers[pid] = {"ip": addr[0], "port": port, "time": time.time()}
                except: pass
                
        loop = asyncio.get_running_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', PORT_DISCOVERY))
        sock.setblocking(False)
        transport, _ = await loop.create_datagram_endpoint(lambda: Proto(self), sock=sock)
        try:
            while True:
                now = time.time()
                for pid in [k for k, v in self.peers.items() if now - v["time"] > 15]:
                    del self.peers[pid]
                await asyncio.sleep(5)
        finally: transport.close()

    async def query_peers(self, ph):
        async with aiohttp.ClientSession() as session:
            for pid, info in list(self.peers.items()):
                try:
                    url = f"http://{info['ip']}:{info['port']}/fetch/{ph}"
                    async with session.get(url, timeout=1.5) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if "response" in data: return data["response"]
                except: continue
        return None

    async def handle_fetch(self, request):
        ph = request.match_info.get("hash")
        val = self.get_local(ph)
        if val: return web.json_response({"response": val})
        return web.json_response({"error": "not_found"}, status=404)

    async def handle_cache(self, request):
        ph = request.match_info.get("hash")
        val = self.get_local(ph)
        if val:
            return web.json_response({"response": val, "source": "local", "peers_detected": list(self.peers.keys())})
        
        val = await self.query_peers(ph)
        if val:
            self.set_local(ph, val)
            return web.json_response({"response": val, "source": "swarm", "peers_detected": list(self.peers.keys())})
            
        return web.json_response({"error": "not_found_in_swarm", "peers_detected": list(self.peers.keys())}, status=404)

    async def start(self):
        app = web.Application()
        app.router.add_get("/cache/{hash}", self.handle_cache)
        app.router.add_get("/fetch/{hash}", self.handle_fetch)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT_API)
        await site.start()
        print(f"[{NODE_ID}] Aegis Gate com TTL, LRU e HMAC Ativo na porta {PORT_API}...")
        await asyncio.gather(self.broadcast_presence(), self.listen_peers())

if __name__ == "__main__":
    server = AegisSecureServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServidor encerrado com segurança.")
