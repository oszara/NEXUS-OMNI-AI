import ollama
from pathlib import Path

MODEL = "qwen3-coder"  # fallback automático si no está

PROMPT_PATH = Path(__file__).parent / "code_reviewer_prompt.txt"


def revisar_codigo(ruta_archivo):
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        return "Archivo no encontrado."

    codigo = ruta.read_text(encoding="utf-8")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": codigo}
        ],
        options={"num_predict": 2048}
    )

    return response["message"]["content"]
