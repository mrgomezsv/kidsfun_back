#!/bin/bash

# Script para actualizar la seguridad del backend
# Uso: sudo ./update_security.sh

set -e

echo "🔒 Actualizando seguridad del KidsFun Backend..."

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Variables
PROJECT_DIR="/opt/kidsfun-backend"
SERVICE_NAME="kidsfun-backend"

echo "📁 Verificando directorio del proyecto..."
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ No se encontró el directorio del proyecto en $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

echo "🔄 Haciendo backup de la configuración actual..."
if [ -f "main.py" ]; then
    cp main.py main.py.backup.$(date +%Y%m%d_%H%M%S)
fi

echo "📥 Obteniendo cambios del repositorio..."
git fetch origin
git reset --hard origin/mrg_prod

echo "🐍 Actualizando dependencias..."
source venv/bin/activate
pip install -r requirements.txt

echo "🔧 Aplicando migraciones de base de datos..."
alembic upgrade head

echo "🛡️ Verificando configuración de seguridad..."
if [ ! -f "app/middleware.py" ]; then
    echo "❌ No se encontró el archivo de middleware de seguridad"
    exit 1
fi

echo "🔄 Reiniciando servicios..."
systemctl restart $SERVICE_NAME
systemctl restart nginx

echo "✅ Verificando estado de los servicios..."
sleep 3

if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ Servicio $SERVICE_NAME está activo"
else
    echo "❌ Error: Servicio $SERVICE_NAME no está activo"
    systemctl status $SERVICE_NAME
    exit 1
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Servicio nginx está activo"
else
    echo "❌ Error: Servicio nginx no está activo"
    systemctl status nginx
    exit 1
fi

echo "🔍 Verificando endpoints de seguridad..."
sleep 2

# Verificar health check
if curl -s -f "https://api.kidsfunyfiestasinfantiles.com/health" > /dev/null; then
    echo "✅ Health check funcionando"
else
    echo "❌ Error en health check"
fi

# Verificar security info
if curl -s -f "https://api.kidsfunyfiestasinfantiles.com/security-info" > /dev/null; then
    echo "✅ Security info endpoint funcionando"
else
    echo "❌ Error en security info endpoint"
fi

echo "📊 Mostrando información de seguridad actualizada..."
curl -s "https://api.kidsfunyfiestasinfantiles.com/security-info" | python3 -m json.tool

echo ""
echo "🎉 ¡Actualización de seguridad completada!"
echo ""
echo "📋 Resumen de mejoras implementadas:"
echo "   ✅ Rate limiting (10 requests/segundo por IP)"
echo "   ✅ Validación de entrada (XSS, SQL injection protection)"
echo "   ✅ Headers de seguridad (HSTS, CSP, X-Frame-Options)"
echo "   ✅ Trusted hosts middleware"
echo "   ✅ Logging de requests para auditoría"
echo "   ✅ Validación de User-Agent y Content-Length"
echo ""
echo "🔍 Para verificar la seguridad:"
echo "   curl https://api.kidsfunyfiestasinfantiles.com/security-info"
echo ""
echo "📝 Para ver logs de seguridad:"
echo "   sudo journalctl -u kidsfun-backend -f"
echo ""
echo "🛡️ La API ahora está protegida contra:"
echo "   - Ataques de rate limiting"
echo "   - XSS (Cross-Site Scripting)"
echo "   - SQL Injection"
echo "   - Command Injection"
echo "   - Clickjacking"
echo "   - MIME sniffing"
echo "   - Requests maliciosos" 