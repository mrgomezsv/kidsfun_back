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
│   ├── middleware.py      # Middleware de seguridad
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic
│   └── routers/           # Endpoints de la API
├── alembic/               # Migraciones de BD
├── main.py               # Aplicación principal
├── requirements.txt      # Dependencias
├── env.example          # Variables de entorno
├── deploy_ubuntu.sh     # Script de despliegue
├── setup_server.sh      # Configuración del servidor
├── update.sh            # Script de actualización automática
├── setup_update_command.sh # Configuración del comando global
├── update_security.sh   # Actualización de seguridad
├── API_DOCUMENTATION.md # Documentación para consumir la API
└── README.md           # Este archivo
```

### Endpoints Principales

- **Documentación**: `http://your-server:8000/docs`
- **Health Check**: `http://your-server:8000/health`
- **Security Info**: `http://your-server:8000/security-info`
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
- ✅ Rate limiting (10 requests/segundo por IP)
- ✅ Validación de entrada (XSS, SQL injection protection)
- ✅ Headers de seguridad (HSTS, CSP, X-Frame-Options)
- ✅ Trusted hosts middleware
- ✅ Logging de requests para auditoría

## 🔄 **Sistema de Actualización Automática**

### **🚀 Comando Global de Actualización**

Una vez desplegado, puedes actualizar el proyecto con **un solo comando**:

```bash
# Actualizar todo automáticamente
sudo update-kidsfun
```

### **⚙️ Configuración del Comando Global**

Para configurar el comando global (solo una vez):

```bash
# Ir al directorio del proyecto
cd /opt/kidsfun-backend

# Configurar el comando global
sudo ./setup_update_command.sh

# Aplicar cambios en la sesión actual
source ~/.bashrc
```

### **🎯 Características del Sistema Automático**

El comando `sudo update-kidsfun` hace **TODO automáticamente**:

- ✅ **Backup automático** de configuración con timestamp
- ✅ **Obtener cambios** del repositorio automáticamente
- ✅ **Actualizar dependencias** de Python
- ✅ **Aplicar migraciones** de base de datos
- ✅ **Reiniciar servicios** (kidsfun-backend y nginx)
- ✅ **Verificar servicios** con retry automático
- ✅ **Verificar endpoints** con retry automático
- ✅ **Limpiar backups** antiguos automáticamente
- ✅ **Manejo de errores** robusto con reintentos

### **📊 Ejemplo de Salida del Comando**

```bash
sudo update-kidsfun
```

**Salida esperada:**
```
🚀 Ejecutando actualización AUTOMÁTICA del KidsFun Backend...
⚠️  Este proceso es COMPLETAMENTE AUTOMÁTICO
⚠️  No se requiere intervención manual

[INFO] 📁 Directorio del proyecto: /opt/kidsfun-backend
[INFO] 🔄 Creando backup automático de la configuración...
[SUCCESS] Backup automático completado
[INFO] 🔧 Configurando Git automáticamente...
[SUCCESS] Git configurado automáticamente
[INFO] 📥 Obteniendo cambios del repositorio automáticamente...
[SUCCESS] Proyecto actualizado automáticamente a la última versión
[SUCCESS] ✅ Middleware de seguridad encontrado
[SUCCESS] ✅ Documentación de API encontrada
[SUCCESS] Dependencias actualizadas automáticamente
[SUCCESS] Migraciones aplicadas automáticamente
[SUCCESS] Servicios reiniciados automáticamente
[SUCCESS] Servicio kidsfun-backend está activo
[SUCCESS] Servicio nginx está activo
[SUCCESS] Health check funcionando
[SUCCESS] Security info endpoint funcionando
🎉 ¡Actualización AUTOMÁTICA completada exitosamente!
```

### **🛠️ Scripts de Actualización Disponibles**

#### **1. Comando Global (Recomendado)**
```bash
# Actualizar con un solo comando desde cualquier lugar
sudo update-kidsfun
```

