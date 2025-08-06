# 🎨 Guía de Despliegue - Angular Frontend en Ubuntu Server

## 📋 **Resumen del Proyecto**

### **Configuración Actual del Servidor**
- **🌐 Servidor:** Ubuntu 22.04 LTS
- **📍 IP:** 82.165.210.146
- **💾 Espacio disponible:** 74GB (de 77GB total)
- **🔧 Servicios activos:**
  - ✅ Nginx (activo y funcionando)
  - ✅ kidsfun-backend (FastAPI en puerto 8000)
  - ✅ SSL configurado para `api.kidsfunyfiestasinfantiles.com`

### **Dominios Configurados**
- **🔗 Backend API:** `https://api.kidsfunyfiestasinfantiles.com` (ya configurado)
- **🎨 Frontend Angular:** `https://kidsfunyfiestasinfantiles.com` (a configurar)

---

## 🎯 **Objetivo**

Desplegar un proyecto Angular en el mismo servidor Ubuntu con:
- ✅ Dominio separado: `https://kidsfunyfiestasinfantiles.com`
- ✅ SSL automático con Certbot
- ✅ Sin afectar el backend existente
- ✅ Configuración de Nginx optimizada
- ✅ Proceso de actualización automatizado

---

## 🚀 **Paso 1: Preparación del Servidor**

### **1.1 Conectarse al servidor**
```bash
ssh root@82.165.210.146
```

### **1.2 Verificar espacio disponible**
```bash
df -h
# Debe mostrar al menos 5GB disponibles
```

### **1.3 Instalar dependencias necesarias**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js y npm (versión LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Angular CLI globalmente
sudo npm install -g @angular/cli

# Instalar PM2 para gestión de procesos
sudo npm install -g pm2

# Verificar instalaciones
node --version
npm --version
ng version
pm2 --version
```

---

## 📁 **Paso 2: Configuración de Directorios**

### **2.1 Crear estructura de directorios**
```bash
# Crear directorio para el frontend
sudo mkdir -p /opt/kidsfun-frontend
sudo mkdir -p /var/www/kidsfun-frontend

# Crear usuario para el frontend
sudo useradd -m -s /bin/bash kidsfun-frontend
sudo usermod -aG sudo kidsfun-frontend

# Asignar permisos
sudo chown -R kidsfun-frontend:kidsfun-frontend /opt/kidsfun-frontend
sudo chown -R kidsfun-frontend:kidsfun-frontend /var/www/kidsfun-frontend

# Crear directorio de logs
sudo mkdir -p /var/log/kidsfun-frontend
sudo chown kidsfun-frontend:kidsfun-frontend /var/log/kidsfun-frontend
```

### **2.2 Verificar estructura**
```bash
ls -la /opt/
ls -la /var/www/
```

---

## 🎨 **Paso 3: Despliegue del Proyecto Angular**

### **3.1 Clonar el proyecto Angular**
```bash
# Cambiar al usuario del frontend
sudo su - kidsfun-frontend

# Navegar al directorio
cd /opt/kidsfun-frontend

# Clonar el repositorio (reemplaza con tu URL)
git clone https://github.com/tu-usuario/kidsfun-frontend.git .

