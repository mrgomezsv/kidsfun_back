#!/bin/bash

# Script para configurar comando global de actualización
# Uso: sudo ./setup_update_command.sh

set -e

echo "🔧 Configurando comando global de actualización..."

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Crear comando global
cat > /usr/local/bin/update-kidsfun << 'EOF'
#!/bin/bash

# Comando global para actualizar KidsFun Backend
# Uso: sudo update-kidsfun

if [ "$EUID" -ne 0 ]; then
    echo "❌ Este comando debe ejecutarse como root (sudo)"
    exit 1
fi

PROJECT_DIR="/opt/kidsfun-backend"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ No se encontró el proyecto en $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

if [ -f "update.sh" ]; then
    echo "🚀 Ejecutando actualización con script universal..."
    ./update.sh
elif [ -f "update_security.sh" ]; then
    echo "🔒 Ejecutando actualización de seguridad..."
    ./update_security.sh
else
    echo "⚠️ No se encontró script de actualización, ejecutando actualización manual..."
    
    # Actualización manual
    echo "📥 Obteniendo cambios del repositorio..."
    git config --global --add safe.directory "$PROJECT_DIR" 2>/dev/null || true
    git fetch origin
    git reset --hard origin/mrg_prod
    
    echo "🐍 Actualizando dependencias..."
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    
    echo "🔧 Aplicando migraciones..."
    alembic upgrade head
    
    echo "🔄 Reiniciando servicios..."
    systemctl restart kidsfun-backend
    systemctl restart nginx
    
    echo "✅ Verificando servicios..."
    sleep 5
    systemctl status kidsfun-backend --no-pager -l
    systemctl status nginx --no-pager -l
    
    echo "🎉 Actualización completada!"
fi
EOF

# Dar permisos de ejecución
chmod +x /usr/local/bin/update-kidsfun

# Crear alias para el usuario root
echo 'alias update-kidsfun="sudo update-kidsfun"' >> /root/.bashrc

# Crear alias para otros usuarios si existen
if [ -d "/home" ]; then
    for user_home in /home/*; do
        if [ -d "$user_home" ]; then
            user=$(basename "$user_home")
            echo "alias update-kidsfun='sudo update-kidsfun'" >> "$user_home/.bashrc"
        fi
    done
fi

echo "✅ Comando global configurado exitosamente!"
echo ""
echo "🎯 Ahora puedes actualizar el proyecto con un solo comando:"
echo "   sudo update-kidsfun"
echo ""
echo "📋 También puedes usar:"
echo "   cd /opt/kidsfun-backend && sudo ./update.sh"
echo "   cd /opt/kidsfun-backend && sudo ./update_security.sh"
echo ""
echo "🔄 Para aplicar los cambios en la sesión actual:"
echo "   source ~/.bashrc" 