import subprocess
import os

MODEL_PATH = os.path.expanduser("~/folgaguard/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf")

def gerar_resposta(prompt: str, max_tokens: int = 100) -> str:
    try:
        resultado = subprocess.run(
            [
                "llama-cli",
                "-m", MODEL_PATH,
                "-p", prompt,
                "-n", str(max_tokens),
                "--no-display-prompt",
                "-q"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        return resultado.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Tempo limite excedido"
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    resposta = gerar_resposta("Olá! Como você pode me ajudar?")
    print(resposta)
