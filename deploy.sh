#!/bin/bash

# Script de despliegue para KidsFun Backend
# Autor: KidsFun Development Team
# Fecha: $(date)

set -e  # Salir si hay algún error

echo "🚀 Iniciando despliegue de KidsFun Backend..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
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
    print_warning "No se encontró archivo .env. Copiando desde env.example..."
    cp env.example .env
    print_warning "Por favor, edita el archivo .env con las configuraciones correctas antes de continuar"
    exit 1
fi

print_status "Verificando dependencias..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no está instalado"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está instalado"
    exit 1
fi

print_success "Dependencias básicas verificadas"

# Crear entorno virtual si no existe
if [ ! -d ".env" ]; then
    print_status "Creando entorno virtual..."
    python3 -m venv .env
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
print_status "Activando entorno virtual..."
source .env/bin/activate

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

# Crear directorio para logs si no existe
if [ ! -d "logs" ]; then
    print_status "Creando directorio de logs..."
    mkdir logs
fi

# Crear directorio para archivos subidos si no existe
if [ ! -d "media" ]; then
    print_status "Creando directorio de archivos..."
    mkdir media
fi

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

# Crear archivo de configuración para Gunicorn
print_status "Creando configuración de Gunicorn..."
cat > gunicorn.conf.py << EOF
# Configuración de Gunicorn para KidsFun Backend
import multiprocessing

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
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de procesos
preload_app = True
daemon = False
pidfile = "logs/gunicorn.pid"

# Configuración de reinicio
graceful_timeout = 30
EOF

print_success "Configuración de Gunicorn creada"

# Crear script de inicio del servicio
print_status "Creando script de inicio del servicio..."
cat > start_service.sh << 'EOF'
#!/bin/bash

# Script para iniciar el servicio de KidsFun Backend
cd "$(dirname "$0")"

# Activar entorno virtual
    source .env/bin/activate

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

# Crear archivo de configuración para systemd (opcional)
print_status "Creando configuración de systemd..."
cat > kidsfun-backend.service << EOF
[Unit]
Description=KidsFun Backend API
After=network.target

[Service]
Type=forking
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/start_service.sh
ExecStop=$(pwd)/stop_service.sh
ExecReload=$(pwd)/restart_service.sh
PIDFile=$(pwd)/logs/gunicorn.pid
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_success "Configuración de systemd creada"

# Mostrar información final
echo ""
print_success "🎉 Despliegue completado exitosamente!"
echo ""
echo "📋 Información del despliegue:"
echo "   • Directorio de trabajo: $(pwd)"
echo "   • Entorno virtual: $(pwd)/.env"
echo "   • Logs: $(pwd)/logs/"
echo "   • Archivos: $(pwd)/media/"
echo ""
echo "🚀 Comandos disponibles:"
echo "   • Iniciar servicio: ./start_service.sh"
echo "   • Parar servicio: ./stop_service.sh"
echo "   • Reiniciar servicio: ./restart_service.sh"
echo "   • Ver estado: ./status_service.sh"
echo ""
echo "📚 Documentación API:"
echo "   • Swagger UI: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo ""
print_warning "Para instalar como servicio del sistema, ejecuta:"
echo "   sudo cp kidsfun-backend.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable kidsfun-backend"
echo "   sudo systemctl start kidsfun-backend"
echo ""
print_success "¡KidsFun Backend está listo para producción! 🎉" 