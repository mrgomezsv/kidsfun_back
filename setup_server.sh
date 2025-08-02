#!/bin/bash

# Script para preparar servidor Ubuntu para KidsFun Backend
# Autor: KidsFun Development Team
# Fecha: 2024

set -e

echo "🚀 Preparando servidor Ubuntu para KidsFun Backend..."

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

# Verificar si estamos ejecutando como root
if [ "$EUID" -eq 0 ]; then
    print_warning "Ejecutando como root. Algunos comandos pueden necesitar ajustes."
fi

print_status "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

print_status "Instalando dependencias del sistema..."

# Python y herramientas básicas
sudo apt install -y python3 python3-pip python3-venv python3-dev

# PostgreSQL client (si la BD está en otro servidor)
sudo apt install -y postgresql-client

# Herramientas de desarrollo
sudo apt install -y build-essential libpq-dev libssl-dev libffi-dev

# Git (para clonar el repositorio)
sudo apt install -y git

# Nginx (opcional, para proxy reverso)
sudo apt install -y nginx

# Supervisor (para gestión de procesos)
sudo apt install -y supervisor

# Logrotate (para rotación de logs)
sudo apt install -y logrotate

# UFW (firewall)
sudo apt install -y ufw

print_success "Dependencias del sistema instaladas"

# Configurar firewall
print_status "Configurando firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 8000/tcp  # Puerto de la aplicación
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

print_success "Firewall configurado"

# Crear usuario para la aplicación (opcional pero recomendado)
print_status "Creando usuario para la aplicación..."
if ! id "kidsfun" &>/dev/null; then
    sudo useradd -m -s /bin/bash kidsfun
    sudo usermod -aG sudo kidsfun
    print_success "Usuario 'kidsfun' creado"
else
    print_warning "Usuario 'kidsfun' ya existe"
fi

# Crear directorio de la aplicación
print_status "Creando directorio de la aplicación..."
sudo mkdir -p /opt/kidsfun-backend
sudo chown $USER:$USER /opt/kidsfun-backend

print_success "Directorio de aplicación creado"

# Configurar Nginx (opcional)
print_status "Configurando Nginx..."
sudo tee /etc/nginx/sites-available/kidsfun-backend << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/kidsfun-backend/static/;
    }

    location /media/ {
        alias /opt/kidsfun-backend/media/;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl enable nginx
sudo systemctl restart nginx

print_success "Nginx configurado"

# Configurar logrotate
print_status "Configurando logrotate..."
sudo tee /etc/logrotate.d/kidsfun-backend << 'EOF'
/opt/kidsfun-backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 kidsfun kidsfun
    postrotate
        systemctl reload kidsfun-backend
    endscript
}
EOF

print_success "Logrotate configurado"

# Configurar supervisor
print_status "Configurando supervisor..."
sudo tee /etc/supervisor/conf.d/kidsfun-backend.conf << 'EOF'
[program:kidsfun-backend]
command=/opt/kidsfun-backend/venv/bin/gunicorn -c /opt/kidsfun-backend/gunicorn.conf.py main:app
directory=/opt/kidsfun-backend
user=kidsfun
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/kidsfun-backend/logs/supervisor.log
EOF

sudo systemctl enable supervisor
sudo systemctl restart supervisor

print_success "Supervisor configurado"

print_success "🎉 Servidor Ubuntu preparado exitosamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Clonar el repositorio en /opt/kidsfun-backend"
echo "2. Copiar archivos del proyecto"
echo "3. Configurar archivo .env"
echo "4. Ejecutar ./deploy.sh"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs: sudo tail -f /opt/kidsfun-backend/logs/error.log"
echo "   • Reiniciar servicio: sudo supervisorctl restart kidsfun-backend"
echo "   • Ver estado: sudo supervisorctl status kidsfun-backend"
echo "   • Ver logs de supervisor: sudo tail -f /opt/kidsfun-backend/logs/supervisor.log" 