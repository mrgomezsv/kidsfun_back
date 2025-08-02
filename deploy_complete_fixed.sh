#!/bin/bash

# Script de despliegue completo para KidsFun Backend (VERSIÓN CORREGIDA)
# Autor: KidsFun Development Team
# Fecha: 2024

set -e

# Configuración
PROJECT_NAME="kidsfun-backend"
DOMAIN="api.kidsfunyfiestasinfantiles.com"
PROJECT_DIR="/opt/kidsfun-backend"
GITHUB_REPO="https://github.com/mrgomezsv/kidsfun_back.git"
BRANCH="mrg_prod"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🚀 Desplegando KidsFun Backend en Ubuntu Server..."
echo "   • Dominio: $DOMAIN"
echo "   • Directorio: $PROJECT_DIR"
echo ""

# Verificar si estamos como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root"
    exit 1
fi

# Verificar si el proyecto ya está clonado
if [ -d "$PROJECT_DIR/.git" ]; then
    print_status "Proyecto ya existe, actualizando..."
    cd $PROJECT_DIR
    sudo -u kidsfun git fetch origin
    sudo -u kidsfun git reset --hard origin/$BRANCH
    print_success "Proyecto actualizado"
else
    print_status "Clonando proyecto desde GitHub..."
    cd $PROJECT_DIR
    sudo -u kidsfun git clone -b $BRANCH $GITHUB_REPO .
    print_success "Proyecto clonado"
fi

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    print_warning "No se encontró archivo .env. Copiando desde env.example..."
    sudo -u kidsfun cp env.example .env
    print_warning "⚠️  IMPORTANTE: Edita el archivo .env con las configuraciones correctas antes de continuar"
    print_warning "   Especialmente el SECRET_KEY y las credenciales de la base de datos"
    exit 1
fi

# Crear entorno virtual si no existe
print_status "Creando entorno virtual..."
if [ ! -d "venv" ]; then
    sudo -u kidsfun python3 -m venv venv
    print_success "Entorno virtual creado"
else
    print_warning "Entorno virtual ya existe"
fi

# Activar entorno virtual e instalar dependencias
print_status "Instalando dependencias de Python..."
sudo -u kidsfun bash -c "source venv/bin/activate && pip install --upgrade pip"
sudo -u kidsfun bash -c "source venv/bin/activate && pip install -r requirements.txt"
print_success "Dependencias instaladas"

# Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/media
mkdir -p $PROJECT_DIR/static
chown -R kidsfun:kidsfun $PROJECT_DIR
print_success "Directorios creados"

# Verificar conexión a la base de datos
print_status "Verificando conexión a la base de datos..."
if sudo -u kidsfun bash -c "source venv/bin/activate && python -c \"
import sys
sys.path.append('.')
from app.database import engine
try:
    with engine.connect() as conn:
        print('✅ Conexión a la base de datos exitosa')
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    sys.exit(1)
\""; then
    print_success "Conexión a base de datos verificada"
else
    print_error "Error en la conexión a la base de datos"
    print_error "Verifica la configuración en .env"
    exit 1
fi

# Ejecutar migraciones
print_status "Ejecutando migraciones de base de datos..."
if sudo -u kidsfun bash -c "source venv/bin/activate && alembic upgrade head"; then
    print_success "Migraciones ejecutadas"
else
    print_warning "Error en migraciones (puede ser normal si no hay cambios)"
fi

# Configurar systemd service
print_status "Configurando servicio systemd..."
# Actualizar el archivo de servicio para usar 'venv' en lugar de '.env'
sed -i 's|/opt/kidsfun-backend/.env/bin/gunicorn|/opt/kidsfun-backend/venv/bin/gunicorn|g' kidsfun-backend.service
cp kidsfun-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable kidsfun-backend
print_success "Servicio systemd configurado"

# Configurar Nginx
print_status "Configurando Nginx..."
cp kidsfun-backend.nginx /etc/nginx/sites-available/kidsfun-backend
sed -i "s/server_name _;/server_name $DOMAIN;/g" /etc/nginx/sites-available/kidsfun-backend
ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl enable nginx
print_success "Nginx configurado"

# Configurar logrotate
print_status "Configurando logrotate..."
cp kidsfun-backend /etc/logrotate.d/kidsfun-backend
print_success "Logrotate configurado"

# Configurar firewall
print_status "Configurando firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_success "Firewall configurado"

# Iniciar servicios
print_status "Iniciando servicios..."
systemctl start nginx
systemctl start kidsfun-backend
print_success "Servicios iniciados"

# Verificar servicios
print_status "Verificando servicios..."
sleep 5

if systemctl is-active --quiet kidsfun-backend; then
    print_success "Servicio kidsfun-backend está activo"
else
    print_error "Error al iniciar kidsfun-backend"
    systemctl status kidsfun-backend
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_success "Servicio nginx está activo"
else
    print_error "Error al iniciar nginx"
    systemctl status nginx
    exit 1
fi

# Configurar SSL con Certbot
print_status "Configurando SSL con Certbot..."
if certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@kidsfunyfiestasinfantiles.com; then
    print_success "SSL configurado exitosamente"
else
    print_warning "Error al configurar SSL. Puedes intentarlo manualmente después:"
    print_warning "certbot --nginx -d $DOMAIN"
fi

# Crear script de actualización
print_status "Creando script de actualización..."
cat > /usr/local/bin/update-kidsfun << 'EOF'
#!/bin/bash

# Script de actualización para KidsFun Backend
# Uso: sudo update-kidsfun

set -e

PROJECT_DIR="/opt/kidsfun-backend"
BRANCH="mrg_prod"

echo "🔄 Actualizando KidsFun Backend..."

# Cambiar al directorio del proyecto
cd $PROJECT_DIR

# Hacer backup de la configuración
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Obtener cambios del repositorio
sudo -u kidsfun git fetch origin
sudo -u kidsfun git reset --hard origin/$BRANCH

# Restaurar configuración
cp .env.backup.* .env

# Actualizar dependencias
sudo -u kidsfun bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Ejecutar migraciones (sin perder datos)
sudo -u kidsfun bash -c "source venv/bin/activate && alembic upgrade head"

# Reiniciar servicios
systemctl restart kidsfun-backend
systemctl restart nginx

echo "✅ Actualización completada"
echo "🔍 Verificando servicios..."
systemctl status kidsfun-backend --no-pager -l
EOF

chmod +x /usr/local/bin/update-kidsfun
print_success "Script de actualización creado"

# Mostrar información final
echo ""
print_success "🎉 Despliegue completado exitosamente!"
echo ""
echo "📋 Información del despliegue:"
echo "   • Dominio: https://$DOMAIN"
echo "   • Directorio: $PROJECT_DIR"
echo "   • Usuario: kidsfun"
echo "   • Puerto: 8000 (interno), 443 (HTTPS)"
echo "   • Logs: $PROJECT_DIR/logs/"
echo "   • Archivos: $PROJECT_DIR/media/"
echo ""
echo "🚀 Comandos de gestión:"
echo "   • Ver estado: systemctl status kidsfun-backend"
echo "   • Reiniciar: systemctl restart kidsfun-backend"
echo "   • Ver logs: journalctl -u kidsfun-backend -f"
echo "   • Actualizar: update-kidsfun"
echo ""
echo "📚 Documentación API:"
echo "   • Swagger UI: https://$DOMAIN/docs"
echo "   • ReDoc: https://$DOMAIN/redoc"
echo ""
echo "🔧 Monitoreo:"
echo "   • Verificar salud: $PROJECT_DIR/health_check.sh"
echo "   • Logs en tiempo real: tail -f $PROJECT_DIR/logs/error.log"
echo ""
print_success "¡KidsFun Backend está desplegado y funcionando! 🎉" 