# O si tienes el proyecto local, usar SCP
# (desde tu máquina local)
scp -r ./dist/kidsfun-frontend/* root@82.165.210.146:/var/www/kidsfun-frontend/
```

### **3.2 Configurar el proyecto**
```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cat > src/environments/environment.prod.ts << EOF
export const environment = {
  production: true,
  apiUrl: 'https://api.kidsfunyfiestasinfantiles.com',
  appName: 'KidsFun'
};
EOF

# Construir para producción
ng build --configuration=production --output-path=/var/www/kidsfun-frontend
```

### **3.3 Configurar permisos**
```bash
# Asignar permisos correctos
sudo chown -R www-data:www-data /var/www/kidsfun-frontend
sudo chmod -R 755 /var/www/kidsfun-frontend
```

---

## 🔧 **Paso 4: Configuración de Nginx**

### **4.1 Crear configuración de Nginx**
```bash
# Crear archivo de configuración
sudo nano /etc/nginx/sites-available/kidsfun-frontend
```

### **4.2 Contenido de la configuración**
```nginx
server {
    server_name kidsfunyfiestasinfantiles.com www.kidsfunyfiestasinfantiles.com;

    # Configuración de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:; font-src 'self' data: https:;" always;

    # Directorio raíz
    root /var/www/kidsfun-frontend;
    index index.html index.htm;

    # Configuración para Angular (SPA)
    location / {
        try_files $uri $uri/ /index.html;
        
        # Cache para archivos estáticos
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Configuración específica para archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary "Accept-Encoding";
    }

    # Configuración para archivos de Angular
    location ~* \.(js|css)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary "Accept-Encoding";
        gzip_static on;
    }

    # Configuración de gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Configuración de logs
    access_log /var/log/nginx/kidsfun-frontend-access.log;
    error_log /var/log/nginx/kidsfun-frontend-error.log;

    # Configuración de rate limiting
    limit_req zone=frontend burst=50 nodelay;

    listen 80;
}

# Configuración para HTTPS (se agregará automáticamente por Certbot)
```

### **4.3 Habilitar el sitio**
```bash
# Crear enlace simbólico
sudo ln -sf /etc/nginx/sites-available/kidsfun-frontend /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

---

## 🔒 **Paso 5: Configuración de SSL**

### **5.1 Obtener certificado SSL**
```bash
# Obtener certificado SSL para el dominio principal
sudo certbot --nginx -d kidsfunyfiestasinfantiles.com -d www.kidsfunyfiestasinfantiles.com --non-interactive --agree-tos --email admin@kidsfunyfiestasinfantiles.com

# Verificar certificados
sudo certbot certificates
```

### **5.2 Verificar configuración SSL**
```bash
# Verificar que el certificado se aplicó correctamente
sudo nginx -t
sudo systemctl reload nginx

# Probar SSL
curl -I https://kidsfunyfiestasinfantiles.com
```

---

## 🚀 **Paso 6: Configuración de Proceso Automatizado**

### **6.1 Crear script de construcción**
```bash
# Crear script de construcción
sudo nano /opt/kidsfun-frontend/build.sh
```

### **6.2 Contenido del script**
```bash
#!/bin/bash

# Script de construcción para KidsFun Frontend
# Uso: ./build.sh

set -e

echo "🚀 Iniciando construcción del Frontend Angular..."

# Variables
PROJECT_DIR="/opt/kidsfun-frontend"
BUILD_DIR="/var/www/kidsfun-frontend"
BACKUP_DIR="/opt/kidsfun-frontend/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Crear backup del build anterior
if [ -d "$BUILD_DIR" ]; then
    echo "📁 Creando backup del build anterior..."
    mkdir -p "$BACKUP_DIR"
    cp -r "$BUILD_DIR" "$BACKUP_DIR/build_backup_$TIMESTAMP"
fi

# Navegar al directorio del proyecto
cd "$PROJECT_DIR"

# Obtener últimos cambios
echo "📥 Obteniendo últimos cambios del repositorio..."
git pull origin main

# Instalar dependencias
echo "📦 Instalando dependencias..."
npm install

# Construir para producción
echo "🔨 Construyendo para producción..."
ng build --configuration=production --output-path="$BUILD_DIR"

# Configurar permisos
echo "🔐 Configurando permisos..."
sudo chown -R www-data:www-data "$BUILD_DIR"
sudo chmod -R 755 "$BUILD_DIR"

# Limpiar backups antiguos (mantener solo los últimos 5)
echo "🧹 Limpiando backups antiguos..."
cd "$BACKUP_DIR"
ls -t | tail -n +6 | xargs -r rm -rf

echo "✅ Construcción completada exitosamente!"
echo "🌐 Frontend disponible en: https://kidsfunyfiestasinfantiles.com"
```

### **6.3 Dar permisos de ejecución**
```bash
sudo chmod +x /opt/kidsfun-frontend/build.sh
```

---

## 🔄 **Paso 7: Configuración de Actualización Automática**

### **7.1 Crear script de actualización**
```bash
# Crear script de actualización
sudo nano /usr/local/bin/update-kidsfun-frontend
```

### **7.2 Contenido del script**
```bash
#!/bin/bash

# Script de actualización automática para KidsFun Frontend
# Uso: sudo update-kidsfun-frontend

if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

PROJECT_DIR="/opt/kidsfun-frontend"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ No se encontró el proyecto en $PROJECT_DIR"
    exit 1
fi

echo "🚀 Ejecutando actualización automática del Frontend Angular..."
echo "⚠️  Este proceso es COMPLETAMENTE AUTOMÁTICO"
echo ""

# Cambiar al usuario del frontend
sudo -u kidsfun-frontend bash -c "cd $PROJECT_DIR && ./build.sh"

echo "🎉 ¡Actualización completada exitosamente!"
echo "🌐 Frontend actualizado en: https://kidsfunyfiestasinfantiles.com"
```

### **7.3 Dar permisos de ejecución**
```bash
sudo chmod +x /usr/local/bin/update-kidsfun-frontend
```

---

## 📊 **Paso 8: Verificación y Testing**

### **8.1 Verificar servicios**
```bash
# Verificar estado de Nginx
sudo systemctl status nginx

# Verificar configuración de Nginx
sudo nginx -t

# Verificar certificados SSL
sudo certbot certificates
```

### **8.2 Probar endpoints**
```bash
# Probar frontend
curl -I https://kidsfunyfiestasinfantiles.com

# Probar backend (debe seguir funcionando)
curl -I https://api.kidsfunyfiestasinfantiles.com/health

# Probar redirección HTTP a HTTPS
curl -I http://kidsfunyfiestasinfantiles.com
```

### **8.3 Verificar logs**
```bash
# Ver logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-frontend-access.log
sudo tail -f /var/log/nginx/kidsfun-frontend-error.log

# Ver logs de SSL
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

---

## 🎯 **Paso 9: Configuración de Monitoreo**

### **9.1 Crear script de monitoreo**
```bash
# Crear script de monitoreo
sudo nano /opt/kidsfun-frontend/monitor.sh
```

### **9.2 Contenido del script**
```bash
#!/bin/bash

# Script de monitoreo para KidsFun Frontend
# Uso: ./monitor.sh

echo "🔍 Monitoreo del Frontend Angular - KidsFun"
echo "=========================================="

# Verificar estado de Nginx
echo "📊 Estado de Nginx:"
sudo systemctl is-active nginx

# Verificar certificados SSL
echo "🔒 Certificados SSL:"
sudo certbot certificates | grep -E "(Certificate Name|Expiry Date)"

# Verificar espacio en disco
echo "💾 Espacio en disco:"
df -h /var/www/kidsfun-frontend

# Verificar logs recientes
echo "📝 Logs recientes (últimas 10 líneas):"
sudo tail -10 /var/log/nginx/kidsfun-frontend-access.log

# Verificar respuesta del sitio
echo "🌐 Respuesta del sitio:"
curl -s -o /dev/null -w "%{http_code}" https://kidsfunyfiestasinfantiles.com
echo " - Status Code"

echo "✅ Monitoreo completado"
```

### **9.3 Dar permisos de ejecución**
```bash
sudo chmod +x /opt/kidsfun-frontend/monitor.sh
```

---

## 📚 **Paso 10: Documentación y Comandos Útiles**

### **10.1 Comandos de gestión**
```bash
# Actualizar frontend
sudo update-kidsfun-frontend

# Verificar estado
sudo systemctl status nginx

# Ver logs en tiempo real
sudo tail -f /var/log/nginx/kidsfun-frontend-access.log

# Monitorear sistema
/opt/kidsfun-frontend/monitor.sh

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar certificados SSL
sudo certbot certificates

# Renovar certificados SSL
sudo certbot renew --dry-run
```

### **10.2 Estructura de directorios final**
```
/opt/
├── kidsfun-backend/          # Backend FastAPI (existente)
│   ├── venv/
│   ├── app/
│   └── ...
└── kidsfun-frontend/         # Frontend Angular (nuevo)
    ├── src/
    ├── dist/
    ├── build.sh
    └── monitor.sh

/var/www/
├── kidsfun-frontend/         # Archivos construidos de Angular
│   ├── index.html
│   ├── assets/
│   └── ...
└── html/                     # Página por defecto (existente)

/etc/nginx/sites-available/
├── kidsfun-backend          # Configuración del backend (existente)
└── kidsfun-frontend         # Configuración del frontend (nuevo)
```

---

## 🚨 **Solución de Problemas**

### **Problema: Error 502 Bad Gateway**
```bash
# Verificar que Nginx está funcionando
sudo systemctl status nginx

# Verificar configuración
sudo nginx -t

# Verificar logs
sudo tail -f /var/log/nginx/kidsfun-frontend-error.log
```

### **Problema: Certificado SSL no funciona**
```bash
# Verificar certificados
sudo certbot certificates

# Renovar certificados
sudo certbot renew

# Verificar configuración SSL
sudo nginx -t
```

### **Problema: Archivos no se actualizan**
```bash
# Verificar permisos
sudo chown -R www-data:www-data /var/www/kidsfun-frontend

# Verificar construcción
cd /opt/kidsfun-frontend
ng build --configuration=production
```

---

## 🎉 **Resultado Final**

### **URLs Disponibles**
- **🎨 Frontend Angular:** `https://kidsfunyfiestasinfantiles.com`
- **🔗 Backend API:** `https://api.kidsfunyfiestasinfantiles.com`
- **📊 Health Check:** `https://api.kidsfunyfiestasinfantiles.com/health`

### **Características Implementadas**
- ✅ **Dominio separado** - Frontend y backend en dominios diferentes
- ✅ **SSL automático** - Certificados Let's Encrypt
- ✅ **Configuración optimizada** - Nginx configurado para Angular SPA
- ✅ **Actualización automática** - Scripts de construcción y despliegue
- ✅ **Monitoreo** - Scripts de verificación y logs
- ✅ **Backups automáticos** - Respaldo de builds anteriores
- ✅ **Sin conflictos** - Backend existente no afectado

---

## 📞 **Soporte**

### **Comandos de emergencia**
```bash
# Reiniciar todo el sistema
sudo reboot

# Verificar todos los servicios
sudo systemctl status nginx kidsfun-backend

# Ver logs completos
sudo journalctl -u nginx -f
sudo journalctl -u kidsfun-backend -f
```

### **Contacto**
- **📧 Email:** soporte@kidsfunyfiestasinfantiles.com
- **🔗 Documentación:** [README.md](./README.md)
- **🌐 Health Check:** `https://api.kidsfunyfiestasinfantiles.com/health`

---

**¡Frontend Angular desplegado exitosamente! 🚀** 