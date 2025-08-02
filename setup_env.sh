#!/bin/bash

# Script para configurar el archivo .env
# Uso: ./setup_env.sh

set -e

echo "🔧 Configurando archivo .env para KidsFun Backend..."

# Verificar si estamos en el directorio correcto
if [ ! -f "env.example" ]; then
    echo "❌ Error: No se encontró env.example. Asegúrate de estar en el directorio del proyecto."
    exit 1
fi

# Crear archivo .env desde la plantilla
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Archivo .env creado desde plantilla"
else
    echo "⚠️  Archivo .env ya existe"
fi

# Generar SECRET_KEY seguro
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Configurar variables con valores por defecto
echo "📝 Configurando variables de entorno..."

# Reemplazar SECRET_KEY
sed -i "s/your-secret-key-here-change-this-in-production/$SECRET_KEY/g" .env

# Configurar DATABASE_URL (asumiendo que PostgreSQL está en el mismo servidor)
sed -i "s|postgresql://username:password@host:port/database_name|postgresql://mrgomez:Karin2100@localhost:5432/smap_kf|g" .env

# Configurar SMTP (Gmail)
sed -i "s/your-email@gmail.com/kidsfun.developer@gmail.com/g" .env
sed -i "s/your-app-password/Karin2100/g" .env

# Configurar CORS para el dominio de producción
sed -i 's|ALLOWED_ORIGINS=\["http://localhost:4200", "https://kidsfunyfiestasinfantiles.com"\]|ALLOWED_ORIGINS=\["http://localhost:4200", "https://kidsfunyfiestasinfantiles.com", "https://www.kidsfunyfiestasinfantiles.com", "https://api.kidsfunyfiestasinfantiles.com"\]|g' .env

# Configurar directorios de producción
sed -i "s|UPLOAD_DIR=media|UPLOAD_DIR=/opt/kidsfun-backend/media|g" .env
sed -i "s|ACCESS_LOG=logs/access.log|ACCESS_LOG=/opt/kidsfun-backend/logs/access.log|g" .env
sed -i "s|ERROR_LOG=logs/error.log|ERROR_LOG=/opt/kidsfun-backend/logs/error.log|g" .env

echo "✅ Configuración completada"
echo ""
echo "📋 Variables configuradas:"
echo "   • SECRET_KEY: Generado automáticamente"
echo "   • DATABASE_URL: postgresql://mrgomez:Karin2100@localhost:5432/smap_kf"
echo "   • SMTP_USER: kidsfun.developer@gmail.com"
echo "   • UPLOAD_DIR: /opt/kidsfun-backend/media"
echo "   • CORS: Incluye api.kidsfunyfiestasinfantiles.com"
echo ""
echo "⚠️  IMPORTANTE: Verifica la configuración antes de continuar:"
echo "   cat .env"
echo ""
echo "🔧 Si necesitas cambiar algo, edita el archivo .env manualmente:"
echo "   nano .env" 