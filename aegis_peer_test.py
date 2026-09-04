import asyncio, socket, json, time, hmac, hashlib
from aiohttp import web

PORT_DISCOVERY, PORT_API = 50005, 50007
SECRET_KEY = b"aegis_secure_swarm_key_2026"

async def broadcast():
    while True:
        try:
            data = {"node_id": "node_secundario", "api_port": PORT_API, "time": time.time()}
            raw_data = json.dumps(data).encode()
            sig = hmac.new(SECRET_KEY, raw_data, hashlib.sha256).hexdigest()
            payload = json.dumps({"data": data, "sig": sig}).encode()
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(payload, ('255.255.255.255', PORT_DISCOVERY))
        except: pass
        await asyncio.sleep(5)

async def fetch_handler(request):
    return web.json_response({"response": "Dado recuperado via Swarm P2P Blindado com sucesso!"})

async def main():
    app = web.Application()
    app.router.add_get("/fetch/{hash}", fetch_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT_API)
    await site.start()
    print("[Peer 2 Blindado] Rodando na porta 50007 com HMAC...")
    await broadcast()

if __name__ == "__main__":
    asyncio.run(main())
