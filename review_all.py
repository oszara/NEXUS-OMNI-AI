"""
review_all.py
=============
Script de revisión automática de código con Ollama + qwen3-coder.

Detecta los archivos Python modificados en el PR actual (vía git diff),
los envía al modelo local de Ollama para revisión y muestra el análisis
en el log de la pipeline.  Si la variable GITHUB_TOKEN está disponible,
también publica el resultado como comentario en el PR.

Uso:
    python review_all.py
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Dirección del servidor Ollama (iniciado por el workflow)
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Modelo a utilizar para la revisión
MODELO = "qwen3-coder"

# Instrucciones del sistema para el modelo
PROMPT_SISTEMA = (
    "Eres un experto revisor de código Python. Analiza el siguiente código "
    "o diff y proporciona una revisión concisa en español con:\n"
    "1. Problemas críticos (bugs, seguridad, rendimiento)\n"
    "2. Mejoras de estilo y legibilidad\n"
    "3. Sugerencias de buenas prácticas\n"
    "Sé breve y directo. Máximo 300 palabras por archivo."
)

# Extensiones consideradas código Python
EXTENSIONES_PYTHON = {".py"}

# Límite de caracteres de contexto enviado al modelo por archivo
MAX_CHARS_CONTEXTO = 4000


# ---------------------------------------------------------------------------
# Obtención de archivos modificados
# ---------------------------------------------------------------------------


def _obtener_archivos_cambiados() -> list:
    """Retorna la lista de archivos Python modificados en el commit actual.

    Intenta primero HEAD^ vs HEAD; si falla (primer commit), usa
    origin/main vs HEAD como base de comparación.

    Returns:
        Lista de rutas de archivos Python existentes con cambios.
    """
    for cmd in (
        ["git", "diff", "--name-only", "HEAD^", "HEAD"],
        ["git", "diff", "--name-only", "origin/main", "HEAD"],
    ):
        try:
            resultado = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            archivos = resultado.stdout.splitlines()
            return [
                a
                for a in archivos
                if os.path.splitext(a)[1] in EXTENSIONES_PYTHON
                and os.path.isfile(a)
            ]
        except subprocess.CalledProcessError:
            continue

    print("[AVISO] No se pudieron obtener los archivos cambiados.")
    return []


def _leer_diff_archivo(ruta: str) -> str:
    """Retorna el diff del archivo; si no hay diff, retorna el contenido completo.

    Args:
        ruta: Ruta relativa al archivo Python.

    Returns:
        Texto del diff o contenido del archivo como cadena.
    """
    for cmd in (
        ["git", "diff", "HEAD^", "HEAD", "--", ruta],
        ["git", "diff", "origin/main", "HEAD", "--", ruta],
    ):
        try:
            resultado = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            diff = resultado.stdout.strip()
            if diff:
                return diff
        except subprocess.CalledProcessError:
            continue

    # Fallback: contenido completo del archivo
    try:
        with open(ruta, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


# ---------------------------------------------------------------------------
# Revisión con Ollama
# ---------------------------------------------------------------------------


def _revisar_con_ollama(nombre: str, contenido: str) -> str:
    """Envía el contenido/diff al modelo Ollama y retorna la revisión.

    Args:
        nombre: Nombre del archivo (usado en el prompt).
        contenido: Texto del diff o código a revisar.

    Returns:
        Revisión generada por el modelo como cadena de texto.
    """
    prompt = (
        f"{PROMPT_SISTEMA}\n\n"
        f"Archivo: {nombre}\n\n"
        f"```python\n{contenido[:MAX_CHARS_CONTEXTO]}\n```"
    )
    payload = json.dumps(
        {"model": MODELO, "prompt": prompt, "stream": False}
    ).encode()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            datos = json.loads(resp.read().decode())
            return datos.get("response", "").strip()
    except urllib.error.URLError as exc:
        return f"[ERROR] No se pudo conectar con Ollama: {exc}"
    except (json.JSONDecodeError, KeyError) as exc:
        return f"[ERROR] Respuesta inesperada de Ollama: {exc}"


# ---------------------------------------------------------------------------
# Publicar comentario en el PR
# ---------------------------------------------------------------------------


def _publicar_comentario_pr(cuerpo: str) -> None:
    """Publica el resultado como comentario en el PR usando la GitHub API.

    Solo actúa si las variables GITHUB_TOKEN, GITHUB_EVENT_PATH y
    GITHUB_REPOSITORY están definidas en el entorno.

    Args:
        cuerpo: Texto en Markdown del comentario a publicar.
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    evento_path = os.environ.get("GITHUB_EVENT_PATH", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not (token and evento_path and repo):
        return

    try:
        with open(evento_path, "r", encoding="utf-8") as fh:
            evento = json.load(fh)
        pr_number = evento.get("pull_request", {}).get("number")
        if not pr_number:
            return
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[AVISO] No se pudo leer el evento del PR: {exc}")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = json.dumps({"body": cuerpo}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 201:
                print("[NEXUS] Comentario publicado en el PR.")
    except urllib.error.URLError as exc:
        print(f"[AVISO] No se pudo publicar el comentario en el PR: {exc}")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main() -> int:
    """Función principal: revisa todos los archivos Python cambiados.

    Returns:
        Código de salida (0 = éxito).
    """
    print("=" * 60)
    print("  NEXUS Review — Revisión IA con Ollama + qwen3-coder")
    print("=" * 60)

    archivos = _obtener_archivos_cambiados()

    if not archivos:
        print("[INFO] No hay archivos Python modificados para revisar.")
        return 0

    print(f"[INFO] Archivos Python modificados: {', '.join(archivos)}\n")

    secciones = ["## 🤖 NEXUS Review — Revisión IA (qwen3-coder)\n"]

    for ruta in archivos:
        print(f"[NEXUS] Revisando: {ruta} ...")
        contenido = _leer_diff_archivo(ruta)
        if not contenido:
            print(f"  → Sin cambios detectables en {ruta}\n")
            continue

        revision = _revisar_con_ollama(ruta, contenido)
        print(f"  → Revisión de {ruta}:\n{revision}\n")
        secciones.append(f"### `{ruta}`\n\n{revision}\n")

    if len(secciones) > 1:
        _publicar_comentario_pr("\n".join(secciones))

    return 0


if __name__ == "__main__":
    sys.exit(main())
