from app.detectors.alucinacao import detectar_alucinacao

def test_afirmacao_categorica():
    resultado = detectar_alucinacao("Isso é comprovadamente verdade, sem dúvida alguma.")
    assert len(resultado) > 0

def test_estatistica_sem_fonte():
    resultado = detectar_alucinacao("Cerca de 87% das pessoas concordam com isso.")
    assert any("Estatística" in r for r in resultado)

def test_texto_neutro_sem_riscos():
    resultado = detectar_alucinacao("O relatório apresenta os números do trimestre.")
    assert resultado == []
