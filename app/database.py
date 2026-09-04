import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./folgaguard.db")

if "postgres" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Auditoria(Base):
    __tablename__ = "auditorias"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    origem = Column(String, nullable=True)
    score_confianca = Column(Float, nullable=True)
    folgas_detectadas = Column(Text, nullable=True)
    parecer = Column(Text, nullable=True)
    data_hora = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(Integer, nullable=True)
    hash_integridade = Column(String, nullable=True)
    avaliacao_ia = Column(Text, nullable=True)

def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    if "postgres" in DATABASE_URL:
        with engine.connect() as conn:
            try:
                conn.execute(text("ALTER TABLE auditorias ADD COLUMN IF NOT EXISTS avaliacao_ia TEXT"))
                conn.commit()
            except Exception:
                pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
