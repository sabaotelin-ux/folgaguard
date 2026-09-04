from typing import Dict, Any


class MotorHibridoAdaptativo:
    def __init__(self):
        self.nlp = None  # análise sintática local desativada por enquanto (spacy não instalado)

        self.bases_conhecimento = {
            "trabalhista": {"peso": 1.2, "termos": ["clt", "jornada", "salário", "rescisão", "aviso prévio", "hora extra", "férias", "folga"]},
            "civil": {"peso": 1.0, "termos": ["contrato", "danos morais", "responsabilidade civil", "obrigação", "posse", "propriedade"]},
            "criminal": {"peso": 1.5, "termos": ["crime", "pena", "dolo", "culpa", "código penal", "infração", "denúncia"]},
            "tributario": {"peso": 1.3, "termos": ["imposto", "tributo", "fisco", "alíquota", "isenção", "receita federal", "ctn"]},
            "administrativo": {"peso": 1.1, "termos": ["licitação", "servidor público", "ato administrativo", "improbidade", "concessão"]},
            "constitucional": {"peso": 1.4, "termos": ["constituição", "stf", "direitos fundamentais", "habeas corpus", "inconstitucionalidade"]},
            "ambiental_agro": {"peso": 1.2, "termos": ["licenciamento ambiental", "agrotóxico", "ibama", "reserva legal", "código florestal"]},
            "empresarial_industrial": {"peso": 1.2, "termos": ["norma regulamentadora", "falência", "recuperação judicial", "sociedade", "propriedade industrial"]},
            "medica_sanitaria": {"peso": 1.3, "termos": ["responsabilidade médica", "erro médico", "vigilância sanitária", "cfm", "prontuário"]}
        }

    def classificar_dominio(self, texto: str) -> str:
        texto_lower = texto.lower()
        pontuacoes = {}
        for dominio, dados in self.bases_conhecimento.items():
            matches = sum(1 for termo in dados["termos"] if termo in texto_lower)
            pontuacoes[dominio] = matches * dados["peso"]

        dominio_vencedor = max(pontuacoes, key=pontuacoes.get)
        return dominio_vencedor if pontuacoes[dominio_vencedor] > 0 else "geral"

    def analisar_complexidade(self, texto: str) -> str:
        if len(texto) < 300:
            return "simples"
        if len(texto) < 1200:
            return "medio"
        return "complexo"

    def auditar_adaptativo(self, texto: str) -> Dict[str, Any]:
        dominio = self.classificar_dominio(texto)
        perfil = self.analisar_complexidade(texto)

        if perfil == "simples":
            estrategia = "regras_deterministicas_locais"
        elif perfil == "medio":
            estrategia = "ia_leve_e_rag_local"
        else:
            estrategia = "pipeline_completo_com_fallback"

        return {
            "dominio_detectado": dominio,
            "nivel_complexidade": perfil,
            "estrategia_utilizada": estrategia,
            "diretriz_base": f"app/knowledge/base_juridica.py -> {dominio}"
        }
