# 🚀 Guía de Despliegue - Backend FastAPI en Servidor Linux

## 📋 **Resumen del Proyecto**

### **🎪 KidsFun Backend API**
Sistema backend completo para la gestión de productos, usuarios, comentarios, likes, eventos, waivers y chat de KidsFun - Fiestas Infantiles.

### **🛠️ Tecnologías Utilizadas**
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos principal
- **SQLAlchemy** - ORM para PostgreSQL
- **Alembic** - Migraciones de base de datos
- **Gunicorn** - Servidor WSGI para producción
- **Nginx** - Reverse proxy y servidor web
- **JWT** - Autenticación con tokens
- **Docker** - Containerización (opcional)

---

## 🎯 **Objetivo**

Desplegar el backend FastAPI en un servidor Linux con:
- ✅ **Base de datos PostgreSQL** configurada y optimizada
- ✅ **Nginx** como reverse proxy
- ✅ **SSL automático** con Certbot
- ✅ **Gunicorn** para producción
- ✅ **Systemd** para gestión de servicios
- ✅ **Logs centralizados** y monitoreo
- ✅ **Backups automáticos** de base de datos
- ✅ **Actualización automatizada** con un comando

---

## 🚀 **Paso 1: Preparación del Servidor**

### **1.1 Conectarse al servidor**
```bash
ssh root@tu-servidor-ip
```

### **1.2 Actualizar sistema**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas básicas
sudo apt install -y curl wget git vim nano htop ufw fail2ban
```

### **1.3 Verificar espacio disponible**
```bash
df -h
# Debe mostrar al menos 10GB disponibles
```

---

## 🗄️ **Paso 2: Instalación y Configuración de PostgreSQL**

### **2.1 Instalar PostgreSQL**
```bash
# Agregar repositorio oficial de PostgreSQL
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Actualizar e instalar
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Verificar instalación
sudo systemctl status postgresql
```

### **2.2 Configurar PostgreSQL**
```bash
# Cambiar al usuario postgres
sudo -u postgres psql

# Crear usuario y base de datos
CREATE USER kidsfun WITH PASSWORD 'tu-password-seguro';
CREATE DATABASE kidsfun_db OWNER kidsfun;
GRANT ALL PRIVILEGES ON DATABASE kidsfun_db TO kidsfun;
\q

# Configurar acceso remoto (opcional)
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Agregar línea: host    all             all             0.0.0.0/0               md5

