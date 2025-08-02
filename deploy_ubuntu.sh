#!/bin/bash

# Script de despliegue para KidsFun Backend en Ubuntu Server
# Autor: KidsFun Development Team
# Fecha: 2024

set -e

echo "🚀 Desplegando KidsFun Backend en Ubuntu Server..."

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

# Verificar si estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    print_error "No se encontró main.py. Asegúrate de estar en el directorio kidsfun_back"
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    print_warning "No se encontró archivo .env. Copiando desde env.production.example..."
    cp env.production.example .env
    print_warning "⚠️  IMPORTANTE: Edita el archivo .env con las configuraciones correctas antes de continuar"
    print_warning "   Especialmente el SECRET_KEY y las credenciales de la base de datos"
    exit 1
fi

# Verificar permisos de sudo
if ! sudo -n true 2>/dev/null; then
    print_error "Este script requiere permisos de sudo. Ejecuta con: sudo ./deploy_ubuntu.sh"
    exit 1
fi

print_status "Verificando dependencias del sistema..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no está instalado. Ejecuta primero: ./setup_server.sh"
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está instalado. Ejecuta primero: ./setup_server.sh"
    exit 1
fi

print_success "Dependencias básicas verificadas"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    print_status "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
print_status "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
print_status "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
print_status "Instalando dependencias..."
pip install -r requirements.txt

print_success "Dependencias instaladas"

# Verificar conexión a la base de datos
print_status "Verificando conexión a la base de datos..."
python -c "
import sys
sys.path.append('.')
from app.database import engine
try:
    with engine.connect() as conn:
        print('✅ Conexión a la base de datos exitosa')
except Exception as e:
    print(f'❌ Error de conexión a la base de datos: {e}')
    sys.exit(1)
"

# Ejecutar migraciones
print_status "Ejecutando migraciones de la base de datos..."
alembic upgrade head

print_success "Migraciones completadas"

# Crear directorios necesarios
print_status "Creando directorios..."
mkdir -p logs
mkdir -p media
mkdir -p static

print_success "Directorios creados"

# Verificar configuración de email
print_status "Verificando configuración de email..."
python -c "
import sys
sys.path.append('.')
from app.config import settings
try:
    import smtplib
    server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
    server.starttls()
    server.login(settings.smtp_user, settings.smtp_password)
    server.quit()
    print('✅ Configuración de email correcta')
except Exception as e:
    print(f'❌ Error en configuración de email: {e}')
    print('⚠️  El sistema funcionará pero no podrá enviar emails')
"

# Configurar permisos
print_status "Configurando permisos..."
sudo chown -R kidsfun:kidsfun /opt/kidsfun-backend
sudo chmod -R 755 /opt/kidsfun-backend
sudo chmod 600 .env

print_success "Permisos configurados"

# Crear archivo de configuración para Gunicorn optimizado para Ubuntu
print_status "Creando configuración de Gunicorn optimizada..."
cat > gunicorn.conf.py << EOF
# Configuración de Gunicorn optimizada para Ubuntu Server
import multiprocessing
import os

# Configuración del servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "/opt/kidsfun-backend/logs/access.log"
errorlog = "/opt/kidsfun-backend/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de procesos
preload_app = True
daemon = False
pidfile = "/opt/kidsfun-backend/logs/gunicorn.pid"
user = "kidsfun"
group = "kidsfun"

# Configuración de reinicio
graceful_timeout = 30

# Configuración de SSL (si está configurado)
keyfile = os.getenv('SSL_KEYFILE', None)
certfile = os.getenv('SSL_CERTFILE', None)
EOF

print_success "Configuración de Gunicorn creada"

# Crear script de inicio del servicio optimizado
print_status "Creando script de inicio del servicio..."
cat > start_service.sh << 'EOF'
#!/bin/bash

# Script para iniciar el servicio de KidsFun Backend en Ubuntu
cd "$(dirname "$0")"

# Activar entorno virtual
source venv/bin/activate

