import re

def detectar_riscos_legislacao(texto):
    alertas = []
    
    # Detecta menção a "artigo" sem especificar a lei (ex: "conforme o artigo 42")
    padrao_artigo_solto = re.findall(r"(?:artigo|art\.)\s*º?\s*\d+", texto, re.IGNORECASE)
    if padrao_artigo_solto and not any(lei in texto.lower() for lei in ["código", "constituição", "clt", "cpc", "cpp", "lei"]):
        alertas.append({
            "tipo": "LEGISLACAO_INCOMPLETA",
            "severidade": "MEDIA",
            "trecho": padrao_artigo_solto[0],
            "explicacao": "Menção a artigo sem especificar o diploma legal correspondente."
        })

    return alertas
