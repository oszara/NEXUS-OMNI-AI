"""
╔══════════════════════════════════════════════════════════════╗
║       NEXUS OMNI MULTI AI OFFLINE v4.0 — INSTALADOR         ║
║  Diagnóstico + Instalación + Compilación + Installer .exe    ║
║  ✅ INSTALACIÓN AUTOMÁTICA — SIN PREGUNTAS                   ║
╚══════════════════════════════════════════════════════════════╝
Ejecuta con CUALQUIER versión de Python:
    python NEXUS_OMNI_AI_OFFLINE_MULTI.py
"""
import os, sys, subprocess, platform, shutil, json, urllib.request
import importlib.util, time, threading
from pathlib import Path
from datetime import datetime

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ════════════════════════════════════════════════════════════════
CFG = {
    "nombre_app":       "NEXUS OMNI Multi-Agente IA",
    "version":          "4.0",
    "publisher":        "NEXUS AI Labs",
    "nombre_exe":       "nexus_omni.exe",
    "nombre_installer": "NEXUS_OMNI_MultiAgente_v4_Setup",
    "modelo_default":   "phi3",
    "python_compat":    [(3,10),(3,11),(3,12)],
    "base_dir":         os.path.join(os.path.expanduser("~"), "Desktop", "NEXUS_OMNI_AI"),
}
CFG["app_dir"]       = os.path.join(CFG["base_dir"], "app")
CFG["installer_dir"] = os.path.join(CFG["base_dir"], "installer")
CFG["output_dir"]    = os.path.join(CFG["base_dir"], "output")
CFG["dist_dir"]      = os.path.join(CFG["app_dir"],  "dist")
CFG["venv_dir"]      = os.path.join(CFG["base_dir"], "venv")
CFG["mcp_dir"]       = os.path.join(CFG["app_dir"],  "mcp_servers")
CFG["exe_name"]      = CFG["nombre_exe"]  # alias para referencias internas

SEP  = "═" * 65
SEP2 = "─" * 65

# ════════════════════════════════════════════════════════════════
# COLORES ANSI
# ════════════════════════════════════════════════════════════════
class C:
    OK   = "\033[92m";  WARN = "\033[93m"; ERR  = "\033[91m"
    CYAN = "\033[96m";  BLUE = "\033[94m"; MAG  = "\033[95m"
    BOLD = "\033[1m";   DIM  = "\033[2m";  RESET= "\033[0m"

def _ok(m):    print(f"  {C.OK}✅ {m}{C.RESET}")
def _warn(m):  print(f"  {C.WARN}⚠️  {m}{C.RESET}")
def _err(m):   print(f"  {C.ERR}❌ {m}{C.RESET}")
def _info(m):  print(f"  {C.CYAN}ℹ️  {m}{C.RESET}")
def _step(n,t,total): print(f"\n{C.BOLD}{C.BLUE}{SEP}\n  PASO {n}/{total} — {t}\n{SEP}{C.RESET}")
def _sub(t):   print(f"\n{C.CYAN}{SEP2}\n  {t}\n{SEP2}{C.RESET}")

# ════════════════════════════════════════════════════════════════
# ESTADO GLOBAL DEL SISTEMA
# ════════════════════════════════════════════════════════════════
class Sistema:
    python_exe       = sys.executable
    python_compat    = False
    ram_gb           = 0
    disco_gb         = 0
    cuda             = False
    ollama_ok        = False
    ollama_corriendo = False
    modelos_ollama   = []
    herramientas     = {}
    pkgs_ok          = []
    pkgs_faltantes   = []
    score            = 0

S = Sistema()

# ════════════════════════════════════════════════════════════════
# PAQUETES REQUERIDOS
# ════════════════════════════════════════════════════════════════
PAQUETES = {
    # pip_name                    : (import_name,          grupo,      critico)
    "pillow":                       ("PIL",                 "Core",     True),
    "pyinstaller":                  ("PyInstaller",         "Core",     True),
    "requests":                     ("requests",            "Core",     True),
    "ollama":                       ("ollama",              "Core",     True),
    "crewai":                        ("crewai",              "Agentes",  False),
    "langchain":                     ("langchain",           "Agentes",  False),
    "langchain-ollama":              ("langchain_ollama",    "Agentes",  False),
    "langchain-community":           ("langchain_community", "Agentes",  False),
    "langgraph":                     ("langgraph",           "Agentes",  False),
    "ag2":                           ("autogen",             "Agentes",  False),
    "mcp":                          ("mcp",                 "Agentes",  False),
    "diffusers":                    ("diffusers",           "Imagen",   False),
    "transformers":                 ("transformers",        "Imagen",   False),
    "accelerate":                   ("accelerate",          "Imagen",   False),
    "safetensors":                  ("safetensors",         "Imagen",   False),
    "chromadb":                     ("chromadb",            "RAG",      False),
    "sentence-transformers":        ("sentence_transformers","RAG",     False),
    "pypdf":                        ("pypdf",               "RAG",      False),
    "python-docx":                  ("docx",                "RAG",      False),
    "pyttsx3":                      ("pyttsx3",             "Voz",      False),
    "SpeechRecognition":            ("speech_recognition",  "Voz",      False),
    "psutil":                       ("psutil",              "Utils",    True),
    "pydantic":                     ("pydantic",            "Utils",    True),
    "rich":                         ("rich",                "Utils",    False),
    "python-dotenv":                ("dotenv",              "Utils",    False),
}

MODELOS_OLLAMA = {
    "phi3":        2.3,   # GB aprox
    "deepseek-r1": 4.7,
    "qwen3":       4.6,
    "qwen3-coder": 4.6,
    "mistral":     4.1,
    "codestral":   12.0,
    "glm4":        5.5,
}

HERRAMIENTAS_SYS = {
    "ollama": ["ollama", "--version"],
    "java":   ["java",   "-version"],
    "javac":  ["javac",  "-version"],
    "git":    ["git",    "--version"],
}

# ════════════════════════════════════════════════════════════════
# ── FASE A: DIAGNÓSTICO ──────────────────────────────────────
# ════════════════════════════════════════════════════════════════

def diag_python():
    _sub("🐍 Python")
    v = sys.version_info
    S.python_compat = (v.major, v.minor) in CFG["python_compat"]
    _ok(f"Python {v.major}.{v.minor}.{v.micro}") if S.python_compat else _warn(f"Python {v.major}.{v.minor} — necesita 3.10-3.12")

    if not S.python_compat:
        # Buscar versión compatible
        candidatos = []
        u = os.environ.get("USERNAME","")
        for vv in ["311","310","312"]:
            candidatos += [
                rf"C:\Python3{vv[1:]}\python.exe",
                rf"C:\Users\{u}\AppData\Local\Programs\Python\Python{vv}\python.exe",
                f"py -3.{vv[1:]}",
            ]
        for cand in candidatos:
            try:
                r = subprocess.run(
                    f'"{cand}" -c "import sys;v=sys.version_info;print(v.major,v.minor,sys.executable)"',
                    shell=True, capture_output=True, text=True, timeout=4
                )
                if r.returncode == 0:
                    parts = r.stdout.strip().split()
                    if len(parts) >= 3:
                        maj, min_, exe = int(parts[0]), int(parts[1]), parts[2]
                        if (maj, min_) in CFG["python_compat"]:
                            S.python_exe = exe
                            S.python_compat = True
                            _ok(f"Encontrado Python {maj}.{min_} → {exe}")
                            return
            except Exception: pass
        _err("No se encontró Python 3.10-3.12. Descarga: https://www.python.org/downloads/release/python-3119/")

def diag_hardware():
    _sub("💻 Hardware")
    # Asegurar psutil
    try: import psutil
    except ImportError:
        subprocess.run(f'"{S.python_exe}" -m pip install psutil --quiet', shell=True)
        import psutil

    mem = psutil.virtual_memory()
    S.ram_gb = round(mem.total / 1e9, 1)
    dis = psutil.disk_usage(os.path.expanduser("~"))
    S.disco_gb = round(dis.free / 1e9, 1)

    color = C.OK if S.ram_gb >= 8 else C.WARN
    print(f"  {color}💾 RAM: {S.ram_gb} GB  |  Disco libre: {S.disco_gb} GB{C.RESET}")
    print(f"  {C.DIM}🖥  CPU: {platform.processor()[:55]}{C.RESET}")

    # GPU
    try:
        import torch
        S.cuda = torch.cuda.is_available()
        if S.cuda:
            _ok(f"GPU CUDA: {torch.cuda.get_device_name(0)}")
        else:
            _warn("Sin GPU CUDA — Stable Diffusion usará CPU")
    except ImportError:
        try:
            r = subprocess.run(["nvidia-smi","--query-gpu=name","--format=csv,noheader"],
                               capture_output=True,text=True,timeout=5)
            if r.returncode == 0 and r.stdout.strip():
                S.cuda = True; _ok(f"GPU detectada: {r.stdout.strip()}")
            else:
                _warn("Sin GPU CUDA detectada")
        except Exception:
            _warn("Sin GPU CUDA")

    # Modelos que caben
    print(f"\n  {C.BOLD}Modelos que caben con {S.ram_gb} GB RAM:{C.RESET}")
    for m, gb in MODELOS_OLLAMA.items():
        if gb <= S.ram_gb * 0.7:
            print(f"    {C.OK}✔ {m:<18} (~{gb} GB){C.RESET}")
        elif gb <= S.ram_gb:
            print(f"    {C.WARN}~ {m:<18} (~{gb} GB) justo{C.RESET}")
        else:
            print(f"    {C.DIM}✗ {m:<18} (~{gb} GB) insuficiente{C.RESET}")

def diag_herramientas():
    _sub("🔧 Herramientas del sistema")
    for nombre, cmd in HERRAMIENTAS_SYS.items():
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            salida = (r.stdout + r.stderr).strip().split("\n")[0][:55]
            if r.returncode == 0 or salida:
                _ok(f"{nombre:<10} {salida}"); S.herramientas[nombre] = True
            else:
                _warn(f"{nombre:<10} no responde"); S.herramientas[nombre] = False
        except FileNotFoundError:
            _err(f"{nombre:<10} NO instalado"); S.herramientas[nombre] = False
        except Exception as e:
            _warn(f"{nombre:<10} error: {e}"); S.herramientas[nombre] = False

    S.ollama_ok = S.herramientas.get("ollama", False)

def diag_ollama():
    _sub("🤖 Ollama — servicio y modelos")
    if not S.ollama_ok:
        _err("Ollama no instalado"); return
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=3)
        S.ollama_corriendo = True; _ok("Ollama API corriendo en :11434")
    except Exception:
        _warn("Ollama instalado pero NO corriendo (ejecuta: ollama serve)")
    try:
        r = subprocess.run(["ollama","list"], capture_output=True, text=True, timeout=8)
        lineas = [l for l in r.stdout.strip().split("\n")[1:] if l.strip()]
        S.modelos_ollama = [l.split()[0] for l in lineas if l.split()]
        if S.modelos_ollama:
            _ok(f"{len(S.modelos_ollama)} modelos instalados: {', '.join(S.modelos_ollama)}")
        else:
            _warn("Sin modelos. Se descargará el básico durante la instalación.")
    except Exception:
        _warn("No se pudo listar modelos")

