#!/bin/bash

# Script para configurar comando global de actualización AUTOMÁTICA
# Uso: sudo ./setup_update_command.sh

set -e

echo "🔧 Configurando comando global de actualización AUTOMÁTICA..."

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Crear comando global AUTOMÁTICO
cat > /usr/local/bin/update-kidsfun << 'EOF'
#!/bin/bash

# Comando global AUTOMÁTICO para actualizar KidsFun Backend
# Uso: sudo update-kidsfun
# Este comando es COMPLETAMENTE AUTOMÁTICO y SEGURO

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

echo "🚀 Ejecutando actualización AUTOMÁTICA del KidsFun Backend..."
echo "⚠️  Este proceso es COMPLETAMENTE AUTOMÁTICO"
echo "⚠️  No se requiere intervención manual"
echo ""

if [ -f "update.sh" ]; then
    echo "🚀 Ejecutando script de actualización AUTOMÁTICA..."
    ./update.sh
elif [ -f "update_security.sh" ]; then
    echo "🔒 Ejecutando actualización de seguridad..."
    ./update_security.sh
else
    echo "⚠️ No se encontró script de actualización, ejecutando actualización manual AUTOMÁTICA..."
    
    # Actualización manual AUTOMÁTICA
    echo "📥 Obteniendo cambios del repositorio automáticamente..."
    git config --global --add safe.directory "$PROJECT_DIR" 2>/dev/null || true
    git fetch origin --quiet
    git reset --hard origin/mrg_prod --quiet
    
    echo "🐍 Actualizando dependencias automáticamente..."
    source venv/bin/activate
    pip install -r requirements.txt --quiet --no-cache-dir
    
    echo "🔧 Aplicando migraciones automáticamente..."
    alembic upgrade head --quiet
    
    echo "🔄 Reiniciando servicios automáticamente..."
    systemctl restart kidsfun-backend
    systemctl restart nginx
    
    echo "✅ Verificando servicios automáticamente..."
    sleep 5
    
    # Verificar servicios con retry
    for i in {1..3}; do
        if systemctl is-active --quiet kidsfun-backend; then
            echo "✅ Servicio kidsfun-backend está activo"
            break
        else
            echo "⚠️ Reintentando kidsfun-backend (intento $i/3)"
            systemctl restart kidsfun-backend
            sleep 3
        fi
    done
    
    for i in {1..3}; do
        if systemctl is-active --quiet nginx; then
            echo "✅ Servicio nginx está activo"
            break
        else
            echo "⚠️ Reintentando nginx (intento $i/3)"
            systemctl restart nginx
            sleep 3
        fi
    done
    
    echo "🎉 Actualización AUTOMÁTICA completada!"
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

echo "✅ Comando global AUTOMÁTICO configurado exitosamente!"
echo ""
echo "🎯 Ahora puedes actualizar el proyecto con un solo comando AUTOMÁTICO:"
echo "   sudo update-kidsfun"
echo ""
echo "📋 También puedes usar:"
echo "   cd /opt/kidsfun-backend && sudo ./update.sh"
echo "   cd /opt/kidsfun-backend && sudo ./update_security.sh"
echo ""
echo "🔄 Para aplicar los cambios en la sesión actual:"
echo "   source ~/.bashrc"
echo ""
echo "⚠️  IMPORTANTE: El comando es COMPLETAMENTE AUTOMÁTICO"
echo "⚠️  No requiere intervención manual"
echo "⚠️  Incluye retry automático en caso de errores" 