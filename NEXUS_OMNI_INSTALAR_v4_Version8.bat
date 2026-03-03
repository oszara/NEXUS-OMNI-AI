@echo off
title NEXUS OMNI MULTI AI - Instalador v4.0
color 0A
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cls
echo.
echo ====================================================
echo NEXUS OMNI MULTI AI OFFLINE v4.0
echo Instalacion automatica completa
echo ====================================================
echo.
echo Iniciando... NO cierre esta ventana.
echo Este proceso puede tardar 15-30 minutos.
echo.

echo [0/8] Configurando PATH de Python 3.11...
set "PY311=%LOCALAPPDATA%\Programs\Python\Python311"
set "PY311S=%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
set "PATH=%PY311%;%PY311S%;%PATH%"
setx PATH "%PY311%;%PY311S%;%PATH%" >nul 2>&1
echo [OK] PATH configurado.
echo.

echo [1/8] Verificando Python 3.11...
set PYTHON311=
if exist "%PY311%\python.exe" (
    set "PYTHON311=%PY311%\python.exe"
    echo [OK] Python 3.11 encontrado: %PYTHON311%
) else (
    echo [INFO] Python 3.11 no encontrado. Descargando e instalando...
    powershell -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-3.11.9-amd64.exe'" 2>nul
    if exist "%TEMP%\python-3.11.9-amd64.exe" (
        echo [INFO] Instalando Python 3.11.9...
        "%TEMP%\python-3.11.9-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
        timeout /t 15 /nobreak >nul
        if exist "%PY311%\python.exe" (
            set "PYTHON311=%PY311%\python.exe"
            set "PATH=%PY311%;%PY311S%;%PATH%"
            setx PATH "%PY311%;%PY311S%;%PATH%" >nul 2>&1
            echo [OK] Python 3.11 instalado y PATH configurado.
        ) else (
            echo [ERROR] No se pudo instalar Python 3.11.
            echo Descargalo: https://www.python.org/downloads/release/python-3119/
            echo Marca "Add Python to PATH" al instalar.
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] No se pudo descargar Python 3.11.
        pause
        exit /b 1
    )
)
echo.

echo [2/8] Preparando carpeta de instalacion...
set "INSTALL_DIR=%USERPROFILE%\Desktop\NEXUS_OMNI_AI"
set "APP_DIR=%USERPROFILE%\Desktop\NEXUS_OMNI_AI\app"
set "DIST_DIR=%USERPROFILE%\Desktop\NEXUS_OMNI_AI\app\dist"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%APP_DIR%" mkdir "%APP_DIR%"
set "BAT_DIR=%~dp0"
set SCRIPT_PY=
if exist "%BAT_DIR%NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py" (
    set "SCRIPT_PY=%BAT_DIR%NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py"
    echo [OK] Script Python encontrado.
) else (
    echo [ERROR] Falta: NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py
    echo Ponlo en la misma carpeta que este .bat
    pause
    exit /b 1
)
echo.

echo [3/8] Actualizando pip...
"%PYTHON311%" -m pip install --upgrade pip wheel setuptools --quiet --timeout 120 2>nul
echo [OK] pip listo.
echo.

echo [4/8] Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Descargando Ollama...
    powershell -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile '%TEMP%\OllamaSetup.exe'" 2>nul
    if exist "%TEMP%\OllamaSetup.exe" (
        echo [INFO] Instalando Ollama...
        "%TEMP%\OllamaSetup.exe" /SILENT /NORESTART
        timeout /t 8 /nobreak >nul
        echo [OK] Ollama instalado.
    ) else (
        echo [AVISO] Descarga manual: https://ollama.com/download
    )
) else (
    echo [OK] Ollama ya instalado.
)
echo.

echo [5/8] Instalando los 25 paquetes en Python 3.11 (5-15 min)...
echo.

echo - Core...
"%PYTHON311%" -m pip install pillow requests psutil pydantic rich python-dotenv --quiet --timeout 180 2>nul
echo [OK] Core instalado.

echo - Ollama SDK...
"%PYTHON311%" -m pip install ollama --quiet --timeout 180 2>nul

echo - PyInstaller...
"%PYTHON311%" -m pip install pyinstaller --quiet --timeout 180 2>nul

echo - LangChain + LangGraph...
"%PYTHON311%" -m pip install "langchain==0.3.25" "langchain-ollama==0.3.3" "langchain-community==0.3.27" "langgraph==0.4.1" --quiet --timeout 300 2>nul

