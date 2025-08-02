#!/bin/bash

# Script de verificación de salud para KidsFun Backend
# Autor: KidsFun Development Team

set -e

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

echo "🔍 Verificando salud del sistema KidsFun Backend..."

# Verificar estado del servicio
print_status "Verificando estado del servicio..."
if sudo systemctl is-active --quiet kidsfun-backend; then
    print_success "Servicio kidsfun-backend está activo"
else
    print_error "Servicio kidsfun-backend no está activo"
    sudo systemctl status kidsfun-backend
fi

# Verificar puerto
print_status "Verificando puerto 8000..."
if netstat -tlnp | grep -q ":8000 "; then
    print_success "Puerto 8000 está abierto"
else
    print_error "Puerto 8000 no está abierto"
fi

# Verificar API health check
print_status "Verificando API health check..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    print_success "API health check OK"
else
    print_error "API health check falló"
fi

# Verificar logs recientes
print_status "Verificando logs recientes..."
if sudo journalctl -u kidsfun-backend --since "5 minutes ago" | grep -q "ERROR"; then
    print_warning "Se encontraron errores en los logs recientes"
    sudo journalctl -u kidsfun-backend --since "5 minutes ago" | grep "ERROR" | tail -5
else
    print_success "No se encontraron errores en los logs recientes"
fi

# Verificar uso de memoria
print_status "Verificando uso de memoria..."
MEMORY_USAGE=$(ps aux | grep gunicorn | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
if [ ! -z "$MEMORY_USAGE" ]; then
    print_success "Uso de memoria: ${MEMORY_USAGE} MB"
else
    print_warning "No se pudo obtener el uso de memoria"
fi

# Verificar espacio en disco
print_status "Verificando espacio en disco..."
DISK_USAGE=$(df /opt/kidsfun-backend | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    print_success "Espacio en disco OK: ${DISK_USAGE}% usado"
else
    print_warning "Espacio en disco alto: ${DISK_USAGE}% usado"
fi

# Verificar archivos de log
print_status "Verificando archivos de log..."
if [ -f "/opt/kidsfun-backend/logs/error.log" ]; then
    LOG_SIZE=$(du -h /opt/kidsfun-backend/logs/error.log | cut -f1)
    print_success "Log de errores: ${LOG_SIZE}"
else
    print_warning "No se encontró el archivo de log de errores"
fi

# Verificar base de datos
print_status "Verificando conexión a base de datos..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    print_success "Conexión a base de datos OK"
else
    print_error "Conexión a base de datos falló"
fi

echo ""
print_success "✅ Verificación de salud completada"
echo ""
echo "📊 Resumen:"
echo "   • Servicio: $(sudo systemctl is-active kidsfun-backend)"
echo "   • Puerto: $(netstat -tlnp | grep ":8000 " | wc -l) procesos"
echo "   • API: $(curl -s http://localhost:8000/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
echo "   • Memoria: ${MEMORY_USAGE} MB"
echo "   • Disco: ${DISK_USAGE}% usado"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs: sudo journalctl -u kidsfun-backend -f"
echo "   • Reiniciar: sudo systemctl restart kidsfun-backend"
echo "   • Estado: sudo systemctl status kidsfun-backend" 