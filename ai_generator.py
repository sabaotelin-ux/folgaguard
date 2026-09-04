import json

class LocalAIEngine:
    def __init__(self):
        pass

    def analyze_asset(self, asset_metadata):
        # Fallback baseado em regras e metadados estruturados
        file_hash = asset_metadata.get("asset_hash", "unknown")[:8]
        dimensions = asset_metadata.get("dimensions", "1080x1920")
        
        summary = f"Obra catalogada via edge-vision [Hash: {file_hash}]. Resolução otimizada para formato vertical ({dimensions})."
        caption = f"✨ Acervo Digital Aegis | Arte e Memória #Shorts #Art #{file_hash}"
        
        return {
            "summary": summary,
            "caption": caption
        }

if __name__ == "__main__":
    ai = LocalAIEngine()
    sample_meta = {"asset_hash": "aedb2882", "dimensions": "1080x1920", "format": "JPEG"}
    print(ai.analyze_asset(sample_meta))
