# NEXUS OMNI AI

**NEXUS OMNI Multi-Agente IA v4.0** — Asistente de inteligencia artificial offline y multi-agente, con integración opcional de [CoPaw](https://github.com/agentscope-ai/CoPaw) (AgentScope-AI / Alibaba).

---

## Descripción

NEXUS OMNI AI es un asistente de IA local que orquesta múltiples agentes especializados:

| Agente | Especialidad |
|---|---|
| 🎯 Orquestador | Distribución inteligente de tareas |
| 💻 Código | Programación (Python, JS, SQL, etc.) |
| 🧠 Razonamiento | Análisis lógico y matemático |
| ✍️ Redacción | Textos, informes y comunicación |
| 📊 Datos | Estadística y análisis de datos |
| 🔍 Investigación | Búsqueda y síntesis de información |

Todo funciona **sin conexión a Internet**, usando modelos LLM locales a través de [Ollama](https://ollama.com).

---

## Características

### Funcionalidades base
- Múltiples agentes especializados con modelos LLM locales (Ollama)
- Soporte para LangChain, LangGraph, CrewAI y AutoGen
- Sistema RAG con ChromaDB para consulta de documentos
- Servidores MCP (Model Context Protocol) para herramientas externas
- Generación de imágenes con Diffusers
- Reconocimiento y síntesis de voz

### Nuevas capacidades con CoPaw
- 🧠 **Memoria persistente** (módulo ReMe de CoPaw) — el agente recuerda contexto entre sesiones
- 🔌 **Arquitectura modular con Skills** — plugins Python reutilizables
- 🌐 **Consola Web local** — interfaz web en `http://localhost:7860`
- 🤖 **Soporte multi-canal** — Discord, DingTalk, consola web y más
- ⏰ **Tareas autónomas programadas** — ejecución por cron o eventos

---

## Instalación

### Opción A — Instalador automático (Windows)

Ejecuta el instalador `.bat` incluido como administrador:

```
NEXUS_OMNI_INSTALAR_v4_Version8.bat
```

El instalador:
1. Instala Python 3.11 si no está presente
2. Descarga e instala Ollama
3. Instala todas las dependencias Python (incluido `copaw`)
4. Descarga el modelo `phi3` (~2.3 GB)
5. Compila el ejecutable con PyInstaller
6. Crea un acceso directo en el Escritorio

### Opción B — Instalación manual

**Requisitos previos:** Python 3.10–3.12, [Ollama](https://ollama.com) instalado y en `PATH`.

```bash
# 1. Instalar dependencias base
pip install -r requirements.txt

# 2. Instalar dependencias completas (opcional, para todas las funciones)
pip install pillow requests psutil pydantic rich python-dotenv ollama \
    langchain langchain-ollama langchain-community langgraph \
    crewai chromadb sentence-transformers pypdf python-docx \
    pyttsx3 SpeechRecognition diffusers transformers copaw

# 3. Descargar el modelo de lenguaje
ollama pull phi3
```

---

## Uso

### Ejecutar NEXUS directamente

```bash
python NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py
```

### Lanzar NEXUS a través de CoPaw (recomendado)

```bash
python copaw_launcher.py
```

Abre el navegador en **http://localhost:7860** para acceder a la consola web.

Variables de entorno opcionales:

| Variable | Por defecto | Descripción |
|---|---|---|
| `COPAW_HOST` | `0.0.0.0` | Dirección de escucha del servidor |
| `COPAW_PORT` | `7860` | Puerto de la consola web |
| `COPAW_DEBUG` | `0` | Activar modo depuración (`1` = sí) |

```bash
# Ejemplo con puerto personalizado
COPAW_PORT=8080 python copaw_launcher.py
```

---

## Estructura del proyecto

```
NEXUS-OMNI-AI/
├── NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py   # Módulo principal
├── NEXUS_OMNI_INSTALAR_v4_Version8.bat           # Instalador Windows
├── requirements.txt                              # Dependencias Python
├── copaw_launcher.py                             # Launcher CoPaw (punto de entrada)
├── copaw_skill_nexus.py                          # Skill de NEXUS para CoPaw
├── copaw_memory_nexus.py                         # Memoria persistente ReMe
└── memory/
    └── nexus_memory.json                         # Datos de memoria local
```

### Archivos de integración CoPaw

| Archivo | Descripción |
|---|---|
| `copaw_launcher.py` | Inicializa CoPaw, registra el Skill y arranca el servidor web |
| `copaw_skill_nexus.py` | Encapsula NEXUS como un Skill reutilizable en CoPaw |
| `copaw_memory_nexus.py` | Gestiona la memoria persistente con ReMe (o JSON local como fallback) |

---

## API de Skills

Puedes usar el Skill de NEXUS directamente desde Python:

```python
from copaw_skill_nexus import NexusOmniSkill

skill = NexusOmniSkill()
respuesta = skill.run("Escribe una función Python que calcule el factorial")
print(respuesta)
```

---

## Memoria persistente

```python
from copaw_memory_nexus import save_memory, load_memory, delete_memory, clear_memory

# Guardar datos entre sesiones
save_memory("usuario", "Carlos")
save_memory("preferencias", {"idioma": "es", "modelo": "phi3"})

# Recuperar datos
nombre = load_memory("usuario")
prefs  = load_memory("preferencias", default={})

# Eliminar una entrada
delete_memory("usuario")

# Borrar toda la memoria
clear_memory()
```

Los datos se guardan en `memory/nexus_memory.json` cuando CoPaw no está disponible,
y en el almacén ReMe de CoPaw cuando sí lo está.

---

## Requisitos del sistema

| Componente | Mínimo recomendado |
|---|---|
| OS | Windows 10/11, Linux, macOS |
| Python | 3.10 — 3.12 |
| RAM | 8 GB (16 GB recomendado) |
| Almacenamiento | 10 GB libres |
| GPU | Opcional (acelera generación de imágenes) |

---

## Licencia

Proyecto desarrollado por **NEXUS AI Labs**.