sudo nano /etc/postgresql/*/main/postgresql.conf
# Cambiar: listen_addresses = '*'

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### **2.3 Verificar conexión**
```bash
# Probar conexión
psql -U kidsfun -d kidsfun_db -h localhost
# Debe conectarse exitosamente
```

---

## 🐍 **Paso 3: Instalación de Python y Dependencias**

### **3.1 Instalar Python 3.12+**
```bash
# Instalar Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Verificar instalación
python3.12 --version
pip3 --version
```

### **3.2 Instalar dependencias del sistema**
```bash
# Instalar dependencias necesarias
sudo apt install -y build-essential libpq-dev libssl-dev libffi-dev python3-dev

# Instalar herramientas adicionales
sudo apt install -y nginx certbot python3-certbot-nginx
```

---

## 📁 **Paso 4: Configuración de Directorios y Usuario**

### **4.1 Crear estructura de directorios**
```bash
# Crear directorio principal
sudo mkdir -p /opt/kidsfun-backend
sudo mkdir -p /var/www/kidsfun-backend
sudo mkdir -p /var/log/kidsfun-backend
sudo mkdir -p /opt/kidsfun-backend/backups

# Crear usuario para la aplicación
sudo useradd -m -s /bin/bash kidsfun
sudo usermod -aG sudo kidsfun

# Asignar permisos
sudo chown -R kidsfun:kidsfun /opt/kidsfun-backend
sudo chown -R kidsfun:kidsfun /var/log/kidsfun-backend
sudo chown -R www-data:www-data /var/www/kidsfun-backend
```

### **4.2 Verificar estructura**
```bash
ls -la /opt/
ls -la /var/log/
```

---

## 🎪 **Paso 5: Despliegue del Proyecto**

### **5.1 Clonar el repositorio**
```bash
# Cambiar al usuario kidsfun
sudo su - kidsfun

# Navegar al directorio
cd /opt/kidsfun-backend

# Clonar el repositorio
git clone https://github.com/tu-usuario/kidsfun_back.git .

# O si tienes el proyecto local, usar SCP
# (desde tu máquina local)
scp -r ./kidsfun_back/* root@tu-servidor-ip:/opt/kidsfun-backend/
```

### **5.2 Configurar entorno virtual**
```bash
# Crear entorno virtual
python3.12 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

### **5.3 Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar configuración
nano .env
```

### **5.4 Contenido del archivo .env**
```bash
# Database Configuration
DATABASE_URL=postgresql://kidsfun:tu-password-seguro@localhost:5432/kidsfun_db

# Security
SECRET_KEY=tu-secret-key-super-seguro-aqui-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:4200", "https://kidsfunyfiestasinfantiles.com", "https://www.kidsfunyfiestasinfantiles.com"]

# File Upload Configuration
UPLOAD_DIR=media
MAX_FILE_SIZE=10485760

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password

# Production Settings
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
TIMEOUT=30
KEEPALIVE=2
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=50

# Logging
LOG_LEVEL=info
ACCESS_LOG=logs/access.log
ERROR_LOG=logs/error.log
```

---

## 🗄️ **Paso 6: Configuración de Base de Datos**

### **6.1 Ejecutar migraciones**
```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar conexión a la base de datos
python -c "from app.database import engine; print('Conexión exitosa')"

# Ejecutar migraciones
alembic upgrade head

# Verificar tablas creadas
psql -U kidsfun -d kidsfun_db -h localhost -c "\dt"
```

### **6.2 Crear directorio de media**
```bash
# Crear directorio para archivos media
mkdir -p media
mkdir -p media/product_images
mkdir -p media/uploads

# Asignar permisos
sudo chown -R kidsfun:kidsfun media/
sudo chmod -R 755 media/
```

---

## 🔧 **Paso 7: Configuración de Gunicorn**

### **7.1 Crear configuración de Gunicorn**
```bash
# Crear archivo de configuración
nano gunicorn.conf.py
```

### **7.2 Contenido de gunicorn.conf.py**
```python
# Configuración de Gunicorn para KidsFun Backend
import multiprocessing
import os

# Configuración básica
bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
timeout = int(os.getenv("TIMEOUT", 30))
keepalive = int(os.getenv("KEEPALIVE", 2))
max_requests = int(os.getenv("MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))

# Configuración de logs
accesslog = os.getenv("ACCESS_LOG", "logs/access.log")
errorlog = os.getenv("ERROR_LOG", "logs/error.log")
loglevel = os.getenv("LOG_LEVEL", "info")

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de rendimiento
preload_app = True
worker_connections = 1000
backlog = 2048

# Configuración de reinicio
graceful_timeout = 30
worker_tmp_dir = "/dev/shm"

# Configuración de usuario
user = os.getenv("GUNICORN_USER", "kidsfun")
group = os.getenv("GUNICORN_GROUP", "kidsfun")

# Configuración de SSL (opcional)
keyfile = os.getenv("SSL_KEYFILE", None)
certfile = os.getenv("SSL_CERTFILE", None)

if keyfile and certfile:
    bind = "0.0.0.0:8443"
    ssl_version = "TLSv1_2"
```

---

## 🚀 **Paso 8: Configuración de Systemd**

### **8.1 Crear servicio de systemd**
```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/kidsfun-backend.service
```

### **8.2 Contenido del servicio**
```ini
[Unit]
Description=KidsFun Backend API
After=network.target postgresql.service
Wants=network.target postgresql.service

[Service]
Type=exec
User=kidsfun
Group=kidsfun
WorkingDirectory=/opt/kidsfun-backend
Environment=PATH=/opt/kidsfun-backend/venv/bin
ExecStart=/opt/kidsfun-backend/venv/bin/gunicorn -c /opt/kidsfun-backend/gunicorn.conf.py main:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=kidsfun-backend

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/kidsfun-backend/media /opt/kidsfun-backend/logs

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```

### **8.3 Habilitar y iniciar servicio**
```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio
sudo systemctl enable kidsfun-backend

# Iniciar servicio
sudo systemctl start kidsfun-backend

# Verificar estado
sudo systemctl status kidsfun-backend
```

---

## 🌐 **Paso 9: Configuración de Nginx**

### **9.1 Crear configuración de Nginx**
```bash
# Crear archivo de configuración
sudo nano /etc/nginx/sites-available/kidsfun-backend
```

### **9.2 Contenido de la configuración**
```nginx
server {
    server_name api.tu-dominio.com;

    # Configuración de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Proxy principal
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Configuración para WebSockets
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Archivos estáticos
    location /static/ {
        alias /opt/kidsfun-backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Archivos de media
    location /media/ {
        alias /opt/kidsfun-backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
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

    # Rate limiting
    limit_req zone=api burst=20 nodelay;

    # Configuración de logs
    access_log /var/log/nginx/kidsfun-backend-access.log;
    error_log /var/log/nginx/kidsfun-backend-error.log;

    listen 80;
}
```

### **9.3 Habilitar sitio**
```bash
# Crear enlace simbólico
sudo ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

---

## 🔒 **Paso 10: Configuración de SSL**

### **10.1 Obtener certificado SSL**
```bash
# Obtener certificado SSL
sudo certbot --nginx -d api.tu-dominio.com --non-interactive --agree-tos --email admin@tu-dominio.com

# Verificar certificados
sudo certbot certificates
```

### **10.2 Verificar configuración SSL**
```bash
# Verificar que el certificado se aplicó correctamente
sudo nginx -t
sudo systemctl reload nginx

# Probar SSL
curl -I https://api.tu-dominio.com
```

---

## 🔄 **Paso 11: Configuración de Actualización Automática**

### **11.1 Crear script de actualización**
```bash
# Crear script de actualización
sudo nano /usr/local/bin/update-kidsfun-backend
```

### **11.2 Contenido del script**
```bash
#!/bin/bash

# Script de actualización automática para KidsFun Backend
# Uso: sudo update-kidsfun-backend

if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

PROJECT_DIR="/opt/kidsfun-backend"
BACKUP_DIR="/opt/kidsfun-backend/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ No se encontró el proyecto en $PROJECT_DIR"
    exit 1
fi

echo "🚀 Ejecutando actualización automática del Backend FastAPI..."
echo "⚠️  Este proceso es COMPLETAMENTE AUTOMÁTICO"
echo ""

# Crear backup de la base de datos
echo "📁 Creando backup de la base de datos..."
mkdir -p "$BACKUP_DIR"
sudo -u postgres pg_dump kidsfun_db > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Crear backup del código
echo "📁 Creando backup del código..."
cp -r "$PROJECT_DIR" "$BACKUP_DIR/code_backup_$TIMESTAMP"

# Cambiar al usuario kidsfun
echo "📥 Obteniendo últimos cambios del repositorio..."
sudo -u kidsfun bash -c "cd $PROJECT_DIR && git pull origin main"

# Activar entorno virtual e instalar dependencias
echo "📦 Instalando dependencias..."
sudo -u kidsfun bash -c "cd $PROJECT_DIR && source venv/bin/activate && pip install -r requirements.txt"

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
sudo -u kidsfun bash -c "cd $PROJECT_DIR && source venv/bin/activate && alembic upgrade head"

# Reiniciar servicio
echo "🔄 Reiniciando servicio..."
sudo systemctl restart kidsfun-backend

# Verificar servicio
echo "✅ Verificando servicio..."
sleep 5
if sudo systemctl is-active --quiet kidsfun-backend; then
    echo "✅ Servicio iniciado correctamente"
else
    echo "❌ Error al iniciar el servicio"
    sudo systemctl status kidsfun-backend
    exit 1
fi

# Limpiar backups antiguos (mantener solo los últimos 5)
echo "🧹 Limpiando backups antiguos..."
cd "$BACKUP_DIR"
ls -t | tail -n +6 | xargs -r rm -rf

echo "🎉 ¡Actualización completada exitosamente!"
echo "🌐 Backend disponible en: https://api.tu-dominio.com"
echo "📊 Health check: https://api.tu-dominio.com/health"
```

### **11.3 Dar permisos de ejecución**
```bash
sudo chmod +x /usr/local/bin/update-kidsfun-backend
```

---

## 📊 **Paso 12: Configuración de Monitoreo**

### **12.1 Crear script de monitoreo**
```bash
# Crear script de monitoreo
sudo nano /opt/kidsfun-backend/monitor.sh
```

### **12.2 Contenido del script**
```bash
#!/bin/bash

# Script de monitoreo para KidsFun Backend
# Uso: ./monitor.sh

echo "🔍 Monitoreo del Backend FastAPI - KidsFun"
echo "=========================================="

# Verificar estado de servicios
echo "📊 Estado de servicios:"
echo "  - Nginx: $(sudo systemctl is-active nginx)"
echo "  - PostgreSQL: $(sudo systemctl is-active postgresql)"
echo "  - KidsFun Backend: $(sudo systemctl is-active kidsfun-backend)"

# Verificar certificados SSL
echo "🔒 Certificados SSL:"
sudo certbot certificates | grep -E "(Certificate Name|Expiry Date)"

# Verificar espacio en disco
echo "💾 Espacio en disco:"
df -h /opt/kidsfun-backend

# Verificar logs recientes
echo "📝 Logs recientes (últimas 10 líneas):"
sudo tail -10 /var/log/nginx/kidsfun-backend-access.log

# Verificar respuesta del API
echo "🌐 Respuesta del API:"
curl -s -o /dev/null -w "%{http_code}" https://api.tu-dominio.com/health
echo " - Status Code"

# Verificar base de datos
echo "🗄️ Estado de la base de datos:"
sudo -u postgres psql -d kidsfun_db -c "SELECT version();" | head -2

echo "✅ Monitoreo completado"
```

### **12.3 Dar permisos de ejecución**
```bash
sudo chmod +x /opt/kidsfun-backend/monitor.sh
```

---

## 🔄 **Paso 13: Configuración de Backups Automáticos**

### **13.1 Crear script de backup**
```bash
# Crear script de backup
sudo nano /opt/kidsfun-backend/backup.sh
```

### **13.2 Contenido del script**
```bash
#!/bin/bash

# Script de backup automático para KidsFun Backend
# Uso: ./backup.sh

BACKUP_DIR="/opt/kidsfun-backend/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "📁 Iniciando backup automático..."

# Crear directorio de backup
mkdir -p "$BACKUP_DIR"

# Backup de la base de datos
echo "🗄️ Creando backup de la base de datos..."
sudo -u postgres pg_dump kidsfun_db > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Backup del código
echo "📁 Creando backup del código..."
tar -czf "$BACKUP_DIR/code_backup_$TIMESTAMP.tar.gz" -C /opt kidsfun-backend

# Backup de archivos media
echo "🖼️ Creando backup de archivos media..."
tar -czf "$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz" -C /opt/kidsfun-backend media

# Limpiar backups antiguos (mantener solo los últimos 7 días)
echo "🧹 Limpiando backups antiguos..."
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completado exitosamente!"
echo "📁 Ubicación: $BACKUP_DIR"
```

### **13.3 Configurar cron para backups automáticos**
```bash
# Editar crontab
sudo crontab -e

# Agregar línea para backup diario a las 2 AM
0 2 * * * /opt/kidsfun-backend/backup.sh >> /var/log/kidsfun-backend/backup.log 2>&1
```

---

## 🚨 **Paso 14: Configuración de Firewall**

### **14.1 Configurar UFW**
```bash
# Habilitar UFW
sudo ufw enable

# Permitir SSH
sudo ufw allow ssh

# Permitir HTTP y HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Permitir PostgreSQL (solo local)
sudo ufw allow from 127.0.0.1 to any port 5432

# Verificar reglas
sudo ufw status
```

---

## 📚 **Paso 15: Verificación y Testing**

### **15.1 Verificar servicios**
```bash
# Verificar estado de todos los servicios
sudo systemctl status nginx postgresql kidsfun-backend

# Verificar configuración de Nginx
sudo nginx -t

# Verificar certificados SSL
sudo certbot certificates
```

### **15.2 Probar endpoints**
```bash
# Probar health check
curl -I https://api.tu-dominio.com/health

# Probar API principal
curl -I https://api.tu-dominio.com/

# Probar documentación
curl -I https://api.tu-dominio.com/docs

# Probar redirección HTTP a HTTPS
curl -I http://api.tu-dominio.com
```

### **15.3 Verificar logs**
```bash
# Ver logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-backend-access.log
sudo tail -f /var/log/nginx/kidsfun-backend-error.log

# Ver logs del backend
sudo journalctl -u kidsfun-backend -f

# Ver logs de SSL
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

---

## 🎯 **Paso 16: Comandos Útiles**

### **16.1 Comandos de gestión**
```bash
# Actualizar backend
sudo update-kidsfun-backend

# Verificar estado
sudo systemctl status kidsfun-backend

# Ver logs en tiempo real
sudo journalctl -u kidsfun-backend -f

# Monitorear sistema
/opt/kidsfun-backend/monitor.sh

# Reiniciar servicios
sudo systemctl restart kidsfun-backend nginx

# Verificar certificados SSL
sudo certbot certificates

# Renovar certificados SSL
sudo certbot renew --dry-run

# Crear backup manual
/opt/kidsfun-backend/backup.sh
```

### **16.2 Estructura de directorios final**
```
/opt/
└── kidsfun-backend/          # Backend FastAPI
    ├── venv/                 # Entorno virtual
    ├── app/                  # Código de la aplicación
    ├── alembic/              # Migraciones
    ├── media/                # Archivos media
    ├── logs/                 # Logs de la aplicación
    ├── backups/              # Backups automáticos
    ├── build.sh              # Script de construcción
    ├── monitor.sh            # Script de monitoreo
    └── backup.sh             # Script de backup

/var/www/
└── kidsfun-backend/          # Archivos estáticos (si aplica)

/etc/nginx/sites-available/
└── kidsfun-backend          # Configuración de Nginx

/etc/systemd/system/
└── kidsfun-backend.service  # Servicio de systemd
```

---

## 🚨 **Solución de Problemas**

### **Problema: Error 502 Bad Gateway**
```bash
# Verificar que el backend está funcionando
sudo systemctl status kidsfun-backend

# Verificar logs del backend
sudo journalctl -u kidsfun-backend -f

# Verificar configuración de Nginx
sudo nginx -t

# Verificar que el puerto 8000 está abierto
sudo netstat -tlnp | grep :8000
```

### **Problema: Error de conexión a la base de datos**
```bash
# Verificar que PostgreSQL está funcionando
sudo systemctl status postgresql

# Verificar conexión
psql -U kidsfun -d kidsfun_db -h localhost

# Verificar configuración en .env
cat /opt/kidsfun-backend/.env | grep DATABASE_URL
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

### **Problema: Archivos media no se sirven**
```bash
# Verificar permisos
sudo chown -R www-data:www-data /opt/kidsfun-backend/media

# Verificar configuración de Nginx
sudo nginx -t

# Verificar logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-backend-error.log
```

---

## 🎉 **Resultado Final**

### **URLs Disponibles**
- **🔗 API Principal:** `https://api.tu-dominio.com`
- **📊 Health Check:** `https://api.tu-dominio.com/health`
- **📚 Documentación:** `https://api.tu-dominio.com/docs`
- **🔒 Security Info:** `https://api.tu-dominio.com/security-info`

### **Características Implementadas**
- ✅ **Base de datos PostgreSQL** - Configurada y optimizada
- ✅ **Nginx reverse proxy** - Configurado para producción
- ✅ **SSL automático** - Certificados Let's Encrypt
- ✅ **Gunicorn WSGI** - Servidor de producción
- ✅ **Systemd service** - Gestión de servicios
- ✅ **Logs centralizados** - Nginx y aplicación
- ✅ **Backups automáticos** - Base de datos y código
- ✅ **Actualización automática** - Script `update-kidsfun-backend`
- ✅ **Monitoreo** - Scripts de verificación
- ✅ **Firewall** - UFW configurado
- ✅ **Rate limiting** - Protección contra ataques
- ✅ **Security headers** - Headers de seguridad

---

## 📞 **Soporte**

### **Comandos de emergencia**
```bash
# Reiniciar todo el sistema
sudo reboot

# Verificar todos los servicios
sudo systemctl status nginx postgresql kidsfun-backend

# Ver logs completos
sudo journalctl -u nginx -f
sudo journalctl -u kidsfun-backend -f
sudo journalctl -u postgresql -f
```

### **Contacto**
- **📧 Email:** soporte@tu-dominio.com
- **🔗 Documentación:** [README.md](./README.md)
- **🌐 Health Check:** `https://api.tu-dominio.com/health`

---

**¡Backend FastAPI desplegado exitosamente! 🚀** 