# Verificar si el servicio ya está corriendo
if [ -f "logs/gunicorn.pid" ]; then
    PID=$(cat logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "El servicio ya está corriendo con PID: $PID"
        exit 0
    else
        echo "Removiendo PID file obsoleto..."
        rm logs/gunicorn.pid
    fi
fi

# Crear directorios si no existen
mkdir -p logs
mkdir -p media

# Verificar permisos
sudo chown -R kidsfun:kidsfun /opt/kidsfun-backend
sudo chmod -R 755 /opt/kidsfun-backend

# Iniciar el servicio
echo "Iniciando KidsFun Backend..."
gunicorn -c gunicorn.conf.py main:app

echo "Servicio iniciado exitosamente"
EOF

chmod +x start_service.sh

# Crear script de parada del servicio
print_status "Creando script de parada del servicio..."
cat > stop_service.sh << 'EOF'
#!/bin/bash

# Script para parar el servicio de KidsFun Backend
cd "$(dirname "$0")"

if [ -f "logs/gunicorn.pid" ]; then
    PID=$(cat logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Parando servicio con PID: $PID"
        kill -TERM $PID
        sleep 5
        
        # Verificar si el proceso se detuvo
        if ps -p $PID > /dev/null 2>&1; then
            echo "Forzando parada del proceso..."
            kill -KILL $PID
        fi
        
        rm logs/gunicorn.pid
        echo "Servicio detenido"
    else
        echo "El servicio no está corriendo"
        rm logs/gunicorn.pid
    fi
else
    echo "No se encontró archivo PID"
fi
EOF

chmod +x stop_service.sh

# Crear script de reinicio del servicio
print_status "Creando script de reinicio del servicio..."
cat > restart_service.sh << 'EOF'
#!/bin/bash

# Script para reiniciar el servicio de KidsFun Backend
cd "$(dirname "$0")"

echo "Reiniciando KidsFun Backend..."

# Parar el servicio
./stop_service.sh

# Esperar un momento
sleep 2

# Iniciar el servicio
./start_service.sh

echo "Servicio reiniciado exitosamente"
EOF

chmod +x restart_service.sh

# Crear script de estado del servicio
print_status "Creando script de estado del servicio..."
cat > status_service.sh << 'EOF'
#!/bin/bash

# Script para verificar el estado del servicio de KidsFun Backend
cd "$(dirname "$0")"

if [ -f "logs/gunicorn.pid" ]; then
    PID=$(cat logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ KidsFun Backend está corriendo (PID: $PID)"
        echo "📊 Información del proceso:"
        ps -p $PID -o pid,ppid,cmd,etime,pcpu,pmem
        echo ""
        echo "📈 Estadísticas de memoria:"
        free -h
        echo ""
        echo "💾 Espacio en disco:"
        df -h /opt/kidsfun-backend
    else
        echo "❌ KidsFun Backend no está corriendo (PID file obsoleto)"
        rm logs/gunicorn.pid
    fi
else
    echo "❌ KidsFun Backend no está corriendo"
fi
EOF

chmod +x status_service.sh

print_success "Scripts de servicio creados"

# Configurar supervisor
print_status "Configurando supervisor..."
sudo tee /etc/supervisor/conf.d/kidsfun-backend.conf << EOF
[program:kidsfun-backend]
command=/opt/kidsfun-backend/venv/bin/gunicorn -c /opt/kidsfun-backend/gunicorn.conf.py main:app
directory=/opt/kidsfun-backend
user=kidsfun
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/kidsfun-backend/logs/supervisor.log
stderr_logfile=/opt/kidsfun-backend/logs/supervisor_error.log
EOF

sudo systemctl enable supervisor
sudo systemctl restart supervisor

print_success "Supervisor configurado"

# Configurar logrotate
print_status "Configurando logrotate..."
sudo tee /etc/logrotate.d/kidsfun-backend << EOF
/opt/kidsfun-backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 kidsfun kidsfun
    postrotate
        sudo supervisorctl restart kidsfun-backend
    endscript
}
EOF

print_success "Logrotate configurado"

# Configurar Nginx (si no está configurado)
if [ ! -f "/etc/nginx/sites-enabled/kidsfun-backend" ]; then
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
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /opt/kidsfun-backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /opt/kidsfun-backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Configuración de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
EOF

    sudo ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo systemctl enable nginx
    sudo systemctl restart nginx
    
    print_success "Nginx configurado"
fi

# Iniciar el servicio
print_status "Iniciando el servicio..."
sudo supervisorctl restart kidsfun-backend

# Esperar un momento para que el servicio se inicie
sleep 5

# Verificar que el servicio esté corriendo
if sudo supervisorctl status kidsfun-backend | grep -q "RUNNING"; then
    print_success "Servicio iniciado correctamente"
else
    print_error "Error al iniciar el servicio"
    sudo supervisorctl status kidsfun-backend
    exit 1
fi

# Mostrar información final
echo ""
print_success "🎉 Despliegue en Ubuntu completado exitosamente!"
echo ""
echo "📋 Información del despliegue:"
echo "   • Directorio: /opt/kidsfun-backend"
echo "   • Usuario: kidsfun"
echo "   • Puerto: 8000 (interno), 80 (Nginx)"
echo "   • Logs: /opt/kidsfun-backend/logs/"
echo "   • Archivos: /opt/kidsfun-backend/media/"
echo ""
echo "🚀 Comandos de gestión:"
echo "   • Ver estado: sudo supervisorctl status kidsfun-backend"
echo "   • Reiniciar: sudo supervisorctl restart kidsfun-backend"
echo "   • Ver logs: sudo tail -f /opt/kidsfun-backend/logs/error.log"
echo "   • Ver logs de supervisor: sudo tail -f /opt/kidsfun-backend/logs/supervisor.log"
echo ""
echo "📚 Documentación API:"
echo "   • Swagger UI: http://tu-servidor/docs"
echo "   • ReDoc: http://tu-servidor/redoc"
echo ""
echo "🔧 Monitoreo:"
echo "   • Estado del sistema: ./status_service.sh"
echo "   • Logs en tiempo real: sudo tail -f /opt/kidsfun-backend/logs/access.log"
echo ""
print_success "¡KidsFun Backend está desplegado y funcionando en Ubuntu! 🎉" 