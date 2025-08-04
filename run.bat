@echo off
:: Establece el título de la ventana.
title Servidor RAG - API y Chat

:: Cambia al directorio del script.
cd /d "%~dp0"

echo.
echo =======================================================
echo      INICIANDO API Y CHAT DEL MODELO RAG
echo =======================================================
echo.

:: Verifica si Python está instalado.
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
echo [PASO 2] Iniciando el servidor de la aplicacion...
echo.
echo El servidor estara disponible en: http://127.0.0.1:8000
echo.
echo Para detener el servidor, cierra esta ventana o presiona CTRL+C.
echo.

:: Ejecuta el servidor Uvicorn.
uvicorn app.main:app --host 0.0.0.0 --port 8000