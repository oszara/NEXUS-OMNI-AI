"""
copaw_launcher.py
=================
Punto de entrada principal para lanzar NEXUS-OMNI-AI a través de CoPaw
(AgentScope-AI / Alibaba).

Este launcher:
  1. Carga la memoria persistente del agente (módulo ReMe vía copaw_memory_nexus).
  2. Registra el Skill de NEXUS (NexusOmniSkill) en CoPaw.
  3. Configura el canal de consola web local.
  4. Inicia el servidor de CoPaw para que el agente esté disponible en el
     navegador en http://localhost:7860 (puerto por defecto).

Instrucciones de uso
--------------------
1. Instalar dependencias::

       pip install copaw ollama

2. Lanzar el servidor::

       python copaw_launcher.py

3. Abrir el navegador en http://localhost:7860

Variables de entorno opcionales
--------------------------------
``COPAW_HOST``
    Dirección de escucha del servidor (por defecto ``0.0.0.0``).
``COPAW_PORT``
    Puerto del servidor web (por defecto ``7860``).
``COPAW_DEBUG``
    Si se define con valor ``1``, activa el modo depuración de CoPaw.
"""

import os

from copaw_memory_nexus import load_memory, save_memory
from copaw_skill_nexus import NexusOmniSkill

# ---------------------------------------------------------------------------
# Configuración del servidor
# ---------------------------------------------------------------------------
HOST = os.environ.get("COPAW_HOST", "0.0.0.0")
PORT = int(os.environ.get("COPAW_PORT", "7860"))
DEBUG = os.environ.get("COPAW_DEBUG", "0") == "1"

# ---------------------------------------------------------------------------
# Integración con CoPaw
# ---------------------------------------------------------------------------
# Se intenta importar el agente y el canal web de CoPaw. Si el paquete no
# está instalado se muestra un error claro con instrucciones de instalación.
try:
    # TODO: ajustar las rutas de importación según la API pública de CoPaw.
    #       Posibles alternativas:
    #         from copaw import Agent, WebConsoleChannel
    #         from copaw.agent import Agent
    #         from copaw.channels import WebConsoleChannel
    from copaw import Agent  # type: ignore
    from copaw.channels import WebConsoleChannel  # type: ignore
    _COPAW_DISPONIBLE = True
except ImportError:
    _COPAW_DISPONIBLE = False


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def _inicializar_memoria() -> None:
    """Carga la memoria persistente y muestra un resumen en consola."""
    sesiones = load_memory("total_sesiones", 0)
    sesiones += 1
    save_memory("total_sesiones", sesiones)
    print(f"[NEXUS] Memoria persistente cargada. Sesión #{sesiones}")


def _crear_agente() -> object:
    """Crea y configura el agente CoPaw con el Skill de NEXUS.

    Retorna
    -------
    Agent
        Instancia del agente CoPaw lista para recibir peticiones.
    """
    skill = NexusOmniSkill()

    if not _COPAW_DISPONIBLE:
        print(
            "[NEXUS] AVISO: CoPaw no está instalado.\n"
            "        Ejecuta: pip install copaw\n"
            "        El servidor no se iniciará hasta que CoPaw esté disponible."
        )
        return skill  # Devolver el skill como stub para pruebas locales

    # TODO: ajustar los parámetros del constructor Agent según la API de CoPaw.
    agente = Agent(
        name="NEXUS-OMNI-AI",
        description=(
            "Agente multi-especialista offline: código, razonamiento, "
            "redacción, datos e investigación."
        ),
        skills=[skill],
    )
    return agente


def _iniciar_servidor(agente) -> None:
    """Configura el canal de consola web y arranca el servidor.

    Parámetros
    ----------
    agente :
        Instancia del agente CoPaw a servir.
    """
    if not _COPAW_DISPONIBLE:
        return

    # TODO: ajustar los parámetros del constructor WebConsoleChannel.
    canal = WebConsoleChannel(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
    print(f"[NEXUS] Iniciando servidor CoPaw en http://{HOST}:{PORT} ...")
    # TODO: ajustar el método de arranque según la API de CoPaw
    #       (p.ej. agente.serve(canal) o canal.run(agente)).
    agente.serve(canal)


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    """Función principal: inicializa memoria, agente y servidor CoPaw."""
    print("=" * 60)
    print("  NEXUS-OMNI-AI — Launcher CoPaw")
    print("=" * 60)

    _inicializar_memoria()
    agente = _crear_agente()
    _iniciar_servidor(agente)


if __name__ == "__main__":
    main()
