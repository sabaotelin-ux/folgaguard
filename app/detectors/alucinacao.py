from app.detectors.validador_semantico import validar_semanticamente


class DetectorAlucinacao:
    def __init__(self):
        self.anos_ignorar = [
            '2024', '2025', '2026',
            '2018', '2002', '1990',
            '2015', '1988', '1973',
            '1940', '1996',
        ]

    def detectar(self, texto):
        alertas = []
        import re
        import datetime

        padrao_invalido = re.compile(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{3}')
        for match in padrao_invalido.finditer(texto):
            alertas.append({
                'tipo': 'ALUCINACAO',
                'severidade': 'ALTA',
                'trecho': match.group(),
                'explicacao': f'O número de processo {match.group()} tem formato inválido (faltam dígitos).'
            })

        datas = re.findall(r'\d{2}/\d{2}/\d{4}', texto)
        hoje = datetime.date.today()
        for data_str in datas:
            try:
                dia, mes, ano = map(int, data_str.split('/'))
                data = datetime.date(ano, mes, dia)
                if data > hoje:
                    alertas.append({
                        'tipo': 'ALUCINACAO',
                        'severidade': 'ALTA',
                        'trecho': data_str,
                        'explicacao': f'A data {data_str} está no futuro, mas foi tratada como fato já ocorrido.'
                    })
            except:
                pass

        alertas.extend(validar_semanticamente(texto))

        sumulas = re.findall(r'Súmula (\d+) do (STF|STJ|TST|TRF)', texto)
        for numero, tribunal in sumulas:
            if tribunal == 'STF' and int(numero) > 700:
                alertas.append({
                    'tipo': 'ALUCINACAO',
                    'severidade': 'MEDIA',
                    'trecho': f'Súmula {numero} do {tribunal}',
                    'explicacao': f'Súmula {numero} não existe no STF. Provavelmente é do STJ ou TST.'
                })

        return alertas

    def _pegar_frase(self, texto, termo):
        frases = texto.split('.')
        for frase in frases:
            if termo.lower() in frase.lower():
                return frase.strip()
        return termo


# Função wrapper para compatibilidade com main.py
def detectar_alucinacao(texto: str) -> list:
    detector = DetectorAlucinacao()
    return detector.detectar(texto)
