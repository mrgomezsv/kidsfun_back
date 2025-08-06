#!/bin/bash

# Script para ejecutar diagnóstico del sistema de productos
# Uso: sudo ./run_diagnosis.sh

set -e

echo "🔍 Ejecutando diagnóstico del sistema de productos..."

# Verificar que estamos en el directorio correcto
if [ ! -f "diagnose_products.py" ]; then
    echo "❌ Error: No se encontró el script de diagnóstico"
    echo "   Asegúrate de estar en el directorio /opt/kidsfun-backend"
    exit 1
fi

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
fi

# Ejecutar diagnóstico
echo "🚀 Iniciando diagnóstico..."
python3 diagnose_products.py

echo "✅ Diagnóstico completado" 