echo - Forzando dependencias criticas POST-LangChain...
"%PYTHON311%" -m pip install --force-reinstall "huggingface-hub>=1.3.0,<2.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "tokenizers>=0.22.0,<=0.23.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "typer>=0.24.0" --quiet --timeout 180 2>nul
echo [OK] Dependencias criticas forzadas.

echo - CrewAI...
"%PYTHON311%" -m pip install "crewai==0.86.0" --quiet --timeout 300 2>nul

echo - Forzando dependencias criticas POST-CrewAI...
"%PYTHON311%" -m pip install --force-reinstall "huggingface-hub>=1.3.0,<2.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "tokenizers>=0.22.0,<=0.23.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "typer>=0.24.0" --quiet --timeout 180 2>nul

echo - AutoGen...
"%PYTHON311%" -m pip install "pyautogen==0.3.2" --quiet --timeout 300 2>nul

echo - MCP...
"%PYTHON311%" -m pip install mcp --quiet --timeout 180 2>nul

echo - ChromaDB + RAG...
"%PYTHON311%" -m pip install chromadb sentence-transformers pypdf python-docx --quiet --timeout 300 2>nul

echo - Voz...
"%PYTHON311%" -m pip install pyttsx3 SpeechRecognition --quiet --timeout 180 2>nul

echo - Diffusers + Transformers (al final)...
"%PYTHON311%" -m pip install diffusers transformers accelerate safetensors --quiet --timeout 300 2>nul

echo - Forzando dependencias criticas FINALES...
"%PYTHON311%" -m pip install --force-reinstall "huggingface-hub>=1.3.0,<2.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "tokenizers>=0.22.0,<=0.23.0" --quiet --timeout 180 2>nul
"%PYTHON311%" -m pip install --force-reinstall "typer>=0.24.0" --quiet --timeout 180 2>nul

echo.
echo [OK] 25 paquetes instalados en Python 3.11.
echo.

echo [6/8] Descargando modelo phi3 (~2.3 GB)...
start /b /min "" ollama serve
timeout /t 5 /nobreak >nul
ollama list 2>nul | findstr "phi3" >nul 2>&1
if errorlevel 1 (
    ollama pull phi3
    echo [OK] phi3 descargado.
) else (
    echo [OK] phi3 ya instalado.
)
echo.

echo [7/8] Compilando NEXUS OMNI con PyInstaller...
echo.

rem Copiar el script al APP_DIR
copy "%SCRIPT_PY%" "%APP_DIR%\NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py" >nul 2>&1

rem Compilar con PyInstaller usando nombre "asistente" para coincidir con instalador.iss
cd /d "%APP_DIR%"
"%PYTHON311%" -m PyInstaller --onefile --windowed --name asistente --distpath "%DIST_DIR%" --workpath "%APP_DIR%\build" --specpath "%APP_DIR%" "NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py"

echo.
echo - Verificando .exe generado...
if exist "%DIST_DIR%\asistente.exe" (
    echo [OK] asistente.exe generado correctamente.
) else (
    echo [AVISO] asistente.exe no encontrado. Buscando cualquier .exe...
    dir "%DIST_DIR%\*.exe" 2>nul
)
echo.

echo [8/8] Creando acceso directo en Escritorio...
set "EXE_PATH=%DIST_DIR%\asistente.exe"
if exist "%EXE_PATH%" (
    powershell -Command "$ws=New-Object -ComObject WScript.Shell; $sc=$ws.CreateShortcut('%USERPROFILE%\Desktop\NEXUS OMNI AI.lnk'); $sc.TargetPath='%EXE_PATH%'; $sc.WorkingDirectory='%APP_DIR%'; $sc.Description='NEXUS OMNI Multi-Agente IA v4.0'; $sc.Save()" 2>nul
    echo [OK] Acceso directo creado.
) else (
    echo [AVISO] El .exe no se genero. Revisa errores arriba.
)
echo.

echo ====================================================
echo INSTALACION COMPLETADA
echo.
echo Abre "NEXUS OMNI AI" desde tu Escritorio.
echo Carpeta: %USERPROFILE%\Desktop\NEXUS_OMNI_AI\
echo ====================================================
echo.

explorer "%USERPROFILE%\Desktop\NEXUS_OMNI_AI"
if exist "%EXE_PATH%" (
    start "" "%EXE_PATH%"
)
pause
exit /b 0