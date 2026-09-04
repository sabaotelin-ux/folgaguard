# Licença MIT - Aegis Gate Swarm Final
import asyncio, sqlite3, socket, json, time, aiohttp
from aiohttp import web

PORT_DISCOVERY, PORT_API = 50005, 50006
NODE_ID = f"node_{socket.gethostname()}"

class AegisNode:
    def __init__(self):
        self.peers = {}
        with sqlite3.connect("aegis_swarm.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS cache (prompt_hash TEXT PRIMARY KEY, response TEXT)")
            conn.commit()

    def get_local(self, ph):
        with sqlite3.connect("aegis_swarm.db") as conn:
            row = conn.execute("SELECT response FROM cache WHERE prompt_hash = ?", (ph,)).fetchone()
            return row[0] if row else None

    def set_local(self, ph, val):
        with sqlite3.connect("aegis_swarm.db") as conn:
            conn.execute("INSERT OR REPLACE INTO cache (prompt_hash, response) VALUES (?, ?)", (ph, val))
            conn.commit()

    async def broadcast_presence(self):
        while True:
            try:
                payload = json.dumps({"node_id": NODE_ID}).encode()
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
                    msg = json.loads(data.decode())
                    pid = msg.get("node_id")
                    if pid and pid != NODE_ID:
                        self.outer.peers[pid] = {"ip": addr[0], "time": time.time()}
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
                    url = f"http://{info['ip']}:{PORT_API}/fetch/{ph}"
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

    async def handle_cache_request(self, request):
        ph = request.match_info.get("hash")
        # 1. Tenta cache local
        val = self.get_local(ph)
        if val: return web.json_response({"response": val, "source": "local"})
        
        # 2. Se não tem, busca na malha P2P
        val = await self.query_peers(ph)
        if val:
            self.set_local(ph, val) # Cacheia localmente o resultado do swarm
            return web.json_response({"response": val, "source": "swarm"})
            
        return web.json_response({"error": "not_found_in_swarm"}, status=404)

    async def start(self):
        app = web.Application()
        app.router.add_get("/cache/{hash}", self.handle_cache_request)
        app.router.add_get("/fetch/{hash}", self.handle_fetch)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT_API)
        await site.start()
        print(f"[{NODE_ID}] Aegis Gate Swarm V2 Rodando! Porta API: {PORT_API}")
        await asyncio.gather(self.broadcast_presence(), self.listen_peers())

if __name__ == "__main__":
    node = AegisNode()
    try: asyncio.run(node.start())
    except KeyboardInterrupt: print("\nEncerrado.")
