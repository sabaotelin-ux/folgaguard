from app.detectors.heuristicas import detectar_folgas, calcular_score

def test_texto_curto_detecta_folga():
    resultado = detectar_folgas("Oi, tudo bem?")
    assert "Resposta muito curta" in resultado

def test_texto_com_baixa_confianca():
    texto = "Não sei ao certo, mas acho que pode funcionar dessa forma aqui."
    resultado = detectar_folgas(texto)
    assert any("Baixa confiança" in f for f in resultado)

def test_texto_solido_sem_folgas():
    texto = "O sistema processa os dados corretamente. Ele valida cada entrada. Depois retorna o resultado final."
    resultado = detectar_folgas(texto)
    assert resultado == []

def test_calcular_score_sem_folgas():
    assert calcular_score([]) == 1.0

def test_calcular_score_com_folgas():
    assert calcular_score(["folga1", "folga2"]) == 0.6
