import re


def detectar_folgas(texto: str) -> list[dict]:
    """
    Retorna alertas com tipo específico, em vez de strings soltas.
    """
    folgas = []
    texto_lower = texto.lower()

    if len(texto) < 50:
        folgas.append({
            "tipo": "ESTRUTURA",
            "severidade": "BAIXA",
            "trecho": texto[:50],
            "explicacao": "Resposta muito curta",
        })

    if "não sei" in texto_lower or "não tenho certeza" in texto_lower:
        folgas.append({
            "tipo": "ESTRUTURA",
            "severidade": "BAIXA",
            "trecho": "não sei / não tenho certeza",
            "explicacao": "Baixa confiança expressa",
        })

    if texto.count(".") < 2 and len(texto) > 100:
        folgas.append({
            "tipo": "ESTRUTURA",
            "severidade": "BAIXA",
            "trecho": texto[:80],
            "explicacao": "Estrutura possivelmente confusa",
        })

    termos_vagos = ["pode ser", "talvez", "em geral"]
    for termo in termos_vagos:
        if re.search(r'\b' + re.escape(termo) + r'\b', texto_lower):
            folgas.append({
                "tipo": "AMBIGUIDADE",
                "severidade": "BAIXA",
                "trecho": termo,
                "explicacao": f"Termo vago detectado: '{termo}'",
            })

    match_lei = re.search(r'\blei\s+(n[°º]?\s*)?\d+[\d./-]*', texto, re.IGNORECASE)
    if match_lei:
        folgas.append({
            "tipo": "FONTE_AUSENTE",
            "severidade": "BAIXA",
            "trecho": match_lei.group().strip(),
            "explicacao": "Lei citada sem referência clara ao código ou lei correspondente",
        })

    match_sumula = re.search(r'\b(súmula|sumula)\s+\d+', texto, re.IGNORECASE)
    if match_sumula:
        folgas.append({
            "tipo": "FONTE_AUSENTE",
            "severidade": "BAIXA",
            "trecho": match_sumula.group().strip(),
            "explicacao": "Menção a jurisprudência/súmula sem fonte ou número verificável",
        })

    match_artigo = re.search(r'\b(art\.|artigo)\s*\d+', texto, re.IGNORECASE)
    if match_artigo:
        folgas.append({
            "tipo": "FONTE_AUSENTE",
            "severidade": "BAIXA",
            "trecho": match_artigo.group().strip(),
            "explicacao": "Artigo citado sem referência clara ao código ou lei correspondente",
        })

    anos = re.finditer(r'(19|20)\d{2}', texto)
    for match in anos:
        inicio = match.start()
        fim = match.end()
        antes = texto[inicio-1] if inicio > 0 else ' '
        depois = texto[fim] if fim < len(texto) else ' '
        if antes not in '0123456789-./' and depois not in '0123456789-./':
            folgas.append({
                "tipo": "FONTE_AUSENTE",
                "severidade": "BAIXA",
                "trecho": match.group(),
                "explicacao": "Data específica citada sem indicação de fonte",
            })
            break

    return folgas


def calcular_score(folgas: list) -> float:
    return max(0.0, 1.0 - (len(folgas) * 0.1))
