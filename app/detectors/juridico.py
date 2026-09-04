import re


class DetectorJuridico:
    def detectar(self, texto):
        alertas = []

        citacoes = re.findall(r'art\.\s*\d+', texto)
        for cit in citacoes:
            if not any(lei in texto for lei in ['Código Civil', 'CLT', 'LGPD', 'CDC', 'CPC']):
                alertas.append({
                    'tipo': 'FONTE_AUSENTE',
                    'severidade': 'MEDIA',
                    'trecho': cit,
                    'explicacao': f'O artigo {cit} foi citado sem indicar qual lei.'
                })

        return alertas


# Função wrapper para compatibilidade com main.py
def detectar_riscos_juridicos(texto: str) -> list:
    detector = DetectorJuridico()
    return detector.detectar(texto)
