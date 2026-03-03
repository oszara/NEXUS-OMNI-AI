# NEXUS-OMNI-AI

Sistema de inteligencia artificial offline multi-modal desarrollado en Python.

---

## 🚀 Descripción

**NEXUS-OMNI-AI** es un motor de IA diseñado para funcionar completamente offline, con soporte multi-modal y capacidades avanzadas de procesamiento de lenguaje natural.

El núcleo principal se encuentra en `NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py`.

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/oszara/NEXUS-OMNI-AI.git
cd NEXUS-OMNI-AI

# Instalar dependencias
pip install -r requirements.txt
```

En Windows también puedes usar el instalador incluido:
```
NEXUS_OMNI_INSTALAR_v4_Version8.bat
```

---

## 🪿 Integración con Goose (block/goose)

[block/goose](https://github.com/block/goose) es un agente autónomo de código abierto que se puede ampliar mediante el **Model Context Protocol (MCP)**. La integración con NEXUS-OMNI-AI permite a Goose utilizar el motor de IA como herramienta y automatizar workflows completos mediante recetas YAML.

### ¿Qué aporta Goose al proyecto?

- **Agente autónomo:** Goose puede razonar, planificar y ejecutar tareas complejas de forma independiente.
- **Protocolo MCP:** Estándar abierto para exponer herramientas a modelos de lenguaje.
- **Recetas YAML:** Workflows reproducibles y automatizados, versionables en Git.
- **Múltiples LLMs:** Compatible con Claude, GPT-4o, Gemini, Ollama y más.

### Instalación de Goose

```bash
# Con pip
pip install goose-ai

# O con el instalador oficial (Linux/macOS)
curl -fsSL https://github.com/block/goose/releases/latest/download/download_cli.sh | bash

# Con Homebrew (macOS)
brew install block/goose/goose
```

### Uso del launcher

```bash
# Sesión interactiva (Goose + extensión NEXUS)
python goose_launcher.py

# Ejecutar la receta de análisis autónomo
python goose_launcher.py --recipe nexus_recipe.yaml
```

### Extensión MCP

El archivo `goose_extension_nexus.py` implementa un servidor MCP (JSON-RPC sobre stdio) que expone dos herramientas:

| Herramienta | Descripción |
|---|---|
| `nexus_query(prompt)` | Envía una consulta al motor NEXUS y retorna la respuesta |
| `nexus_status()` | Retorna el estado actual del sistema (versión, modo, motor) |

Puedes probar la extensión directamente:

```bash
echo '{"method":"tools/list","params":{}}' | python goose_extension_nexus.py
echo '{"method":"tools/call","params":{"name":"nexus_status","arguments":{}}}' | python goose_extension_nexus.py
```

### Receta YAML

El archivo `nexus_recipe.yaml` define un workflow autónomo de análisis y mejora:
1. Verificar el estado del sistema vía `nexus_status`.
2. Analizar el archivo principal e identificar mejoras.
3. Consultar el motor NEXUS con `nexus_query`.
4. Generar un reporte ejecutivo en español.

### Modos de uso

| Modo | Comando | Descripción |
|---|---|---|
| Solo NEXUS | *(ejecutar directamente el script principal)* | Motor de IA sin agente |
| NEXUS + Goose | `python goose_launcher.py` | Sesión interactiva con agente autónomo |
| NEXUS + Goose (receta) | `python goose_launcher.py --recipe nexus_recipe.yaml` | Workflow automatizado |

---

## 📁 Estructura del Proyecto

| Archivo | Descripción |
|---|---|
| `NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py` | Motor principal de IA |
| `NEXUS_OMNI_INSTALAR_v4_Version8.bat` | Instalador Windows |
| `goose_extension_nexus.py` | Extensión MCP para Goose |
| `goose_launcher.py` | Launcher de Goose |
| `nexus_recipe.yaml` | Receta YAML para workflows autónomos |
| `.goosehints` | Contexto del proyecto para Goose |
| `requirements.txt` | Dependencias del proyecto |

---

## 📋 Requisitos

- Python 3.8+
- [Goose](https://github.com/block/goose) (para la integración con agente)
- [Ollama](https://ollama.ai) (recomendado para uso offline)

---

## 🔒 Notas

- El archivo `NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py` **no debe modificarse** directamente.
- Todos los módulos de integración son no intrusivos.
- Los comentarios y mensajes están en español.
