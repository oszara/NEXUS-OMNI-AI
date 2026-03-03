# NEXUS OMNI Multi-Agente IA v4.0

Sistema de IA offline multi-agente con 7 agentes especializados que trabajan en paralelo.
Instalación automática con un solo click — sin configuración manual.

## ✨ Características

- 🤖 **7 Agentes IA** trabajando en paralelo (Orquestador, Código, Razonamiento, Redacción, Datos, Investigación, Integrador)
- 🔧 **5 Motores de IA**: CrewAI, LangGraph, AutoGen, LangChain, MCP
- 🎨 **Generación de imágenes** con Stable Diffusion
- 📚 **RAG** (Retrieval Augmented Generation) con ChromaDB
- 🎙️ **Voz** (texto a voz y reconocimiento de voz)
- 🔌 **7 Servidores MCP** (archivos, web, código, imágenes, RAG, voz, memoria)
- 💻 Interfaz gráfica completa con Tkinter
- 🔒 100% Offline después de la instalación inicial

## 🚀 Instalación — Un Solo Click

### Requisitos mínimos

- Windows 10/11
- 8 GB RAM (mínimo 4 GB)
- 10 GB de espacio libre en disco
- Conexión a internet (solo para la instalación inicial)

### Pasos

1. **Descarga** este repositorio (botón verde `Code` → `Download ZIP`) o clónalo:
   ```
   git clone https://github.com/oszara/NEXUS-OMNI-AI.git
   ```

2. **Doble click** en `INSTALAR.bat`

3. **Espera** 15-30 minutos mientras se instala todo automáticamente:
   - Python 3.11 (si no está instalado)
   - Ollama + modelo phi3 (~2.3 GB)
   - 25 paquetes de IA
   - Compilación de la aplicación
   - Acceso directo en el Escritorio

4. **¡Listo!** Abre `NEXUS OMNI AI` desde tu Escritorio.

> **Nota:** Si `INSTALAR.bat` no funciona, puedes usar `NEXUS_OMNI_INSTALAR_v4_Version8.bat` como alternativa.

## 📁 Estructura del proyecto

```
NEXUS-OMNI-AI/
├── INSTALAR.bat                              ← Un solo click para instalar
├── NEXUS_OMNI_INSTALAR_v4_Version8.bat       ← Instalador alternativo (BAT completo)
├── NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py ← Script principal de instalación
├── requirements.txt                           ← Dependencias Python
└── README.md                                  ← Este archivo
```

## 🛠️ Instalación manual (avanzado)

Si prefieres instalar manualmente:

```bash
# 1. Instalar Python 3.11 desde https://www.python.org/downloads/release/python-3119/
# 2. Instalar dependencias
pip install -r requirements.txt
# 3. Instalar Ollama desde https://ollama.com/download
# 4. Descargar modelo base
ollama pull phi3
# 5. Ejecutar el instalador principal
python NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py
```

## 🤖 Modelos soportados

| Modelo | Tamaño | Descripción |
|--------|--------|-------------|
| phi3 | ~2.3 GB | Rápido, ligero, ideal para empezar |
| deepseek-r1 | ~4.7 GB | Razonamiento superior |
| qwen3 | ~4.6 GB | General y análisis de datos |
| qwen3-coder | ~4.6 GB | Especialista en código |
| mistral | ~4.1 GB | Redacción y textos |
| codestral | ~12 GB | Código avanzado |
| glm4 | ~5.5 GB | Multimodal |

## 📄 Licencia

MIT — Uso libre para cualquier propósito.
