#!/bin/bash

# Script para configurar Nginx correctamente
# Uso: sudo ./setup_nginx.sh

set -e

echo "🔧 Configurando Nginx para KidsFun Backend..."

# Verificar si estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root"
    exit 1
fi

# 1. Agregar rate limiting al archivo principal de Nginx
echo "📝 Configurando rate limiting en nginx.conf..."

# Buscar la línea donde agregar rate limiting
if ! grep -q "limit_req_zone.*zone=api" /etc/nginx/nginx.conf; then
    # Agregar rate limiting antes de los includes
    sed -i '/include \/etc\/nginx\/sites-enabled\/\*/i \    # Rate limiting zones\n    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;\n' /etc/nginx/nginx.conf
    echo "✅ Rate limiting agregado a nginx.conf"
else
    echo "⚠️  Rate limiting ya existe en nginx.conf"
fi

# 2. Copiar configuración del sitio
echo "📝 Configurando sitio web..."
cp kidsfun-backend.nginx /etc/nginx/sites-available/kidsfun-backend

# 3. Habilitar sitio y deshabilitar default
ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 4. Verificar configuración
echo "🔍 Verificando configuración de Nginx..."
if nginx -t; then
    echo "✅ Configuración de Nginx válida"
else
    echo "❌ Error en configuración de Nginx"
    exit 1
fi

# 5. Reiniciar Nginx
echo "🔄 Reiniciando Nginx..."
systemctl restart nginx

# 6. Verificar estado
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx está funcionando correctamente"
else
    echo "❌ Error al iniciar Nginx"
    systemctl status nginx
    exit 1
fi

echo ""
echo "🎉 Nginx configurado exitosamente!"
echo "📋 Próximos pasos:"
echo "   • Configurar SSL: sudo certbot --nginx -d api.kidsfunyfiestasinfantiles.com"
echo "   • Verificar API: curl http://api.kidsfunyfiestasinfantiles.com/health" 