def diag_paquetes():
    _sub("📦 Paquetes Python")
    S.pkgs_ok.clear(); S.pkgs_faltantes.clear()
    grupos_ok = {}; grupos_fal = {}
    for pip_name,(import_name,grupo,_) in PAQUETES.items():
        try:
            r = subprocess.run(
                f'"{S.python_exe}" -c "import {import_name}; '
                f'v=getattr(__import__(\"{import_name}\"),\"__version__\",\"?\"); print(v)"',
                shell=True, capture_output=True, text=True, timeout=6
            )
            if r.returncode == 0:
                ver = r.stdout.strip() or "?"
                S.pkgs_ok.append(pip_name)
                grupos_ok.setdefault(grupo,[]).append((pip_name,ver))
            else:
                S.pkgs_faltantes.append(pip_name)
                grupos_fal.setdefault(grupo,[]).append(pip_name)
        except Exception:
            S.pkgs_faltantes.append(pip_name)
            grupos_fal.setdefault(grupo,[]).append(pip_name)

    for grupo in ["Core","Agentes","Imagen","RAG","Voz","Utils"]:
        ok_list  = grupos_ok.get(grupo,[])
        fal_list = grupos_fal.get(grupo,[])
        if ok_list or fal_list:
            print(f"\n  {C.BOLD}  [{grupo}]{C.RESET}")
            for pkg,ver in ok_list:  print(f"    {C.OK}✔ {pkg:<40} v{ver}{C.RESET}")
            for pkg    in fal_list:  print(f"    {C.ERR}✗ {pkg:<40} FALTA{C.RESET}")

    total = len(PAQUETES)
    print(f"\n  {C.BOLD}{len(S.pkgs_ok)}/{total} instalados  |  {len(S.pkgs_faltantes)} faltantes{C.RESET}")

def calcular_score():
    puntos = sum([
        S.python_compat,
        len(S.pkgs_ok) >= 10,
        S.ollama_ok,
        S.ollama_corriendo,
        len(S.modelos_ollama) > 0,
        S.disco_gb >= 10,
        S.ram_gb >= 4,
    ])
    S.score = int((puntos / 7) * 100)

def mostrar_score():
    barra = "█" * int(S.score/10) + "░" * (10-int(S.score/10))
    color = C.OK if S.score>=80 else (C.WARN if S.score>=50 else C.ERR)
    print(f"\n  {C.BOLD}Diagnóstico: {color}[{barra}] {S.score}%{C.RESET}")

# ════════════════════════════════════════════════════════════════
# ── FASE B: INSTALACIÓN INTELIGENTE ─────────────────────────
# ════════════════════════════════════════════════════════════════

def instalar_ollama_si_falta():
    if S.ollama_ok: return
    _sub("⬇️ Instalando Ollama (AUTOMÁTICO)")
    _info("Ollama no encontrado. Descargando e instalando automáticamente...")
    url  = "https://ollama.com/download/OllamaSetup.exe"
    dest = os.path.join(os.environ.get("TEMP","."),"OllamaSetup.exe")
    print(f"  {C.CYAN}⏳ Descargando Ollama...{C.RESET}", end="", flush=True)

    def _progreso(b, bs, ts):
        if ts > 0:
            pct = min(100, int(b*bs*100/ts))
            print(f"\r  {C.CYAN}⏳ Descargando Ollama... {pct}%{C.RESET}", end="", flush=True)

    try:
        urllib.request.urlretrieve(url, dest, _progreso)
        print()
        _info("Instalando Ollama (puede pedir permisos de administrador)...")
        subprocess.run([dest, "/SILENT"], check=True)
        _ok("Ollama instalado correctamente")
        S.ollama_ok = True
        time.sleep(2)
        subprocess.Popen(["ollama","serve"], creationflags=0x00000008)
        time.sleep(3)
        S.ollama_corriendo = True
    except Exception as e:
        _err(f"Error instalando Ollama: {e}")
        _info("Instala manualmente desde: https://ollama.com/download")

def gestionar_venv():
    _sub("🔧 Entorno Virtual Python")
    v = sys.version_info
    if (v.major, v.minor) in CFG["python_compat"]:
        _ok(f"Python {v.major}.{v.minor} es compatible — usando Python actual")
        return

    if not S.python_compat:
        _err("Sin Python compatible. Instala Python 3.11 y vuelve a ejecutar.")
        _info("https://www.python.org/downloads/release/python-3119/")
        sys.exit(1)

    venv_python = os.path.join(CFG["venv_dir"], "Scripts", "python.exe")
    if os.path.exists(venv_python):
        _ok(f"Entorno virtual ya existe: {CFG['venv_dir']}")
        S.python_exe = venv_python
        return

    _info(f"Creando entorno virtual con {S.python_exe}...")
    os.makedirs(CFG["venv_dir"], exist_ok=True)
    r = subprocess.run(f'"{S.python_exe}" -m venv "{CFG["venv_dir"]}"', shell=True)
    if r.returncode == 0 and os.path.exists(venv_python):
        subprocess.run(f'"{venv_python}" -m pip install pip --upgrade --quiet', shell=True)
        S.python_exe = venv_python
        _ok("Entorno virtual creado y listo")
    else:
        _err("No se pudo crear el entorno virtual")

def instalar_paquetes():
    _sub("Instalando paquetes faltantes (AUTOMATICO)")
    if not S.pkgs_faltantes:
        _ok("Todos los paquetes ya estan instalados"); return

    criticos  = [p for p in S.pkgs_faltantes if PAQUETES.get(p,(None,None,False))[2]]
    opcionales= [p for p in S.pkgs_faltantes if not PAQUETES.get(p,(None,None,False))[2]]

    print(f"\n  {C.BOLD}Paquetes a instalar ({len(S.pkgs_faltantes)} total):{C.RESET}")
    if criticos:
        print(f"  {C.ERR}  Criticos ({len(criticos)}): {', '.join(p.split('==')[0] for p in criticos)}{C.RESET}")
    if opcionales:
        print(f"  {C.WARN}  Opcionales ({len(opcionales)}): {', '.join(p.split('==')[0] for p in opcionales)}{C.RESET}")

    _info("Instalando TODOS los paquetes automaticamente...")

    # Actualizar pip primero
    subprocess.run(
        f'"{S.python_exe}" -m pip install pip wheel setuptools --upgrade --quiet',
        shell=True
    )

    # Mapa de alternativas para paquetes con nombres cambiados
    ALTERNATIVAS = {
        "ag2":       ["ag2", "autogen-agentchat", "pyautogen"],
        "crewai":    ["crewai"],
    }

    a_instalar = S.pkgs_faltantes
    fallidos = []
    for i, pkg in enumerate(a_instalar, 1):
        nombre = pkg.split("==")[0].split(">=")[0].split("<=")[0]
        print(f"  [{i:02d}/{len(a_instalar):02d}] {C.CYAN}Instalando {nombre:<30}{C.RESET}", end="", flush=True)

        # Comando especial para torch
        if nombre == "torch":
            idx_url = ("https://download.pytorch.org/whl/cu121" if S.cuda
                       else "https://download.pytorch.org/whl/cpu")
            cmd = f'"{S.python_exe}" -m pip install torch --index-url {idx_url} --quiet --timeout 300'
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if r.returncode == 0:
                print(f"  {C.OK}OK{C.RESET}")
            else:
                print(f"  {C.ERR}FALLO{C.RESET}")
                fallidos.append(nombre)
            continue

        # Intentar alternativas para paquetes con nombres cambiados
        alts = ALTERNATIVAS.get(nombre, [nombre])
        instalado = False
        for alt in alts:
            r = subprocess.run(
                f'"{S.python_exe}" -m pip install "{alt}" --quiet --timeout 300',
                shell=True, capture_output=True, text=True
            )
            if r.returncode == 0:
                print(f"  {C.OK}OK ({alt}){C.RESET}")
                instalado = True
                break

        if not instalado:
            print(f"  {C.ERR}FALLO{C.RESET}")
            fallidos.append(nombre)

    if fallidos:
        _warn(f"No se pudieron instalar (opcionales): {', '.join(fallidos)}")
        _info("La app funcionara sin ellos con fallback a Ollama directo")
    else:
        _ok("Todos los paquetes instalados correctamente")

def instalar_modelos_ollama():
    _sub("🤖 Modelos Ollama (AUTOMÁTICO)")
    if not S.ollama_ok:
        _warn("Ollama no disponible, omitiendo modelos"); return

    ya = set(m.split(":")[0] for m in S.modelos_ollama)

    # Si ya hay modelos, no instalar nada
    if ya:
        _ok(f"Modelos ya instalados: {', '.join(ya)}"); return

    disponibles = [(m, gb) for m, gb in MODELOS_OLLAMA.items()
                   if m not in ya and gb <= S.ram_gb * 0.75]

    if not disponibles:
        _ok("Los modelos recomendados para tu hardware ya están instalados"); return

    print(f"\n  {C.BOLD}Modelos disponibles para tu hardware ({S.ram_gb} GB RAM):{C.RESET}")
    for i, (m, gb) in enumerate(disponibles, 1):
        desc = {
            "phi3":        "Rápido, ligero, ideal para empezar",
            "deepseek-r1": "Razonamiento superior",
            "qwen3":       "General y análisis de datos",
            "qwen3-coder": "Especialista en código",
            "mistral":     "Redacción y textos",
            "codestral":   "Código avanzado",
            "glm4":        "Multimodal",
        }.get(m,"")
        print(f"    {C.CYAN}{i}.{C.RESET} {m:<18} ~{gb} GB  — {desc}")

    # Instalar automáticamente phi3 como modelo base mínimo
    a_descargar = []
    for m, gb in disponibles:
        if m == "phi3":
            a_descargar.append(m)
            break
    if not a_descargar and disponibles:
        # phi3 no disponible (muy poca RAM?), tomar el más pequeño
        a_descargar = [min(disponibles, key=lambda x: x[1])[0]]

    _info(f"Instalando modelo base automáticamente: {', '.join(a_descargar)}")
    _info("(Puedes descargar más modelos desde la app con el botón ⬇️ Pull)")

    for modelo in a_descargar:
        print(f"\n  {C.CYAN}⏳ ollama pull {modelo} ...{C.RESET}")
        r = subprocess.run(["ollama","pull",modelo])
        _ok(f"{modelo} listo") if r.returncode == 0 else _err(f"Error en {modelo}")
        if r.returncode == 0:
            S.modelos_ollama.append(modelo)

# ════════════════════════════════════════════════════════════════
# ── FASE C: CONSTRUCCIÓN DE LA APP ───────────────────────────
# ════════════════════════════════════════════════════════════════

