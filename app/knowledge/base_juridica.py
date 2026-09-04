"""
Base de conhecimento jurídico do Folgaguard.

ATENÇÃO: as entradas abaixo foram redigidas com base em conhecimento
geral e devem ser revisadas por um profissional do Direito antes de
uso em produção com clientes reais. Um erro aqui faz o sistema
"corrigir" o usuário com informação incorreta — pior do que não
detectar nada.
"""

import re
from dataclasses import dataclass


@dataclass
class FatoJuridico:
    id: str
    padroes: list[str]
    fato_correto: str
    fonte: str
    categoria: str


BASE_JURIDICA: list[FatoJuridico] = [

    # ---------- CÓDIGO CIVIL ----------
    FatoJuridico(
        id="cc_art_389",
        padroes=[r"art\.?\s*389\b"],
        fato_correto=(
            "O art. 389 do CC trata das consequências gerais do "
            "inadimplemento (perdas e danos, juros, correção monetária "
            "e honorários advocatícios) — não estabelece, por si só, "
            "nenhum percentual de multa."
        ),
        fonte="Código Civil, art. 389",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_393",
        padroes=[r"art\.?\s*393\b"],
        fato_correto=(
            "O art. 393 trata de caso fortuito e força maior como "
            "excludentes de responsabilidade — não se aplica a "
            "inadimplemento voluntário ou a cláusulas contratuais em geral."
        ),
        fonte="Código Civil, art. 393",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_412",
        padroes=[r"art\.?\s*412\b"],
        fato_correto=(
            "O limite de 50% da cláusula penal (art. 412) incide sobre "
            "o valor da obrigação principal, não sobre o valor total do "
            "contrato. A exigência de comprovação de prejuízo para a "
            "cláusula penal moratória está no art. 416, não no art. 412."
        ),
        fonte="Código Civil, art. 412",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_413",
        padroes=[r"art\.?\s*413\b"],
        fato_correto=(
            "O art. 413 autoriza expressamente a redução judicial da "
            "cláusula penal quando manifestamente excessiva, ou se o "
            "cumprimento da obrigação foi parcial. Ou seja, cláusula "
            "penal não é imune à revisão judicial."
        ),
        fonte="Código Civil, art. 413",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_416",
        padroes=[r"art\.?\s*416\b"],
        fato_correto=(
            "A cláusula penal moratória exige comprovação de prejuízo "
            "quando estipulada para esse fim específico — não é automática."
        ),
        fonte="Código Civil, art. 416",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_421",
        padroes=[r"art\.?\s*421\b"],
        fato_correto=(
            "O art. 421 trata da função social do contrato como limite "
            "à liberdade contratual — não afirma que a autonomia da "
            "vontade é absoluta ou inquestionável; pelo contrário, "
            "relativiza essa liberdade."
        ),
        fonte="Código Civil, art. 421",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_478_479",
        padroes=[r"art\.?\s*47[89]\b"],
        fato_correto=(
            "Os arts. 478/479 tratam da teoria da imprevisão (resolução "
            "ou revisão de contrato por onerosidade excessiva decorrente "
            "de acontecimentos extraordinários e imprevisíveis) — exigem "
            "requisitos específicos, não bastando qualquer dificuldade "
            "financeira da parte."
        ),
        fonte="Código Civil, arts. 478-479",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_927",
        padroes=[r"art\.?\s*927\b"],
        fato_correto=(
            "O art. 927 estabelece o dever geral de reparar o dano "
            "causado por ato ilícito. A responsabilidade objetiva "
            "(independente de culpa) só se aplica nas hipóteses "
            "específicas previstas em lei ou quando a atividade "
            "implicar risco para terceiros — não é regra geral."
        ),
        fonte="Código Civil, art. 927",
        categoria="codigo_civil",
    ),
    FatoJuridico(
        id="cc_art_944",
        padroes=[r"art\.?\s*944\b"],
        fato_correto=(
            "O art. 944 estabelece que a indenização se mede pela "
            "extensão do dano — não autoriza indenização punitiva "
            "genérica nem valores arbitrários desvinculados do prejuízo."
        ),
        fonte="Código Civil, art. 944",
        categoria="codigo_civil",
    ),

    # ---------- CLT ----------
    FatoJuridico(
        id="clt_art_482",
        padroes=[r"art\.?\s*482\b"],
        fato_correto=(
            "O art. 482 da CLT trata das hipóteses de justa causa para "
            "dispensa do empregado em relação de emprego — não se aplica "
            "a contratos civis entre partes sem vínculo empregatício."
        ),
        fonte="CLT, art. 482",
        categoria="trabalhista",
    ),
    FatoJuridico(
        id="clt_art_477",
        padroes=[r"art\.?\s*477\b"],
        fato_correto=(
            "O art. 477 da CLT trata do pagamento de verbas rescisórias "
            "e seu prazo — não trata de multa contratual civil nem se "
            "aplica fora da relação de emprego."
        ),
        fonte="CLT, art. 477",
        categoria="trabalhista",
    ),

    # ---------- CDC ----------
    FatoJuridico(
        id="cdc_art_6",
        padroes=[r"art\.?\s*6\b.{0,60}(cdc|consumidor)"],
        fato_correto=(
            "O art. 6º do CDC lista direitos básicos do consumidor "
            "(informação, proteção contra publicidade enganosa, "
            "facilitação de defesa em juízo, entre outros) — não cria, "
            "por si só, direito a indenização automática em qualquer "
            "situação de insatisfação do consumidor."
        ),
        fonte="CDC, art. 6º",
        categoria="consumidor",
    ),
    FatoJuridico(
        id="cdc_art_39",
        padroes=[r"art\.?\s*39\b.{0,60}(cdc|consumidor)"],
        fato_correto=(
            "O art. 39 do CDC lista práticas abusivas vedadas ao "
            "fornecedor — a vedação é específica às condutas listadas, "
            "não uma proibição genérica de qualquer prática comercial."
        ),
        fonte="CDC, art. 39",
        categoria="consumidor",
    ),

    # ---------- LGPD ----------
    FatoJuridico(
        id="lgpd_art_7",
        padroes=[r"art\.?\s*7[º°]?\b.{0,80}(lgpd|dados pessoais)"],
        fato_correto=(
            "O art. 7º da LGPD lista DEZ hipóteses que autorizam o "
            "tratamento de dados pessoais (consentimento é apenas uma "
            "delas) — não é correto afirmar que o tratamento só pode "
            "ocorrer mediante consentimento."
        ),
        fonte="LGPD, art. 7º",
        categoria="lgpd",
    ),
    FatoJuridico(
        id="lgpd_art_11",
        padroes=[r"art\.?\s*11\b.{0,80}(lgpd|dados sens[ií]veis)"],
        fato_correto=(
            "O art. 11 da LGPD trata do tratamento de dados sensíveis, "
            "com hipóteses próprias (não apenas consentimento) — "
            "diferente do regime geral do art. 7º."
        ),
        fonte="LGPD, art. 11",
        categoria="lgpd",
    ),
    FatoJuridico(
        id="lgpd_art_33",
        padroes=[
            r"art\.?\s*33\b",
            r"lgpd|lei\s*geral\s*de\s*prote[cç][aã]o\s*de\s*dados|13\.?709",
        ],
        fato_correto=(
            "A transferência internacional de dados não é simplesmente "
            "vedada — é condicionada ao cumprimento de requisitos "
            "específicos previstos na LGPD."
        ),
        fonte="LGPD, art. 33",
        categoria="lgpd",
    ),

    # ---------- ARBITRAGEM ----------
    FatoJuridico(
        id="lei_arbitragem_art_22",
        padroes=[
            r"art\.?\s*22\b",
            r"9\.?307\s*/\s*96|lei\s*(n[ºo]?\.?\s*)?9\.?307",
        ],
        fato_correto=(
            "O art. 22 da Lei de Arbitragem (Lei 9.307/96) trata da "
            "nomeação de árbitros, não de dispensa de formalidades para "
            "comunicações ou notificações entre as partes."
        ),
        fonte="Lei 9.307/96, art. 22",
        categoria="arbitragem",
    ),
    FatoJuridico(
        id="lei_arbitragem_art_32_33",
        padroes=[r"art\.?\s*3[23]\b.{0,80}(arbitragem|9\.?307)"],
        fato_correto=(
            "A sentença arbitral admite controle judicial em hipóteses "
            "específicas de nulidade (arts. 32/33 da Lei 9.307/96) — "
            "não é correto afirmar que não cabe nenhum controle judicial "
            "sobre ela."
        ),
        fonte="Lei 9.307/96, arts. 32-33",
        categoria="arbitragem",
    ),
]


def _dividir_em_frases(texto: str) -> list[str]:
    marcador = "\x00"
    protegido = re.sub(
        r'\b(art|arts)\.',
        lambda m: m.group(0).replace('.', marcador),
        texto,
        flags=re.IGNORECASE,
    )
    frases = re.split(r"(?<=[.!?])\s+", protegido)
    return [f.replace(marcador, '.') for f in frases]


def buscar_por_referencia(texto: str) -> list[tuple]:
    resultados = []
    for frase in _dividir_em_frases(texto):
        frase_lower = frase.lower()
        for fato in BASE_JURIDICA:
            if all(re.search(padrao, frase_lower) for padrao in fato.padroes):
                resultados.append((fato, frase.strip()))
    return resultados
