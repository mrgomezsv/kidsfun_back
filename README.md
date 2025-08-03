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
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🚀 Uso

### Desarrollo Local
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor de desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
# Usar Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Con Docker (opcional)
```bash
# Construir imagen
docker build -t kidsfun-backend .

# Ejecutar contenedor
docker run -p 8000:8000 kidsfun-backend
```

## 📚 API Documentation

### Documentación Interactiva
- **Swagger UI**: https://api.kidsfunyfiestasinfantiles.com/docs
- **ReDoc**: https://api.kidsfunyfiestasinfantiles.com/redoc

### Documentación Completa
- **[API Documentation](API_DOCUMENTATION.md)** - Guía completa para consumir las APIs
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Guía técnica para desarrolladores

### Endpoints Principales

#### Públicos
- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /security-info` - Información de seguridad
- `GET /api/products/` - Listar productos
- `GET /api/products/{id}` - Obtener producto específico
- `GET /api/commentaries/` - Listar comentarios
- `GET /api/events/` - Listar eventos

#### Protegidos (Requieren Autenticación)
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Registro
- `POST /api/products/` - Crear producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto
- `POST /api/commentaries/` - Crear comentario
- `GET /api/likes/` - Listar likes
- `POST /api/likes/` - Crear like
- `GET /api/users/` - Listar usuarios
- `GET /api/waiver/` - Listar waivers
- `POST /api/waiver/` - Crear waiver
- `GET /api/chat/` - Listar salas de chat

## 🧪 Testing

### Tests Automatizados
```bash
# Ejecutar todos los tests
python -m pytest

# Tests con coverage
python -m pytest --cov=app

# Tests específicos
python -m pytest tests/test_products.py
```

### Tests Manuales
```bash
# Test de todas las APIs
python test_all_apis_smart.py

# Obtener datos reales de todas las APIs
python test_all_apis_with_data.py
```

### Ejemplo de Test
```python
import requests

def test_get_products():
    response = requests.get('https://api.kidsfunyfiestasinfantiles.com/api/products/')
    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0
```

## 🚀 Deployment

### Ubuntu Server (Recomendado)
```bash
# Clonar en servidor
git clone https://github.com/mrgomezsv/kidsfun_back.git /opt/kidsfun-backend

# Configurar sistema
sudo bash setup_server.sh

# Deploy automático
sudo bash deploy.sh
```

### Variables de Entorno de Producción
```bash
# .env.production
DATABASE_URL=postgresql://mrgomez:password@localhost/smap_kf
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_ORIGINS=["https://kidsfunyfiestasinfantiles.com"]
```

### Systemd Service
```ini
[Unit]
Description=KidsFun Backend API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/kidsfun-backend
Environment=PATH=/opt/kidsfun-backend/venv/bin
ExecStart=/opt/kidsfun-backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📁 Estructura del Proyecto

```
kidsfun_back/
├── alembic/                 # Migraciones de base de datos
├── app/
│   ├── models/             # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── product.py      # Modelo de productos
│   │   ├── user.py         # Modelo de usuarios
│   │   ├── commentary.py   # Modelo de comentarios
│   │   ├── like.py         # Modelo de likes
│   │   ├── event.py        # Modelo de eventos
│   │   ├── waiver.py       # Modelo de waivers
│   │   └── chat.py         # Modelo de chat
│   ├── routers/            # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── auth.py         # Autenticación
│   │   ├── products.py     # Productos
│   │   ├── users.py        # Usuarios
│   │   ├── commentaries.py # Comentarios
│   │   ├── likes.py        # Likes
│   │   ├── events.py       # Eventos
│   │   ├── waiver.py       # Waivers
│   │   └── chat.py         # Chat
│   ├── schemas/            # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── product.py      # Esquemas de productos
│   │   ├── user.py         # Esquemas de usuarios
│   │   ├── commentary.py   # Esquemas de comentarios
│   │   ├── like.py         # Esquemas de likes
│   │   ├── event.py        # Esquemas de eventos
│   │   ├── waiver.py       # Esquemas de waivers
│   │   └── chat.py         # Esquemas de chat
│   ├── utils/              # Utilidades
│   │   ├── __init__.py
│   │   ├── email.py        # Envío de emails
│   │   └── pdf.py          # Generación de PDFs
│   ├── __init__.py
│   ├── config.py           # Configuración
│   └── database.py         # Conexión a base de datos
├── logs/                   # Logs de la aplicación
├── alembic.ini            # Configuración de Alembic
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
├── API_DOCUMENTATION.md   # Documentación de la API
├── DEVELOPER_GUIDE.md     # Guía para desarrolladores
├── test_all_apis_smart.py # Tests inteligentes
├── test_all_apis_with_data.py # Tests con datos reales
└── README.md              # Este archivo
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