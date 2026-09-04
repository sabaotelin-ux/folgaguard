import sqlite3
import math
import re

DB_NAME = "aegis_unified.db"

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def get_vector(text, vocabulary):
    tokens = tokenize(text)
    return [tokens.count(word) for word in vocabulary]

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in v1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in v2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def semantic_search(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    rows = cursor.execute("SELECT asset_hash, ai_summary, ai_caption FROM media_cache").fetchall()
    conn.close()

    if not rows:
        print("[Busca Semântica] Nenhum registro encontrado no acervo.")
        return

    documents = []
    for asset_hash, summary, caption in rows:
        content = f"{summary or ''} {caption or ''}"
        documents.append((asset_hash, content))

    corpus_texts = [doc[1] for doc in documents] + [query]
    vocabulary = list(set(word for text in corpus_texts for word in tokenize(text)))

    query_vector = get_vector(query, vocabulary)
    
    results = []
    for asset_hash, content in documents:
        doc_vector = get_vector(content, vocabulary)
        score = cosine_similarity(query_vector, doc_vector)
        if score > 0.0:
            results.append((score, asset_hash, content))

    results.sort(key=lambda x: x[0], reverse=True)

    print(f"\n[Resultados para a busca: '{query}']")
    for score, asset_hash, content in results:
        print(f"- Hash: {asset_hash[:12]}... | Similaridade: {score:.2f} | Conteúdo: {content}")

if __name__ == "__main__":
    import sys
    query_term = sys.argv[1] if len(sys.argv) > 1 else "arte"
    semantic_search(query_term)
