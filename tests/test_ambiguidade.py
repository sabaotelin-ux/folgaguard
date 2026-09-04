from app.detectors.ambiguidade import detectar_ambiguidade

def test_detecta_termo_vago():
    resultado = detectar_ambiguidade("Talvez isso funcione, depende do contexto.")
    assert len(resultado) > 0

def test_texto_sem_ambiguidade():
    resultado = detectar_ambiguidade("O motor converte energia térmica em mecânica.")
    assert resultado == []

def test_multiplas_alternativas():
    texto = "Pode ser A ou B ou C ou D, não está claro."
    resultado = detectar_ambiguidade(texto)
    assert any("Múltiplas alternativas" in r for r in resultado)