#### **2. Script Universal**
```bash
# Actualizar con el script universal
cd /opt/kidsfun-backend
sudo ./update.sh
```

#### **3. Script de Seguridad**
```bash
# Actualizar con el script de seguridad
cd /opt/kidsfun-backend
sudo ./update_security.sh
```

### **📁 Sistema de Backups**

Los backups se guardan automáticamente en:
```
/opt/kidsfun-backend/backups/
├── main.py.backup.20241203_001500
├── .env.backup.20241203_001500
├── main.py.backup.20241203_002000
└── .env.backup.20241203_002000
```

**Características:**
- ✅ **Backup automático** antes de cada actualización
- ✅ **Timestamp único** para cada backup
- ✅ **Limpieza automática** (mantiene solo los últimos 5)
- ✅ **Recuperación fácil** si algo sale mal

### **🔧 Verificación Post-Actualización**

Después de cada actualización, puedes verificar:

```bash
# Verificar servicios
sudo systemctl status kidsfun-backend
sudo systemctl status nginx

# Verificar endpoints
curl https://api.kidsfunyfiestasinfantiles.com/health
curl https://api.kidsfunyfiestasinfantiles.com/security-info

# Ver logs
sudo journalctl -u kidsfun-backend -f
```

### **🚨 Solución de Problemas**

#### **Si el comando no funciona:**
```bash
# Verificar que existe
which update-kidsfun

# Reconfigurar si es necesario
cd /opt/kidsfun-backend
sudo ./setup_update_command.sh
source ~/.bashrc
```

#### **Si hay errores de permisos:**
```bash
# Dar permisos de ejecución
chmod +x update.sh
chmod +x setup_update_command.sh
```

#### **Si hay errores de Git:**
```bash
# Configurar Git manualmente
git config --global --add safe.directory /opt/kidsfun-backend
```

### **📋 Comandos Útiles de Actualización**

```bash
# Actualización completa automática
sudo update-kidsfun

# Verificar estado antes de actualizar
sudo systemctl status kidsfun-backend
curl https://api.kidsfunyfiestasinfantiles.com/health

# Ver logs durante la actualización
sudo journalctl -u kidsfun-backend -f

# Verificar después de la actualización
curl https://api.kidsfunyfiestasinfantiles.com/security-info
```

### Actualización de Seguridad

Para aplicar las últimas mejoras de seguridad:

```bash
# Actualizar seguridad
chmod +x update_security.sh
sudo ./update_security.sh
```

Este script:
- ✅ Hace backup de la configuración actual
- ✅ Obtiene cambios del repositorio
- ✅ Actualiza dependencias
- ✅ Aplica migraciones
- ✅ Reinicia servicios
- ✅ Verifica que todo funcione correctamente

### Soporte

Para problemas o consultas:
- Revisar logs: `sudo journalctl -u kidsfun-backend -f`
- Verificar configuración: `cat /opt/kidsfun-backend/.env`
- Reiniciar servicio: `sudo systemctl restart kidsfun-backend`

## 📚 **Documentación para Consumir la API**

### **📖 Guía Completa de Integración**

Para consumir la API de KidsFun, consulta la documentación completa:

