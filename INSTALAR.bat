@echo off
chcp 65001 >nul 2>&1
title NEXUS OMNI AI — Instalador Un Solo Click
color 0A
cls
echo.
echo ============================================================
echo   NEXUS OMNI MULTI AI v4.0 — INSTALACION UN SOLO CLICK
echo ============================================================
echo.
echo   Este script instalara todo lo necesario automaticamente:
echo     - Python 3.11 (si no esta instalado)
echo     - Ollama + modelo phi3
echo     - 25 paquetes de IA (CrewAI, LangGraph, AutoGen...)
echo     - Compilacion de la app (.exe)
echo     - Acceso directo en el Escritorio
echo.
echo   NO cierre esta ventana. Puede tardar 15-30 minutos.
echo.
echo ============================================================
echo.

REM Detectar Python compatible (3.10, 3.11, 3.12)
set "PYTHON_EXE="

REM Intentar Python del sistema
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('python -c "import sys; print(sys.version_info.minor)"  2^>nul') do set "PY_MINOR=%%v"
    if "%PY_MINOR%"=="10" set "PYTHON_EXE=python"
    if "%PY_MINOR%"=="11" set "PYTHON_EXE=python"
    if "%PY_MINOR%"=="12" set "PYTHON_EXE=python"
)

REM Intentar Python 3.11 en ubicacion tipica
if "%PYTHON_EXE%"=="" (
    set "PY311=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    if exist "%PY311%" set "PYTHON_EXE=%PY311%"
)

REM Si no hay Python compatible, ejecutar el BAT completo que lo instala
if "%PYTHON_EXE%"=="" (
    echo [INFO] Python 3.10-3.12 no encontrado.
    echo [INFO] Ejecutando instalador completo que incluye Python...
    echo.
    call "%~dp0NEXUS_OMNI_INSTALAR_v4_Version8.bat"
    exit /b %errorlevel%
)

echo [OK] Python encontrado: %PYTHON_EXE%
echo.

REM Ejecutar el script principal de Python (instalacion automatica completa)
echo [INFO] Ejecutando instalador principal...
echo.
"%PYTHON_EXE%" "%~dp0NEXUS_OMNI_AI_OFFLINE_MULTI_v4_MEJORADO.py"

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Hubo un problema. Intentando con el instalador alternativo...
    call "%~dp0NEXUS_OMNI_INSTALAR_v4_Version8.bat"
)

exit /b 0
