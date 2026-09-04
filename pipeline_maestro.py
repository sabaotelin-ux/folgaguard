import os
import asyncio
import sqlite3
import time
import hashlib
import subprocess
from PIL import Image
from ai_generator import LocalAIEngine

DB_NAME = "aegis_unified.db"
ASSET_DIR = "./assets"

class AdvancedMaestro:
    def __init__(self):
        os.makedirs(ASSET_DIR, exist_ok=True)
        self.queue = asyncio.Queue()
        self.ai_engine = LocalAIEngine()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS media_cache (
                    asset_hash TEXT PRIMARY KEY,
                    output_path TEXT,
                    ai_summary TEXT,
                    ai_caption TEXT,
                    created_at REAL
                )
            """)
            conn.commit()

    def check_cache(self, file_hash):
        with sqlite3.connect(DB_NAME) as conn:
            row = conn.execute("SELECT output_path FROM media_cache WHERE asset_hash = ?", (file_hash,)).fetchone()
            return row[0] if row else None

    def save_cache(self, file_hash, out_path, summary, caption):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO media_cache 
                (asset_hash, output_path, ai_summary, ai_caption, created_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (file_hash, out_path, summary, caption, time.time()))
            conn.commit()

    async def worker(self, name):
        while True:
            filename = await self.queue.get()
            try:
                await self.process_file(filename)
            except Exception as e:
                print(f"[{name}] Erro ao processar {filename}: {e}")
            finally:
                self.queue.task_done()

    async def process_file(self, filename):
        path = os.path.join(ASSET_DIR, filename)
        if not os.path.exists(path):
            return

        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        cached_out = self.check_cache(file_hash)
        if cached_out and os.path.exists(cached_out):
            print(f"[Cache Hit] {filename} já processado anteriormente.")
            return

        with Image.open(path) as img:
            width, height = img.size
            img_format = img.format

        asset_meta = {
            "asset_hash": file_hash,
            "dimensions": f"{width}x{height}",
            "format": img_format
        }

        print(f"[Processando] Gerando metadados e renderizando 9:16 para {filename}...")
        ai_data = self.ai_engine.analyze_asset(asset_meta)
        summary = ai_data.get("summary", "")
        caption = ai_data.get("caption", "")

        output_name = f"output_{file_hash[:8]}.mp4"
        
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", path,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-t", "5", "-shortest", "-c:v", "libx264", "-c:a", "aac",
            output_name
        ]
        
        process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await process.communicate()
        
        if process.returncode == 0:
            self.save_cache(file_hash, output_name, summary, caption)
            print(f"[Sucesso] Renderizado e catalogado no SQLite: {output_name}")
            print(f"[IA Summary]: {summary}")

    async def watch_directory(self):
        print(f"[Watchdog] Monitorando diretório {ASSET_DIR} em tempo real...")
        seen = set()
        while True:
            current_files = set(os.listdir(ASSET_DIR))
            new_files = current_files - seen
            for f in new_files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    await self.queue.put(f)
            seen = current_files
            await asyncio.sleep(2)

async def main():
    maestro = AdvancedMaestro()
    workers = [asyncio.create_task(maestro.worker(f"Worker-{i}")) for i in range(2)]
    watcher = asyncio.create_task(maestro.watch_directory())
    await asyncio.gather(watcher, maestro.queue.join())

if __name__ == "__main__":
    asyncio.run(main())
