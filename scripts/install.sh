#!/bin/bash

# Script de instalación para ZTech Twitter Bot
# Ejecutar con: bash scripts/install.sh

set -e

echo "🤖 Instalando ZTech Twitter Bot..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detectado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip."
    exit 1
fi

# Crear entorno virtual (opcional)
read -p "¿Crear entorno virtual? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Entorno virtual creado y activado"
fi

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip3 install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p logs
mkdir -p data

# Configurar archivo de entorno
if [ ! -f .env ]; then
    echo "⚙️ Configurando archivo de entorno..."
    cp env.example .env
    echo "✅ Archivo .env creado. Por favor edita las credenciales."
else
    echo "ℹ️ Archivo .env ya existe"
fi

# Verificar configuración
echo "🔍 Verificando configuración..."
python3 main.py --config-check

if [ $? -eq 0 ]; then
    echo "✅ Configuración válida"
else
    echo "⚠️ Configuración incompleta. Por favor revisa el archivo .env"
fi

echo ""
echo "🎉 Instalación completada!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Edita el archivo .env con tus credenciales de Twitter"
echo "2. Ejecuta: python3 main.py --mode test"
echo "3. Si todo funciona, ejecuta: python3 main.py --mode continuous"
echo ""
echo "📖 Para más información, consulta el README.md"
