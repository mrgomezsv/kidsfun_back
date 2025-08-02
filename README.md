# KidsFun Backend API

Backend API para el sistema de gestión de KidsFun construido con FastAPI.

## 🚀 Despliegue en Producción (Ubuntu Server)

### Requisitos Previos

- Ubuntu Server 20.04 o superior
- Python 3.8+
- PostgreSQL
- Nginx (opcional, para proxy reverso)

### Instalación Automática (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd kidsfun_back
```

2. **Configurar variables de entorno**
```bash
cp env.example .env
nano .env
```

**Configuraciones importantes en `.env`:**
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `SECRET_KEY`: Clave secreta para JWT (generar una segura)
- `SMTP_USER` y `SMTP_PASSWORD`: Credenciales de email

3. **Ejecutar script de despliegue**
```bash
chmod +x deploy_ubuntu.sh
sudo ./deploy_ubuntu.sh
```

El script automáticamente:
- ✅ Instala dependencias del sistema
- ✅ Crea entorno virtual `.env`
- ✅ Instala dependencias de Python
- ✅ Verifica conexión a base de datos
- ✅ Ejecuta migraciones
- ✅ Configura Gunicorn
- ✅ Crea servicio systemd
- ✅ Inicia el servicio

### Instalación Manual

Si prefieres instalar manualmente:

1. **Configurar servidor**
```bash
chmod +x setup_server.sh
sudo ./setup_server.sh
```

2. **Configurar aplicación**
```bash
cp env.example .env
nano .env  # Editar configuraciones
```

3. **Crear entorno virtual**
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

4. **Verificar base de datos**
```bash
source .env/bin/activate
alembic upgrade head
```

5. **Ejecutar con Gunicorn**
```bash
source .env/bin/activate
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Gestión del Servicio

```bash
# Verificar estado
sudo systemctl status kidsfun-backend

# Iniciar servicio
sudo systemctl start kidsfun-backend

# Parar servicio
sudo systemctl stop kidsfun-backend

# Reiniciar servicio
sudo systemctl restart kidsfun-backend

# Habilitar inicio automático
sudo systemctl enable kidsfun-backend

# Ver logs
sudo journalctl -u kidsfun-backend -f
```

### Configuración de Nginx (Opcional)

Para usar Nginx como proxy reverso:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media/ {
        alias /opt/kidsfun-backend/media/;
    }
}
```

### Estructura del Proyecto

```
kidsfun_back/
├── app/
│   ├── config.py          # Configuración
│   ├── database.py        # Configuración de BD
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic
│   └── routers/           # Endpoints de la API
├── alembic/               # Migraciones de BD
├── main.py               # Aplicación principal
├── requirements.txt      # Dependencias
├── env.example          # Variables de entorno
├── deploy_ubuntu.sh     # Script de despliegue
├── setup_server.sh      # Configuración del servidor
└── README.md           # Este archivo
```

### Endpoints Principales

- **Documentación**: `http://your-server:8000/docs`
- **Health Check**: `http://your-server:8000/health`
- **API Base**: `http://your-server:8000/api`

### Monitoreo y Logs

- **Logs de aplicación**: `/opt/kidsfun-backend/logs/`
- **Logs del sistema**: `sudo journalctl -u kidsfun-backend`
- **Estado del servicio**: `sudo systemctl status kidsfun-backend`

### Seguridad

- ✅ Variables de entorno para credenciales
- ✅ JWT para autenticación
- ✅ CORS configurado
- ✅ Validación de datos con Pydantic
- ✅ Logs de acceso y errores

### Soporte

Para problemas o consultas:
- Revisar logs: `sudo journalctl -u kidsfun-backend -f`
- Verificar configuración: `cat /opt/kidsfun-backend/.env`
- Reiniciar servicio: `sudo systemctl restart kidsfun-backend`

## 🎉 **DESPLIEGUE EXITOSO - VERIFICACIÓN**

### ✅ **Estado Actual del Sistema**

Tu API de KidsFun está **completamente desplegada y funcionando** en producción:

- **🌐 URL Principal:** https://api.kidsfunyfiestasinfantiles.com
- **🔒 SSL/HTTPS:** Configurado automáticamente con Certbot
- **📊 Health Check:** https://api.kidsfunyfiestasinfantiles.com/health
- **📚 Documentación:** https://api.kidsfunyfiestasinfantiles.com/docs

### 🚀 **Comandos de Gestión Disponibles**

```bash
# Verificar estado de servicios
sudo systemctl status kidsfun-backend
sudo systemctl status nginx

# Reiniciar servicios
sudo systemctl restart kidsfun-backend
sudo systemctl restart nginx

# Ver logs en tiempo real
sudo journalctl -u kidsfun-backend -f

# Actualizar el proyecto (nuevas versiones)
sudo update-kidsfun
```

### 🔧 **Verificación del Sistema**

```bash
# Verificar que la API responda
curl https://api.kidsfunyfiestasinfantiles.com/health

# Verificar SSL
curl -I https://api.kidsfunyfiestasinfantiles.com

# Verificar salud del sistema
cd /opt/kidsfun-backend
sudo ./health_check.sh
```

### 📊 **Monitoreo y Logs**

```bash
# Logs de aplicación
tail -f /opt/kidsfun-backend/logs/error.log

# Logs del sistema
sudo journalctl -u kidsfun-backend -f

# Logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-backend-error.log
```

### 🎯 **¿Qué verás al entrar a https://api.kidsfunyfiestasinfantiles.com?**

Al acceder a la URL principal, verás:

```json
{
    "message": "KidsFun API",
    "version": "1.0.0",
    "docs": "/docs"
}
```

### 📚 **URLs Importantes**

- **🏠 Página Principal:** https://api.kidsfunyfiestasinfantiles.com
- **💚 Health Check:** https://api.kidsfunyfiestasinfantiles.com/health
- **📖 Swagger UI:** https://api.kidsfunyfiestasinfantiles.com/docs
- **📋 ReDoc:** https://api.kidsfunyfiestasinfantiles.com/redoc

### 🔐 **Endpoints de la API**

- **Autenticación:** `/api/auth/`
- **Usuarios:** `/api/users/`
- **Productos:** `/api/products/`
- **Likes:** `/api/likes/`
- **Comentarios:** `/api/commentaries/`
- **Eventos:** `/api/events/`
- **Waivers:** `/api/waiver/`
- **Chat:** `/api/chat/`

### 🛡️ **Características de Seguridad Implementadas**

- ✅ **SSL/HTTPS** automático con Let's Encrypt
- ✅ **Rate Limiting** (10 requests/segundo)
- ✅ **CORS** configurado para dominios permitidos
- ✅ **JWT** para autenticación
- ✅ **Validación** de datos con Pydantic
- ✅ **Logs** de acceso y errores
- ✅ **Firewall** configurado

### 🔄 **Sistema de Actualización**

Para actualizar el proyecto con nuevas versiones:

```bash
# Actualización automática
sudo update-kidsfun
```

Este comando:
- ✅ Hace backup de la configuración
- ✅ Obtiene cambios del repositorio
- ✅ Actualiza dependencias
- ✅ Ejecuta migraciones (sin perder datos)
- ✅ Reinicia servicios

### 🎉 **¡Tu API está lista para producción!**

El sistema está completamente funcional con todas las mejores prácticas de seguridad y rendimiento implementadas. 