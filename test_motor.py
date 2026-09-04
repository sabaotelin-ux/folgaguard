from app.detectors.motor_hibrido import MotorHibridoAdaptativo

def testar_motor():
    motor = MotorHibridoAdaptativo()

    textos_teste = [
        "A empresa demitiu o funcionário sem pagar o aviso prévio e as horas extras da jornada.",
        "O contrato de compra e venda gerou danos morais e materiais por inadimplemento contratual.",
        "O réu foi acusado de cometer crime de furto qualificado com dolo, conforme o código penal.",
        "A autuação fiscal aplicou uma multa indevida com base na alíquota do imposto sem respeitar o CTN."
    ]

    print("--- INICIANDO TESTES DO MOTOR HÍBRIDO ADAPTATIVO ---\n")
    for i, texto in enumerate(textos_teste, 1):
        resultado = motor.auditar_adaptativo(texto)
        print(f"Teste {i}:")
        print(f"  Texto: {texto[:50]}...")
        print(f"  Domínio: {resultado['dominio_detectado']}")
        print(f"  Complexidade: {resultado['nivel_complexidade']}")
        print(f"  Estratégia: {resultado['estrategia_utilizada']}")
        print("-" * 50)

if __name__ == "__main__":
    testar_motor()
