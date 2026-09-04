import re


class DetectorAmbiguidade:
    def detectar(self, texto):
        alertas = []
        texto_lower = texto.lower()

        termos = [
            'prazo razoável', 'tempo hábil',
            'em breve', 'assim que possível', 'oportunamente'
        ]

        for termo in termos:
            if termo.lower() in texto_lower:
                alertas.append({
                    'tipo': 'AMBIGUIDADE',
                    'severidade': 'BAIXA',
                    'trecho': self._pegar_frase(texto, termo),
                    'explicacao': f'O termo "{termo}" é vago e pode gerar ambiguidade jurídica.'
                })

        if re.search(r'\bdepende\b', texto_lower):
            alertas.append({
                'tipo': 'AMBIGUIDADE',
                'severidade': 'BAIXA',
                'trecho': 'depende',
                'explicacao': 'O termo "depende" é vago e pode gerar ambiguidade jurídica.'
            })

        ocorrencias_ou = re.findall(r'\bou\b', texto_lower)
        if len(ocorrencias_ou) >= 3:
            alertas.append({
                'tipo': 'AMBIGUIDADE',
                'severidade': 'MEDIA',
                'trecho': f'{len(ocorrencias_ou)} ocorrências do conectivo "ou"',
                'explicacao': 'Múltiplas alternativas apresentadas sem definição clara.'
            })

        return alertas

    def _pegar_frase(self, texto, termo):
        frases = texto.split('.')
        for frase in frases:
            if termo.lower() in frase.lower():
                return frase.strip()
        return termo


def detectar_ambiguidade(texto: str) -> list:
    detector = DetectorAmbiguidade()
    return detector.detectar(texto)
