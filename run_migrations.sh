#!/bin/bash

# Script para ejecutar migraciones de la base de datos
echo "Ejecutando migraciones de la base de datos..."

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Entorno virtual activado"
fi

# Ejecutar migraciones
echo "Ejecutando migraciones..."
alembic upgrade head

echo "Migraciones completadas exitosamente" 