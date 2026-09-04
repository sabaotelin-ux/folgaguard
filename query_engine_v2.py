def query_llm_engine(prompt: str, motor=None, permite_groq: bool = False):
    inicio = time.time()

    if motor is None:
        engine_priority = ["local_qwen"] + (["groq"] if permite_groq else [])
    elif isinstance(motor, list):
        engine_priority = motor
    else:
        engine_priority = [motor]

    ultimo_erro = None
    for nome_motor in engine_priority:
        try:
            if nome_motor == "groq":
                resposta = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                texto = resposta.choices[0].message.content
                fonte = "groq"
            else:
                texto = generate_local_response(prompt)
                fonte = "local_qwen"

            latencia_ms = (time.time() - inicio) * 1000
            return {"resposta": texto, "source": fonte, "latency_ms": latencia_ms}
        except Exception as e:
            ultimo_erro = e
            continue

    latencia_ms = (time.time() - inicio) * 1000
    return {"resposta": f"Erro ao consultar motores: {ultimo_erro}", "source": "erro", "latency_ms": latencia_ms}
