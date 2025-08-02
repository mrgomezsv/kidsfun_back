# 🚀 Guía de Despliegue - KidsFun Backend en Ubuntu Server

Esta guía te llevará paso a paso para desplegar el backend de KidsFun en un servidor Ubuntu.

## 📋 Prerrequisitos

### **1. Servidor Ubuntu**
- Ubuntu 20.04 LTS o superior
- Acceso SSH con permisos de sudo
- Mínimo 2GB RAM
- Mínimo 10GB espacio en disco

### **2. Información Necesaria**
- IP del servidor Ubuntu
- Credenciales de la base de datos PostgreSQL
- Configuración de email (Gmail)
- Dominio (opcional)

## 🔧 Paso 1: Preparar el Servidor

### **1.1 Conectarse al servidor**
```bash
ssh usuario@tu-servidor-ubuntu
```

### **1.2 Ejecutar script de preparación**
```bash
# Descargar el script de preparación
wget https://raw.githubusercontent.com/tu-repo/kidsfun-backend/main/setup_server.sh
chmod +x setup_server.sh
sudo ./setup_server.sh
```

**Este script instalará:**
- ✅ Python 3 y pip
- ✅ PostgreSQL client
- ✅ Nginx (proxy reverso)
- ✅ Supervisor (gestión de procesos)
- ✅ UFW (firewall)
- ✅ Logrotate (rotación de logs)
- ✅ Usuario `kidsfun` para la aplicación

## 📁 Paso 2: Preparar el Código

### **2.1 Clonar el repositorio**
```bash
# Crear directorio de la aplicación
sudo mkdir -p /opt/kidsfun-backend
sudo chown $USER:$USER /opt/kidsfun-backend
cd /opt/kidsfun-backend

# Clonar el repositorio (reemplaza con tu URL)
git clone https://github.com/tu-usuario/kidsfun-backend.git .
```

### **2.2 Configurar variables de entorno**
```bash
# Copiar archivo de configuración de producción
cp env.production.example .env

# Editar el archivo .env
nano .env
```

**Configuraciones importantes en `.env`:**
```bash
# Base de datos
DATABASE_URL=postgresql://usuario:password@servidor:5432/base_datos

# Seguridad (¡CAMBIAR ESTO!)
SECRET_KEY=tu-super-secret-key-muy-largo-y-seguro

# Email
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-password-de-aplicacion

# Dominio (si tienes)
ALLOWED_ORIGINS=["https://tu-dominio.com", "https://www.tu-dominio.com"]
```

## 🚀 Paso 3: Desplegar la Aplicación

### **3.1 Ejecutar script de despliegue**
```bash
# Hacer ejecutable el script
chmod +x deploy_ubuntu.sh

# Ejecutar despliegue
sudo ./deploy_ubuntu.sh
```

**Este script:**
- ✅ Instala dependencias de Python
- ✅ Verifica conexión a la base de datos
- ✅ Ejecuta migraciones
- ✅ Configura Gunicorn
- ✅ Configura Supervisor
- ✅ Configura Nginx
- ✅ Inicia el servicio

### **3.2 Verificar el despliegue**
```bash
# Verificar estado del servicio
sudo supervisorctl status kidsfun-backend

# Ver logs
sudo tail -f /opt/kidsfun-backend/logs/error.log

# Probar la API
curl http://localhost:8000/health
```

## 🔧 Paso 4: Configuración Adicional

### **4.1 Configurar SSL/HTTPS (Recomendado)**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Configurar renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **4.2 Configurar backup automático**
```bash
# Crear script de backup
sudo nano /opt/kidsfun-backend/backup.sh
```

```bash
#!/bin/bash
# Script de backup para KidsFun Backend
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/kidsfun-backend"

mkdir -p $BACKUP_DIR

# Backup de la base de datos
pg_dump $DATABASE_URL > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de archivos
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /opt/kidsfun-backend/media

# Mantener solo los últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
chmod +x /opt/kidsfun-backend/backup.sh

# Agregar a crontab para backup diario
sudo crontab -e
# Agregar: 0 2 * * * /opt/kidsfun-backend/backup.sh
```

