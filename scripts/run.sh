#!/bin/bash

# Script para ejecutar ZTech Twitter Bot
# Uso: bash scripts/run.sh [modo] [tipo]

set -e

# Configuración por defecto
MODE=${1:-continuous}
POST_TYPE=${2:-single}

echo "🤖 Iniciando ZTech Twitter Bot..."
echo "📋 Modo: $MODE"
echo "📝 Tipo de publicación: $POST_TYPE"
echo ""

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado."
    echo "📝 Copia env.example a .env y configura tus credenciales."
    exit 1
fi

# Verificar configuración
echo "🔍 Verificando configuración..."
python3 main.py --config-check

if [ $? -ne 0 ]; then
    echo "❌ Error en la configuración. Revisa el archivo .env"
    exit 1
fi

echo "✅ Configuración válida"
echo ""

# Ejecutar bot según el modo
case $MODE in
    "test")
        echo "🧪 Ejecutando modo de prueba..."
        python3 main.py --mode test
        ;;
    "single")
        echo "📝 Ejecutando publicación única..."
        python3 main.py --mode single --post-type $POST_TYPE
        ;;
    "stats")
        echo "📊 Mostrando estadísticas..."
        python3 main.py --mode stats
        ;;
    "cleanup")
        echo "🧹 Limpiando datos antiguos..."
        python3 main.py --mode cleanup
        ;;
    "continuous")
        echo "🔄 Iniciando modo continuo..."
        echo "⏹️ Presiona Ctrl+C para detener"
        python3 main.py --mode continuous
        ;;
    *)
        echo "❌ Modo no válido: $MODE"
        echo "📋 Modos disponibles: test, single, stats, cleanup, continuous"
        exit 1
        ;;
esac

echo ""
echo "✅ Ejecución completada"
