"""
copaw_memory_nexus.py
=====================
Módulo de memoria persistente para NEXUS-OMNI-AI usando el sistema ReMe
de CoPaw (AgentScope-AI / Alibaba).

Proporciona almacenamiento local de clave-valor que sobrevive entre sesiones,
permitiendo al agente NEXUS recordar información relevante del usuario y del
contexto de conversaciones anteriores.

Uso básico::

    from copaw_memory_nexus import save_memory, load_memory

    save_memory("nombre_usuario", "Carlos")
    nombre = load_memory("nombre_usuario")
    print(nombre)  # "Carlos"
"""

import json
import os

# ---------------------------------------------------------------------------
# Integración con el módulo ReMe de CoPaw
# ---------------------------------------------------------------------------
# Se intenta utilizar la API oficial de ReMe. Si CoPaw no está instalado se
# usa un backend de fichero JSON como fallback transparente.
try:
    # TODO: ajustar la ruta de importación a la clase ReMe de CoPaw cuando
    #       esté disponible (p.ej. "from copaw.memory import ReMe").
    from copaw.memory import ReMe as _ReMe  # type: ignore
    _COPAW_DISPONIBLE = True
except ImportError:
    _ReMe = None
    _COPAW_DISPONIBLE = False

# ---------------------------------------------------------------------------
# Configuración del almacenamiento
# ---------------------------------------------------------------------------
_DIRECTORIO_MEMORIA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "memory"
)
_ARCHIVO_MEMORIA = os.path.join(_DIRECTORIO_MEMORIA, "nexus_memory.json")

os.makedirs(_DIRECTORIO_MEMORIA, exist_ok=True)

# ---------------------------------------------------------------------------
# Backend basado en CoPaw ReMe (cuando está disponible)
# ---------------------------------------------------------------------------
_reme_instancia = None

if _COPAW_DISPONIBLE and _ReMe is not None:
    try:
        # TODO: pasar los parámetros de configuración correctos según la API
        #       de ReMe (ruta de almacenamiento, nombre del agente, etc.).
        _reme_instancia = _ReMe(storage_path=_DIRECTORIO_MEMORIA)
    except Exception:
        _reme_instancia = None

# ---------------------------------------------------------------------------
# Backend de fichero JSON (fallback cuando CoPaw no está disponible)
# ---------------------------------------------------------------------------


def _leer_json() -> dict:
    """Lee el archivo de memoria JSON y retorna su contenido como diccionario."""
    if not os.path.exists(_ARCHIVO_MEMORIA):
        return {}
    try:
        with open(_ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _escribir_json(datos: dict) -> None:
    """Escribe el diccionario dado en el archivo de memoria JSON."""
    with open(_ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def save_memory(key: str, value) -> None:
    """Guarda un valor en la memoria persistente asociado a la clave dada.

    Si CoPaw ReMe está disponible se usa su API nativa; en caso contrario
    se persiste en un fichero JSON local.

    Parámetros
    ----------
    key : str
        Identificador único del dato a recordar.
    value :
        Valor a almacenar. Debe ser serializable a JSON cuando se usa el
        backend de fichero.
    """
    if _reme_instancia is not None:
        try:
            # TODO: ajustar el método de escritura según la API de ReMe.
            _reme_instancia.set(key, value)
            return
        except Exception:
            pass  # Caer al backend JSON si ReMe falla

    datos = _leer_json()
    datos[key] = value
    _escribir_json(datos)


def load_memory(key: str, default=None):
    """Recupera un valor de la memoria persistente por su clave.

    Parámetros
    ----------
    key : str
        Identificador del dato a recuperar.
    default :
        Valor devuelto si la clave no existe en la memoria.

    Retorna
    -------
    El valor almacenado o ``default`` si no se encuentra.
    """
    if _reme_instancia is not None:
        try:
            # TODO: ajustar el método de lectura según la API de ReMe.
            resultado = _reme_instancia.get(key)
            if resultado is not None:
                return resultado
        except Exception:
            pass  # Caer al backend JSON si ReMe falla

    return _leer_json().get(key, default)


def delete_memory(key: str) -> None:
    """Elimina una entrada de la memoria persistente.

    Parámetros
    ----------
    key : str
        Identificador del dato a eliminar.
    """
    if _reme_instancia is not None:
        try:
            # TODO: ajustar el método de borrado según la API de ReMe.
            _reme_instancia.delete(key)
            return
        except Exception:
            pass

    datos = _leer_json()
    datos.pop(key, None)
    _escribir_json(datos)


def clear_memory() -> None:
    """Elimina toda la memoria persistente almacenada."""
    if _reme_instancia is not None:
        try:
            # TODO: ajustar el método de limpieza según la API de ReMe.
            _reme_instancia.clear()
            return
        except Exception:
            pass

    _escribir_json({})
