def query_llm_engine(prompt: str, motor: str = "groq"):
    inicio = time.time()
    try:
        if motor == "groq":
            resposta = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            texto = resposta.choices[0].message.content
            fonte = "groq"
        else:
            texto = generate_local_response(prompt)
            fonte = "local_qwen"
    except Exception as e:
        texto = f"Erro ao consultar motor: {e}"
        fonte = "erro"

    latencia_ms = (time.time() - inicio) * 1000
    return {"resposta": texto, "source": fonte, "latency_ms": latencia_ms}