def crear_carpetas():
    _sub("📁 Creando estructura de carpetas")
    for c in [
        CFG["base_dir"], CFG["app_dir"], CFG["installer_dir"],
        CFG["output_dir"], CFG["mcp_dir"],
        os.path.join(CFG["app_dir"],"memory"),
        os.path.join(CFG["app_dir"],"exports"),
        os.path.join(CFG["app_dir"],"imagenes_generadas"),
        os.path.join(CFG["app_dir"],"documentos_rag"),
        os.path.join(CFG["app_dir"],"sd_models"),
    ]:
        os.makedirs(c, exist_ok=True)
        print(f"  {C.DIM}  ✔ {c}{C.RESET}")
    _ok("Carpetas creadas")

def crear_mcp_servers():
    _sub("🔧 Creando servidores MCP")

    archivos = {}

    archivos["mcp_files.py"] = '''import os,json,sys
def leer_archivo(ruta):
    try:
        with open(ruta,"r",encoding="utf-8") as f: return f.read()
    except Exception as e: return f"Error: {e}"
def escribir_archivo(ruta,contenido):
    try:
        os.makedirs(os.path.dirname(ruta) or ".",exist_ok=True)
        with open(ruta,"w",encoding="utf-8") as f: f.write(contenido)
        return f"Escrito: {ruta}"
    except Exception as e: return f"Error: {e}"
def listar_directorio(ruta="."):
    try: return "\\n".join(os.listdir(ruta))
    except Exception as e: return f"Error: {e}"
def buscar_en_archivos(directorio,patron):
    res=[]
    try:
        for root,_,files in os.walk(directorio):
            for fname in files:
                fp=os.path.join(root,fname)
                try:
                    with open(fp,"r",encoding="utf-8",errors="ignore") as f:
                        for i,line in enumerate(f,1):
                            if patron.lower() in line.lower():
                                res.append(f"{fp}:{i}: {line.strip()}")
                except: pass
    except Exception as e: return f"Error: {e}"
    return "\\n".join(res[:50]) or "Sin resultados"
TOOLS={"leer_archivo":leer_archivo,"escribir_archivo":escribir_archivo,
       "listar_directorio":listar_directorio,"buscar_en_archivos":buscar_en_archivos}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_web.py"] = '''import urllib.request,urllib.parse,json,sys
def buscar_web(query,max_resultados=5):
    try:
        url="https://api.duckduckgo.com/?q="+urllib.parse.quote(query)+"&format=json&no_html=1"
        with urllib.request.urlopen(url,timeout=8) as r: data=json.loads(r.read().decode())
        res=[]
        if data.get("AbstractText"): res.append(f"Resumen: {data['AbstractText']}")
        for item in data.get("RelatedTopics",[])[:max_resultados]:
            if isinstance(item,dict) and item.get("Text"): res.append(f"• {item['Text']}")
        return "\\n".join(res) if res else "Sin resultados."
    except Exception as e: return f"Error: {e}"
def verificar_internet():
    try: urllib.request.urlopen("https://www.google.com",timeout=3); return "Conectado"
    except: return "Sin conexión"
TOOLS={"buscar_web":buscar_web,"verificar_internet":verificar_internet}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_code.py"] = '''import subprocess,sys,os,json,tempfile
def ejecutar_python(codigo):
    try:
        r=subprocess.run([sys.executable,"-c",codigo],capture_output=True,text=True,timeout=15)
        return r.stdout or r.stderr or "(sin output)"
    except subprocess.TimeoutExpired: return "Timeout 15s"
    except Exception as e: return f"Error: {e}"
def ejecutar_java(codigo):
    try:
        d=tempfile.mkdtemp(); fp=os.path.join(d,"Main.java")
        with open(fp,"w") as f:
            f.write(f"public class Main{{\\n  public static void main(String[] args){{\\n    {codigo}\\n  }}\\n}}")
        r1=subprocess.run(["javac",fp],capture_output=True,text=True)
        if r1.returncode!=0: return f"Error javac:\\n{r1.stderr}"
        r2=subprocess.run(["java","-cp",d,"Main"],capture_output=True,text=True,timeout=10)
        return r2.stdout or r2.stderr or "(sin output)"
    except FileNotFoundError: return "Java no encontrado. Instala JDK."
    except Exception as e: return f"Error: {e}"
def ejecutar_cmd(comando):
    try:
        r=subprocess.run(comando,shell=True,capture_output=True,text=True,timeout=15)
        return r.stdout or r.stderr or "(sin output)"
    except Exception as e: return f"Error: {e}"
TOOLS={"ejecutar_python":ejecutar_python,"ejecutar_java":ejecutar_java,"ejecutar_cmd":ejecutar_cmd}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_image.py"] = '''import sys,os,json,importlib
def generar_imagen(prompt,modelo="runwayml/stable-diffusion-v1-5",
                   ancho=512,alto=512,pasos=20,ruta_salida="imagen.png"):
    if not importlib.util.find_spec("diffusers"):
        return "ERROR: pip install diffusers torch"
    try:
        import torch
        from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler
        device="cuda" if torch.cuda.is_available() else "cpu"
        dtype=torch.float16 if device=="cuda" else torch.float32
        base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        local=os.path.join(base,"sd_models",modelo.replace("/","_"))
        fuente=local if os.path.exists(local) else modelo
        pipe=StableDiffusionPipeline.from_pretrained(fuente,torch_dtype=dtype,
            safety_checker=None,requires_safety_checker=False)
        pipe.scheduler=DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe=pipe.to(device)
        if device=="cpu": pipe.enable_attention_slicing()
        img=pipe(prompt,width=ancho,height=alto,num_inference_steps=pasos).images[0]
        out=os.path.join(base,"imagenes_generadas"); os.makedirs(out,exist_ok=True)
        ruta=os.path.join(out,ruta_salida); img.save(ruta)
        return f"IMAGEN_GUARDADA:{ruta}"
    except Exception as e: return f"Error: {e}"
TOOLS={"generar_imagen":generar_imagen}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_rag.py"] = '''import sys,os,json,importlib
def _base(): return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def indexar_documento(ruta_archivo):
    if not importlib.util.find_spec("chromadb"): return "ERROR: pip install chromadb sentence-transformers"
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        db=os.path.join(_base(),"memory","rag_db")
        c=chromadb.PersistentClient(path=db)
        ef=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        col=c.get_or_create_collection("docs",embedding_function=ef)
        ext=os.path.splitext(ruta_archivo)[1].lower()
        if ext==".pdf":
            from pypdf import PdfReader
            texto=" ".join(p.extract_text() or "" for p in PdfReader(ruta_archivo).pages)
        elif ext==".docx":
            from docx import Document
            texto=" ".join(p.text for p in Document(ruta_archivo).paragraphs)
        else:
            with open(ruta_archivo,"r",encoding="utf-8",errors="ignore") as f: texto=f.read()
        chunks=[texto[i:i+500] for i in range(0,len(texto),500) if texto[i:i+500].strip()]
        n=os.path.basename(ruta_archivo)
        col.upsert(documents=chunks,ids=[f"{n}_{i}" for i in range(len(chunks))],
                   metadatas=[{"fuente":n,"chunk":i} for i in range(len(chunks))])
        return f"Indexados {len(chunks)} fragmentos de: {n}"
    except Exception as e: return f"Error: {e}"
def buscar_en_documentos(query,n_resultados=5):
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        db=os.path.join(_base(),"memory","rag_db")
        if not os.path.exists(db): return "Sin documentos indexados."
        c=chromadb.PersistentClient(path=db)
        ef=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        col=c.get_or_create_collection("docs",embedding_function=ef)
        r=col.query(query_texts=[query],n_results=n_resultados)
        docs=r.get("documents",[[]])[0]; metas=r.get("metadatas",[[]])[0]
        if not docs: return "Sin resultados."
        return "\\n\\n".join(f"[{m.get('fuente','?')}]\\n{d}" for d,m in zip(docs,metas))
    except Exception as e: return f"Error: {e}"
def listar_documentos_indexados():
    try:
        import chromadb
        db=os.path.join(_base(),"memory","rag_db")
        if not os.path.exists(db): return "Sin documentos."
        metas=chromadb.PersistentClient(path=db).get_or_create_collection("docs").get()["metadatas"]
        fuentes=sorted(set(m.get("fuente","?") for m in metas))
        return f"{len(fuentes)} docs:\\n"+"\\n".join(f"  • {f}" for f in fuentes)
    except Exception as e: return f"Error: {e}"
TOOLS={"indexar_documento":indexar_documento,"buscar_en_documentos":buscar_en_documentos,
       "listar_documentos_indexados":listar_documentos_indexados}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_voice.py"] = '''import sys,json,importlib
def texto_a_voz(texto,velocidad=150,voz_idx=0):
    if not importlib.util.find_spec("pyttsx3"): return "ERROR: pip install pyttsx3"
    try:
        import pyttsx3
        e=pyttsx3.init(); vs=e.getProperty("voices")
        if vs and voz_idx<len(vs): e.setProperty("voice",vs[voz_idx].id)
        e.setProperty("rate",velocidad); e.say(texto); e.runAndWait()
        return f"Hablado: {texto[:60]}"
    except Exception as e: return f"Error TTS: {e}"
def reconocer_voz(duracion=5):
    if not importlib.util.find_spec("speech_recognition"): return "ERROR: pip install SpeechRecognition pyaudio"
    try:
        import speech_recognition as sr
        r=sr.Recognizer()
        with sr.Microphone() as src:
            r.adjust_for_ambient_noise(src,duration=0.5)
            audio=r.listen(src,timeout=duracion,phrase_time_limit=duracion)
        try: return f"Reconocido: {r.recognize_google(audio,language='es-ES')}"
        except sr.UnknownValueError: return "No se entendió."
        except sr.RequestError: return "Sin conexión para reconocimiento."
    except Exception as e: return f"Error STT: {e}"
def listar_voces():
    if not importlib.util.find_spec("pyttsx3"): return "ERROR: pip install pyttsx3"
    try:
        import pyttsx3; e=pyttsx3.init(); vs=e.getProperty("voices")
        return "\\n".join(f"{i}: {v.name}" for i,v in enumerate(vs))
    except Exception as e: return f"Error: {e}"
