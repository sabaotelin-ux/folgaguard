"""
Validador semântico do Folgaguard.
"""

import logging
from dataclasses import dataclass

from app.knowledge.base_juridica import FatoJuridico, buscar_por_referencia
from app.detectors.ia_juiz import obter_lista_chaves

logger = logging.getLogger("uvicorn.error")


@dataclass
class AlertaSemantico:
    tipo: str
    severidade: str
    trecho: str
    explicacao: str


def _montar_prompt_lote(itens: list[tuple[FatoJuridico, str]]) -> str:
    partes = [
        "Você é um revisor jurídico extremamente rigoroso. Para cada item "
        "numerado abaixo, compare a AFIRMAÇÃO com o FATO CORRETO e decida "
        "se a afirmação CONTRADIZ o fato (mesmo que parcialmente, inclusive "
        "por omissão ou combinação incorreta de informações) ou está "
        "CONSISTENTE com ele.\n\n"
        "Responda EXATAMENTE no formato abaixo, uma linha por item, "
        "sem texto adicional:\n"
        "1: CONTRADIZ ou CONSISTENTE\n"
        "2: CONTRADIZ ou CONSISTENTE\n"
        "(e assim por diante)\n\n"
    ]

    for i, (fato, frase) in enumerate(itens, start=1):
        partes.append(
            f"--- ITEM {i} ---\n"
            f"FATO CORRETO ({fato.fonte}): {fato.fato_correto}\n"
            f"AFIRMAÇÃO A AVALIAR: {frase}\n\n"
        )

    return "".join(partes)


def _parsear_resposta_lote(resposta: str, total_itens: int) -> dict[int, str]:
    """
    Extrai o veredito de cada item numerado. Corrigido: em vez de usar
    lstrip (que apaga todos os dígitos, não só o prefixo), agora extrai
    só os caracteres numéricos da parte antes dos ":".
    """
    resultados = {}
    for linha in resposta.strip().split("\n"):
        linha = linha.strip()
        if ":" not in linha:
            continue
        numero_str, veredito = linha.split(":", 1)
        digitos = "".join(c for c in numero_str if c.isdigit())
        if not digitos:
            continue
        numero = int(digitos)
        veredito = veredito.strip().upper()
        if veredito.startswith("CONTRADIZ"):
            resultados[numero] = "CONTRADIZ"
        elif veredito.startswith("CONSISTENTE"):
            resultados[numero] = "CONSISTENTE"
    return resultados


def chamar_llm(prompt: str) -> str:
    from google import genai

    chaves = obter_lista_chaves()
    if not chaves:
        logger.error("[validador_semantico] Nenhuma chave de API encontrada")
        return ""

    logger.info(f"[validador_semantico] {len(chaves)} chave(s) disponível(is)")

    for i, chave in enumerate(chaves):
        try:
            cliente = genai.Client(api_key=chave)
            resposta = cliente.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            texto_resposta = resposta.text.strip()
            logger.info(f"[validador_semantico] Sucesso na chave {i+1}")
            logger.info(f"[validador_semantico] RESPOSTA CRUA: {texto_resposta}")
            return texto_resposta
        except Exception as e:
            erro_str = str(e).lower()
            logger.error(f"[validador_semantico] ERRO na chave {i+1}: {type(e).__name__}: {e}")
            if "429" in erro_str or "quota" in erro_str or "503" in erro_str or "unavailable" in erro_str:
                continue
            break

    return ""


def validar(texto: str) -> list[AlertaSemantico]:
    itens = buscar_por_referencia(texto)
    if not itens:
        return []

    prompt = _montar_prompt_lote(itens)
    resposta = chamar_llm(prompt)
    if not resposta:
        return []

    veredictos = _parsear_resposta_lote(resposta, len(itens))

    alertas: list[AlertaSemantico] = []
    for i, (fato, frase) in enumerate(itens, start=1):
        if veredictos.get(i) == "CONTRADIZ":
            alertas.append(
                AlertaSemantico(
                    tipo="ALUCINACAO",
                    severidade="ALTA",
                    trecho=frase,
                    explicacao=(
                        f"A afirmação contradiz o entendimento correto sobre "
                        f"{fato.id}: {fato.fato_correto}"
                    ),
                )
            )

    return alertas


def validar_semanticamente(texto: str) -> list[dict]:
    return [alerta.__dict__ for alerta in validar(texto)]
