@echo off
REM Script para ejecutar ZTech Twitter Bot en Windows
REM Uso: scripts\run.bat [modo] [tipo]

set MODE=%1
set POST_TYPE=%2

if "%MODE%"=="" set MODE=continuous
if "%POST_TYPE%"=="" set POST_TYPE=single

echo 🤖 Iniciando ZTech Twitter Bot...
echo 📋 Modo: %MODE%
echo 📝 Tipo de publicación: %POST_TYPE%
echo.

REM Verificar que existe el archivo .env
if not exist .env (
    echo ❌ Archivo .env no encontrado.
    echo 📝 Copia env.example a .env y configura tus credenciales.
    pause
    exit /b 1
)

REM Verificar configuración
echo 🔍 Verificando configuración...
python main.py --config-check

if errorlevel 1 (
    echo ❌ Error en la configuración. Revisa el archivo .env
    pause
    exit /b 1
)

echo ✅ Configuración válida
echo.

REM Ejecutar bot según el modo
if "%MODE%"=="test" (
    echo 🧪 Ejecutando modo de prueba...
    python main.py --mode test
) else if "%MODE%"=="single" (
    echo 📝 Ejecutando publicación única...
    python main.py --mode single --post-type %POST_TYPE%
) else if "%MODE%"=="stats" (
    echo 📊 Mostrando estadísticas...
    python main.py --mode stats
) else if "%MODE%"=="cleanup" (
    echo 🧹 Limpiando datos antiguos...
    python main.py --mode cleanup
) else if "%MODE%"=="continuous" (
    echo 🔄 Iniciando modo continuo...
    echo ⏹️ Presiona Ctrl+C para detener
    python main.py --mode continuous
) else (
    echo ❌ Modo no válido: %MODE%
    echo 📋 Modos disponibles: test, single, stats, cleanup, continuous
    pause
    exit /b 1
)

echo.
echo ✅ Ejecución completada
pause
