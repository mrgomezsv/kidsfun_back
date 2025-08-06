#!/bin/bash

# KidsFun Backend - Script de inicio rápido
# Este script configura e inicia el backend Node.js

echo "🎪 KidsFun Backend - Node.js/Express"
echo "====================================="

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor instala Node.js 18+"
    exit 1
fi

# Verificar versión de Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js versión 18+ es requerida. Versión actual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detectado"

# Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm no está instalado"
    exit 1
fi

echo "✅ npm $(npm -v) detectado"

# Verificar si existe package.json
if [ ! -f "package.json" ]; then
    echo "❌ package.json no encontrado. Asegúrate de estar en el directorio correcto"
    exit 1
fi

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Copiando env.example a .env..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Archivo .env creado. Por favor edítalo con tus configuraciones"
        echo "   - DATABASE_URL: URL de tu base de datos PostgreSQL"
        echo "   - SECRET_KEY: Clave secreta para JWT"
        echo "   - Otras configuraciones según necesites"
        echo ""
        echo "🔧 Después de configurar .env, ejecuta este script nuevamente"
        exit 0
    else
        echo "❌ env.example no encontrado"
        exit 1
    fi
fi

# Instalar dependencias si no existen
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

# Verificar conexión a la base de datos
echo "🔍 Verificando conexión a la base de datos..."
node -e "
const { sequelize } = require('./config/database');
sequelize.authenticate()
  .then(() => {
    console.log('✅ Conexión a la base de datos exitosa');
    process.exit(0);
  })
  .catch(err => {
    console.error('❌ Error conectando a la base de datos:', err.message);
    console.log('💡 Asegúrate de que:');
    console.log('   - PostgreSQL esté ejecutándose');
    console.log('   - La base de datos exista');
    console.log('   - Las credenciales en .env sean correctas');
    process.exit(1);
  });
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Ejecutar migraciones si es necesario
echo "🔄 Verificando migraciones..."
npm run migrate

# Iniciar el servidor
echo "🚀 Iniciando servidor..."
echo "📊 Servidor disponible en: http://localhost:$(grep PORT .env | cut -d'=' -f2 || echo '8000')"
echo "📚 Documentación: http://localhost:$(grep PORT .env | cut -d'=' -f2 || echo '8000')/docs"
echo "🏥 Health check: http://localhost:$(grep PORT .env | cut -d'=' -f2 || echo '8000')/health"
echo ""
echo "🛑 Para detener el servidor, presiona Ctrl+C"
echo ""

# Iniciar en modo desarrollo
npm run dev 