@echo off
:: Establece el título de la ventana de la consola.
title Cargador de Datos RAG

:: Cambia al directorio donde se encuentra el script.
cd /d "%~dp0"

echo.
echo =======================================================
echo      CARGADOR DE BASE DE DATOS PARA EL MODELO RAG
echo =======================================================
echo.
echo Este script instalara las dependencias y procesara
echo los PDFs en la carpeta 'source'.
echo.

:: Verifica si Python está instalado y en el PATH.
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no se encuentra. Por favor, instala Python y asegúrate de que esté en el PATH.
    pause
    exit
)

:: Verifica si requirements.txt existe.
if not exist "requirements.txt" (
    echo [ERROR] No se encuentra el archivo requirements.txt.
    pause
    exit
)

echo [PASO 1] Verificando e instalando dependencias...
pip install -r requirements.txt

echo.
echo [PASO 2] Iniciando el proceso de carga de PDFs...
echo No cierres esta ventana hasta que el proceso finalice.
echo.

:: Ejecuta el script de ingesta de datos.
python -m scripts.ingest_data

echo.
echo =======================================================
echo      PROCESO DE CARGA FINALIZADO
echo =======================================================
echo.
pause