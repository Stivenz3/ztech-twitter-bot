@echo off
REM Script de instalación para ZTech Twitter Bot en Windows
REM Ejecutar con: scripts\install.bat

echo 🤖 Instalando ZTech Twitter Bot...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instala Python 3.8 o superior.
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Verificar pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está instalado. Por favor instala pip.
    pause
    exit /b 1
)

REM Crear entorno virtual (opcional)
set /p create_venv="¿Crear entorno virtual? (y/n): "
if /i "%create_venv%"=="y" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual creado y activado
)

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

REM Crear directorios necesarios
echo 📁 Creando directorios...
if not exist logs mkdir logs
if not exist data mkdir data

REM Configurar archivo de entorno
if not exist .env (
    echo ⚙️ Configurando archivo de entorno...
    copy env.example .env
    echo ✅ Archivo .env creado. Por favor edita las credenciales.
) else (
    echo ℹ️ Archivo .env ya existe
)

REM Verificar configuración
echo 🔍 Verificando configuración...
python main.py --config-check

if errorlevel 1 (
    echo ⚠️ Configuración incompleta. Por favor revisa el archivo .env
) else (
    echo ✅ Configuración válida
)

echo.
echo 🎉 Instalación completada!
echo.
echo 📝 Próximos pasos:
echo 1. Edita el archivo .env con tus credenciales de Twitter
echo 2. Ejecuta: python main.py --mode test
echo 3. Si todo funciona, ejecuta: python main.py --mode continuous
echo.
echo 📖 Para más información, consulta el README.md
pause
