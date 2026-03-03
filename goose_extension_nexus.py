"""
Extensión MCP de NEXUS-OMNI-AI para block/goose.
Expone las capacidades de NEXUS como herramienta mediante el Model Context Protocol.

Uso:
    python goose_extension_nexus.py

El proceso se ejecuta en modo stdio, recibiendo peticiones JSON-RPC por stdin
y enviando respuestas JSON-RPC por stdout.
"""

import json
import sys


class NexusExtension:
    """Servidor MCP que expone NEXUS-OMNI-AI como herramienta para Goose."""

    # Versión de la extensión
    VERSION = "v4"

    def nexus_query(self, prompt: str) -> str:
        """Procesa una consulta usando el motor de NEXUS-OMNI-AI.

        Args:
            prompt: La consulta o pregunta para enviar al motor NEXUS.

        Returns:
            Respuesta generada por el sistema NEXUS-OMNI-AI.
        """
        # TODO: integrar dinámicamente con NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO
        # Por ahora retornamos una respuesta placeholder compatible con el protocolo MCP.
        return f"[NEXUS] Respuesta a: {prompt}"

    def nexus_status(self) -> dict:
        """Retorna el estado actual del sistema NEXUS.

        Returns:
            Diccionario con información de estado del sistema NEXUS-OMNI-AI.
        """
        return {
            "estado": "activo",
            "version": self.VERSION,
            "modo": "offline",
            "motor": "NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO",
        }

    def _tools_list(self) -> dict:
        """Retorna la lista de herramientas disponibles en formato MCP."""
        return {
            "result": {
                "tools": [
                    {
                        "name": "nexus_query",
                        "description": (
                            "Envía una consulta al motor de inteligencia artificial "
                            "NEXUS-OMNI-AI y retorna la respuesta generada."
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "La consulta o pregunta para NEXUS",
                                }
                            },
                            "required": ["prompt"],
                        },
                    },
                    {
                        "name": "nexus_status",
                        "description": (
                            "Retorna el estado actual del sistema NEXUS-OMNI-AI, "
                            "incluyendo versión y modo de operación."
                        ),
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                ]
            }
        }

    def _tools_call(self, params: dict) -> dict:
        """Ejecuta la herramienta indicada con los argumentos proporcionados.

        Args:
            params: Diccionario con 'name' (nombre de la herramienta) y
                    'arguments' (argumentos de la llamada).

        Returns:
            Respuesta MCP con el resultado de la herramienta.
        """
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        if tool_name == "nexus_query":
            resultado = self.nexus_query(args.get("prompt", ""))
            return {
                "result": {
                    "content": [{"type": "text", "text": resultado}]
                }
            }

        if tool_name == "nexus_status":
            resultado = self.nexus_status()
            return {
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(resultado, ensure_ascii=False),
                        }
                    ]
                }
            }

        # Herramienta no encontrada
        return {
            "error": {
                "code": -32601,
                "message": f"Herramienta no encontrada: {tool_name}",
            }
        }

    def handle_request(self, request: dict) -> dict:
        """Maneja peticiones MCP (JSON-RPC) entrantes.

        Args:
            request: Diccionario con la petición JSON-RPC (method + params).

        Returns:
            Diccionario con la respuesta JSON-RPC correspondiente.
        """
        method = request.get("method", "")
        params = request.get("params", {})

        if method == "tools/list":
            return self._tools_list()

        if method == "tools/call":
            return self._tools_call(params)

        # Método no reconocido — error estándar JSON-RPC
        return {
            "error": {
                "code": -32601,
                "message": f"Método no encontrado: {method}",
            }
        }


if __name__ == "__main__":
    # Arrancar el servidor MCP en modo stdio (compatible con block/goose)
    extension = NexusExtension()

    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            peticion = json.loads(linea)
            respuesta = extension.handle_request(peticion)
            print(json.dumps(respuesta, ensure_ascii=False), flush=True)
        except json.JSONDecodeError as error:
            print(
                json.dumps(
                    {"error": {"code": -32700, "message": f"Error de parseo JSON: {error}"}}
                ),
                flush=True,
            )
        except Exception as error:  # pylint: disable=broad-exception-caught
            print(
                json.dumps({"error": {"code": -32603, "message": str(error)}}),
                flush=True,
            )