TOOLS={"texto_a_voz":texto_a_voz,"reconocer_voz":reconocer_voz,"listar_voces":listar_voces}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    archivos["mcp_memory.py"] = '''import sys,os,json
def _p(): return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"memory","memoria.json")
def _c():
    p=_p()
    if os.path.exists(p):
        with open(p,"r",encoding="utf-8") as f: return json.load(f)
    return {"notas":{},"hechos":[]}
def _g(d):
    p=_p(); os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)
def guardar_hecho(hecho):
    d=_c(); d["hechos"].append(hecho); d["hechos"]=d["hechos"][-200:]; _g(d); return f"Guardado: {hecho}"
def recordar_hechos(query=""):
    h=_c()["hechos"]
    if query: h=[x for x in h if query.lower() in x.lower()]
    return "\\n".join(f"• {x}" for x in h[-50:]) or "Sin hechos."
def guardar_nota(clave,valor):
    d=_c(); d["notas"][clave]=valor; _g(d); return f"Nota: {clave}={valor}"
def leer_nota(clave): return _c()["notas"].get(clave,f"'{clave}' no encontrado.")
def listar_notas():
    n=_c()["notas"]; return "\\n".join(f"  {k}: {v}" for k,v in n.items()) or "Sin notas."
def limpiar_memoria(): _g({"notas":{},"hechos":[]}); return "Memoria limpiada."
TOOLS={"guardar_hecho":guardar_hecho,"recordar_hechos":recordar_hechos,
       "guardar_nota":guardar_nota,"leer_nota":leer_nota,
       "listar_notas":listar_notas,"limpiar_memoria":limpiar_memoria}
if __name__=="__main__":
    for line in sys.stdin:
        try:
            req=json.loads(line); res=TOOLS[req["tool"]](**req.get("args",{}))
            print(json.dumps({"result":res})); sys.stdout.flush()
        except Exception as e: print(json.dumps({"error":str(e)})); sys.stdout.flush()
'''

    for nombre, contenido in archivos.items():
        ruta = os.path.join(CFG["mcp_dir"], nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"  {C.DIM}  ✔ {nombre}{C.RESET}")
    _ok("7 servidores MCP creados")

def crear_asistente_py():
    _sub("🐍 Creando nexus_omni_app.py")
    ruta = os.path.join(CFG["app_dir"], "asistente.py")
    contenido = _get_asistente_codigo()
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    _ok(f"asistente.py escrito ({len(contenido):,} caracteres)")

