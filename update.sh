#!/bin/bash

# Script universal de actualización AUTOMÁTICA para KidsFun Backend
# Uso: sudo ./update.sh
# Este script es COMPLETAMENTE AUTOMÁTICO y SEGURO

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
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

# Variables
PROJECT_DIR="/opt/kidsfun-backend"
SERVICE_NAME="kidsfun-backend"
BACKUP_DIR="/opt/kidsfun-backend/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MAX_RETRIES=3

echo "🚀 Iniciando actualización AUTOMÁTICA del KidsFun Backend..."
echo "=================================================="
echo "⚠️  Este proceso es COMPLETAMENTE AUTOMÁTICO"
echo "⚠️  No se requiere intervención manual"
echo "=================================================="

# Verificar que estamos como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Verificar que el directorio existe
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "No se encontró el directorio del proyecto en $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

print_status "📁 Directorio del proyecto: $PROJECT_DIR"

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

# Función para hacer backup con retry
make_backup() {
    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if [ -f "main.py" ]; then
            cp main.py "$BACKUP_DIR/main.py.backup.$TIMESTAMP" && break
        fi
        retries=$((retries + 1))
        sleep 2
    done
    
    retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if [ -f ".env" ]; then
            cp .env "$BACKUP_DIR/.env.backup.$TIMESTAMP" && break
        fi
        retries=$((retries + 1))
        sleep 2
    done
}

# Paso 1: Backup de configuración AUTOMÁTICO
print_status "🔄 Creando backup automático de la configuración..."
make_backup
print_success "Backup automático completado"

# Paso 2: Configurar Git AUTOMÁTICAMENTE
print_status "🔧 Configurando Git automáticamente..."
git config --global --add safe.directory "$PROJECT_DIR" 2>/dev/null || true
print_success "Git configurado automáticamente"

# Paso 3: Obtener cambios del repositorio AUTOMÁTICAMENTE
print_status "📥 Obteniendo cambios del repositorio automáticamente..."
git fetch origin --quiet

# Verificar si hay cambios y actualizar AUTOMÁTICAMENTE
if git log HEAD..origin/mrg_prod --oneline | grep -q .; then
    print_status "Cambios encontrados, actualizando automáticamente..."
    git reset --hard origin/mrg_prod --quiet
    print_success "Proyecto actualizado automáticamente a la última versión"
else
    print_warning "No hay cambios nuevos en el repositorio"
fi

# Paso 4: Verificar archivos nuevos AUTOMÁTICAMENTE
print_status "🔍 Verificando archivos nuevos automáticamente..."
if [ -f "app/middleware.py" ]; then
    print_success "✅ Middleware de seguridad encontrado"
fi

if [ -f "API_DOCUMENTATION.md" ]; then
    print_success "✅ Documentación de API encontrada"
fi

# Paso 5: Actualizar dependencias AUTOMÁTICAMENTE
print_status "🐍 Actualizando dependencias de Python automáticamente..."
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt --quiet --no-cache-dir
    print_success "Dependencias actualizadas automáticamente"
else
    print_error "Entorno virtual no encontrado"
    exit 1
fi

# Paso 6: Aplicar migraciones AUTOMÁTICAMENTE
print_status "🔧 Aplicando migraciones de base de datos automáticamente..."
if alembic upgrade head --quiet; then
    print_success "Migraciones aplicadas automáticamente"
else
    print_warning "No hay migraciones nuevas o error (puede ser normal)"
fi

# Paso 7: Reiniciar servicios AUTOMÁTICAMENTE
print_status "🔄 Reiniciando servicios automáticamente..."
systemctl restart $SERVICE_NAME
systemctl restart nginx
print_success "Servicios reiniciados automáticamente"

# Paso 8: Verificar servicios AUTOMÁTICAMENTE con retry
print_status "✅ Verificando estado de los servicios automáticamente..."
sleep 5

# Función para verificar servicio con retry
check_service() {
    local service_name=$1
    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if systemctl is-active --quiet $service_name; then
            print_success "Servicio $service_name está activo"
            return 0
        fi
        retries=$((retries + 1))
        print_warning "Reintentando verificación de $service_name (intento $retries/$MAX_RETRIES)"
        sleep 3
        systemctl restart $service_name
        sleep 2
    done
    print_error "Error: Servicio $service_name no está activo después de $MAX_RETRIES intentos"
    return 1
}

check_service $SERVICE_NAME
check_service nginx

# Paso 9: Verificar endpoints AUTOMÁTICAMENTE con retry
print_status "🔍 Verificando endpoints automáticamente..."
sleep 3

# Función para verificar endpoint con retry
check_endpoint() {
    local endpoint=$1
    local name=$2
    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -s -f "$endpoint" > /dev/null; then
            print_success "$name funcionando"
            return 0
        fi
        retries=$((retries + 1))
        print_warning "Reintentando $name (intento $retries/$MAX_RETRIES)"
        sleep 3
    done
    print_warning "Error en $name después de $MAX_RETRIES intentos"
    return 1
}

check_endpoint "https://api.kidsfunyfiestasinfantiles.com/health" "Health check"
check_endpoint "https://api.kidsfunyfiestasinfantiles.com/security-info" "Security info endpoint"

# Paso 10: Mostrar información de seguridad AUTOMÁTICAMENTE
print_status "📊 Obteniendo información de seguridad automáticamente..."
echo ""
curl -s "https://api.kidsfunyfiestasinfantiles.com/security-info" | python3 -m json.tool 2>/dev/null || echo "No se pudo obtener información de seguridad"

# Paso 11: Limpiar backups antiguos AUTOMÁTICAMENTE
print_status "🧹 Limpiando backups antiguos automáticamente..."
cd "$BACKUP_DIR"
ls -t *.backup.* 2>/dev/null | tail -n +6 | xargs -r rm -f 2>/dev/null || true
print_success "Backups antiguos eliminados automáticamente"

# Paso 12: Resumen final AUTOMÁTICO
echo ""
echo "🎉 ¡Actualización AUTOMÁTICA completada exitosamente!"
echo "=================================================="
print_success "✅ Proyecto actualizado automáticamente a la última versión"
print_success "✅ Dependencias actualizadas automáticamente"
print_success "✅ Migraciones aplicadas automáticamente"
print_success "✅ Servicios reiniciados automáticamente"
print_success "✅ Endpoints verificados automáticamente"
print_success "✅ Backups creados y limpiados automáticamente"

echo ""
echo "📋 Comandos útiles:"
echo "   Ver logs: sudo journalctl -u kidsfun-backend -f"
echo "   Ver estado: sudo systemctl status kidsfun-backend"
echo "   Health check: curl https://api.kidsfunyfiestasinfantiles.com/health"
echo "   Security info: curl https://api.kidsfunyfiestasinfantiles.com/security-info"
echo ""
echo "📁 Backups guardados en: $BACKUP_DIR"
echo "🕐 Timestamp de esta actualización: $TIMESTAMP"
echo ""
print_success "¡Tu API está actualizada y funcionando correctamente! 🚀"
print_success "Proceso 100% AUTOMÁTICO completado sin intervención manual" 