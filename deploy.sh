#!/bin/bash

# KidsFun Backend - Script de despliegue para producción
# Este script despliega el backend Node.js en producción

set -e

echo "🎪 KidsFun Backend - Despliegue de Producción"
echo "=============================================="

# Verificar si estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo "❌ package.json no encontrado. Asegúrate de estar en el directorio correcto"
    exit 1
fi

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado. Crea el archivo .env con las configuraciones de producción"
    exit 1
fi

# Verificar si PM2 está instalado
if ! command -v pm2 &> /dev/null; then
    echo "📦 Instalando PM2..."
    npm install -g pm2
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Instalar dependencias de producción
echo "📦 Instalando dependencias de producción..."
npm ci --only=production

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
npm run migrate

# Detener aplicación si está ejecutándose
echo "🛑 Deteniendo aplicación si está ejecutándose..."
pm2 stop kidsfun-backend 2>/dev/null || true
pm2 delete kidsfun-backend 2>/dev/null || true

# Iniciar aplicación con PM2
echo "🚀 Iniciando aplicación con PM2..."
pm2 start ecosystem.config.js --env production

# Guardar configuración de PM2
echo "💾 Guardando configuración de PM2..."
pm2 save

# Configurar PM2 para iniciar con el sistema
echo "⚙️  Configurando PM2 para iniciar con el sistema..."
pm2 startup 2>/dev/null || true

# Mostrar estado
echo "📊 Estado de la aplicación:"
pm2 status

echo ""
echo "✅ Despliegue completado exitosamente!"
echo "🌐 La aplicación está ejecutándose en modo producción"
echo "📊 Para ver logs: pm2 logs kidsfun-backend"
echo "🛑 Para detener: pm2 stop kidsfun-backend"
echo "🔄 Para reiniciar: pm2 restart kidsfun-backend" 