# KidsFun Backend API

Backend API para el sistema de gestión de KidsFun construido con FastAPI.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos principal
- **JWT**: Autenticación con tokens JWT
- **Pydantic**: Validación de datos y serialización
- **CORS**: Soporte para Cross-Origin Resource Sharing
- **File Upload**: Subida de archivos e imágenes

## 📋 Requisitos

- Python 3.8+
- PostgreSQL
- pip

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
cd kidsfun_back
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

5. **Configurar base de datos**
```bash
# Asegúrate de que PostgreSQL esté corriendo
# Las tablas se crearán automáticamente al ejecutar la aplicación
```

## 🚀 Ejecutar

```bash
# Desarrollo
uvicorn main:app --reload

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentación API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrarse
- `GET /api/auth/me` - Obtener usuario actual

### Productos
- `GET /api/products/` - Listar productos
- `GET /api/products/{id}` - Obtener producto
- `POST /api/products/` - Crear producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto
- `POST /api/products/{id}/upload-image` - Subir imagen

### Likes
- `GET /api/likes/` - Listar likes
- `POST /api/likes/` - Crear/actualizar like
- `DELETE /api/likes/{id}` - Eliminar like

### Comentarios
- `GET /api/commentaries/` - Listar comentarios
- `POST /api/commentaries/` - Crear comentario
- `DELETE /api/commentaries/{id}` - Eliminar comentario

### Eventos
- `GET /api/events/` - Listar eventos
- `GET /api/events/{id}` - Obtener evento
- `POST /api/events/` - Crear evento
- `PUT /api/events/{id}` - Actualizar evento
- `DELETE /api/events/{id}` - Eliminar evento

### Waivers (NUEVO)
- `POST /api/waiver/` - Crear waiver con QR
- `POST /api/waiver/validate` - Validar waiver por QR
- `GET /api/waiver/{qr_code}` - Obtener datos del waiver
- `GET /api/waiver/user/{user_id}` - Obtener waivers del usuario
- `POST /api/waiver/admin/validator` - Crear validador (admin)

### Chat (NUEVO)
- `GET /api/chat/rooms` - Obtener salas de chat
- `POST /api/chat/rooms` - Crear sala de chat
- `GET /api/chat/rooms/{room_id}/messages` - Obtener mensajes
- `POST /api/chat/rooms/{room_id}/messages` - Enviar mensaje
- `POST /api/chat/admin/administrators` - Crear administrador
- `GET /api/chat/admin/administrators` - Listar administradores
- `PUT /api/chat/admin/administrators/{admin_id}/toggle` - Activar/desactivar admin
- `WS /api/chat/ws/{chat_id}` - WebSocket para chat en tiempo real

## 🗄️ Base de Datos

El backend se conecta a la base de datos PostgreSQL existente del proyecto Django. Los modelos están mapeados a las tablas existentes:

- `auth_user` - Usuarios
- `t_app_product` - Productos
- `t_app_like` - Likes
- `t_app_commentary` - Comentarios
- `t_app_event` - Eventos
- `t_app_chat_*` - Chat y mensajes
- `t_app_product_waiver*` - Datos de waiver

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens) para autenticación:

1. **Login**: `POST /api/auth/login` con username y password
2. **Token**: Se recibe un access_token
3. **Autorización**: Incluir `Authorization: Bearer <token>` en headers

## 📁 Estructura del Proyecto

```
kidsfun_back/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuración
│   ├── database.py        # Configuración de BD
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic
│   └── routers/           # Endpoints de la API
├── main.py               # Aplicación principal
├── requirements.txt      # Dependencias
├── env.example          # Variables de entorno
└── README.md           # Este archivo
```

## 🚀 Despliegue

### Despliegue Automático (Recomendado)

Para desplegar automáticamente en producción:

```bash
# Ejecutar script de despliegue
./deploy.sh
```

Este script:
- ✅ Verifica dependencias
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Verifica conexión a BD
- ✅ Ejecuta migraciones
- ✅ Verifica configuración de email
- ✅ Crea scripts de servicio
- ✅ Configura Gunicorn

### Despliegue Manual

Si prefieres desplegar manualmente:

1. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

2. **Instalar dependencias**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
alembic upgrade head
```

4. **Ejecutar con Gunicorn**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Gestión del Servicio

Una vez desplegado, puedes gestionar el servicio con:

```bash
# Iniciar servicio
./start_service.sh

# Parar servicio
./stop_service.sh

# Reiniciar servicio
./restart_service.sh

# Ver estado
./status_service.sh
```

### Instalación como Servicio del Sistema

Para que el backend se inicie automáticamente:

```bash
# Copiar archivo de servicio
sudo cp kidsfun-backend.service /etc/systemd/system/

# Recargar configuración
sudo systemctl daemon-reload

# Habilitar servicio
sudo systemctl enable kidsfun-backend

# Iniciar servicio
sudo systemctl start kidsfun-backend

# Verificar estado
sudo systemctl status kidsfun-backend
```

## 🔧 Desarrollo

Para desarrollo local:

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🆕 Nuevas Funcionalidades

### Sistema de Waivers
- ✅ Creación de waivers con QR codes únicos
- ✅ Validación de waivers por QR
- ✅ Generación automática de PDFs
- ✅ Envío de emails con PDFs adjuntos
- ✅ Gestión de familiares por waiver
- ✅ Expiración automática (24 horas)

### Sistema de Chat
- ✅ Salas de chat por usuario
- ✅ Mensajería en tiempo real con WebSockets
- ✅ Gestión de administradores de chat
- ✅ Historial de mensajes
- ✅ Notificaciones automáticas

### Migraciones de Base de Datos
- ✅ Alembic configurado para migraciones
- ✅ Scripts automáticos de migración
- ✅ Compatibilidad con base de datos existente

### Configuración de Producción
- ✅ Script de despliegue automático
- ✅ Configuración de Gunicorn optimizada
- ✅ Scripts de gestión de servicio
- ✅ Configuración de systemd
- ✅ Logging y monitoreo 