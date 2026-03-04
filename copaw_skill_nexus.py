"""
copaw_skill_nexus.py
====================
Skill de CoPaw que integra las capacidades offline de NEXUS-OMNI-AI.

Este módulo encapsula el agente NEXUS como un Skill reutilizable dentro del
ecosistema CoPaw (AgentScope-AI / Alibaba). Para activarlo, CoPaw debe tener
instalado el paquete ``copaw`` (pip install copaw) y este archivo debe
encontrarse en el directorio raíz del proyecto.

Uso básico::

    from copaw_skill_nexus import NexusOmniSkill
    skill = NexusOmniSkill()
    respuesta = skill.run("¿Cuál es la capital de Francia?")
    print(respuesta)
"""

import importlib
import sys
import os

# ---------------------------------------------------------------------------
# Clase base de Skill
# ---------------------------------------------------------------------------
# Se intenta importar la clase base desde CoPaw. Si CoPaw no está instalado
# se usa un stub para que el módulo pueda cargarse sin errores, mostrando
# un aviso claro al desarrollador.
try:
    # TODO: ajustar la ruta de importación cuando la API pública de CoPaw
    #       lo requiera (p.ej. "from copaw.skill import BaseSkill").
    from copaw.skill import BaseSkill  # type: ignore
except ImportError:  # pragma: no cover
    class BaseSkill:  # type: ignore
        """Stub de BaseSkill para cuando CoPaw no está instalado."""
        pass


# ---------------------------------------------------------------------------
# Skill principal
# ---------------------------------------------------------------------------
class NexusOmniSkill(BaseSkill):
    """Skill de CoPaw que expone las capacidades offline de NEXUS-OMNI-AI.

    Atributos
    ----------
    name : str
        Identificador único del skill dentro de CoPaw.
    description : str
        Descripción breve que CoPaw usa para seleccionar el skill.
    """

    name: str = "nexus_omni"
    description: str = (
        "Ejecuta capacidades offline de NEXUS-OMNI-AI como Skill de CoPaw. "
        "Soporta múltiples agentes especializados: código, razonamiento, "
        "redacción, datos e investigación."
    )

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """Inicializa el Skill cargando (si está disponible) el módulo
        principal de NEXUS para delegar las consultas."""
        super().__init__()
        self._nexus = self._cargar_nexus()

    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------

    def run(self, query: str) -> str:
        """Procesa una consulta usando el agente NEXUS-OMNI-AI.

        Parámetros
        ----------
        query : str
            Texto de la consulta o instrucción para el agente.

        Retorna
        -------
        str
            Respuesta generada por NEXUS-OMNI-AI.
        """
        if self._nexus is None:
            # Si el módulo principal no está disponible se devuelve un
            # mensaje indicativo para facilitar la depuración.
            return f"[NEXUS] Procesando: {query}"

        try:
            # Delegar al método de consulta del módulo principal de NEXUS.
            # TODO: ajustar el nombre de la función/método según la API
            #       interna de NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py.
            if hasattr(self._nexus, "consultar_agente"):
                return self._nexus.consultar_agente(query)
            # Fallback genérico
            return f"[NEXUS] Procesando: {query}"
        except Exception as exc:  # pragma: no cover
            return f"[NEXUS] Error al procesar la consulta: {exc}"

    # ------------------------------------------------------------------
    # Ayudantes internos
    # ------------------------------------------------------------------

    @staticmethod
    def _cargar_nexus():
        """Intenta importar dinámicamente el módulo principal de NEXUS.

        Retorna
        -------
        module | None
            El módulo importado o ``None`` si no se puede cargar.
        """
        nombre_modulo = "NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO"
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        if ruta_base not in sys.path:
            sys.path.insert(0, ruta_base)
        try:
            return importlib.import_module(nombre_modulo)
        except Exception:
            # El módulo principal no está disponible en este entorno.
            return None
