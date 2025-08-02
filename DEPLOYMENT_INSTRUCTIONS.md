# 🚀 Instrucciones de Despliegue - KidsFun Backend

## 📋 Información del Servidor

- **Dominio:** `api.kidsfunyfiestasinfantiles.com`
- **Servidor:** Ubuntu (PostgreSQL ya instalado)
- **Base de datos:** `smap_kf` (usuario: `mrgomez`)

## 🎯 Despliegue Automático (Recomendado)

### Paso 1: Descargar el script de despliegue

```bash
# En tu servidor Ubuntu (como root)
cd /tmp
wget https://raw.githubusercontent.com/mrgomezsv/kidsfun_back/mrg_prod/deploy_complete.sh
chmod +x deploy_complete.sh
```

### Paso 2: Ejecutar el despliegue

```bash
# Ejecutar como root
sudo ./deploy_complete.sh
```

**El script automáticamente:**
- ✅ Instala todas las dependencias (Python, Nginx, Certbot)
- ✅ Crea usuario `kidsfun`
- ✅ Clona el proyecto desde GitHub
- ✅ Configura variables de entorno
- ✅ Instala dependencias de Python
- ✅ Configura systemd service
- ✅ Configura Nginx con SSL
- ✅ Crea script de actualización
- ✅ Inicia todos los servicios

## 🔧 Despliegue Manual (Si prefieres control total)

### Paso 1: Instalar dependencias

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y nginx certbot python3-certbot-nginx
sudo apt install -y git curl wget unzip postgresql-client logrotate
```

### Paso 2: Crear usuario y directorio

```bash
sudo useradd -m -s /bin/bash kidsfun
sudo usermod -aG sudo kidsfun
sudo mkdir -p /opt/kidsfun-backend
sudo chown kidsfun:kidsfun /opt/kidsfun-backend
```

### Paso 3: Clonar proyecto

```bash
cd /opt/kidsfun-backend
sudo -u kidsfun git clone -b mrg_prod https://github.com/mrgomezsv/kidsfun_back.git .
```

### Paso 4: Configurar entorno

```bash
# Configurar variables de entorno automáticamente
sudo -u kidsfun ./setup_env.sh

# O configurar manualmente
sudo -u kidsfun cp env.example .env
sudo -u kidsfun nano .env
```

### Paso 5: Crear entorno virtual e instalar dependencias

```bash
sudo -u kidsfun python3 -m venv .env
sudo -u kidsfun bash -c "source .env/bin/activate && pip install -r requirements.txt"
```

### Paso 6: Configurar servicios

```bash
# Systemd service
sudo cp kidsfun-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kidsfun-backend

# Nginx
sudo cp kidsfun-backend.nginx /etc/nginx/sites-available/kidsfun-backend
sudo ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Logrotate
sudo cp kidsfun-backend /etc/logrotate.d/kidsfun-backend
```

### Paso 7: Configurar firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### Paso 8: Iniciar servicios

```bash
sudo systemctl start nginx
sudo systemctl start kidsfun-backend
```

### Paso 9: Configurar SSL

```bash
sudo certbot --nginx -d api.kidsfunyfiestasinfantiles.com --non-interactive --agree-tos --email admin@kidsfunyfiestasinfantiles.com
```

## 🔄 Actualización del Proyecto

### Actualización Automática

```bash
# Usar el script de actualización creado
sudo update-kidsfun
```

### Actualización Manual

```bash
cd /opt/kidsfun-backend

# Hacer backup de configuración
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Obtener cambios
sudo -u kidsfun git fetch origin
sudo -u kidsfun git reset --hard origin/mrg_prod

# Restaurar configuración
cp .env.backup.* .env

# Actualizar dependencias
sudo -u kidsfun bash -c "source .env/bin/activate && pip install -r requirements.txt"

# Ejecutar migraciones (sin perder datos)
sudo -u kidsfun bash -c "source .env/bin/activate && alembic upgrade head"

# Reiniciar servicios
sudo systemctl restart kidsfun-backend
sudo systemctl restart nginx
```

## 🛠️ Comandos de Gestión

### Verificar estado de servicios

```bash
# Estado del backend
sudo systemctl status kidsfun-backend

# Estado de Nginx
sudo systemctl status nginx

# Logs del backend
sudo journalctl -u kidsfun-backend -f

# Logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-backend-error.log
```

### Reiniciar servicios

```bash
sudo systemctl restart kidsfun-backend
sudo systemctl restart nginx
```

### Verificar salud del sistema

```bash
cd /opt/kidsfun-backend
sudo ./health_check.sh
```

## 📊 Monitoreo

### Verificar API

```bash
# Health check
curl https://api.kidsfunyfiestasinfantiles.com/health

# Documentación
curl https://api.kidsfunyfiestasinfantiles.com/docs
```

### Verificar SSL

```bash
# Verificar certificado SSL
sudo certbot certificates

# Renovar certificado (automático, pero puedes forzar)
sudo certbot renew --force-renewal
```

## 🔐 Configuración de Base de Datos

### Verificar conexión

```bash
# Conectar a PostgreSQL
psql -U mrgomez -d smap_kf -h localhost

# Verificar tablas
\dt

# Salir
\q
```

### Backup de base de datos

```bash
# Crear backup
pg_dump -U mrgomez -d smap_kf > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql -U mrgomez -d smap_kf < backup_file.sql
```

## 🚨 Solución de Problemas

### Si el servicio no inicia

```bash
# Ver logs detallados
sudo journalctl -u kidsfun-backend -n 50

# Verificar configuración
sudo systemctl status kidsfun-backend --no-pager -l
```

### Si Nginx no funciona

```bash
# Verificar configuración
sudo nginx -t

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### Si SSL no funciona

```bash
# Verificar certificado
sudo certbot certificates

# Reconfigurar SSL
sudo certbot --nginx -d api.kidsfunyfiestasinfantiles.com
```

## 📞 URLs Importantes

- **API Principal:** https://api.kidsfunyfiestasinfantiles.com
- **Documentación Swagger:** https://api.kidsfunyfiestasinfantiles.com/docs
- **Documentación ReDoc:** https://api.kidsfunyfiestasinfantiles.com/redoc
- **Health Check:** https://api.kidsfunyfiestasinfantiles.com/health

## ✅ Verificación Final

Después del despliegue, verifica que todo funcione:

1. **API responde:** `curl https://api.kidsfunyfiestasinfantiles.com/health`
2. **SSL funciona:** El navegador muestra el candado verde
3. **Documentación accesible:** https://api.kidsfunyfiestasinfantiles.com/docs
4. **Logs sin errores:** `sudo journalctl -u kidsfun-backend --since "5 minutes ago"`

¡Tu API estará lista para producción! 🎉 