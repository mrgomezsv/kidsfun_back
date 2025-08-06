# 🎪 KidsFun Backend API

Sistema backend completo para la gestión de productos, usuarios, comentarios, likes, eventos, waivers y chat de KidsFun - Fiestas Infantiles.

## 🚀 Estado del Proyecto

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)

## 📋 Índice

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [🔄 Actualización del Servidor](#-actualización-del-servidor)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)

## ✨ Características

### 🔐 Autenticación y Seguridad
- **JWT Authentication** con tokens de acceso y renovación
- **Rate Limiting** (10 requests/segundo por IP)
- **CORS** configurado para dominios específicos
- **SSL Required** - HTTPS obligatorio
- **Input Validation** - Protección contra XSS y SQL injection
- **Security Headers** - HSTS, CSP, X-Frame-Options

### 🎪 Gestión de Productos
- **CRUD Completo** - Create, Read, Update, Delete
- **Filtros Avanzados** - Por categoría, búsqueda, estado
- **Múltiples Imágenes** - Hasta 5 imágenes por producto
- **YouTube Integration** - URLs de videos
- **Paginación** - Limit y offset
- **Relaciones** - Con likes y comentarios

### 💬 Sistema Social
- **Comentarios** - Sistema de comentarios por producto
- **Likes** - Sistema de favoritos
- **Usuarios** - Gestión completa de usuarios
- **Chat** - Sistema de chat en tiempo real

### 📅 Eventos y Waivers
- **Eventos** - Gestión de eventos
- **Waivers** - Sistema de permisos con QR codes
- **PDF Generation** - Generación automática de documentos

### 📊 Monitoreo y Logs
- **Request Logging** - Logs detallados de todas las requests
- **Error Tracking** - Captura y registro de errores
- **Health Checks** - Endpoints de monitoreo
- **Analytics** - Seguimiento de uso

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para PostgreSQL
- **PostgreSQL** - Base de datos principal
- **Alembic** - Migraciones de base de datos
- **Pydantic** - Validación de datos y serialización
- **JWT** - Autenticación con tokens
- **Gunicorn** - Servidor WSGI para producción

### Seguridad
- **bcrypt** - Hash de contraseñas
- **python-multipart** - Manejo de archivos
- **python-jose** - JWT tokens
- **passlib** - Utilidades de contraseñas

### Utilidades
- **requests** - Cliente HTTP
- **python-dotenv** - Variables de entorno
- **email-validator** - Validación de emails
- **Pillow** - Procesamiento de imágenes

## 📦 Instalación

### Prerrequisitos
- Python 3.12+
- PostgreSQL 15+
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/mrgomezsv/kidsfun_back.git
cd kidsfun_back
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 5. Configurar Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb smap_kf

# Ejecutar migraciones
alembic upgrade head
```

## ⚙️ Configuración

### Variables de Entorno (.env)
```bash
# Base de Datos
DATABASE_URL=postgresql://user:password@localhost/smap_kf

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:4200", "https://kidsfunyfiestasinfantiles.com"]

# Rate Limiting
RATE_LIMIT_PER_SECOND=10

# Email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🚀 Deployment

### Despliegue Automático (Recomendado)
```bash
# En el servidor Ubuntu (como root)
cd /tmp
wget https://raw.githubusercontent.com/mrgomezsv/kidsfun_back/mrg_prod/deploy_final.sh
chmod +x deploy_final.sh
sudo ./deploy_final.sh
```

### Despliegue Manual
```bash
# Instalar dependencias
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y nginx certbot python3-certbot-nginx
sudo apt install -y git curl wget unzip postgresql-client logrotate

# Crear usuario y directorio
sudo useradd -m -s /bin/bash kidsfun
sudo usermod -aG sudo kidsfun
sudo mkdir -p /opt/kidsfun-backend
sudo chown kidsfun:kidsfun /opt/kidsfun-backend

# Clonar proyecto
cd /opt/kidsfun-backend
sudo -u kidsfun git clone -b mrg_prod https://github.com/mrgomezsv/kidsfun_back.git .

# Configurar entorno
sudo -u kidsfun ./setup_env.sh

# Crear entorno virtual e instalar dependencias
sudo -u kidsfun python3 -m venv venv
sudo -u kidsfun bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Configurar servicios
sudo cp kidsfun-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kidsfun-backend

# Configurar Nginx
sudo cp kidsfun-backend.nginx /etc/nginx/sites-available/kidsfun-backend
sudo ln -sf /etc/nginx/sites-available/kidsfun-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Iniciar servicios
sudo systemctl start nginx
sudo systemctl start kidsfun-backend

# Configurar SSL
sudo certbot --nginx -d api.kidsfunyfiestasinfantiles.com --non-interactive --agree-tos --email admin@kidsfunyfiestasinfantiles.com
```

## 🔄 Actualización del Servidor

### 🎯 Actualización Automática (RECOMENDADO)

#### Opción 1: Comando Global
```bash
# En el servidor (como root)
sudo update-kidsfun
```

#### Opción 2: Script Principal
```bash
# En el servidor (desde /opt/kidsfun-backend)
cd /opt/kidsfun-backend
chmod +x update.sh
sudo ./update.sh
```

#### Opción 3: Script de Seguridad
```bash
# En el servidor (desde /opt/kidsfun-backend)
cd /opt/kidsfun-backend
sudo ./update_security.sh
```

### 📋 Lo que hace la actualización automática:

1. **📁 Backup automático** - Guarda configuración actual
2. **📥 Git pull** - Obtiene últimos cambios del repositorio
3. **🐍 Dependencias** - Instala/actualiza Python packages
4. **🔧 Migraciones** - Aplica cambios de base de datos (sin perder datos)
5. **🔄 Servicios** - Reinicia kidsfun-backend y nginx
6. **✅ Verificación** - Health checks y endpoints
7. **🧹 Limpieza** - Elimina backups antiguos

### 🚨 Solución de problemas comunes:

#### Problema: Permisos denegados
```bash
# Dar permisos de ejecución
cd /opt/kidsfun-backend
chmod +x update.sh
sudo ./update.sh
```

#### Problema: Servicio no inicia
```bash
# Verificar logs
sudo journalctl -u kidsfun-backend -f

# Reiniciar manualmente
sudo systemctl restart kidsfun-backend
sudo systemctl restart nginx
```

#### Problema: Base de datos
```bash
# Verificar conexión
cd /opt/kidsfun-backend
source venv/bin/activate
python -c "from app.database import engine; print('DB OK')"
```

### ✅ Verificación después de la actualización:

```bash
# Verificar estado del servicio
sudo systemctl status kidsfun-backend

# Verificar que la API funciona
curl https://api.kidsfunyfiestasinfantiles.com/health

# Verificar que los datos se devuelven correctamente
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/26" | jq '.price'
```

### 🎉 Resultado esperado:

```
🎉 ¡Actualización AUTOMÁTICA completada exitosamente!
==================================================
✅ Proyecto actualizado automáticamente a la última versión
✅ Dependencias actualizadas automáticamente
✅ Migraciones aplicadas automáticamente
✅ Servicios reiniciados automáticamente
✅ Endpoints verificados automáticamente
✅ Backups creados y limpiados automáticamente
```

### 📊 Comandos útiles:

```bash
# Ver logs en tiempo real
sudo journalctl -u kidsfun-backend -f

# Ver estado del servicio
sudo systemctl status kidsfun-backend

# Health check
curl https://api.kidsfunyfiestasinfantiles.com/health

# Security info
curl https://api.kidsfunyfiestasinfantiles.com/security-info
```

## 🎪 Uso

### Iniciar el Servidor
```bash
# Desarrollo
uvicorn main:app --reload

# Producción
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Acceder a la Documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales
- **Health Check**: `GET /health`
- **Productos**: `GET /api/products/`
- **Usuarios**: `GET /api/users/`
- **Autenticación**: `POST /api/auth/login`

## 📚 API Documentation

### Documentación Completa
- **[API Documentation](API_DOCUMENTATION.md)** - Guía completa de endpoints
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Guía técnica para desarrolladores

### Endpoints Principales
- **Productos**: Gestión completa de productos con imágenes
- **Usuarios**: Sistema de usuarios y autenticación
- **Comentarios**: Sistema social de comentarios
- **Likes**: Sistema de favoritos
- **Eventos**: Gestión de eventos
- **Waivers**: Sistema de permisos con QR
- **Chat**: Sistema de chat en tiempo real

## 🧪 Testing

### Tests Automáticos
```bash
# Ejecutar todos los tests
python -m pytest

# Tests específicos
python test_all_apis_smart.py
python test_all_apis_with_data.py
python test_security.py
```

### Verificación Manual
```bash
# Health check
curl https://api.kidsfunyfiestasinfantiles.com/health

# Verificar productos
curl https://api.kidsfunyfiestasinfantiles.com/api/products/

# Verificar seguridad
curl https://api.kidsfunyfiestasinfantiles.com/security-info
```

## 📁 Estructura del Proyecto

```
kidsfun_back/
├── app/                    # Aplicación principal
│   ├── models/            # Modelos SQLAlchemy
│   │   ├── product.py     # Modelo de productos
│   │   ├── user.py        # Modelo de usuarios
│   │   ├── commentary.py  # Modelo de comentarios
│   │   ├── like.py        # Modelo de likes
│   │   ├── event.py       # Modelo de eventos
│   │   ├── waiver.py      # Modelo de waivers
│   │   └── chat.py        # Modelo de chat
│   ├── routers/           # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── auth.py        # Autenticación
│   │   ├── products.py    # Productos
│   │   ├── users.py       # Usuarios
│   │   ├── commentaries.py # Comentarios
│   │   ├── likes.py       # Likes
│   │   ├── events.py      # Eventos
│   │   ├── waiver.py      # Waivers
│   │   └── chat.py        # Chat
│   ├── schemas/           # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── product.py     # Esquemas de productos
│   │   ├── user.py        # Esquemas de usuarios
│   │   ├── commentary.py  # Esquemas de comentarios
│   │   ├── like.py        # Esquemas de likes
│   │   ├── event.py       # Esquemas de eventos
│   │   ├── waiver.py      # Esquemas de waivers
│   │   └── chat.py        # Esquemas de chat
│   ├── utils/             # Utilidades
│   │   ├── __init__.py
│   │   ├── email.py       # Envío de emails
│   │   └── pdf.py         # Generación de PDFs
│   ├── __init__.py
│   ├── config.py          # Configuración
│   └── database.py        # Conexión a base de datos
├── logs/                  # Logs de la aplicación
├── alembic.ini           # Configuración de Alembic
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
├── API_DOCUMENTATION.md  # Documentación de la API
├── DEVELOPER_GUIDE.md    # Guía para desarrolladores
├── test_all_apis_smart.py # Tests inteligentes
├── test_all_apis_with_data.py # Tests con datos reales
└── README.md             # Este archivo
```

## 📊 Estado Actual del Sistema

### ✅ APIs Funcionando (100%)
- **Productos**: 41 productos cargados y funcionando
- **Comentarios**: 2 comentarios cargados
- **Eventos**: Sistema listo (0 eventos actualmente)
- **Usuarios**: Sistema protegido y funcional
- **Likes**: Sistema protegido y funcional
- **Waivers**: Sistema protegido y funcional
- **Chat**: Sistema protegido y funcional

### 🔧 Características Implementadas
- ✅ Autenticación JWT completa
- ✅ Rate limiting (10 req/seg)
- ✅ CORS configurado
- ✅ Validación de datos
- ✅ Manejo de errores
- ✅ Logs detallados
- ✅ Health checks
- ✅ Documentación interactiva

## 🤝 Contribución

### Cómo Contribuir
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código
- Usar **Black** para formateo de código
- Seguir **PEP 8** para estilo de código
- Documentar todas las funciones
- Escribir tests para nuevas funcionalidades

### Reportar Bugs
- Usar el sistema de Issues de GitHub
- Incluir pasos para reproducir el bug
- Adjuntar logs si es posible
- Especificar versión del sistema

## 📞 Soporte

### Contacto
- **Email**: soporte@kidsfunyfiestasinfantiles.com
- **Documentación**: https://api.kidsfunyfiestasinfantiles.com/docs
- **Issues**: https://github.com/mrgomezsv/kidsfun_back/issues

### Recursos Útiles
- **[API Documentation](API_DOCUMENTATION.md)** - Guía completa
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Guía técnica
- **[Health Check](https://api.kidsfunyfiestasinfantiles.com/health)** - Estado del sistema

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **FastAPI** por el excelente framework
- **SQLAlchemy** por el ORM robusto
- **PostgreSQL** por la base de datos confiable
- **Comunidad de Python** por las herramientas de calidad

---

**¡Gracias por usar KidsFun Backend API! 🎉**

*Última actualización: Agosto 2025*
*Versión: 1.0.0* 