def _get_asistente_codigo():
    """Retorna el código completo de la aplicación"""
    return r'''
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading, queue, subprocess, os, sys
import json, time, importlib
import ollama

TIENE_CREWAI    = importlib.util.find_spec("crewai")           is not None
TIENE_LANGGRAPH = importlib.util.find_spec("langgraph")        is not None
TIENE_AUTOGEN   = (importlib.util.find_spec("autogen") is not None or
                   importlib.util.find_spec("autogen_agentchat") is not None)
TIENE_LANGCHAIN = importlib.util.find_spec("langchain_ollama") is not None
TIENE_DIFFUSERS = importlib.util.find_spec("diffusers")        is not None
TIENE_CHROMADB  = importlib.util.find_spec("chromadb")         is not None
TIENE_TTS       = importlib.util.find_spec("pyttsx3")          is not None

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MCP_PATH  = os.path.join(BASE_PATH, "mcp_servers")

BG1="#08080f";BG2="#0f0f20";BG3="#161630";BG4="#0a0a18";BG5="#111125"
CT="#e8e8f8";CM="#44445a";COK="#00ff88";CWN="#f0a500"
FC=("Consolas",10);FU=("Segoe UI",10);FB=("Segoe UI",10,"bold")
FT=("Segoe UI",13,"bold");FS=("Segoe UI",9);FM=("Consolas",9)

cola_ui=queue.Queue(); resultados={}

AGENTES={
    "orquestador":  {"modelo":"deepseek-r1","fallback":"phi3","color":"#f0a500","icono":"🎯","nombre":"Orquestador","motor":"crewai",
        "system":'Eres el ORQUESTADOR. Responde SOLO con JSON:\n{"resumen":"breve","tareas":{"codigo":"tarea o null","razonamiento":"tarea o null","redaccion":"tarea o null","datos":"tarea o null","investigacion":"tarea o null"}}'},
    "codigo":       {"modelo":"qwen3-coder","fallback":"codestral","color":"#00ff88","icono":"💻","nombre":"Código","motor":"langgraph",
        "system":"Eres EXPERTO EN PROGRAMACION. Python, Java, JS, SQL. Escribe código funcional."},
    "razonamiento": {"modelo":"deepseek-r1","fallback":"phi3","color":"#ff6b6b","icono":"🧠","nombre":"Razonamiento","motor":"autogen",
        "system":"Eres EXPERTO EN RAZONAMIENTO LOGICO. Piensa paso a paso."},
    "redaccion":    {"modelo":"mistral","fallback":"phi3","color":"#a78bfa","icono":"✍️","nombre":"Redacción","motor":"langchain",
        "system":"Eres EXPERTO EN REDACCION. Textos profesionales, resumen, traducción ES/EN."},
    "datos":        {"modelo":"qwen3","fallback":"phi3","color":"#38bdf8","icono":"📊","nombre":"Datos","motor":"langchain",
        "system":"Eres EXPERTO EN ANALISIS DE DATOS. Estadística, patrones, SQL."},
    "investigacion":{"modelo":"phi3","fallback":"mistral","color":"#fb923c","icono":"🔍","nombre":"Investigación","motor":"mcp",
        "system":"Eres EXPERTO EN INVESTIGACION. Busca hechos, verifica, sintetiza."},
    "integrador":   {"modelo":"deepseek-r1","fallback":"phi3","color":"#facc15","icono":"🔗","nombre":"Integrador","motor":"crewai",
        "system":"Eres el INTEGRADOR FINAL. Combina respuestas en UNA respuesta cohesiva y completa."},
}

def modelos_ok():
    try:
        r=subprocess.run(["ollama","list"],capture_output=True,text=True)
        return [l.split()[0] for l in r.stdout.strip().split("\n")[1:] if l.strip()]
    except: return []

def get_modelo(key):
    cfg=AGENTES[key]; inst=modelos_ok()
    for m in [cfg["modelo"],cfg["fallback"]]:
        if any(m in x for x in inst): return m
    return inst[0] if inst else "phi3"

def _ollama(modelo,system,prompt):
    try:
        r=ollama.chat(model=modelo,messages=[{"role":"system","content":system},{"role":"user","content":prompt}],options={"num_predict":2048})
        return r["message"]["content"]
    except Exception as e: return f"[Error {modelo}]: {e}"

def _crewai(modelo,system,prompt):
    if not TIENE_CREWAI: return _ollama(modelo,system,prompt)
    try:
        from crewai import Agent,Task,Crew,LLM
        llm=LLM(model=f"ollama/{modelo}",base_url="http://localhost:11434")
        ag=Agent(role="Especialista",goal=system[:200],backstory=system,llm=llm,verbose=False,allow_delegation=False)
        ta=Task(description=prompt,expected_output="Respuesta completa",agent=ag)
        return str(Crew(agents=[ag],tasks=[ta],verbose=False).kickoff())
    except: return _ollama(modelo,system,prompt)

def _langgraph(modelo,system,prompt):
    if not TIENE_LANGGRAPH or not TIENE_LANGCHAIN: return _ollama(modelo,system,prompt)
    try:
        from langchain_ollama import OllamaLLM
        from langgraph.graph import StateGraph,END
        from typing import TypedDict
        class S(TypedDict): i:str; o:str
        llm=OllamaLLM(model=modelo)
        def nodo(s): return {"i":s["i"],"o":llm.invoke(f"{system}\n\nTarea: {s['i']}")}
        g=StateGraph(S); g.add_node("r",nodo); g.set_entry_point("r"); g.add_edge("r",END)
        return g.compile().invoke({"i":prompt,"o":""})["o"]
    except: return _ollama(modelo,system,prompt)

def _autogen(modelo,system,prompt):
    if not TIENE_AUTOGEN: return _ollama(modelo,system,prompt)
    try:
        # Soporte para autogen, ag2 y autogen_agentchat
        ag = None
        for mod_name in ["autogen", "autogen_agentchat", "ag2"]:
            try:
                ag = __import__(mod_name)
                break
            except ImportError:
                pass
        if ag is None: return _ollama(modelo,system,prompt)
        cfg={"config_list":[{"model":modelo,"base_url":"http://localhost:11434/v1","api_key":"ollama"}],"timeout":90}
        asist=ag.AssistantAgent(name="asist",system_message=system,llm_config=cfg)
        user=ag.UserProxyAgent(name="user",human_input_mode="NEVER",max_consecutive_auto_reply=1,code_execution_config=False)
        user.initiate_chat(asist,message=prompt,silent=True)
        for m in reversed(asist.chat_messages.get(user,[])):
            if m.get("role")=="assistant": return m.get("content","")
        return _ollama(modelo,system,prompt)
    except: return _ollama(modelo,system,prompt)

def _langchain(modelo,system,prompt):
    if not TIENE_LANGCHAIN: return _ollama(modelo,system,prompt)
    try:
        from langchain_ollama import OllamaLLM
        from langchain.prompts import PromptTemplate
        llm=OllamaLLM(model=modelo)
        chain=PromptTemplate(input_variables=["s","p"],template="{s}\n\nTarea: {p}") | llm
        return str(chain.invoke({"s":system,"p":prompt}))
    except: return _ollama(modelo,system,prompt)

def _mcp_motor(modelo,system,prompt):
    ctx=""
    if any(p in prompt.lower() for p in ["qué es","cuál","busca","investiga","what is","search"]):
        try:
            req=json.dumps({"tool":"buscar_web","args":{"query":prompt[:200]}})
            r=subprocess.run([sys.executable,os.path.join(MCP_PATH,"mcp_web.py")],
                             input=req+"\n",capture_output=True,text=True,timeout=10)
            if r.stdout:
                d=json.loads(r.stdout.strip().split("\n")[0])
                if d.get("result"): ctx=f"\n[Web]: {d['result']}"
        except: pass
    return _ollama(modelo,system,prompt+ctx)

EJECUTORES={"crewai":_crewai,"langgraph":_langgraph,"autogen":_autogen,
            "langchain":_langchain,"mcp":_mcp_motor,"ollama":_ollama}

def run_agente(key,subtarea,cb_p,cb_t):
    cfg=AGENTES[key]; modelo=get_modelo(key); motor=cfg["motor"]
    if motor not in EJECUTORES: motor="ollama"
    cb_p(key,f"⏳ [{motor.upper()}] {modelo}")
    res=EJECUTORES[motor](modelo,cfg["system"],subtarea)
    resultados[key]=res; cb_t(key,res,cfg["color"]); cb_p(key,f"✅ [{motor.upper()}] {modelo}")

def mcp_call(srv,tool,args,timeout=20):
    try:
        req=json.dumps({"tool":tool,"args":args})
        r=subprocess.run([sys.executable,os.path.join(MCP_PATH,srv)],
                         input=req+"\n",capture_output=True,text=True,timeout=timeout)
        if r.stdout:
            d=json.loads(r.stdout.strip().split("\n")[0])
            return d.get("result",d.get("error","Sin resultado"))
        return r.stderr or "Sin respuesta"
    except Exception as e: return f"Error MCP: {e}"

def orquestar(preg,cb_p,cb_t):
    resultados.clear()
    cb_p("orquestador","⏳ CrewAI analizando...")
    resp=_crewai(get_modelo("orquestador"),AGENTES["orquestador"]["system"],preg)
    cb_t("orquestador",resp,AGENTES["orquestador"]["color"])
    tareas={}
    try:
        i=resp.find("{"); j=resp.rfind("}")+1
        if i>=0 and j>i: tareas=json.loads(resp[i:j]).get("tareas",{})
    except:
        for k in ["codigo","razonamiento","redaccion","datos","investigacion"]: tareas[k]=preg
    activos=[k for k,v in tareas.items() if v and k in AGENTES]
    cb_p("orquestador",f"✅ {len(activos)} agentes activos")
    hilos=[threading.Thread(target=run_agente,args=(k,tareas[k],cb_p,cb_t),daemon=True) for k in activos]
    for t in hilos: t.start()
    for t in hilos: t.join()
    cb_p("integrador","⏳ CrewAI integrando...")
    partes=[f"PREGUNTA:\n{preg}\n"]
    for k in activos:
        if k in resultados:
            cfg=AGENTES[k]
            partes.append(f"\n--- {cfg['icono']} {cfg['nombre']} [{cfg['motor'].upper()}] ---\n{resultados[k]}")
    final=_crewai(get_modelo("integrador"),AGENTES["integrador"]["system"],"\n".join(partes))
    cb_t("integrador",final,AGENTES["integrador"]["color"])
    cb_p("integrador","✅ Integración completa")
    return final

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS OMNI Multi-Agente IA v4.0")
        self.geometry("1400x860"); self.configure(bg=BG1); self.resizable(True,True)
        try: self.iconbitmap(os.path.join(BASE_PATH,"icono.ico"))
        except: pass
        self._ui(); self.after(80,self._poll)

    def _ui(self):
        top=tk.Frame(self,bg=BG3,pady=5); top.pack(fill=tk.X)
        tk.Label(top,text="🤖 NEXUS OMNI Multi-Agente IA v4.0",bg=BG3,fg=CT,font=FT).pack(side=tk.LEFT,padx=12)
        caps=[("CrewAI",TIENE_CREWAI),("LangGraph",TIENE_LANGGRAPH),("AutoGen",TIENE_AUTOGEN),
              ("LangChain",TIENE_LANGCHAIN),("SD",TIENE_DIFFUSERS),("RAG",TIENE_CHROMADB),("TTS",TIENE_TTS)]
        for nm,ok in caps:
            tk.Label(top,text=f"{'✔' if ok else '✗'}{nm}",bg=BG3,fg=COK if ok else CWN,font=FM).pack(side=tk.LEFT,padx=3)
        for txt,cmd,col in [("📋 Modelos",self._ver_modelos,"#223355"),
                             ("⬇️ Pull",self._pull_modelo,"#332255"),
                             ("💾 Guardar",self._guardar,"#223355"),
                             ("ℹ️ HW",self._info_hw,"#223344")]:
            tk.Button(top,text=txt,command=cmd,bg=col,fg=CT,font=FS,relief=tk.FLAT,padx=8,cursor="hand2").pack(side=tk.RIGHT,padx=2)

        pw=tk.PanedWindow(self,orient=tk.HORIZONTAL,bg=BG1,sashwidth=5); pw.pack(expand=True,fill="both",padx=5,pady=4)
        izq=tk.Frame(pw,bg=BG1); pw.add(izq,minsize=360)
        tk.Label(izq,text="💬 Chat Principal  [Ctrl+Enter]",bg=BG3,fg=CT,font=FB,pady=4).pack(fill=tk.X)
        self.chat=scrolledtext.ScrolledText(izq,wrap=tk.WORD,bg=BG2,fg=CT,font=FC,state=tk.DISABLED,bd=0,padx=12,pady=8)
        self.chat.pack(expand=True,fill="both")
        for tag,col,fnt in [("user","#e94560",FB),("final","#facc15",FB),("sys",CM,FS),("body",CT,FC)]:
            self.chat.tag_config(tag,foreground=col,font=fnt)
        self._ins("sys","Motores: "+" | ".join(n for n,ok in caps if ok)+"\n\n")
        tk.Frame(izq,bg=BG3,height=2).pack(fill=tk.X,pady=3)
        me=tk.Frame(izq,bg=BG1); me.pack(fill=tk.X,pady=(0,4))
        self.entrada=tk.Text(me,height=4,bg=BG2,fg=CT,font=FU,insertbackground=CT,bd=0,padx=10,pady=6,wrap=tk.WORD)
        self.entrada.pack(side=tk.LEFT,expand=True,fill=tk.X); self.entrada.bind("<Control-Return>",self._enviar)
        mb=tk.Frame(me,bg=BG1); mb.pack(side=tk.RIGHT,padx=(4,0))
        self.btn=tk.Button(mb,text="Enviar ▶\nTodos los agentes",command=self._enviar,
                           bg="#e94560",fg="white",font=FB,relief=tk.FLAT,padx=12,pady=8,cursor="hand2")
        self.btn.pack(fill=tk.X,pady=(0,3))
        tk.Button(mb,text="Limpiar 🗑",command=self._limpiar,bg=BG3,fg=CT,font=FS,relief=tk.FLAT,padx=12,pady=4,cursor="hand2").pack(fill=tk.X)

        der=tk.Frame(pw,bg=BG1); pw.add(der,minsize=700)
        tk.Label(der,text="🔬 Agentes en tiempo real",bg=BG3,fg=CT,font=FB,pady=4).pack(fill=tk.X)
        self.lbl_prog=tk.Label(der,text="En espera...",bg=BG4,fg=CM,font=FS,anchor="w",padx=8,pady=2); self.lbl_prog.pack(fill=tk.X)
        sty=ttk.Style(); sty.theme_use("default")
        sty.configure("V4.TNotebook",background=BG4,borderwidth=0)
        sty.configure("V4.TNotebook.Tab",background=BG5,foreground=CM,padding=[6,3],font=FS)
        sty.map("V4.TNotebook.Tab",background=[("selected",BG2)],foreground=[("selected",CT)])
        self.nb=ttk.Notebook(der,style="V4.TNotebook"); self.nb.pack(expand=True,fill="both",padx=3,pady=3)
        self.tab_txt={}; self.tab_lbl={}

        for key in ["orquestador","codigo","razonamiento","redaccion","datos","investigacion","integrador"]:
            cfg=AGENTES[key]; fr=tk.Frame(self.nb,bg=BG2); self.nb.add(fr,text=f"{cfg['icono']} {cfg['nombre']}")
            hdr=tk.Frame(fr,bg=BG3,pady=2); hdr.pack(fill=tk.X)
            disp=cfg["motor"] in ["ollama","mcp"] or {"crewai":TIENE_CREWAI,"langgraph":TIENE_LANGGRAPH,"autogen":TIENE_AUTOGEN,"langchain":TIENE_LANGCHAIN}.get(cfg["motor"],False)
            tk.Label(hdr,text=f"{cfg['icono']} {cfg['nombre']}  Motor:{cfg['motor'].upper()}  {'✔' if disp else '⚠→ollama'}  {cfg['modelo']}",
                     bg=BG3,fg=cfg["color"] if disp else CWN,font=FS).pack(side=tk.LEFT,padx=8)
            self.tab_lbl[key]=tk.Label(hdr,text="⬜ Espera",bg=BG3,fg=CM,font=FS); self.tab_lbl[key].pack(side=tk.RIGHT,padx=8)
            txt=scrolledtext.ScrolledText(fr,wrap=tk.WORD,bg=BG2,fg=CT,font=FC,bd=0,padx=10,pady=6,state=tk.DISABLED)
            txt.pack(expand=True,fill="both")
            txt.tag_config("h",foreground=cfg["color"],font=FB); txt.tag_config("b",foreground=CT); txt.tag_config("m",foreground=CM,font=FS)
            self.tab_txt[key]=txt

        # Pestañas extra
        for tab_name, tab_text, builder in [
            ("img",  "🎨 Imagen SD",  self._build_tab_img),
            ("rag",  "📚 RAG Docs",   self._build_tab_rag),
            ("voz",  "🎙️ Voz",        self._build_tab_voz),
            ("mcp",  "🔧 MCP Tools",  self._build_tab_mcp),
        ]:
            fr=tk.Frame(self.nb,bg=BG2); self.nb.add(fr,text=tab_text); builder(fr)

        bot=tk.Frame(der,bg=BG4); bot.pack(fill=tk.X,padx=3,pady=(0,3))
        self.lbl_m=tk.Label(bot,text="...",bg=BG4,fg=CM,font=FS); self.lbl_m.pack(side=tk.LEFT,padx=6)
        threading.Thread(target=self._upd_mods,daemon=True).start()

    def _build_tab_img(self,fr):
        tk.Label(fr,text=f"🎨 Stable Diffusion  {'✅' if TIENE_DIFFUSERS else '⚠️ pip install diffusers torch'}",bg=BG3,fg="#ff79c6",font=FB,pady=4).pack(fill=tk.X)
        fp=tk.Frame(fr,bg=BG4,pady=4); fp.pack(fill=tk.X,padx=6)
        tk.Label(fp,text="Prompt:",bg=BG4,fg=CM,font=FS).grid(row=0,column=0,padx=4,sticky="w")
        self.img_p=tk.Entry(fp,bg=BG2,fg=CT,font=FU,insertbackground=CT,bd=0,width=55)
        self.img_p.insert(0,"a futuristic robot in neon city, digital art, 4k"); self.img_p.grid(row=0,column=1,padx=4,pady=2,sticky="ew")
        tk.Label(fp,text="Pasos:",bg=BG4,fg=CM,font=FS).grid(row=0,column=2,padx=4)
        self.img_s=tk.Entry(fp,bg=BG2,fg=CT,font=FS,bd=0,width=4,insertbackground=CT); self.img_s.insert(0,"20"); self.img_s.grid(row=0,column=3,padx=2)
        fp.columnconfigure(1,weight=1)
        tk.Button(fp,text="🎨 Generar",command=self._gen_img,bg="#ff79c6",fg="black",font=FB,relief=tk.FLAT,padx=14,pady=5,cursor="hand2").grid(row=1,column=0,columnspan=4,pady=6)
        self.img_lbl=tk.Label(fr,bg=BG2,text="La imagen aparecerá aquí",fg=CM,font=FU); self.img_lbl.pack(expand=True)
        self.img_st=tk.Label(fr,text="",bg=BG2,fg=CM,font=FS); self.img_st.pack()

    def _build_tab_rag(self,fr):
        tk.Label(fr,text=f"📚 RAG  {'✅' if TIENE_CHROMADB else '⚠️ pip install chromadb sentence-transformers'}",bg=BG3,fg="#38bdf8",font=FB,pady=4).pack(fill=tk.X)
        frb=tk.Frame(fr,bg=BG4,pady=4); frb.pack(fill=tk.X,padx=6)
        for txt,cmd in [("📂 Indexar",self._rag_idx),("🔍 Buscar",self._rag_buscar),("📋 Listar",self._rag_list)]:
            tk.Button(frb,text=txt,command=cmd,bg=BG3,fg=CT,font=FS,relief=tk.FLAT,padx=10,pady=5,cursor="hand2").pack(side=tk.LEFT,padx=4)
        tk.Label(fr,text="Query:",bg=BG4,fg=CM,font=FS,anchor="w",padx=8).pack(fill=tk.X)
        self.rag_q=tk.Entry(fr,bg=BG2,fg=CT,font=FU,bd=0,insertbackground=CT); self.rag_q.pack(fill=tk.X,padx=8,pady=2)
        self.rag_o=scrolledtext.ScrolledText(fr,wrap=tk.WORD,bg=BG2,fg=COK,font=FM,bd=0,padx=10,pady=6,state=tk.DISABLED)
        self.rag_o.pack(expand=True,fill="both",padx=6,pady=4)

    def _build_tab_voz(self,fr):
        tk.Label(fr,text=f"🎙️ Voz  {'✅' if TIENE_TTS else '⚠️ pip install pyttsx3 SpeechRecognition'}",bg=BG3,fg="#c084fc",font=FB,pady=4).pack(fill=tk.X)
        self.voz_t=tk.Text(fr,height=5,bg=BG2,fg=CT,font=FU,insertbackground=CT,bd=0,padx=10,pady=6,wrap=tk.WORD)
        self.voz_t.insert("1.0","Escribe el texto que quieres escuchar..."); self.voz_t.pack(fill=tk.X,padx=8,pady=6)
        fvb=tk.Frame(fr,bg=BG2); fvb.pack(pady=4)
        for txt,cmd,col in [("🔊 Leer",self._tts,"#7c3aed"),("🎙️ Escuchar",self._stt,"#be185d"),("📋 Voces",self._voces,"#1e40af")]:
            tk.Button(fvb,text=txt,command=cmd,bg=col,fg="white",font=FB,relief=tk.FLAT,padx=12,pady=6,cursor="hand2").pack(side=tk.LEFT,padx=6)
        self.voz_o=scrolledtext.ScrolledText(fr,wrap=tk.WORD,bg=BG2,fg="#c084fc",font=FM,bd=0,padx=10,state=tk.DISABLED,height=8)
        self.voz_o.pack(expand=True,fill="both",padx=8,pady=(0,6))

    def _build_tab_mcp(self,fr):
        tk.Label(fr,text="🔧 MCP Tools — 7 servidores",bg=BG3,fg="#00d4ff",font=FB,pady=4).pack(fill=tk.X)
        fmb=tk.Frame(fr,bg=BG4,pady=4); fmb.pack(fill=tk.X,padx=5)
        herrs=[("📂 Listar dir",lambda:self._mr("mcp_files.py","listar_directorio",{"ruta":"."})),
               ("📄 Leer arch.",self._ml),("✏️ Escribir",self._mw),("🌐 Web",self._mweb),
               ("🐍 Python",lambda:self._mc("ejecutar_python","codigo")),
               ("☕ Java",lambda:self._mc("ejecutar_java","codigo")),
               ("💻 CMD",lambda:self._mc("ejecutar_cmd","comando")),
               ("🔍 Buscar txt",self._mbuscar),
               ("💾 Nota",self._mnota),("📖 Notas",lambda:self._mr("mcp_memory.py","listar_notas",{})),
               ("🧠 Hechos",lambda:self._mr("mcp_memory.py","recordar_hechos",{})),
               ("🗑 Limpiar",lambda:self._mr("mcp_memory.py","limpiar_memoria",{}))]
        for i,(txt,cmd) in enumerate(herrs):
            tk.Button(fmb,text=txt,command=cmd,bg=BG3,fg=CT,font=FS,relief=tk.FLAT,padx=7,pady=4,cursor="hand2").grid(row=i//6,column=i%6,padx=2,pady=2,sticky="ew")
        for c in range(6): fmb.columnconfigure(c,weight=1)
        tk.Label(fr,text="Entrada:",bg=BG4,fg=CM,font=FS,anchor="w",padx=8).pack(fill=tk.X)
        self.mi=tk.Text(fr,height=4,bg=BG2,fg=CT,font=FM,bd=0,padx=8,pady=6,insertbackground=CT); self.mi.pack(fill=tk.X,padx=6)
        tk.Label(fr,text="Salida:",bg=BG4,fg=CM,font=FS,anchor="w",padx=8).pack(fill=tk.X,pady=(4,0))
        self.mo=scrolledtext.ScrolledText(fr,wrap=tk.WORD,bg=BG2,fg=COK,font=FM,bd=0,padx=8,state=tk.DISABLED)
        self.mo.pack(expand=True,fill="both",padx=6,pady=(0,6))

    # ── Helpers ──────────────────────────────────────────
    def _ins(self,tag,txt):
        self.chat.config(state=tk.NORMAL); self.chat.insert(tk.END,txt,tag); self.chat.see(tk.END); self.chat.config(state=tk.DISABLED)
    def _it(self,key,txt,tag="b"):
        if key not in self.tab_txt: return
        w=self.tab_txt[key]; w.config(state=tk.NORMAL); w.insert(tk.END,txt,tag); w.see(tk.END); w.config(state=tk.DISABLED)
    def _ct(self,key):
        if key not in self.tab_txt: return
        w=self.tab_txt[key]; w.config(state=tk.NORMAL); w.delete("1.0",tk.END); w.config(state=tk.DISABLED)
    def _om(self,txt): self.mo.config(state=tk.NORMAL); self.mo.delete("1.0",tk.END); self.mo.insert(tk.END,txt); self.mo.config(state=tk.DISABLED)
    def _or(self,txt): self.rag_o.config(state=tk.NORMAL); self.rag_o.delete("1.0",tk.END); self.rag_o.insert(tk.END,txt); self.rag_o.config(state=tk.DISABLED)
    def _ov(self,txt): self.voz_o.config(state=tk.NORMAL); self.voz_o.delete("1.0",tk.END); self.voz_o.insert(tk.END,txt); self.voz_o.config(state=tk.DISABLED)
    def _cb_p(self,key,msg): cola_ui.put(("p",key,msg))
    def _cb_t(self,key,txt,col): cola_ui.put(("t",key,txt,col))
    def _poll(self):
        try:
            while True:
                it=cola_ui.get_nowait()
                if it[0]=="p":
                    _,k,m=it
                    if k in self.tab_lbl: self.tab_lbl[k].config(text=m)
                    self.lbl_prog.config(text=f"{AGENTES[k]['icono']} {AGENTES[k]['nombre']}: {m}")
                elif it[0]=="t":
                    _,k,txt,_=it; self._ct(k); self._it(k,"─"*48+"\n","m"); self._it(k,txt); self._it(k,"\n"+"─"*48+"\n","m")
                elif it[0]=="final":
                    _,txt=it; self._ins("final","🔗 Respuesta Integrada:\n"); self._ins("body",txt+"\n\n")
                    self.btn.config(state=tk.NORMAL,text="Enviar ▶\nTodos los agentes")
                    self.lbl_prog.config(text="✅ Todos los agentes completaron")
        except queue.Empty: pass
        self.after(80,self._poll)
    def _enviar(self,e=None):
        preg=self.entrada.get("1.0",tk.END).strip()
        if not preg: return
        self.entrada.delete("1.0",tk.END); self.btn.config(state=tk.DISABLED,text="⏳ Agentes\ntrabajando...")
        for k in AGENTES: self._ct(k)
        self._ins("user","👤 Tú:\n"); self._ins("body",preg+"\n\n"); self._ins("sys","⚙️ Orquestando...\n\n")
        threading.Thread(target=lambda:cola_ui.put(("final",orquestar(preg,self._cb_p,self._cb_t))),daemon=True).start()
    def _limpiar(self):
        self.chat.config(state=tk.NORMAL); self.chat.delete("1.0",tk.END); self.chat.config(state=tk.DISABLED)
        for k in AGENTES: self._ct(k)
        self._ins("sys","🗑 Limpiado.\n\n")
    def _gen_img(self):
        p=self.img_p.get(); s=int(self.img_s.get() or 20); nm=f"img_{int(time.time())}.png"
        self.img_st.config(text="⏳ Generando... (1-5 min CPU)")
        def _r():
            res=mcp_call("mcp_image.py","generar_imagen",{"prompt":p,"pasos":s,"ruta_salida":nm},timeout=300)
            if res.startswith("IMAGEN_GUARDADA:"): self.after(0,lambda:self._show_img(res.split(":",1)[1]))
            else: self.after(0,lambda:self.img_st.config(text=f"❌ {res}"))
        threading.Thread(target=_r,daemon=True).start()
    def _show_img(self,ruta):
        try:
            from PIL import Image,ImageTk
            img=Image.open(ruta).resize((500,500)); imgtk=ImageTk.PhotoImage(img)
            self.img_lbl.config(image=imgtk,text=""); self.img_lbl.image=imgtk; self.img_st.config(text=f"✅ {ruta}")
        except Exception as e: self.img_st.config(text=f"Error: {e}")
    def _rag_idx(self):
        ruta=filedialog.askopenfilename(filetypes=[("Docs","*.pdf *.txt *.docx *.md"),("Todos","*.*")])
        if ruta:
            self._or(f"⏳ Indexando {os.path.basename(ruta)}...")
            def _r():
                res=mcp_call("mcp_rag.py","indexar_documento",{"ruta_archivo":ruta},timeout=60)
                self.after(0,lambda r=res:self._or(r))
            threading.Thread(target=_r,daemon=True).start()
    def _rag_buscar(self):
        q=self.rag_q.get().strip() or "tema principal"
        def _r():
            res=mcp_call("mcp_rag.py","buscar_en_documentos",{"query":q})
            self.after(0,lambda r=res:self._or(r))
        threading.Thread(target=_r,daemon=True).start()
    def _rag_list(self):
        def _r():
            res=mcp_call("mcp_rag.py","listar_documentos_indexados",{})
            self.after(0,lambda r=res:self._or(r))
        threading.Thread(target=_r,daemon=True).start()
    def _tts(self):
        t=self.voz_t.get("1.0",tk.END).strip()
        if t:
            def _r():
                res=mcp_call("mcp_voice.py","texto_a_voz",{"texto":t})
                self.after(0,lambda r=res:self._ov(r))
            threading.Thread(target=_r,daemon=True).start()
    def _stt(self):
        self._ov("🎙️ Escuchando 5s...")
        def _r():
            res=mcp_call("mcp_voice.py","reconocer_voz",{"duracion":5},timeout=15)
            self.after(0,lambda r=res:self._ov(r))
            if res.startswith("Reconocido:"): self.after(0,lambda:self.entrada.insert(tk.END,res.split(":",1)[1].strip()))
        threading.Thread(target=_r,daemon=True).start()
    def _voces(self):
        def _r():
            res=mcp_call("mcp_voice.py","listar_voces",{})
            self.after(0,lambda r=res:self._ov(r))
        threading.Thread(target=_r,daemon=True).start()
    def _mr(self,srv,tool,args):
        def _r():
            res=mcp_call(srv,tool,args)
            self.after(0,lambda r=res:self._om(r))
        threading.Thread(target=_r,daemon=True).start()
    def _ml(self):
        r=filedialog.askopenfilename()
        if r: self._mr("mcp_files.py","leer_archivo",{"ruta":r})
    def _mw(self):
        c=self.mi.get("1.0",tk.END).strip(); r=filedialog.asksaveasfilename()
        if r and c: self._mr("mcp_files.py","escribir_archivo",{"ruta":r,"contenido":c})
    def _mweb(self):
        q=self.mi.get("1.0",tk.END).strip() or "IA 2026"; self._mr("mcp_web.py","buscar_web",{"query":q})
    def _mc(self,tool,ak):
        c=self.mi.get("1.0",tk.END).strip()
        if c: self._mr("mcp_code.py",tool,{ak:c})
        else: self._om("Escribe código en el área de entrada.")
    def _mbuscar(self):
        p=self.mi.get("1.0",tk.END).strip() or "def "
        d=filedialog.askdirectory()
        if d: self._mr("mcp_files.py","buscar_en_archivos",{"directorio":d,"patron":p})
    def _mnota(self):
        t=self.mi.get("1.0",tk.END).strip()
        if "=" in t:
            k,v=t.split("=",1); self._mr("mcp_memory.py","guardar_nota",{"clave":k.strip(),"valor":v.strip()})
        else: self._mr("mcp_memory.py","guardar_hecho",{"hecho":t})
    def _ver_modelos(self):
        try: r=subprocess.run(["ollama","list"],capture_output=True,text=True); txt=r.stdout
        except Exception as e: txt=f"Error: {e}"
        w=tk.Toplevel(self); w.title("Modelos"); w.configure(bg=BG1); w.geometry("560x400")
        t=scrolledtext.ScrolledText(w,bg=BG2,fg=CT,font=FM,bd=0,padx=10); t.pack(expand=True,fill="both",padx=8,pady=8); t.insert(tk.END,txt); t.config(state=tk.DISABLED)
    def _pull_modelo(self):
        opts=["phi3","deepseek-r1","qwen3","qwen3-coder","mistral","codestral","deepseek-v3","glm4"]
        w=tk.Toplevel(self); w.title("Pull"); w.configure(bg=BG1); w.geometry("380x180")
        tk.Label(w,text="Modelo:",bg=BG1,fg=CT,font=FU).pack(pady=8)
        cb=ttk.Combobox(w,values=opts,font=FU,width=28); cb.current(0); cb.pack()
        lbl=tk.Label(w,text="",bg=BG1,fg=CWN,font=FS); lbl.pack(pady=4)
        def _p():
            m=cb.get(); lbl.config(text=f"⏳ {m}...")
            def _r():
                r=subprocess.run(["ollama","pull",m],capture_output=True,text=True)
                self.after(0,lambda:lbl.config(text=f"{'✅' if r.returncode==0 else '❌'} {m}"))
            threading.Thread(target=_r,daemon=True).start()
        tk.Button(w,text="⬇️ Descargar",command=_p,bg="#553388",fg="white",font=FB,relief=tk.FLAT,padx=14,pady=5,cursor="hand2").pack(pady=6)
    def _info_hw(self):
        info="SISTEMA\n"+"═"*40+"\n"
        try:
            import platform,psutil
            info+=f"OS: {platform.system()} {platform.release()}\n"
            info+=f"RAM: {psutil.virtual_memory().total//1073741824}GB total / {psutil.virtual_memory().available//1073741824}GB libre\n"
            info+=f"Disco libre: {psutil.disk_usage(os.path.expanduser('~')).free//1073741824}GB\n"
        except: pass
        try:
            import torch; info+=f"\nPyTorch: {torch.__version__}\nCUDA: {torch.cuda.is_available()}\n"
            if torch.cuda.is_available(): info+=f"GPU: {torch.cuda.get_device_name(0)}\n"
        except: info+="\nPyTorch no instalado\n"
        info+="\nMOTORES:\n"
        for nm,ok in [("CrewAI",TIENE_CREWAI),("LangGraph",TIENE_LANGGRAPH),("AutoGen",TIENE_AUTOGEN),
                      ("LangChain",TIENE_LANGCHAIN),("Diffusers",TIENE_DIFFUSERS),("ChromaDB",TIENE_CHROMADB),("pyttsx3",TIENE_TTS)]:
            info+=f"  {'✅' if ok else '❌'} {nm}\n"
        w=tk.Toplevel(self); w.title("Hardware"); w.configure(bg=BG1); w.geometry("460x420")
        t=scrolledtext.ScrolledText(w,bg=BG2,fg=COK,font=FM,bd=0,padx=10); t.pack(expand=True,fill="both",padx=8,pady=8); t.insert(tk.END,info); t.config(state=tk.DISABLED)
    def _guardar(self):
        ruta=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Texto","*.txt"),("Todos","*.*")])
        if not ruta: return
        with open(ruta,"w",encoding="utf-8") as f:
            f.write("═"*60+"\n CHAT\n"+"═"*60+"\n"); f.write(self.chat.get("1.0",tk.END))
            for k,cfg in AGENTES.items():
                if k in self.tab_txt:
                    f.write(f"\n{'═'*60}\n {cfg['icono']} {cfg['nombre']}\n{'═'*60}\n"); f.write(self.tab_txt[k].get("1.0",tk.END))
        messagebox.showinfo("Guardado",f"Guardado:\n{ruta}")
    def _upd_mods(self):
        inst=modelos_ok(); txt="Modelos: "+" · ".join(inst[:8]) if inst else "⚠️ Sin modelos"
        self.after(0,lambda:self.lbl_m.config(text=txt))

if __name__=="__main__":
    App().mainloop()
'''

