# Licença MIT - Aegis Gate Peer 2
import asyncio, sqlite3, socket, json, time, aiohttp
from aiohttp import web

PORT_DISCOVERY, PORT_API = 50005, 50007
NODE_ID = "node_peer_secundario"

class AegisPeerNode:
    def __init__(self):
        self.peers = {}
        with sqlite3.connect("aegis_swarm_2.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS cache (prompt_hash TEXT PRIMARY KEY, response TEXT)")
            conn.commit()

    def get_local(self, ph):
        with sqlite3.connect("aegis_swarm_2.db") as conn:
            row = conn.execute("SELECT response FROM cache WHERE prompt_hash = ?", (ph,)).fetchone()
            return row[0] if row else None

    async def broadcast_presence(self):
        while True:
            try:
                payload = json.dumps({"node_id": NODE_ID}).encode()
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(payload, ('127.0.0.1', PORT_DISCOVERY))
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
                await asyncio.sleep(5)
        finally: transport.close()

    async def handle_fetch(self, request):
        ph = request.match_info.get("hash")
        val = self.get_local(ph)
        if val: return web.json_response({"response": val})
        return web.json_response({"error": "not_found"}, status=404)

    async def start(self):
        app = web.Application()
        app.router.add_get("/fetch/{hash}", self.handle_fetch)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT_API)
        await site.start()
        print(f"[{NODE_ID}] Peer 2 Rodando! Porta API: {PORT_API}")
        await asyncio.gather(self.broadcast_presence(), self.listen_peers())

if __name__ == "__main__":
    node = AegisPeerNode()
    try: asyncio.run(node.start())
    except KeyboardInterrupt: print("\nEncerrado.")
