import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


class GeradorRelatorio:
    def __init__(self):
        self.severidades = {
            'ALUCINACAO': 'ALTA',
            'CONTRADICAO': 'MEDIA',
            'CERTEZA_EXCESSIVA': 'MEDIA',
            'FONTE_AUSENTE': 'BAIXA',
            'AMBIGUIDADE': 'BAIXA',
        }
        self.pesos = {'ALTA': 5, 'MEDIA': 3, 'BAIXA': 1}

    def gerar(self, alertas, texto):
        for alerta in alertas:
            alerta['severidade'] = self.severidades.get(alerta['tipo'], 'BAIXA')
        score = self._calcular_score(alertas)
        return {
            'alertas': alertas,
            'score': score,
            'total_alertas': len(alertas),
            'contagem': self._contar_por_severidade(alertas),
        }

    def _calcular_score(self, alertas):
        score = 100
        for alerta in alertas:
            score -= self.pesos.get(alerta.get('severidade', 'BAIXA'), 1)
        return max(0, score)

    def _contar_por_severidade(self, alertas):
        contagem = {'ALTA': 0, 'MEDIA': 0, 'BAIXA': 0}
        for alerta in alertas:
            sev = alerta.get('severidade', 'BAIXA')
            if sev in contagem:
                contagem[sev] += 1
        return contagem


COR_ALTA = HexColor("#c0392b")
COR_MEDIA = HexColor("#d68910")
COR_BAIXA = HexColor("#2471a3")
COR_TITULO = HexColor("#1a3c6e")
COR_TEXTO = HexColor("#222222")


def _cor_severidade(sev):
    return {"ALTA": COR_ALTA, "MEDIA": COR_MEDIA, "BAIXA": COR_BAIXA}.get(sev, COR_TEXTO)


def _cor_score(score):
    if score >= 80:
        return HexColor("#1e8449")
    if score >= 50:
        return COR_MEDIA
    return COR_ALTA


def gerar_pdf_relatorio(registros) -> io.BytesIO:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    margem = 2 * cm
    y = altura - margem

    for reg in registros:
        # Cabeçalho com faixa colorida
        c.setFillColor(COR_TITULO)
        c.rect(0, y - 0.3 * cm, largura, 1.4 * cm, fill=True, stroke=False)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margem, y, "🛡 Folgaguard — Relatório de Auditoria")
        y -= 1.6 * cm

        c.setFillColor(COR_TEXTO)
        c.setFont("Helvetica", 10)
        c.drawString(margem, y, f"ID: {reg.id}    Origem: {reg.origem}")
        y -= 0.6 * cm
        c.drawString(margem, y, f"Data: {reg.data_hora.isoformat()}")
        y -= 0.6 * cm

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(_cor_score(reg.score_confianca))
        c.drawString(margem, y, f"Score de confiança: {reg.score_confianca}")
        y -= 0.6 * cm

        c.setFillColor(COR_TEXTO)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margem, y, f"Parecer: {reg.parecer}")
        y -= 0.6 * cm

        c.setFont("Helvetica", 8)
        c.drawString(margem, y, f"Hash de integridade: {reg.hash_integridade}")
        y -= 1 * cm

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(COR_TITULO)
        c.drawString(margem, y, "Texto auditado:")
        y -= 0.6 * cm
        c.setFont("Helvetica", 9)
        c.setFillColor(COR_TEXTO)
        for linha in _quebrar_texto(reg.texto, 95):
            if y < margem:
                c.showPage()
                y = altura - margem
            c.drawString(margem, y, linha)
            y -= 0.5 * cm

        y -= 0.5 * cm
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(COR_TITULO)
        if y < margem:
            c.showPage()
            y = altura - margem
        c.drawString(margem, y, "Riscos detectados:")
        y -= 0.7 * cm

        try:
            grupos = json.loads(reg.folgas_detectadas)
        except (TypeError, ValueError):
            grupos = []

        for grupo in grupos:
            sev = grupo.get('severidade', 'BAIXA')
            cor = _cor_severidade(sev)
            if y < margem:
                c.showPage()
                y = altura - margem

            # Barra colorida de destaque à esquerda do grupo de risco
            c.setFillColor(cor)
            c.rect(margem - 0.3 * cm, y - 0.1 * cm, 0.15 * cm, 0.5 * cm, fill=True, stroke=False)

            c.setFont("Helvetica-Bold", 10)
            c.drawString(margem, y, f"{grupo.get('tipo', '')}  [{sev}]")
            y -= 0.55 * cm
            c.setFont("Helvetica", 9)
            c.setFillColor(COR_TEXTO)
            for ocorrencia in grupo.get("ocorrencias", []):
                if y < margem:
                    c.showPage()
                    y = altura - margem
                trecho = f'  "{ocorrencia.get("trecho", "")}"'
                for linha in _quebrar_texto(trecho, 95):
                    c.drawString(margem + 0.4 * cm, y, linha)
                    y -= 0.45 * cm
            y -= 0.3 * cm

        c.showPage()
        y = altura - margem

    c.save()
    buffer.seek(0)
    return buffer


def _quebrar_texto(texto, largura_maxima):
    palavras = texto.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 <= largura_maxima:
            linha_atual = f"{linha_atual} {palavra}".strip()
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas
