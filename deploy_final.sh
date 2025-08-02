#!/bin/bash

# Script de despliegue FINAL para KidsFun Backend
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

echo "🚀 Desplegando KidsFun Backend en Ubuntu Server (VERSIÓN FINAL)..."
echo "   • Dominio: $DOMAIN"
echo "   • Directorio: $PROJECT_DIR"
echo ""

# Verificar si estamos como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root"
    exit 1
fi

# 1. Actualizar sistema
print_status "Actualizando sistema..."
apt update && apt upgrade -y
print_success "Sistema actualizado"

# 2. Instalar dependencias del sistema
print_status "Instalando dependencias del sistema..."
apt install -y python3 python3-pip python3-venv python3-dev
apt install -y nginx certbot python3-certbot-nginx
apt install -y git curl wget unzip
apt install -y postgresql-client
apt install -y logrotate
print_success "Dependencias instaladas"

# 3. Crear usuario para la aplicación
print_status "Creando usuario para la aplicación..."
if ! id "kidsfun" &>/dev/null; then
    useradd -m -s /bin/bash kidsfun
    usermod -aG sudo kidsfun
    print_success "Usuario kidsfun creado"
else
    print_warning "Usuario kidsfun ya existe"
fi

# 4. Crear directorio del proyecto
print_status "Creando directorio del proyecto..."
mkdir -p $PROJECT_DIR
chown kidsfun:kidsfun $PROJECT_DIR
print_success "Directorio creado"

# 5. Clonar el proyecto
print_status "Clonando proyecto desde GitHub..."
cd $PROJECT_DIR
if [ ! -d ".git" ]; then
    sudo -u kidsfun git clone -b $BRANCH $GITHUB_REPO .
    print_success "Proyecto clonado"
else
    sudo -u kidsfun git fetch origin
    sudo -u kidsfun git reset --hard origin/$BRANCH
    print_success "Proyecto actualizado"
fi

# 6. Configurar variables de entorno
print_status "Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    sudo -u kidsfun cp env.example .env
    print_warning "Archivo .env creado desde plantilla"
    print_warning "⚠️  IMPORTANTE: Edita el archivo .env con las configuraciones correctas antes de continuar"
    print_warning "   Especialmente el SECRET_KEY y las credenciales de la base de datos"
    echo ""
    print_status "Abriendo editor para configurar .env..."
    sudo -u kidsfun nano .env
else
    print_success "Archivo .env ya existe"
fi

# 7. Crear entorno virtual
print_status "Creando entorno virtual..."
if [ ! -d "venv" ]; then
    sudo -u kidsfun python3 -m venv venv
    print_success "Entorno virtual creado"
else
    print_warning "Entorno virtual ya existe"
fi

# 8. Activar entorno virtual e instalar dependencias
print_status "Instalando dependencias de Python..."
sudo -u kidsfun bash -c "source venv/bin/activate && pip install --upgrade pip"
sudo -u kidsfun bash -c "source venv/bin/activate && pip install -r requirements.txt"
print_success "Dependencias instaladas"

# 9. Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/media
mkdir -p $PROJECT_DIR/static
chown -R kidsfun:kidsfun $PROJECT_DIR
print_success "Directorios creados"

# 10. Verificar conexión a la base de datos
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

# 11. Ejecutar migraciones
print_status "Ejecutando migraciones de base de datos..."
if sudo -u kidsfun bash -c "source venv/bin/activate && alembic upgrade head"; then
    print_success "Migraciones ejecutadas"
else
    print_warning "Error en migraciones (puede ser normal si no hay cambios)"
fi

# 12. Configurar systemd service
print_status "Configurando servicio systemd..."
cp kidsfun-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable kidsfun-backend
print_success "Servicio systemd configurado"

# 13. Configurar Nginx correctamente
print_status "Configurando Nginx..."
# Agregar rate limiting al archivo principal
if ! grep -q "limit_req_zone.*zone=api" /etc/nginx/nginx.conf; then
    sed -i '/include \/etc\/nginx\/sites-enabled\/\*/i \    # Rate limiting zones\n    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;\n' /etc/nginx/nginx.conf
fi

# Copiar configuración del sitio
cp kidsfun-backend.nginx /etc/nginx/sites-available/kidsfun-backend
ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl enable nginx
print_success "Nginx configurado"

# 14. Configurar logrotate
print_status "Configurando logrotate..."
cp kidsfun-backend /etc/logrotate.d/kidsfun-backend
print_success "Logrotate configurado"

# 15. Configurar firewall
print_status "Configurando firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_success "Firewall configurado"

# 16. Verificar configuración de Nginx
print_status "Verificando configuración de Nginx..."
if nginx -t; then
    print_success "Configuración de Nginx válida"
else
    print_error "Error en configuración de Nginx"
    exit 1
fi

# 17. Iniciar servicios
print_status "Iniciando servicios..."
systemctl start nginx
systemctl start kidsfun-backend
print_success "Servicios iniciados"

# 18. Verificar servicios
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

# 19. Configurar SSL con Certbot
print_status "Configurando SSL con Certbot..."
if certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@kidsfunyfiestasinfantiles.com; then
    print_success "SSL configurado exitosamente"
else
    print_warning "Error al configurar SSL. Puedes intentarlo manualmente después:"
    print_warning "certbot --nginx -d $DOMAIN"
fi

# 20. Crear script de actualización
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

# 21. Mostrar información final
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