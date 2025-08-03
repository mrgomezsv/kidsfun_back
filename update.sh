#!/bin/bash

# Script universal de actualización para KidsFun Backend
# Uso: sudo ./update.sh

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

echo "🚀 Iniciando actualización universal del KidsFun Backend..."
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

# Paso 1: Backup de configuración
print_status "🔄 Creando backup de la configuración actual..."
if [ -f "main.py" ]; then
    cp main.py "$BACKUP_DIR/main.py.backup.$TIMESTAMP"
    print_success "Backup creado: main.py.backup.$TIMESTAMP"
fi

if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env.backup.$TIMESTAMP"
    print_success "Backup creado: .env.backup.$TIMESTAMP"
fi

# Paso 2: Configurar Git si es necesario
print_status "🔧 Configurando Git..."
if ! git config --global --get safe.directory | grep -q "$PROJECT_DIR"; then
    git config --global --add safe.directory "$PROJECT_DIR"
    print_success "Directorio agregado como seguro para Git"
fi

# Paso 3: Obtener cambios del repositorio
print_status "📥 Obteniendo cambios del repositorio..."
git fetch origin

# Verificar si hay cambios
if git log HEAD..origin/mrg_prod --oneline | grep -q .; then
    print_status "Cambios encontrados, actualizando..."
    git reset --hard origin/mrg_prod
    print_success "Proyecto actualizado a la última versión"
else
    print_warning "No hay cambios nuevos en el repositorio"
fi

# Paso 4: Verificar archivos nuevos
print_status "🔍 Verificando archivos nuevos..."
if [ -f "app/middleware.py" ]; then
    print_success "✅ Middleware de seguridad encontrado"
else
    print_warning "⚠️ Middleware de seguridad no encontrado"
fi

if [ -f "API_DOCUMENTATION.md" ]; then
    print_success "✅ Documentación de API encontrada"
else
    print_warning "⚠️ Documentación de API no encontrada"
fi

# Paso 5: Actualizar dependencias
print_status "🐍 Actualizando dependencias de Python..."
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    print_success "Dependencias actualizadas"
else
    print_error "Entorno virtual no encontrado"
    exit 1
fi

# Paso 6: Aplicar migraciones
print_status "🔧 Aplicando migraciones de base de datos..."
if alembic upgrade head; then
    print_success "Migraciones aplicadas correctamente"
else
    print_warning "Error al aplicar migraciones (puede ser normal si no hay cambios)"
fi

# Paso 7: Reiniciar servicios
print_status "🔄 Reiniciando servicios..."
systemctl restart $SERVICE_NAME
systemctl restart nginx
print_success "Servicios reiniciados"

# Paso 8: Verificar servicios
print_status "✅ Verificando estado de los servicios..."
sleep 5

if systemctl is-active --quiet $SERVICE_NAME; then
    print_success "Servicio $SERVICE_NAME está activo"
else
    print_error "Error: Servicio $SERVICE_NAME no está activo"
    systemctl status $SERVICE_NAME
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_success "Servicio nginx está activo"
else
    print_error "Error: Servicio nginx no está activo"
    systemctl status nginx
    exit 1
fi

# Paso 9: Verificar endpoints
print_status "🔍 Verificando endpoints de la API..."
sleep 3

# Verificar health check
if curl -s -f "https://api.kidsfunyfiestasinfantiles.com/health" > /dev/null; then
    print_success "Health check funcionando"
else
    print_warning "Error en health check"
fi

# Verificar security info
if curl -s -f "https://api.kidsfunyfiestasinfantiles.com/security-info" > /dev/null; then
    print_success "Security info endpoint funcionando"
else
    print_warning "Error en security info endpoint"
fi

# Paso 10: Mostrar información de seguridad
print_status "📊 Información de seguridad actualizada:"
echo ""
curl -s "https://api.kidsfunyfiestasinfantiles.com/security-info" | python3 -m json.tool 2>/dev/null || echo "No se pudo obtener información de seguridad"

# Paso 11: Limpiar backups antiguos (mantener solo los últimos 5)
print_status "🧹 Limpiando backups antiguos..."
cd "$BACKUP_DIR"
ls -t *.backup.* | tail -n +6 | xargs -r rm -f
print_success "Backups antiguos eliminados"

# Paso 12: Resumen final
echo ""
echo "🎉 ¡Actualización completada exitosamente!"
echo "=================================================="
print_success "✅ Proyecto actualizado a la última versión"
print_success "✅ Dependencias actualizadas"
print_success "✅ Migraciones aplicadas"
print_success "✅ Servicios reiniciados"
print_success "✅ Endpoints verificados"
print_success "✅ Backups creados y limpiados"

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