## 📊 Paso 5: Monitoreo y Mantenimiento

### **5.1 Comandos de gestión**
```bash
# Ver estado del servicio
sudo supervisorctl status kidsfun-backend

# Reiniciar servicio
sudo supervisorctl restart kidsfun-backend

# Ver logs en tiempo real
sudo tail -f /opt/kidsfun-backend/logs/access.log
sudo tail -f /opt/kidsfun-backend/logs/error.log

# Ver logs de supervisor
sudo tail -f /opt/kidsfun-backend/logs/supervisor.log
```

### **5.2 Monitoreo del sistema**
```bash
# Ver uso de memoria
free -h

# Ver uso de disco
df -h

# Ver procesos
htop

# Ver puertos abiertos
sudo netstat -tlnp
```

### **5.3 Actualizaciones**
```bash
# Actualizar código
cd /opt/kidsfun-backend
git pull origin main

# Reiniciar servicio
sudo supervisorctl restart kidsfun-backend

# Verificar que todo funcione
curl http://localhost:8000/health
```

## 🔍 Paso 6: Verificación Final

### **6.1 Probar endpoints principales**
```bash
# Health check
curl http://tu-servidor/health

# Documentación API
curl http://tu-servidor/docs

# Probar autenticación
curl -X POST http://tu-servidor/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'
```

### **6.2 Verificar logs**
```bash
# Ver logs de acceso
sudo tail -f /opt/kidsfun-backend/logs/access.log

# Ver logs de errores
sudo tail -f /opt/kidsfun-backend/logs/error.log

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🚨 Solución de Problemas

### **Problema: Servicio no inicia**
```bash
# Verificar logs de supervisor
sudo tail -f /opt/kidsfun-backend/logs/supervisor_error.log

# Verificar configuración
sudo supervisorctl reread
sudo supervisorctl update
```

### **Problema: Error de conexión a BD**
```bash
# Verificar conectividad
psql $DATABASE_URL -c "SELECT 1;"

# Verificar variables de entorno
cat /opt/kidsfun-backend/.env
```

### **Problema: Error de permisos**
```bash
# Corregir permisos
sudo chown -R kidsfun:kidsfun /opt/kidsfun-backend
sudo chmod -R 755 /opt/kidsfun-backend
sudo chmod 600 /opt/kidsfun-backend/.env
```

### **Problema: Puerto ocupado**
```bash
# Ver qué está usando el puerto 8000
sudo netstat -tlnp | grep :8000

# Matar proceso si es necesario
sudo kill -9 PID_DEL_PROCESO
```

## 📞 Soporte

### **Información útil para debugging:**
- **Logs de aplicación**: `/opt/kidsfun-backend/logs/`
- **Logs de Nginx**: `/var/log/nginx/`
- **Logs de supervisor**: `/var/log/supervisor/`
- **Configuración**: `/opt/kidsfun-backend/.env`

### **Comandos de emergencia:**
```bash
# Parar todo
sudo supervisorctl stop kidsfun-backend
sudo systemctl stop nginx

# Reiniciar todo
sudo systemctl restart nginx
sudo supervisorctl restart kidsfun-backend

# Ver estado completo
sudo systemctl status nginx
sudo supervisorctl status kidsfun-backend
```

## ✅ Checklist de Despliegue

- [ ] Servidor Ubuntu preparado
- [ ] Repositorio clonado en `/opt/kidsfun-backend`
- [ ] Archivo `.env` configurado
- [ ] Script de despliegue ejecutado
- [ ] Servicio iniciado y funcionando
- [ ] Nginx configurado y funcionando
- [ ] SSL configurado (opcional)
- [ ] Backup configurado
- [ ] Monitoreo configurado
- [ ] Pruebas realizadas

¡Tu backend de KidsFun está listo para producción! 🎉 