**📄 [API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

Esta guía incluye:

#### **🔐 Autenticación y Seguridad**
- ✅ Obtener y usar tokens JWT
- ✅ Registro de usuarios
- ✅ Mejores prácticas de seguridad
- ✅ Manejo de errores de autenticación

#### **📋 Endpoints Detallados**
- ✅ **Autenticación**: Login, registro, obtener usuario actual
- ✅ **Usuarios**: CRUD completo de usuarios
- ✅ **Productos**: Gestión de productos con imágenes
- ✅ **Likes**: Sistema de likes para productos
- ✅ **Comentarios**: Sistema de comentarios
- ✅ **Eventos**: Gestión de eventos
- ✅ **Waivers**: Sistema de waivers con QR
- ✅ **Chat**: Sistema de chat en tiempo real

#### **📱 Ejemplos por Tecnología**
- ✅ **JavaScript/Fetch**: Ejemplos con fetch API
- ✅ **Axios**: Configuración con interceptors
- ✅ **React Hooks**: Custom hooks para React
- ✅ **cURL**: Ejemplos de línea de comandos

#### **🔒 Mejores Prácticas de Seguridad**
- ✅ Manejo seguro de tokens
- ✅ Renovación automática de tokens
- ✅ Validación de datos del cliente
- ✅ Manejo de errores de seguridad
- ✅ Rate limiting y protección contra ataques

#### **🚨 Limitaciones y Rate Limiting**
- ✅ Rate limit: 10 requests por segundo por IP
- ✅ Tamaño máximo de archivo: 10MB
- ✅ Tiempo de expiración del token: 30 minutos
- ✅ Máximo de productos por página: 100

### **🎯 URLs de Documentación**

- **📖 Swagger UI**: https://api.kidsfunyfiestasinfantiles.com/docs
- **📋 ReDoc**: https://api.kidsfunyfiestasinfantiles.com/redoc
- **💚 Health Check**: https://api.kidsfunyfiestasinfantiles.com/health
- **🛡️ Security Info**: https://api.kidsfunyfiestasinfantiles.com/security-info

### **🔐 Ejemplo Rápido de Autenticación**

```javascript
// Login para obtener token
const login = async (username, password) => {
  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `username=${username}&password=${password}`
  });
  
  const data = await response.json();
  localStorage.setItem('auth_token', data.access_token);
  return data;
};

// Usar token en requests
const getProducts = async () => {
  const token = localStorage.getItem('auth_token');
  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/products/', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
};
```

## 🎉 **DESPLIEGUE EXITOSO - VERIFICACIÓN**

### ✅ **Estado Actual del Sistema**

Tu API de KidsFun está **completamente desplegada y funcionando** en producción:

- **🌐 URL Principal:** https://api.kidsfunyfiestasinfantiles.com
- **🔒 SSL/HTTPS:** Configurado automáticamente con Certbot
- **📊 Health Check:** https://api.kidsfunyfiestasinfantiles.com/health
- **📚 Documentación:** https://api.kidsfunyfiestasinfantiles.com/docs
- **🛡️ Security Info:** https://api.kidsfunyfiestasinfantiles.com/security-info

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

# Actualizar seguridad
sudo ./update_security.sh
```

### 🔧 **Verificación del Sistema**

```bash
# Verificar que la API responda
curl https://api.kidsfunyfiestasinfantiles.com/health

# Verificar SSL
curl -I https://api.kidsfunyfiestasinfantiles.com

# Verificar información de seguridad
curl https://api.kidsfunyfiestasinfantiles.com/security-info

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
    "docs": "/docs",
    "security": {
        "rate_limit": "10 requests/second",
        "ssl_required": true,
        "cors_enabled": true
    }
}
```

### 📚 **URLs Importantes**

- **🏠 Página Principal:** https://api.kidsfunyfiestasinfantiles.com
- **💚 Health Check:** https://api.kidsfunyfiestasinfantiles.com/health
- **📖 Swagger UI:** https://api.kidsfunyfiestasinfantiles.com/docs
- **📋 ReDoc:** https://api.kidsfunyfiestasinfantiles.com/redoc
- **🛡️ Security Info:** https://api.kidsfunyfiestasinfantiles.com/security-info

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
- ✅ **Rate Limiting** (10 requests/segundo por IP)
- ✅ **CORS** configurado para dominios permitidos
- ✅ **JWT** para autenticación
- ✅ **Validación** de datos con Pydantic
- ✅ **Logs** de acceso y errores
- ✅ **Firewall** configurado
- ✅ **XSS Protection** con validación de entrada
- ✅ **SQL Injection Protection** con validación de patrones
- ✅ **Security Headers** (HSTS, CSP, X-Frame-Options)
- ✅ **Trusted Hosts** middleware
- ✅ **Request Logging** para auditoría
- ✅ **Input Validation** con patrones sospechosos

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