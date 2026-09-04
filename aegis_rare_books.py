import sqlite3
import sys

DB_NAME = "aegis_unified.db"

def catalog_rare_book(title, author, provenance, details):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rare_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            provenance TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO rare_books (title, author, provenance, details)
        VALUES (?, ?, ?, ?)
    ''', (title, author, provenance, details))
    
    conn.commit()
    conn.close()
    print(f"[Acervo Raro] Obra catalogada com sucesso no SQLite: {title}")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "Livro de Arte Histórico"
    author = sys.argv[2] if len(sys.argv) > 2 else "Autor / Artista Referência"
    provenance = "Aquisição em livraria de sebos / Exemplar autenticado"
    details = "Preserva dedicatória original, colofão e placas gráficas soltas."
    
    catalog_rare_book(title, author, provenance, details)
