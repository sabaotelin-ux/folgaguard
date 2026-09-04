import os
import json
import hashlib
from PIL import Image

class EdgeVisionScanner:
    def __init__(self, target_dir="./assets"):
        self.target_dir = target_dir
        os.makedirs(self.target_dir, exist_ok=True)

    def process_image(self, filename):
        path = os.path.join(self.target_dir, filename)
        if not os.path.exists(path):
            return {"error": "Imagem não localizada no diretório edge."}
        
        with Image.open(path) as img:
            width, height = img.size
            img_format = img.format
            
            with open(path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

        return {
            "asset_hash": file_hash,
            "dimensions": f"{width}x{height}",
            "format": img_format,
            "status": "ready_for_pipeline"
        }
