class DetectorCerteza:
    def detectar(self, texto):
        alertas = []
        palavras = [
            'vedado', 'vedada', 'obrigatório', 'obrigatória',
            'sempre', 'nunca', 'impossível', 'incontroversível',
            'indiscutível', 'sem possibilidade de revisão',
            'em nenhuma hipótese', 'absolutamente', 'totalmente',
            'é certo que', 'não há dúvida', 'inequívoco',
            'é medida inadequada', 'deve prevalecer',
            'desnecessária a comprovação',
            'sem exceção', 'não há possibilidade',
            'em todos os casos', 'definitivamente',
            'certamente', 'é fato que', 'com certeza',
            'não há como', 'é impossível'
        ]

        for palavra in palavras:
            pos = texto.lower().find(palavra.lower())
            if pos != -1:
                # Pega o trecho exato ao redor da palavra
                inicio = max(0, pos - 60)
                fim = min(len(texto), pos + len(palavra) + 60)
                trecho = texto[inicio:fim].strip()
                alertas.append({
                    'tipo': 'CERTEZA_EXCESSIVA',
                    'severidade': 'MEDIA',
                    'trecho': trecho,
                    'explicacao': f'A expressão "{palavra}" expressa certeza absoluta sem ressalvas legais.'
                })
        return alertas


def detectar_certeza(texto: str) -> list:
    detector = DetectorCerteza()
    return detector.detectar(texto)
