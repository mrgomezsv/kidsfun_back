# KidsFun Backend - Node.js/Express

Backend API para el sistema de gestión de KidsFun construido con Node.js, Express y PostgreSQL.

## 🚀 Características

- **Framework**: Express.js
- **Base de datos**: PostgreSQL con Sequelize ORM
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación**: Express-validator
- **Seguridad**: Helmet, CORS, Rate limiting
- **Archivos**: Multer para upload de imágenes
- **Logging**: Morgan y Winston
- **Compresión**: Gzip compression

## 📋 Requisitos

- Node.js >= 18.0.0
- PostgreSQL >= 12.0
- npm o yarn

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
cd kidsfun_back
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

4. **Configurar la base de datos**
```bash
# Crear base de datos PostgreSQL
createdb kidsfun

# Ejecutar migraciones
npm run migrate
```

5. **Iniciar el servidor**
```bash
# Desarrollo
npm run dev

# Producción
npm start
```

## 🔧 Configuración

### Variables de entorno (.env)

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/kidsfun

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
PORT=8000
HOST=0.0.0.0
NODE_ENV=development

# File Upload Configuration
UPLOAD_DIR=media
MAX_FILE_SIZE=10485760

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SECURE=false
```

## 📚 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrarse
- `GET /api/auth/me` - Obtener usuario actual
- `POST /api/auth/refresh` - Refrescar token

### Usuarios
- `GET /api/users` - Obtener todos los usuarios (admin)
- `GET /api/users/:id` - Obtener usuario por ID
- `PUT /api/users/:id` - Actualizar perfil
- `PUT /api/users/:id/password` - Cambiar contraseña
- `PUT /api/users/:id/status` - Actualizar estado (admin)

### Productos
- `GET /api/products` - Obtener productos
- `GET /api/products/:id` - Obtener producto por ID
- `POST /api/products` - Crear producto
- `PUT /api/products/:id` - Actualizar producto
- `DELETE /api/products/:id` - Eliminar producto

### Likes
- `GET /api/likes/product/:productId` - Obtener likes de un producto
- `GET /api/likes/user/:userId` - Obtener likes de un usuario
- `POST /api/likes/toggle/:productId` - Toggle like
- `GET /api/likes/check/:productId` - Verificar si usuario dio like
- `GET /api/likes/count/:productId` - Contar likes de un producto

### Comentarios
- `GET /api/commentaries/product/:productId` - Obtener comentarios de un producto
- `GET /api/commentaries/user/:userId` - Obtener comentarios de un usuario
- `POST /api/commentaries` - Crear comentario
- `PUT /api/commentaries/:id` - Actualizar comentario
- `DELETE /api/commentaries/:id` - Eliminar comentario
- `GET /api/commentaries/:id` - Obtener comentario por ID

### Otros
- `GET /health` - Health check
- `GET /security-info` - Información de seguridad

## 🗄️ Estructura de la Base de Datos

### Tablas principales

1. **auth_user** - Usuarios del sistema
2. **t_app_product_product** - Productos
3. **commentaries** - Comentarios
4. **likes** - Likes de productos

## 🔒 Seguridad

- **Rate limiting**: 10 requests por segundo por IP
- **CORS**: Configurado para dominios específicos
- **Helmet**: Headers de seguridad
- **JWT**: Autenticación con tokens
- **Validación**: Input validation con express-validator
- **File upload**: Validación de tipos y tamaños

## 🚀 Despliegue

### Producción

1. **Configurar variables de producción**
```bash
NODE_ENV=production
DATABASE_URL=your-production-db-url
SECRET_KEY=your-production-secret-key
```

2. **Instalar dependencias de producción**
```bash
npm ci --only=production
```

3. **Ejecutar migraciones**
```bash
npm run migrate
```

4. **Iniciar servidor**
```bash
npm start
```

### Con PM2

```bash
# Instalar PM2
npm install -g pm2

# Iniciar aplicación
pm2 start server.js --name kidsfun-backend

# Configurar para iniciar con el sistema
pm2 startup
pm2 save
```

### Con Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 8000

CMD ["npm", "start"]
```

## 📝 Scripts Disponibles

- `npm start` - Iniciar servidor en producción
- `npm run dev` - Iniciar servidor en desarrollo con nodemon
- `npm run migrate` - Ejecutar migraciones de base de datos
- `npm run seed` - Poblar base de datos con datos de ejemplo
- `npm test` - Ejecutar tests

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Para soporte, email support@kidsfun.com o crear un issue en el repositorio. 
