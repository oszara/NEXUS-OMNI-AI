# 📖 Manual de Usuario — NEXUS OMNI Multi-Agente IA v4.0

## Guía Completa Paso a Paso

---

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#1-requisitos-del-sistema)
2. [Instalación Paso a Paso](#2-instalación-paso-a-paso)
3. [Primer Inicio de la Aplicación](#3-primer-inicio-de-la-aplicación)
4. [Interfaz Principal — Descripción General](#4-interfaz-principal--descripción-general)
5. [Cómo Enviar tu Primera Consulta](#5-cómo-enviar-tu-primera-consulta)
6. [Los 7 Agentes de IA — Guía Individual](#6-los-7-agentes-de-ia--guía-individual)
   - [🎯 Agente Orquestador](#-agente-orquestador)
   - [💻 Agente de Código](#-agente-de-código)
   - [🧠 Agente de Razonamiento](#-agente-de-razonamiento)
   - [✍️ Agente de Redacción](#️-agente-de-redacción)
   - [📊 Agente de Datos](#-agente-de-datos)
   - [🔍 Agente de Investigación](#-agente-de-investigación)
   - [🔗 Agente Integrador](#-agente-integrador)
7. [Generación de Imágenes con Stable Diffusion](#7-generación-de-imágenes-con-stable-diffusion)
8. [Sistema RAG — Documentos Inteligentes](#8-sistema-rag--documentos-inteligentes)
9. [Funciones de Voz](#9-funciones-de-voz)
10. [Herramientas MCP](#10-herramientas-mcp)
11. [Gestión de Modelos de IA](#11-gestión-de-modelos-de-ia)
12. [Sistema de Memoria Persistente](#12-sistema-de-memoria-persistente)
13. [Guardar y Exportar Conversaciones](#13-guardar-y-exportar-conversaciones)
14. [Atajos de Teclado](#14-atajos-de-teclado)
15. [Solución de Problemas](#15-solución-de-problemas)
16. [Preguntas Frecuentes (FAQ)](#16-preguntas-frecuentes-faq)

---

## 1. Requisitos del Sistema

Antes de instalar NEXUS OMNI AI, asegúrate de cumplir con estos requisitos:

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **Sistema Operativo** | Windows 10 (64-bit) | Windows 10/11 (64-bit) |
| **RAM** | 4 GB | 8 GB o más |
| **Espacio en disco** | 10 GB libres | 20 GB libres |
| **Python** | 3.10 | 3.11 (se instala automáticamente) |
| **GPU (opcional)** | — | NVIDIA con CUDA (acelera imágenes) |
| **Internet** | Necesario solo para instalación inicial | Banda ancha para descargar modelos |
| **Micrófono** | — | Necesario para reconocimiento de voz |

> **💡 Nota:** Después de la instalación inicial, NEXUS OMNI AI funciona **100% offline** (sin conexión a internet), excepto las funciones de búsqueda web y reconocimiento de voz.

---

## 2. Instalación Paso a Paso

### Método A: Instalador Automático (.bat) — Recomendado

Este es el método más sencillo. El archivo `.bat` automatiza todo el proceso.

**Paso 1:** Localiza el archivo `NEXUS_OMNI_INSTALAR_v4_Version8.bat` en la carpeta del proyecto.

**Paso 2:** Haz **clic derecho** sobre el archivo y selecciona **"Ejecutar como administrador"**.

> ⚠️ **Importante:** Se necesitan permisos de administrador. Si aparece un cuadro de diálogo del sistema, haz clic en **"Sí"**.

**Paso 3:** El instalador ejecutará automáticamente 8 etapas. Verás el progreso en la ventana de comandos:

```
[1/8] Verificando Python 3.11...
[2/8] Preparando carpetas de trabajo...
[3/8] Actualizando pip...
[4/8] Verificando e instalando Ollama...
[5/8] Instalando 25 paquetes de dependencias...
[6/8] Descargando modelo de IA (phi3)...
[7/8] Compilando aplicación con PyInstaller...
[8/8] Creando acceso directo en el escritorio...
```

**Paso 4:** Espera a que finalice el proceso (15-30 minutos dependiendo de tu conexión a internet y la velocidad del equipo).

**Paso 5:** Al terminar, encontrarás:
- Un **acceso directo** en tu escritorio llamado **"NEXUS OMNI AI"**
- La carpeta de la aplicación en `C:\Users\TuUsuario\Desktop\NEXUS_OMNI_AI\`

### Método B: Script de Python

**Paso 1:** Abre una terminal (cmd o PowerShell) como administrador.

**Paso 2:** Navega a la carpeta del proyecto:
```bash
cd ruta/a/NEXUS-OMNI-AI
```

**Paso 3:** Ejecuta el script principal:
```bash
python NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py
```

**Paso 4:** El script realizará un diagnóstico completo de tu sistema:
- Verificará la versión de Python
- Detectará hardware (RAM, GPU CUDA, disco)
- Comprobará herramientas del sistema (Ollama, Java, Git)
- Escaneará dependencias de paquetes
- Calculará compatibilidad de modelos

**Paso 5:** Sigue las instrucciones en pantalla para completar la instalación.

### ¿Qué se instala?

El proceso crea la siguiente estructura de carpetas:

```
📁 NEXUS_OMNI_AI/
├── 📁 app/
│   ├── 📁 dist/             → nexus_omni.exe (aplicación compilada)
│   ├── 📁 mcp_servers/      → 7 servidores MCP
│   ├── 📁 memory/           → Datos de memoria persistente
│   │   ├── 📁 rag_db/       → Base de datos vectorial (ChromaDB)
│   │   └── 📄 memoria.json  → Hechos y notas guardadas
│   ├── 📁 imagenes_generadas/ → Imágenes creadas con Stable Diffusion
│   ├── 📁 documentos_rag/    → Documentos indexados
│   ├── 📁 sd_models/         → Modelos de Stable Diffusion (caché)
│   └── 📁 exports/           → Conversaciones exportadas
├── 📁 output/                → Instalador standalone (.exe)
└── 📄 config_sistema.json    → Configuración del sistema
```

---

## 3. Primer Inicio de la Aplicación

**Paso 1:** Haz doble clic en el acceso directo **"NEXUS OMNI AI"** en tu escritorio, o ejecuta directamente `nexus_omni.exe` desde la carpeta `app/dist/`.

**Paso 2:** La aplicación se iniciará y verás la interfaz principal con el tema oscuro cyberpunk.

**Paso 3:** Verifica en la parte superior de la ventana:
- **Estado de Ollama:** Debe mostrar "✅ Ollama conectado" o similar.
- **Modelos disponibles:** Se listarán los modelos instalados.

> **💡 Consejo:** Si Ollama no está iniciado, la aplicación intentará iniciarlo automáticamente. Si no lo consigue, abre una terminal y ejecuta `ollama serve` antes de abrir la aplicación.

**Paso 4:** ¡Listo! Ya puedes comenzar a usar NEXUS OMNI AI.

---

## 4. Interfaz Principal — Descripción General

La ventana de la aplicación (1400×860 píxeles) se divide en las siguientes secciones:

```
┌─────────────────────────────────────────────────────────────────────┐
│  🤖 NEXUS OMNI Multi-Agente IA v4.0                                │
│  [Indicadores] [📋 Modelos] [⬇️ Pull] [💾 Guardar] [ℹ️ HW Info]    │
├──────────────────────────┬──────────────────────────────────────────┤
│                          │                                          │
│   PANEL IZQUIERDO        │        PANEL DERECHO                     │
│   💬 Chat Principal      │   🔬 Agentes en Tiempo Real              │
│                          │                                          │
│   [Historial de chat]    │   [Pestañas de agentes + herramientas]   │
│                          │   🎯│💻│🧠│✍️│📊│🔍│🔗│🎨│📚│🎙️│🔧      │
│   ┌──────────────────┐   │                                          │
│   │ Escribe aquí...  │   │   [Contenido de la pestaña activa]      │
│   └──────────────────┘   │                                          │
│   [Enviar ▶] [🗑 Limpiar]│                                          │
│                          │                                          │
└──────────────────────────┴──────────────────────────────────────────┘
```

### Panel Izquierdo — Chat Principal
- **Área de historial:** Muestra toda la conversación (preguntas y respuestas finales).
- **Campo de entrada:** Cuadro de texto de 4 líneas para escribir tu consulta.
- **Botón "Enviar ▶":** Envía la consulta a todos los agentes.
- **Botón "🗑 Limpiar":** Borra todo el historial de chat.

### Panel Derecho — Agentes y Herramientas
Contiene **11 pestañas** organizadas por función:

| Pestaña | Función |
|---------|---------|
| 🎯 Orquestador | Salida del agente coordinador |
| 💻 Código | Respuestas de generación de código |
| 🧠 Razonamiento | Análisis lógico paso a paso |
| ✍️ Redacción | Textos profesionales y traducciones |
| 📊 Datos | Análisis de datos y estadísticas |
| 🔍 Investigación | Resultados de búsqueda e investigación |
| 🔗 Integrador | Respuesta final unificada |
| 🎨 Imagen SD | Generación de imágenes con Stable Diffusion |
| 📚 RAG Docs | Indexación y búsqueda de documentos |
| 🎙️ Voz | Texto a voz y reconocimiento de voz |
| 🔧 MCP Tools | 11 herramientas rápidas de utilidad |

### Barra Superior — Botones de Acción

| Botón | Función |
|-------|---------|
| 📋 **Modelos** | Ver lista de modelos de Ollama instalados |
| ⬇️ **Pull** | Descargar nuevos modelos de IA |
| 💾 **Guardar** | Exportar toda la conversación a archivo .txt |
| ℹ️ **HW Info** | Ver información del hardware del sistema |

---

## 5. Cómo Enviar tu Primera Consulta

Sigue estos pasos para interactuar con NEXUS OMNI AI:

**Paso 1:** Haz clic en el **campo de texto** del panel izquierdo.

**Paso 2:** Escribe tu pregunta o solicitud. Por ejemplo:
```
¿Cómo puedo crear una API REST en Python con FastAPI?
```

**Paso 3:** Presiona **Ctrl+Enter** o haz clic en el botón **"Enviar ▶"**.

**Paso 4:** Observa cómo trabajan los agentes:
- El botón cambiará a **"⏳ Agentes trabajando..."**
- En el panel derecho, cada pestaña de agente se actualizará en tiempo real.
- Un indicador de estado mostrará el progreso.

**Paso 5:** Espera la respuesta. El proceso sigue este flujo:

```
Tu pregunta
    ↓
🎯 Orquestador analiza y distribuye tareas
    ↓
💻🧠✍️📊🔍 Todos los agentes trabajan EN PARALELO
    ↓
🔗 Integrador combina todas las respuestas
    ↓
✅ Respuesta final aparece en el Chat Principal
```

**Paso 6:** Lee la respuesta integrada en el Chat Principal (panel izquierdo). Para ver qué respondió cada agente individualmente, haz clic en las pestañas del panel derecho.

**Paso 7:** El botón volverá a mostrar **"Enviar ▶ Todos los agentes"**, indicando que puedes enviar una nueva consulta.

> **💡 Consejo:** Cuanto más específica sea tu pregunta, mejores serán las respuestas de los agentes.

---

## 6. Los 7 Agentes de IA — Guía Individual

### 🎯 Agente Orquestador

**Motor:** CrewAI  
**Modelos:** deepseek-r1 → phi3 (fallback)  
**Color:** Amarillo (#f0a500)

**¿Qué hace?**  
Es el "cerebro director" del sistema. Analiza tu pregunta, la descompone en subtareas y las asigna al agente más adecuado.

**¿Cómo funciona internamente?**  
1. Recibe tu pregunta completa.
2. Analiza el tipo de solicitud (código, redacción, análisis, etc.).
3. Genera un JSON con la distribución de tareas:
   ```json
   {
     "resumen": "El usuario quiere crear una API REST...",
     "tareas": {
       "codigo": "Generar código de la API con FastAPI",
       "razonamiento": "Analizar la arquitectura óptima",
       "redaccion": "Documentar los endpoints"
     }
   }
   ```
4. Cada agente recibe solo la subtarea asignada.

**Cuándo brilla:**  
- Preguntas complejas que requieren múltiples perspectivas.
- Solicitudes que combinan código, explicación y análisis.

**Ejemplo de uso:**
```
Pregunta: "Diseña un sistema de autenticación seguro para una app web"

→ El Orquestador asigna:
  - Código: implementar JWT + bcrypt
  - Razonamiento: analizar vectores de ataque
  - Redacción: documentar el flujo de autenticación
  - Datos: estadísticas de seguridad
```

---

### 💻 Agente de Código

**Motor:** LangGraph  
**Modelos:** qwen3-coder → codestral (fallback)  
**Color:** Verde (#00ff88)

**¿Qué hace?**  
Genera código funcional en múltiples lenguajes de programación.

**Lenguajes soportados:**
- Python 🐍
- JavaScript / TypeScript
- Java ☕
- SQL
- HTML/CSS
- Y más...

**Cómo sacarle el máximo provecho:**

**Paso 1:** Sé específico con lo que necesitas:
```
✅ Bueno: "Crea una función en Python que ordene una lista de 
          diccionarios por el campo 'edad' de mayor a menor"
❌ Vago:  "Haz algo con listas"
```

**Paso 2:** Indica el lenguaje si es importante:
```
"Escribe esto en Java" o "Necesito esto en JavaScript ES6"
```

**Paso 3:** Pide explicaciones si las necesitas:
```
"Genera el código y explica cada sección con comentarios"
```

**Ejemplo de interacción:**
```
Tú: "Crea un servidor web básico en Python con Flask que tenga 
     3 endpoints: /users, /products y /health"

💻 Código responde:
   → Código completo del servidor Flask
   → Importaciones necesarias
   → Configuración de rutas
   → Ejemplo de ejecución
```

---

### 🧠 Agente de Razonamiento

**Motor:** AutoGen  
**Modelos:** deepseek-r1 → phi3 (fallback)  
**Color:** Rojo (#ff6b6b)

**¿Qué hace?**  
Realiza análisis lógico y razonamiento paso a paso. Es ideal para problemas que requieren pensamiento estructurado.

**Cuándo usarlo:**
- Problemas matemáticos o de lógica
- Análisis de pros y contras
- Planificación estratégica
- Resolución de acertijos
- Evaluación de opciones

**Cómo sacarle el máximo provecho:**

**Paso 1:** Plantea problemas que necesiten razonamiento:
```
"¿Cuál es la mejor arquitectura para una app que necesita 
manejar 10,000 usuarios concurrentes: monolítica o microservicios?"
```

**Paso 2:** Pide el razonamiento explícito:
```
"Explica paso a paso cómo resolverías este problema de 
optimización de rutas"
```

**Ejemplo de interacción:**
```
Tú: "Si tengo un presupuesto de $5,000 para un servidor, 
     ¿debería comprar uno potente o varios pequeños?"

🧠 Razonamiento responde:
   → Paso 1: Análisis de requisitos...
   → Paso 2: Comparación de costos...
   → Paso 3: Evaluación de escalabilidad...
   → Paso 4: Consideración de redundancia...
   → Conclusión: ...
```

---

### ✍️ Agente de Redacción

**Motor:** LangChain  
**Modelos:** mistral → phi3 (fallback)  
**Color:** Púrpura (#a78bfa)

**¿Qué hace?**  
Genera textos profesionales, resúmenes, traducciones y contenido editorial.

**Capacidades:**
- Redacción formal e informal
- Resúmenes ejecutivos
- Traducción Español ↔ Inglés
- Emails profesionales
- Documentación técnica
- Artículos y blogs

**Cómo sacarle el máximo provecho:**

**Paso 1:** Indica el tono que necesitas:
```
"Redacta un email formal al cliente explicando el retraso 
del proyecto"
```

**Paso 2:** Para traducciones, sé explícito:
```
"Traduce al inglés: 'Nuestra empresa se especializa en 
soluciones de inteligencia artificial'"
```

**Paso 3:** Para resúmenes, proporciona el texto:
```
"Resume en 3 párrafos el siguiente artículo: [pega el texto]"
```

**Ejemplo de interacción:**
```
Tú: "Escribe una descripción profesional para LinkedIn 
     de un desarrollador Full Stack con 5 años de experiencia"

✍️ Redacción responde:
   → Descripción optimizada para LinkedIn
   → Palabras clave relevantes
   → Tono profesional pero personal
```

---

### 📊 Agente de Datos

**Motor:** LangChain  
**Modelos:** qwen3 → phi3 (fallback)  
**Color:** Cian (#38bdf8)

**¿Qué hace?**  
Realiza análisis de datos, genera consultas SQL y trabaja con estadísticas.

**Capacidades:**
- Consultas SQL (SELECT, JOIN, GROUP BY, etc.)
- Análisis estadístico
- Interpretación de datos
- Patrones y tendencias
- Generación de esquemas de base de datos

**Cómo sacarle el máximo provecho:**

**Paso 1:** Describe tus datos:
```
"Tengo una tabla 'ventas' con columnas: id, producto, 
cantidad, precio, fecha. Necesito las ventas totales por mes"
```

**Paso 2:** Pide análisis específicos:
```
"¿Qué patrones hay en estos datos de temperatura mensual: 
15, 18, 22, 28, 32, 35, 33, 30, 25, 20, 16, 14?"
```

**Ejemplo de interacción:**
```
Tú: "Diseña el esquema de base de datos para una tienda 
     online con productos, categorías, usuarios y pedidos"

📊 Datos responde:
   → Esquema SQL completo con CREATE TABLE
   → Relaciones entre tablas (FOREIGN KEY)
   → Índices recomendados
   → Ejemplo de consultas útiles
```

---

### 🔍 Agente de Investigación

**Motor:** MCP  
**Modelos:** phi3 → mistral (fallback)  
**Color:** Naranja (#fb923c)

**¿Qué hace?**  
Realiza búsquedas web, verifica hechos y sintetiza información de múltiples fuentes.

**Capacidades:**
- Búsqueda web (DuckDuckGo)
- Verificación de hechos
- Síntesis de información
- Investigación temática

> **⚠️ Nota:** La búsqueda web requiere conexión a internet. Sin conexión, el agente trabajará con su conocimiento base.

**Cómo sacarle el máximo provecho:**

**Paso 1:** Haz preguntas que requieran investigación:
```
"¿Cuáles son las últimas tendencias en inteligencia 
artificial para 2025?"
```

**Paso 2:** Pide verificación de datos:
```
"Verifica si es cierto que Python es el lenguaje más 
usado en ciencia de datos"
```

**Ejemplo de interacción:**
```
Tú: "Investiga las diferencias entre React, Vue y Angular 
     para elegir un framework frontend"

🔍 Investigación responde:
   → Comparativa basada en fuentes web
   → Pros y contras de cada uno
   → Estadísticas de uso y comunidad
   → Recomendación contextualizada
```

---

### 🔗 Agente Integrador

**Motor:** CrewAI  
**Modelos:** deepseek-r1 → phi3 (fallback)  
**Color:** Amarillo (#facc15)

**¿Qué hace?**  
Es el último en actuar. Espera las respuestas de todos los demás agentes y las combina en una **única respuesta coherente y completa**.

**¿Cómo funciona?**
1. Espera a que los 6 agentes anteriores terminen.
2. Recibe todas las respuestas individuales.
3. Elimina redundancias y contradicciones.
4. Organiza la información de forma lógica.
5. Genera una respuesta unificada y bien estructurada.

**Lo que ves en el Chat Principal es la respuesta del Integrador.**

> **💡 Consejo:** Si quieres ver la respuesta cruda de un agente específico, haz clic en su pestaña individual en el panel derecho.

---

## 7. Generación de Imágenes con Stable Diffusion

### Requisitos Previos
- Modelo de Stable Diffusion (se descarga automáticamente la primera vez)
- GPU NVIDIA con CUDA (recomendado) o CPU (más lento)
- ~4 GB de espacio libre para el modelo

### Paso a Paso

**Paso 1:** Haz clic en la pestaña **"🎨 Imagen SD"** en el panel derecho.

**Paso 2:** Escribe un **prompt** (descripción de la imagen deseada) en el campo de texto. Por ejemplo:
```
a futuristic robot standing in a neon-lit cyberpunk city 
at night, detailed, 4k, digital art
```

> **💡 Consejo:** Los prompts en inglés suelen dar mejores resultados porque el modelo fue entrenado principalmente en inglés.

**Paso 3:** Configura los **Pasos** (Steps):
- **20 pasos** (por defecto): Buena calidad, velocidad aceptable.
- **10-15 pasos**: Resultado rápido, menor calidad.
- **30-50 pasos**: Mayor calidad, más tiempo de generación.

**Paso 4:** Haz clic en el botón **"🎨 Generar"**.

**Paso 5:** Espera a que se genere la imagen:
- **Con GPU NVIDIA:** ~30 segundos
- **Con CPU:** 1-5 minutos (dependiendo del hardware)

**Paso 6:** La imagen se mostrará automáticamente en la interfaz (escalada a 500×500 píxeles).

**Paso 7:** La imagen se guarda automáticamente en:
```
NEXUS_OMNI_AI/app/imagenes_generadas/img_YYYYMMDD_HHMMSS.png
```

### Consejos para Mejores Resultados

| Técnica | Ejemplo |
|---------|---------|
| Sé descriptivo | "a red dragon breathing fire on a mountain, fantasy art, detailed scales" |
| Indica estilo | "oil painting style", "watercolor", "digital art", "photorealistic" |
| Añade calidad | "4k", "highly detailed", "sharp focus", "studio lighting" |
| Usa negativas | Evita describir lo que NO quieres (el modelo no soporta prompts negativos en esta versión) |

---

## 8. Sistema RAG — Documentos Inteligentes

El sistema RAG (Retrieval-Augmented Generation) te permite **indexar tus propios documentos** y hacer **búsquedas semánticas** sobre ellos.

### ¿Qué es una Búsqueda Semántica?
A diferencia de una búsqueda por palabras clave, la búsqueda semántica **entiende el significado** de tu consulta. Por ejemplo:
- Buscas: "salario de empleados"
- Encuentra: fragmentos que hablen de "remuneración del personal" (aunque no use las mismas palabras)

### Formatos Soportados
- 📄 **PDF** (.pdf)
- 📝 **Word** (.docx)
- 📃 **Texto plano** (.txt)
- 📋 **Markdown** (.md)

### Paso a Paso: Indexar un Documento

**Paso 1:** Haz clic en la pestaña **"📚 RAG Docs"** en el panel derecho.

**Paso 2:** Haz clic en el botón **"📂 Indexar"**.

**Paso 3:** Se abrirá un cuadro de diálogo para seleccionar archivos. Navega hasta tu documento y selecciónalo.

**Paso 4:** El sistema procesará el documento:
1. Extrae el texto del archivo.
2. Divide el texto en fragmentos de 500 caracteres.
3. Genera embeddings (vectores numéricos) con SentenceTransformers.
4. Almacena los vectores en ChromaDB (base de datos vectorial).

**Paso 5:** Verás un mensaje de confirmación: **"Indexados X fragmentos de: nombre_archivo"**.

> **💡 Consejo:** Puedes indexar múltiples documentos. Todos se almacenan en la misma base de datos y son buscables de forma conjunta.

### Paso a Paso: Buscar en Documentos

**Paso 1:** En la pestaña **"📚 RAG Docs"**, escribe tu consulta en el campo de búsqueda.

**Paso 2:** Haz clic en **"🔍 Buscar"**.

**Paso 3:** El sistema mostrará los **5 fragmentos más relevantes** de tus documentos indexados, junto con:
- El texto del fragmento
- El nombre del documento fuente
- La relevancia semántica

### Paso a Paso: Ver Documentos Indexados

**Paso 1:** En la pestaña **"📚 RAG Docs"**, haz clic en **"📋 Listar"**.

**Paso 2:** Se mostrará la lista de todos los documentos que has indexado previamente.

### Dónde se Almacenan los Datos
- **Base de datos vectorial:** `NEXUS_OMNI_AI/app/memory/rag_db/`
- **Modelo de embeddings:** `all-MiniLM-L6-v2` (se descarga automáticamente la primera vez)

---

## 9. Funciones de Voz

### Texto a Voz (TTS) — Lectura en Voz Alta

**Motor:** pyttsx3 (funciona offline)

**Paso 1:** Haz clic en la pestaña **"🎙️ Voz"** en el panel derecho.

**Paso 2:** Escribe o pega el texto que quieres escuchar en el área de texto.

**Paso 3:** Haz clic en el botón **"🔊 Leer"**.

**Paso 4:** El sistema leerá el texto en voz alta a través de los altavoces del sistema.

**Configuración:**
- **Velocidad:** 150 palabras por minuto (configurable desde el servidor MCP de voz).
- **Voz:** Se usa la voz por defecto del sistema (configurable con `voz_idx`).

### Reconocimiento de Voz (STT) — Voz a Texto

**Motor:** Google Speech Recognition (requiere internet)  
**Idioma:** Español (es-ES)

**Paso 1:** Asegúrate de tener un **micrófono conectado** y **conexión a internet**.

**Paso 2:** En la pestaña **"🎙️ Voz"**, haz clic en **"🎙️ Escuchar"**.

**Paso 3:** **Habla claramente** durante los próximos 5 segundos.

**Paso 4:** El texto reconocido se insertará automáticamente en el campo de entrada del chat.

**Paso 5:** Revisa el texto y presiona **Ctrl+Enter** para enviarlo como consulta.

> **⚠️ Nota:** Esta función requiere conexión a internet ya que utiliza la API de Google Speech Recognition.

### Ver Voces Disponibles

**Paso 1:** En la pestaña **"🎙️ Voz"**, haz clic en **"📋 Voces"**.

**Paso 2:** Se mostrará la lista de todas las voces de texto a voz disponibles en tu sistema, con sus índices.

---

## 10. Herramientas MCP

La pestaña **"🔧 MCP Tools"** ofrece acceso directo a 11 herramientas de utilidad organizadas en categorías.

### 📂 Herramientas de Archivos

#### Listar Directorio
**Qué hace:** Muestra los archivos y carpetas de un directorio.
```
1. Haz clic en "📂 Listar Dir"
2. Introduce la ruta del directorio (o deja "." para el actual)
3. Se mostrará la lista de contenidos
```

#### Leer Archivo
**Qué hace:** Muestra el contenido de un archivo de texto.
```
1. Haz clic en "📄 Leer Archivo"
2. Introduce la ruta completa del archivo
3. Se mostrará el contenido del archivo
```

#### Buscar en Archivos
**Qué hace:** Busca un patrón de texto dentro de archivos de un directorio.
```
1. Haz clic en "🔍 Buscar Archivos"
2. Introduce el directorio y el patrón de búsqueda
3. Se mostrarán hasta 50 coincidencias con números de línea
```

### 🌐 Herramientas Web

#### Buscar en la Web
**Qué hace:** Realiza una búsqueda web usando DuckDuckGo.
```
1. Haz clic en "🌐 Buscar Web"
2. Introduce tu consulta de búsqueda
3. Se mostrarán resultados con resúmenes y enlaces
```
> Requiere conexión a internet.

#### Verificar Internet
**Qué hace:** Comprueba si tienes conexión a internet.
```
1. Haz clic en "📡 Internet"
2. Mostrará "Conectado" o "Sin conexión"
```

### 🐍 Herramientas de Código

#### Ejecutar Python
**Qué hace:** Ejecuta código Python y muestra el resultado.
```
1. Haz clic en "🐍 Python"
2. Escribe o pega tu código Python
3. Se ejecutará con un timeout de 15 segundos
4. Verás la salida (stdout) y errores (stderr)
```

#### Ejecutar Java
**Qué hace:** Compila y ejecuta código Java.
```
1. Haz clic en "☕ Java"
2. Escribe o pega tu código Java (clase con main)
3. Se compilará y ejecutará con timeout de 10 segundos
4. Verás la salida del programa
```
> Requiere Java (JDK) instalado en el sistema.

#### Ejecutar Comando del Sistema
**Qué hace:** Ejecuta un comando en la terminal del sistema.
```
1. Haz clic en "💻 CMD"
2. Introduce el comando que deseas ejecutar
3. Se ejecutará con timeout de 15 segundos
4. Verás la salida del comando
```
> ⚠️ Ten cuidado con los comandos que ejecutas.

### 💾 Herramientas de Memoria

#### Guardar Nota/Hecho
**Qué hace:** Guarda información en la memoria persistente.
```
1. Haz clic en "💾 Nota"
2. Para guardar una nota con clave: escribe "clave=valor" 
   Ejemplo: "email=juan@correo.com"
3. Para guardar un hecho: escribe solo el texto
   Ejemplo: "El proyecto usa Python 3.11"
```

#### Ver Notas
**Qué hace:** Lista todas las notas guardadas (clave-valor).
```
1. Haz clic en "📖 Notas"
2. Se mostrarán todas las notas con sus claves y valores
```

#### Ver Hechos
**Qué hace:** Muestra los hechos guardados en memoria.
```
1. Haz clic en "🧠 Hechos"
2. Se mostrarán los últimos 50 hechos (con filtro opcional)
```

#### Limpiar Memoria
**Qué hace:** Borra todos los hechos y notas almacenados.
```
1. Haz clic en "🗑 Limpiar"
2. Se eliminará todo el contenido de la memoria
```
> ⚠️ Esta acción es irreversible.

---

## 11. Gestión de Modelos de IA

### Ver Modelos Instalados

**Paso 1:** Haz clic en el botón **"📋 Modelos"** en la barra superior.

**Paso 2:** Se mostrará la lista de todos los modelos de Ollama instalados en tu sistema con su tamaño y versión.

### Descargar Nuevos Modelos

**Paso 1:** Haz clic en el botón **"⬇️ Pull"** en la barra superior.

**Paso 2:** Selecciona el modelo que deseas descargar del menú desplegable:

| Modelo | Tamaño | Especialidad |
|--------|--------|--------------|
| **phi3** | ~2.3 GB | Modelo ligero, rápido (por defecto) |
| **deepseek-r1** | ~4.7 GB | Razonamiento superior |
| **qwen3** | ~4.6 GB | Propósito general |
| **qwen3-coder** | ~4.6 GB | Especialista en código |
| **mistral** | ~4.1 GB | Redacción y escritura |
| **codestral** | ~12 GB | Código avanzado (necesita mucha RAM) |
| **glm4** | ~5.5 GB | Multimodal |

**Paso 3:** Espera a que se descargue. El progreso se mostrará en la interfaz.

> **💡 Consejo sobre RAM:**
> - **4 GB RAM:** Solo phi3
> - **8 GB RAM:** phi3 + deepseek-r1 o mistral
> - **16 GB+ RAM:** Todos los modelos

### Sistema de Fallback (Respaldo)
Si un agente necesita un modelo que no está instalado, automáticamente usará uno alternativo:

```
Agente de Código:   qwen3-coder → codestral → phi3 (último recurso)
Agente Orquestador: deepseek-r1 → phi3
Agente Redacción:   mistral → phi3
```

---

## 12. Sistema de Memoria Persistente

NEXUS OMNI AI incluye un sistema de memoria que **persiste entre sesiones**.

### Tipos de Memoria

#### 📝 Notas (Clave-Valor)
Almacena información estructurada como pares clave-valor.
```
Ejemplo:
  nombre = "Juan García"
  proyecto = "Sistema de Inventario"
  lenguaje = "Python"
```

#### 📋 Hechos (Lista)
Almacena datos como una lista de hechos relevantes.
```
Ejemplo:
  - "El usuario prefiere Python sobre JavaScript"
  - "El proyecto debe estar listo para marzo"
  - "Se usa PostgreSQL como base de datos"
```

### Cómo Usar la Memoria

**Guardar una nota:**
1. Ve a la pestaña **"🔧 MCP Tools"**.
2. Haz clic en **"💾 Nota"**.
3. Escribe en formato `clave=valor`:
   ```
   tecnologia_preferida=React
   ```

**Guardar un hecho:**
1. Ve a la pestaña **"🔧 MCP Tools"**.
2. Haz clic en **"💾 Nota"**.
3. Escribe el hecho directamente (sin el formato `clave=valor`):
   ```
   El cliente necesita soporte para dispositivos móviles
   ```

**Consultar notas:**
1. Haz clic en **"📖 Notas"** para ver todas las notas almacenadas.

**Consultar hechos:**
1. Haz clic en **"🧠 Hechos"** para ver los últimos 50 hechos.

**Limpiar memoria:**
1. Haz clic en **"🗑 Limpiar"** para borrar toda la memoria.

### Dónde se Almacena
La memoria se guarda en el archivo:
```
NEXUS_OMNI_AI/app/memory/memoria.json
```

**Estructura del archivo:**
```json
{
  "notas": {
    "nombre": "Juan",
    "proyecto": "Mi App",
    "tecnologia": "React"
  },
  "hechos": [
    "El usuario trabaja con Python",
    "El proyecto tiene deadline en marzo",
    "Se necesita base de datos PostgreSQL"
  ]
}
```

**Límites:**
- **Notas:** Sin límite (clave-valor ilimitadas)
- **Hechos:** Se conservan los últimos 200 (los más antiguos se eliminan automáticamente)

---

## 13. Guardar y Exportar Conversaciones

### Paso a Paso

**Paso 1:** Haz clic en el botón **"💾 Guardar"** en la barra superior.

**Paso 2:** Se abrirá un cuadro de diálogo "Guardar como".

**Paso 3:** Elige la ubicación y el nombre del archivo (formato `.txt`).

**Paso 4:** Haz clic en **"Guardar"**.

### ¿Qué se Guarda?
El archivo exportado incluye **todo el contenido** de la sesión:

```
═══════════════════════════════════════
 CHAT
═══════════════════════════════════════
[Todo el historial del Chat Principal]

═══════════════════════════════════════
 🎯 Orquestador
═══════════════════════════════════════
[Respuesta completa del Orquestador]

═══════════════════════════════════════
 💻 Código
═══════════════════════════════════════
[Todo el código generado]

═══════════════════════════════════════
 🧠 Razonamiento
═══════════════════════════════════════
[Análisis lógico completo]

═══════════════════════════════════════
 ✍️ Redacción
═══════════════════════════════════════
[Textos generados]

═══════════════════════════════════════
 📊 Datos
═══════════════════════════════════════
[Análisis de datos]

═══════════════════════════════════════
 🔍 Investigación
═══════════════════════════════════════
[Resultados de investigación]

═══════════════════════════════════════
 🔗 Integrador
═══════════════════════════════════════
[Respuesta final integrada]
```

---

## 14. Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| **Ctrl + Enter** | Enviar mensaje a todos los agentes |
| **Tab** | Insertar tabulación en campos de texto |
| **Clic en pestaña** | Cambiar entre agentes/herramientas |

---

## 15. Solución de Problemas

### Problemas de Instalación

| Problema | Solución |
|----------|----------|
| **"Python no encontrado"** | El instalador `.bat` descargará Python 3.11 automáticamente. Si falla, instala Python 3.11 manualmente desde [python.org](https://python.org) |
| **"Ollama no encontrado"** | El instalador lo descarga automáticamente. Si falla, instala Ollama manualmente desde [ollama.com](https://ollama.com) |
| **Error en paquetes** | Ejecuta el `.bat` nuevamente; forzará la reinstalación de dependencias críticas |
| **PyInstaller falla** | Asegúrate de tener suficiente espacio en disco (~2 GB libres) |

### Problemas al Usar la Aplicación

| Problema | Solución |
|----------|----------|
| **"Ollama no conectado"** | Abre una terminal y ejecuta `ollama serve`. Espera unos segundos y reinicia la app |
| **Agente muestra error de modelo** | El modelo necesario no está instalado. Haz clic en "⬇️ Pull" y descarga el modelo indicado |
| **Respuesta muy lenta** | Usa modelos más pequeños (phi3). Cierra otras aplicaciones para liberar RAM |
| **La app no responde** | Los agentes trabajan en paralelo y pueden tardar. Espera a que el botón vuelva a "Enviar ▶" |

### Problemas con Funciones Específicas

| Problema | Solución |
|----------|----------|
| **No hay audio (TTS)** | Verifica el volumen de los altavoces. Asegúrate de que pyttsx3 esté instalado |
| **STT dice "Sin conexión"** | El reconocimiento de voz necesita internet. Verifica tu conexión. Asegúrate de que el micrófono esté conectado |
| **RAG: "Sin documentos indexados"** | Debes indexar al menos un documento primero usando "📂 Indexar" |
| **Imagen: generación muy lenta** | Es normal en CPU (1-5 min). Si tienes GPU NVIDIA, el sistema la usará automáticamente |
| **Imagen: error de memoria** | Reduce los pasos a 10-15 o cierra otras aplicaciones para liberar RAM |

### Verificaciones Rápidas

Si algo no funciona, verifica lo siguiente:

```bash
# ¿Ollama está funcionando?
ollama list

# ¿Qué modelos tienes instalados?
ollama list

# ¿Tienes el modelo por defecto?
ollama run phi3 "hola"

# ¿Los archivos de la app existen?
dir %USERPROFILE%\Desktop\NEXUS_OMNI_AI\app\dist\
```

---

## 16. Preguntas Frecuentes (FAQ)

### General

**P: ¿Necesito internet para usar NEXUS OMNI AI?**  
R: No, después de la instalación funciona 100% offline. Solo necesitas internet para: búsqueda web (🔍 Investigación), reconocimiento de voz (STT) y descargar nuevos modelos.

**P: ¿Cuánto espacio ocupa la instalación completa?**  
R: Con el modelo phi3 (por defecto), aproximadamente 5 GB. Con todos los modelos instalados, puede llegar a 30-40 GB.

**P: ¿Puedo usar la app en Mac o Linux?**  
R: El instalador automático (.bat) es exclusivo de Windows. Sin embargo, el script Python puede adaptarse a otros sistemas operativos con modificaciones manuales.

### Sobre los Agentes

**P: ¿Puedo usar un solo agente en vez de todos?**  
R: Actualmente, al enviar una consulta, todos los agentes trabajan en paralelo. Sin embargo, puedes ver la respuesta individual de cada agente en su pestaña correspondiente.

**P: ¿Qué pasa si un agente falla?**  
R: El sistema tiene un mecanismo de fallback. Si el modelo preferido de un agente no está disponible, usará automáticamente un modelo alternativo (generalmente phi3).

**P: ¿Por qué algunos agentes tardan más que otros?**  
R: Cada agente usa un motor y modelo diferente. Los modelos más grandes (como codestral a 12 GB) producen mejores resultados pero tardan más.

### Sobre Modelos

**P: ¿Cuál es el mejor modelo para empezar?**  
R: Phi3 es el modelo por defecto y funciona bien para la mayoría de tareas. Si tienes suficiente RAM (8 GB+), agrega deepseek-r1 para mejor razonamiento.

**P: ¿Puedo usar modelos que no están en la lista?**  
R: Sí, puedes instalar cualquier modelo compatible con Ollama ejecutando `ollama pull nombre_modelo` en la terminal.

### Sobre Datos y Privacidad

**P: ¿Mis datos salen de mi computadora?**  
R: No. Todo el procesamiento de IA se realiza localmente en tu máquina. Las únicas excepciones son la búsqueda web (DuckDuckGo) y el reconocimiento de voz (Google API), que requieren enviar datos a servidores externos.

**P: ¿Cómo borro mis datos?**  
R: Puedes borrar la memoria persistente desde "🔧 MCP Tools" → "🗑 Limpiar". Para borrar documentos indexados, elimina la carpeta `app/memory/rag_db/`. Para borrar imágenes generadas, elimina los archivos en `app/imagenes_generadas/`.

---

## 🎯 Resumen de Flujo de Trabajo Recomendado

```
1. 🚀 Inicia NEXUS OMNI AI
2. ✅ Verifica que Ollama está conectado (barra superior)
3. 📝 Escribe tu consulta en el campo de texto
4. ⏎  Presiona Ctrl+Enter para enviar
5. 👀 Observa los agentes trabajando en las pestañas
6. 📖 Lee la respuesta integrada en el Chat Principal
7. 🔍 Revisa respuestas individuales si necesitas detalle
8. 💾 Guarda la conversación si es importante
9. 🔄 Repite con nuevas consultas
```

### Para tareas especializadas:
- **Necesitas código** → Revisa la pestaña 💻 Código
- **Necesitas análisis** → Revisa la pestaña 🧠 Razonamiento
- **Necesitas documentos** → Usa 📚 RAG Docs para indexar y buscar
- **Necesitas imágenes** → Usa 🎨 Imagen SD
- **Necesitas dictar** → Usa 🎙️ Voz para hablar
- **Necesitas automatizar** → Usa 🔧 MCP Tools

---

> **📌 Versión del Manual:** 1.0  
> **📌 Versión de la Aplicación:** NEXUS OMNI Multi-Agente IA v4.0  
> **📌 Última Actualización:** Marzo 2026