def crear_icono():
    _sub("🎨 Creando icono")
    from PIL import Image, ImageDraw
    import math
    sizes=[256,128,64,48,32,16]; images=[]
    for size in sizes:
        img=Image.new("RGBA",(size,size),(0,0,0,0)); draw=ImageDraw.Draw(img)
        for i in range(size//2,0,-1):
            ratio=i/(size//2)
            draw.ellipse([size//2-i,size//2-i,size//2+i,size//2+i],
                fill=(int(5+15*ratio),int(5+10*ratio),int(15+145*ratio),255))
        for idx in range(7):
            ang=math.radians(idx*(360/7)-90)
            px=int(size//2+(size//3)*math.cos(ang)); py=int(size//2+(size//3)*math.sin(ang))
            r2=size//10; draw.ellipse([px-r2,py-r2,px+r2,py+r2],fill=(0,200,220,220))
        images.append(img)
    for dest in [os.path.join(CFG["app_dir"],"icono.ico"),
                 os.path.join(CFG["installer_dir"],"icono.ico")]:
        images[0].save(dest,format="ICO",sizes=[(s,s) for s in sizes],append_images=images[1:])
    _ok("icono.ico creado")

def crear_wizard_images():
    _sub("🖼️ Imágenes wizard")
    from PIL import Image, ImageDraw
    import math
    W,H=164,314; img=Image.new("RGB",(W,H)); draw=ImageDraw.Draw(img)
    for y in range(H):
        ratio=y/H; draw.line([(0,y),(W,y)],fill=(int(3+4*ratio),int(3+4*ratio),int(8+62*ratio)))
    cx,cy=W//2,65
    for idx in range(7):
        ang=math.radians(idx*51.4-90); px=int(cx+36*math.cos(ang)); py=int(cy+36*math.sin(ang))
        draw.ellipse([px-7,py-7,px+7,py+7],fill=(0,120,200)); draw.line([cx,cy,px,py],fill=(0,60,120),width=1)
    draw.ellipse([cx-12,cy-12,cx+12,cy+12],fill=(0,30,100))
    for x,y,t,c in [(5,112,"Multi-Agente",(0,210,255)),(5,130,"IA v4.0",(200,220,255)),
                    (5,155,"CrewAI",(255,160,60)),(5,171,"LangGraph",(255,160,60)),
                    (5,187,"AutoGen",(255,160,60)),(5,203,"LangChain",(255,160,60)),
                    (5,219,"MCP·RAG·SD·Voz",(255,160,60)),(5,252,"7 Agentes Paralelos",(80,255,150)),
                    (5,269,"Python 3.11",(80,200,120)),(5,285,"100% Offline",(80,200,120))]:
        draw.text((x,y),t,fill=c)
    img.save(os.path.join(CFG["installer_dir"],"wizard_image.bmp"),format="BMP")
    img2=Image.new("RGB",(55,58),(3,3,12)); d2=ImageDraw.Draw(img2)
    for idx in range(7):
        ang=math.radians(idx*51.4-90); px=int(27+20*math.cos(ang)); py=int(29+20*math.sin(ang))
        d2.ellipse([px-4,py-4,px+4,py+4],fill=(0,120,200))
    img2.save(os.path.join(CFG["installer_dir"],"wizard_small.bmp"),format="BMP")
    _ok("Imágenes wizard creadas")

def crear_licencia():
    _sub("📄 Licencia")
    with open(os.path.join(CFG["installer_dir"],"licencia.txt"),"w",encoding="utf-8") as f:
        f.write("TERMINOS DE USO\n===============\nAsistente Multi-Agente IA v4.0\n\n"
                "CrewAI·LangGraph·AutoGen·LangChain·MCP: MIT/CC-BY\n"
                "diffusers (SD): Apache 2.0 | ChromaDB: Apache 2.0\n"
                "Phi-3/DeepSeek: MIT | Qwen3/Mistral: Apache 2.0\n\n"
                "- No se recopilan datos del usuario.\n"
                "- Funciona offline tras instalación inicial.\n\n"
                "Al instalar aceptas estos términos.\n")
    _ok("licencia.txt creada")

def compilar_exe():
    _sub("⚙️ Compilando .exe con PyInstaller")
    print(f"  {C.CYAN}⏳ Esto puede tardar 3-6 minutos...{C.RESET}")
    sep = ";" if sys.platform == "win32" else ":"
    r = subprocess.run(
        f'"{S.python_exe}" -m PyInstaller '
        f'--onefile --windowed '
        f'--icon=icono.ico '
        f'--name=nexus_omni '
        f'--distpath=dist '
        f'--workpath=build '
        f'--specpath=. '
        f'--add-data "mcp_servers{sep}mcp_servers" '
        f'asistente.py',
        shell=True, cwd=CFG["app_dir"]
    )
    exe = os.path.join(CFG["dist_dir"],"nexus_omni.exe")
    if os.path.exists(exe):
        size_mb = os.path.getsize(exe) / 1e6
        _ok(f"{CFG['nombre_exe']} creado ({size_mb:.1f} MB)")
        return True
    else:
        _err("Error compilando .exe"); return False

def crear_ps1():
    _sub("📄 Script PowerShell para Ollama")
    with open(os.path.join(CFG["installer_dir"],"instalar_ollama.ps1"),"w",encoding="utf-8") as f:
        f.write("$ErrorActionPreference='Stop'\n"
                "$dest=Join-Path $env:TEMP 'OllamaSetup.exe'\n"
                "$cmd=Get-Command ollama -ErrorAction SilentlyContinue\n"
                "if(-not $cmd){\n"
                "    Write-Host 'Descargando Ollama...'\n"
                "    Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile $dest\n"
                "    Start-Process -FilePath $dest -ArgumentList '/SILENT' -Wait\n"
                "    Write-Host 'Ollama instalado.'\n"
                "}else{Write-Host 'Ollama ya estaba instalado.'}\n")
    _ok("instalar_ollama.ps1 creado")

def crear_iss():
    _sub("📝 Script Inno Setup")
    d = CFG
    lineas=[
        f'#define MyAppName      "{d["nombre_app"]}"',
        f'#define MyAppVersion   "{d["version"]}"',
        f'#define MyAppPublisher "{d["publisher"]}"',
        f'#define MyAppExeName   "{d["nombre_exe"]}"',
        "","[Setup]",
        "AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567891}",
        "AppName={#MyAppName}","AppVersion={#MyAppVersion}","AppPublisher={#MyAppPublisher}",
        r"DefaultDirName={autopf}\AsistenteMultiAgenteV4","DefaultGroupName={#MyAppName}",
        f"OutputDir={d['output_dir']}",f"OutputBaseFilename={d['nombre_installer']}",
        "Compression=lzma","SolidCompression=yes","WizardStyle=modern",
        "LicenseFile=licencia.txt","SetupIconFile=icono.ico",
        "WizardImageFile=wizard_image.bmp","WizardSmallImageFile=wizard_small.bmp",
        "WizardImageStretch=no","WizardImageBackColor=$03030C",
        "","[Languages]",
        'Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"',
        'Name: "english"; MessagesFile: "compiler:Default.isl"',
        "","[Tasks]",
        'Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Opciones:"',
        "","[Files]",
        f'Source: "{d["dist_dir"]}\\{d["nombre_exe"]}"; DestDir: "{{app}}"; Flags: ignoreversion',
        f'Source: "{d["app_dir"]}\\icono.ico"; DestDir: "{{app}}"; Flags: ignoreversion',
        f'Source: "{d["installer_dir"]}\\instalar_ollama.ps1"; DestDir: "{{app}}"; Flags: ignoreversion',
        f'Source: "{d["mcp_dir"]}\\*"; DestDir: "{{app}}\\mcp_servers"; Flags: ignoreversion recursesubdirs',
        "","[Icons]",
        r'Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icono.ico"',
        r'Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icono.ico"; Tasks: desktopicon',
        "","[Run]",
        r'Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\instalar_ollama.ps1"""; StatusMsg: "Instalando Ollama..."; Flags: runhidden waituntilterminated',
        "",
        f'Filename: "cmd.exe"; Parameters: "/c ollama pull {d["modelo_default"]}"; StatusMsg: "Descargando modelo base ({d["modelo_default"]})..."; Flags: runhidden waituntilterminated',
        "",
        r'Filename: "{app}\{#MyAppExeName}"; Description: "Abrir Asistente Multi-Agente IA v4.0"; Flags: nowait postinstall skipifsilent',
    ]
    with open(os.path.join(d["installer_dir"],"instalador.iss"),"w",encoding="utf-8") as f:
        f.write("\n".join(lineas)+"\n")
    _ok("instalador.iss creado")

def compilar_inno():
    _sub("📦 Compilando instalador con Inno Setup")
    iscc = None
    for ruta in [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    ]:
        if os.path.exists(ruta): iscc = ruta; break

    iss_path = os.path.join(CFG["installer_dir"],"instalador.iss")
    if iscc:
        r = subprocess.run(f'"{iscc}" "{iss_path}"', shell=True)
        final = os.path.join(CFG["output_dir"], CFG["nombre_installer"]+".exe")
        if os.path.exists(final):
            size_mb = os.path.getsize(final)/1e6
            _ok(f"INSTALADOR FINAL → {final}  ({size_mb:.1f} MB)")
            return final
        else:
            _warn("No se encontró el .exe en output/")
    else:
        _warn("Inno Setup no encontrado")
        _info("Descarga gratis: https://jrsoftware.org/isinfo.php")
        _info("Luego vuelve a ejecutar este script")
    return None

# ════════════════════════════════════════════════════════════════
# ── REPORTE FINAL ────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════
def reporte_final(installer_path):
    print(f"\n{C.BOLD}{C.BLUE}{SEP}{C.RESET}")
    print(f"{C.BOLD}{C.BLUE}  RESUMEN FINAL{C.RESET}")
    print(f"{C.BOLD}{C.BLUE}{SEP}{C.RESET}")

    items = [
        ("Python compatible",   S.python_compat,                  S.python_exe),
        ("Ollama instalado",    S.ollama_ok,                      "ollama serve para iniciarlo"),
        ("Ollama corriendo",    S.ollama_corriendo,               "http://localhost:11434"),
        ("Modelos instalados",  len(S.modelos_ollama) > 0,        ", ".join(S.modelos_ollama[:4]) or "ninguno"),
        ("Paquetes Python",     len(S.pkgs_faltantes) == 0,       f"{len(S.pkgs_ok)}/{len(PAQUETES)} instalados"),
        ("App compilada",       os.path.exists(os.path.join(CFG["dist_dir"],"nexus_omni.exe")), "nexus_omni.exe"),
        ("Instalador creado",   installer_path is not None,       installer_path or "pendiente Inno Setup"),
    ]

    for desc, estado, detalle in items:
        fn = _ok if estado else _warn
        fn(f"{desc:<25} {detalle}")

    puntos = sum(1 for _,e,_ in items if e)
    score = int(puntos/len(items)*100)
    barra = "█"*int(score/10) + "░"*(10-int(score/10))
    color = C.OK if score>=80 else (C.WARN if score>=50 else C.ERR)
    print(f"\n  {C.BOLD}Score final: {color}[{barra}] {score}%{C.RESET}")

    if installer_path:
        print(f"""
{C.BOLD}{C.OK}
  ╔══════════════════════════════════════════════════════════╗
  ║  🎉 ¡NEXUS OMNI LISTO! Tu instalador está en:           ║
  ║                                                          ║
  ║  {installer_path[:54]:<54}  ║
  ║                                                          ║
  ║  ✔ Cópialo a USB / Google Drive / Mega                  ║
  ║  ✔ En cualquier PC: doble clic → instala todo           ║
  ║  ✔ Descarga Ollama + modelo automáticamente             ║
  ╚══════════════════════════════════════════════════════════╝
{C.RESET}""")
    else:
        print(f"\n  {C.WARN}El .exe de la app está en: {os.path.join(CFG['dist_dir'],'nexus_omni.exe')}")
        print(f"  Instala Inno Setup para generar el instalador completo.{C.RESET}")

    # Guardar config
    os.makedirs(CFG["base_dir"], exist_ok=True)
    with open(os.path.join(CFG["base_dir"],"config_sistema.json"),"w") as f:
        json.dump({
            "fecha":          datetime.now().isoformat(),
            "python_exe":     S.python_exe,
            "score":          score,
            "modelos":        S.modelos_ollama,
            "installer":      installer_path,
        }, f, indent=2)

# ════════════════════════════════════════════════════════════════
# MAIN — FLUJO COMPLETO
# ════════════════════════════════════════════════════════════════
def main():
    if platform.system() == "Windows":
        os.system("color"); subprocess.run("", shell=True)

    print(f"\n{C.BOLD}{C.BLUE}{SEP}")
    print("  🚀 NEXUS OMNI MULTI AI OFFLINE v4.0")
    print("     INSTALADOR COMPLETO — UN SOLO ARCHIVO")
    print("     ✅ INSTALACIÓN 100% AUTOMÁTICA — SIN PREGUNTAS")
    print(f"{SEP}{C.RESET}")
    print(f"  {C.DIM}Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}  |  OS: {platform.system()} {platform.release()}{C.RESET}\n")

    TOTAL = 15

    # ══ FASE A: DIAGNÓSTICO ══════════════════════════════
    _step(1, "DIAGNÓSTICO — Python",           TOTAL); diag_python()
    _step(2, "DIAGNÓSTICO — Hardware",         TOTAL); diag_hardware()
    _step(3, "DIAGNÓSTICO — Herramientas",     TOTAL); diag_herramientas()
    _step(4, "DIAGNÓSTICO — Ollama y modelos", TOTAL); diag_ollama()
    _step(5, "DIAGNÓSTICO — Paquetes Python",  TOTAL); diag_paquetes()

    calcular_score(); mostrar_score()

    # Mostrar resumen de lo que se va a instalar
    print(f"\n{C.BOLD}{C.CYAN}{'═'*65}")
    print("  🚀 NEXUS OMNI — INSTALACIÓN AUTOMÁTICA EN PROGRESO")
    print(f"{'═'*65}{C.RESET}")
    if S.pkgs_faltantes:
        print(f"  {C.WARN}📦 Se instalarán {len(S.pkgs_faltantes)} paquetes Python faltantes{C.RESET}")
    if not S.ollama_ok:
        print(f"  {C.WARN}🤖 Se descargará e instalará Ollama{C.RESET}")
    if not S.modelos_ollama:
        print(f"  {C.WARN}🧠 Se descargará el modelo phi3 (~2.3 GB){C.RESET}")
    if not S.pkgs_faltantes and S.ollama_ok and S.modelos_ollama:
        print(f"  {C.OK}✅ Sistema listo — procediendo a compilar la app{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*65}{C.RESET}\n")

    # ══ FASE B: INSTALACIÓN ══════════════════════════════
    _step(6,  "INSTALACIÓN — Ollama",          TOTAL); instalar_ollama_si_falta()
    _step(7,  "INSTALACIÓN — Entorno virtual", TOTAL); gestionar_venv()
    _step(8,  "INSTALACIÓN — Paquetes Python", TOTAL); instalar_paquetes()
    _step(9,  "INSTALACIÓN — Modelos Ollama",  TOTAL); instalar_modelos_ollama()

    # Re-verificar paquetes después de instalar
    _sub("🔄 Verificación final de paquetes")
    S.pkgs_ok.clear(); S.pkgs_faltantes.clear()
    diag_paquetes()

    # ══ FASE C: CONSTRUCCIÓN ═════════════════════════════
    _step(10, "BUILD — Carpetas",              TOTAL); crear_carpetas()
    _step(11, "BUILD — Servidores MCP",        TOTAL); crear_mcp_servers()
    _step(12, "BUILD — App principal",         TOTAL); crear_asistente_py()
    _step(13, "BUILD — Recursos (icono/imgs)", TOTAL)
    crear_icono(); crear_wizard_images(); crear_licencia()

    _step(14, "BUILD — Compilar .exe",         TOTAL)
    exe_ok = compilar_exe()

    _step(15, "BUILD — Instalador Inno Setup", TOTAL)
    crear_ps1(); crear_iss()
    installer_path = compilar_inno() if exe_ok else None

    # ══ REPORTE ══════════════════════════════════════════
    reporte_final(installer_path)

    if installer_path or exe_ok:
        try: os.startfile(CFG["output_dir"] if installer_path else CFG["dist_dir"])
        except Exception: pass

    input(f"\n  {C.BOLD}Presiona ENTER para cerrar...{C.RESET}")

if __name__ == "__main__":
    main()