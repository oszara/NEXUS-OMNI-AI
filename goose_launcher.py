"""
Launcher de NEXUS-OMNI-AI con block/goose.

Inicia una sesión interactiva de Goose con la extensión NEXUS cargada,
o ejecuta una receta YAML si se pasa la opción --recipe.

Uso:
    python goose_launcher.py                          # Sesión interactiva
    python goose_launcher.py --recipe nexus_recipe.yaml  # Ejecutar receta
"""

import argparse
import os
import shutil
import subprocess
import sys


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║        NEXUS-OMNI-AI  ×  block/goose  Launcher              ║
║  Sistema de IA Offline Multi-Modal con Agente Autónomo       ║
╚══════════════════════════════════════════════════════════════╝
"""

# Comando de la extensión MCP que Goose ejecutará como proceso hijo
EXTENSION_CMD = [sys.executable, "goose_extension_nexus.py"]

# Instrucciones de instalación mostradas cuando Goose no está disponible
INSTRUCCIONES_INSTALACION = """
Goose no está instalado o no se encuentra en el PATH.

Para instalarlo elige una de las siguientes opciones:

  Opción 1 — Con pip:
      pip install goose-ai

  Opción 2 — Con el instalador oficial (Linux/macOS):
      curl -fsSL https://github.com/block/goose/releases/latest/download/download_cli.sh | bash

  Opción 3 — Con Homebrew (macOS):
      brew install block/goose/goose

Más información: https://github.com/block/goose
"""


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------


def verificar_goose() -> bool:
    """Verifica que el binario 'goose' esté disponible en el sistema.

    Returns:
        True si Goose está instalado y accesible, False en caso contrario.
    """
    return shutil.which("goose") is not None


def construir_args_extension() -> list:
    """Construye los argumentos CLI para registrar la extensión NEXUS en Goose.

    Returns:
        Lista de argumentos para pasar a 'goose run' o 'goose session'.
    """
    extension_cmd_str = " ".join(EXTENSION_CMD)
    return [
        "--extension",
        f"nexus:{extension_cmd_str}",
    ]


def iniciar_sesion_interactiva() -> int:
    """Inicia una sesión interactiva de Goose con la extensión NEXUS cargada.

    Returns:
        Código de retorno del proceso de Goose.
    """
    print("[NEXUS] Iniciando sesión interactiva con Goose...")

    cmd = ["goose", "session"] + construir_args_extension()

    print(f"[NEXUS] Ejecutando: {' '.join(cmd)}\n")
    resultado = subprocess.run(cmd, check=False)
    return resultado.returncode


def ejecutar_receta(ruta_receta: str) -> int:
    """Ejecuta una receta YAML de Goose.

    Args:
        ruta_receta: Ruta al archivo de receta YAML.

    Returns:
        Código de retorno del proceso de Goose.
    """
    if not os.path.isfile(ruta_receta):
        print(f"[ERROR] No se encontró el archivo de receta: {ruta_receta}")
        return 1

    print(f"[NEXUS] Ejecutando receta: {ruta_receta}")

    cmd = ["goose", "run", "--recipe", ruta_receta] + construir_args_extension()

    print(f"[NEXUS] Ejecutando: {' '.join(cmd)}\n")
    resultado = subprocess.run(cmd, check=False)
    return resultado.returncode


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main() -> int:
    """Función principal del launcher."""
    # Mostrar banner de bienvenida
    print(BANNER)

    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Launcher de NEXUS-OMNI-AI con block/goose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--recipe",
        metavar="ARCHIVO",
        help="Ruta a la receta YAML de Goose a ejecutar",
    )
    args = parser.parse_args()

    # Verificar que Goose esté instalado
    if not verificar_goose():
        print("[ERROR] Goose no está disponible en este sistema.")
        print(INSTRUCCIONES_INSTALACION)
        return 1

    # Ejecutar la acción correspondiente
    if args.recipe:
        return ejecutar_receta(args.recipe)

    return iniciar_sesion_interactiva()


if __name__ == "__main__":
    sys.exit(main())
