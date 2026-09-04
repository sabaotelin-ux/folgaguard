from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os
import json
import hashlib
from app.database import criar_tabelas, get_db, Auditoria
from app.models import AuditRequest
from app.detectors.alucinacao import detectar_alucinacao
from app.detectors.ambiguidade import detectar_ambiguidade
from app.detectors.heuristicas import detectar_folgas
from app.detectors.certeza import detectar_certeza
from app.detectors.juridico import detectar_riscos_juridicos
from app.detectors.ia_juiz import avaliar_com_ia
from app.detectors.motor_hibrido import MotorHibridoAdaptativo
from app.relatorio import gerar_pdf_relatorio

app = FastAPI(title="Folgaguard", version="1.0.0")

PESO = {"ALTA": 15, "MEDIA": 10, "BAIXA": 5}
ORDEM = {"ALTA": 3, "MEDIA": 2, "BAIXA": 1}

motor_hibrido = MotorHibridoAdaptativo()


def verificar_chave(x_api_key: str = Header(default=None)):
    chave = os.environ.get("FOLGAGUARD_API_KEY")
    if chave and x_api_key != chave:
        raise HTTPException(status_code=401, detail="Chave invalida")
    return True


def normalizar(alerta):
    if isinstance(alerta, str):
        return {"tipo": "GERAL", "severidade": "MEDIA", "trecho": alerta, "explicacao": alerta}
    if "severidade" not in alerta:
        alerta["severidade"] = "MEDIA"
    return alerta


def remover_duplicatas(alertas):
    vistos = set()
    unicos = []
    for a in alertas:
        chave = (a.get("tipo"), a.get("trecho"), a.get("explicacao"))
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(a)
    return unicos


def calcular_score(alertas):
    total = sum(PESO.get(a.get("severidade", "BAIXA"), 5) for a in alertas)
    return max(0.0, 100.0 - total)


def agrupar(alertas):
    grupos = {}
    for a in alertas:
        tipo = a.get("tipo", "OUTRO")
        if tipo not in grupos:
            grupos[tipo] = {"tipo": tipo, "severidade": a.get("severidade", "BAIXA"), "ocorrencias": []}
        sev_nova = a.get("severidade", "BAIXA")
        if ORDEM.get(sev_nova, 0) > ORDEM.get(grupos[tipo]["severidade"], 0):
            grupos[tipo]["severidade"] = sev_nova
        grupos[tipo]["ocorrencias"].append({"trecho": a.get("trecho", ""), "explicacao": a.get("explicacao", "")})
    return list(grupos.values())


def parecer(alertas):
    sevs = [a.get("severidade") for a in alertas]
    if "ALTA" in sevs: return "Resposta com risco alto"
    if "MEDIA" in sevs: return "Resposta com riscos moderados"
    if "BAIXA" in sevs: return "Resposta com pequenas ressalvas"
    return "Resposta aparentemente solida"


def gerar_hash(texto, data, score):
    return hashlib.sha256((texto + "|" + data + "|" + str(score)).encode()).hexdigest()


def executar_auditoria(texto, origem, db):
    classificacao = motor_hibrido.auditar_adaptativo(texto)

    todos = (detectar_alucinacao(texto) + detectar_certeza(texto) +
             detectar_riscos_juridicos(texto) + detectar_ambiguidade(texto) +
             detectar_folgas(texto))

    alertas = remover_duplicatas([normalizar(a) for a in todos])
    score = calcular_score(alertas)
    grupos = agrupar(alertas)
    p = parecer(alertas)

    ia = avaliar_com_ia(texto)
    avaliacao = ia.get("observacao") if ia.get("disponivel") else "Avaliacao de IA indisponivel"

    agora = datetime.utcnow()
    hash_val = gerar_hash(texto, agora.isoformat(), score)

    reg = Auditoria(texto=texto, origem=origem, score_confianca=score,
                    folgas_detectadas=json.dumps(grupos), parecer=p,
                    data_hora=agora, hash_integridade=hash_val,
                    avaliacao_ia=avaliacao)
    db.add(reg)
    db.commit()
    db.refresh(reg)

    return {"id": reg.id, "score_confianca": score, "folgas_detectadas": grupos,
            "parecer": p, "avaliacao_ia": avaliacao,
            "classificacao": classificacao,
            "data_hora": reg.data_hora.isoformat(), "hash_integridade": reg.hash_integridade}


def gerar_relatorio_pdf(id, db):
    reg = db.query(Auditoria).filter(Auditoria.id == id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Nao encontrado")
    pdf = gerar_pdf_relatorio([reg])
    return StreamingResponse(pdf, media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename=relatorio_{id}.pdf"})


@app.on_event("startup")
def iniciar_banco():
    criar_tabelas()


@app.get("/")
def root():
    return {"mensagem": "Folgaguard esta rodando!", "status": "online"}


@app.get("/app")
def pagina_web():
    return FileResponse("app/static/index.html", media_type="text/html")


@app.post("/auditar")
def auditar(request: AuditRequest, db: Session = Depends(get_db),
            autorizado: bool = Depends(verificar_chave)):
    return executar_auditoria(request.texto, request.origem or "desconhecida", db)


@app.get("/historico")
def historico(db: Session = Depends(get_db), autorizado: bool = Depends(verificar_chave)):
    regs = db.query(Auditoria).order_by(Auditoria.data_hora.desc()).all()
    return [{"id": r.id, "texto": r.texto[:100] + "..." if len(r.texto) > 100 else r.texto,
             "score": r.score_confianca, "parecer": r.parecer,
             "data": r.data_hora.isoformat(), "hash_integridade": r.hash_integridade}
            for r in regs]


@app.get("/relatorio/{id}")
def relatorio(id: int, db: Session = Depends(get_db), autorizado: bool = Depends(verificar_chave)):
    return gerar_relatorio_pdf(id, db)


@app.post("/web/auditar")
def auditar_web(request: AuditRequest, db: Session = Depends(get_db)):
    return executar_auditoria(request.texto, request.origem or "desconhecida", db)


@app.get("/web/relatorio/{id}")
def relatorio_web(id: int, db: Session = Depends(get_db)):
    return gerar_relatorio_pdf(id, db)
