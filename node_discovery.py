import asyncio
import json
import socket
import time

PORT = 50005
BROADCAST_INTERVAL = 5
NODE_ID = f"node_{socket.gethostname()}"

class SwarmDiscovery:
    def __init__(self, port=PORT):
        self.port = port
        self.peers = {}

    async def broadcast_presence(self):
        loop = asyncio.get_running_loop()
        while True:
            try:
                payload = json.dumps({"node_id": NODE_ID, "timestamp": time.time()}).encode('utf-8')
                await loop.run_in_executor(None, self._send_udp_broadcast, payload)
            except Exception:
                pass
            await asyncio.sleep(BROADCAST_INTERVAL)

    def _send_udp_broadcast(self, payload):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(payload, ('255.255.255.255', self.port))

    async def listen_for_peers(self):
        class ServerProtocol(asyncio.DatagramProtocol):
            def __init__(self, outer):
                self.outer = outer
            def datagram_received(self, data, addr):
                try:
                    message = json.loads(data.decode('utf-8'))
                    peer_id = message.get("node_id")
                    if peer_id and peer_id != NODE_ID:
                        self.outer.peers[peer_id] = {"ip": addr[0], "last_seen": time.time()}
                except Exception:
                    pass

        loop = asyncio.get_running_loop()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass
        sock.bind(('0.0.0.0', self.port))
        sock.setblocking(False)

        transport, _ = await loop.create_datagram_endpoint(
            lambda: ServerProtocol(self),
            sock=sock
        )
        try:
            while True:
                current_time = time.time()
                inactive = [pid for pid, info in self.peers.items() if current_time - info['last_seen'] > 15]
                for pid in inactive:
                    del self.peers[pid]
                await asyncio.sleep(5)
        finally:
            transport.close()

    async def start(self):
        print(f"[{NODE_ID}] Iniciando descoberta na porta {self.port}...")
        await asyncio.gather(self.broadcast_presence(), self.listen_for_peers())

if __name__ == "__main__":
    discovery = SwarmDiscovery()
    try:
        asyncio.run(discovery.start())
    except KeyboardInterrupt:
        print(f"\n[{NODE_ID}] Encerrado.")
