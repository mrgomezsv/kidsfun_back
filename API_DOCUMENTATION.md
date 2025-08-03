# 🎪 KidsFun API Documentation

## 📋 Índice
- [Información General](#información-general)
- [Autenticación](#autenticación)
- [Endpoints Públicos](#endpoints-públicos)
- [API de Productos](#api-de-productos)
- [API de Comentarios](#api-de-comentarios)
- [API de Eventos](#api-de-eventos)
- [API de Usuarios](#api-de-usuarios)
- [API de Likes](#api-de-likes)
- [API de Waivers](#api-de-waivers)
- [API de Chat](#api-de-chat)
- [Códigos de Error](#códigos-de-error)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🌐 Información General

### Base URL
```
https://api.kidsfunyfiestasinfantiles.com
```

### Versión
```
v1.0.0
```

### Formato de Respuesta
Todas las respuestas están en formato JSON con la siguiente estructura:
```json
{
  "data": "contenido de la respuesta",
  "message": "mensaje descriptivo (opcional)",
  "status": "success/error"
}
```

### Rate Limiting
- **Límite**: 10 requests por segundo por IP
- **Ventana**: 1 segundo
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite de requests
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Tiempo de reset

### Seguridad
- **SSL Required**: Todas las requests deben usar HTTPS
- **CORS**: Configurado para dominios específicos
- **Headers de Seguridad**: HSTS, CSP, X-Frame-Options

---

## 🔐 Autenticación

### JWT Token
La mayoría de endpoints requieren autenticación mediante JWT tokens.

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

#### Respuesta Exitosa
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "username": "usuario",
    "is_superuser": false
  }
}
```

#### Uso del Token
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📡 Endpoints Públicos

### 1. Información de la API
```http
GET /
```

**Respuesta:**
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

### 2. Health Check
```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy"
}
```

### 3. Información de Seguridad
```http
GET /security-info
```

**Respuesta:**
```json
{
  "security_features": {
    "rate_limiting": "10 requests per second per IP",
    "input_validation": "XSS and SQL injection protection",
    "cors": "Configured for specific domains",
    "trusted_hosts": "Only allowed hosts accepted",
    "security_headers": "HSTS, CSP, X-Frame-Options, etc.",
    "ssl_required": true,
    "jwt_authentication": true,
    "request_logging": true
  },
  "rate_limits": {
    "requests_per_second": 10,
    "window_size": "1 second",
    "storage": "In-memory (Redis recommended for production)"
  },
  "allowed_origins": [
    "http://localhost:4200",
    "https://kidsfunyfiestasinfantiles.com",
    "https://www.kidsfunyfiestasinfantiles.com",
    "https://api.kidsfunyfiestasinfantiles.com"
  ],
  "max_file_size": "10485760 bytes"
}
```

---

## 🎪 API de Productos

### Obtener Todos los Productos
```http
GET /api/products/
```

**Parámetros de Query:**
- `skip` (int, opcional): Número de productos a saltar (default: 0)
- `limit` (int, opcional): Número máximo de productos (default: 100, max: 100)
- `category` (string, opcional): Filtrar por categoría
- `search` (string, opcional): Buscar en título
- `publicated` (boolean, opcional): Filtrar por estado de publicación

**Ejemplo:**
```http
GET /api/products/?category=option1&search=bounce&limit=10
```

**Respuesta:**
```json
[
  {
    "id": 26,
    "title": "Red Mechanical Bull",
    "description": "Saddle up for a rip-roaring good time...",
    "price": "1.00",
    "category": "option2",
    "youtube_url": "https://youtube.com/shorts/_JdBZDHso5w?si=4xaiz0j3ExjEQt5p",
    "dimensions": "15x15x10ft",
    "circuits": null,
    "space": null,
    "img": "product_images/img_5_oO5U4ei.jpg",
    "img1": "product_images/img_3_sPgiwc8.jpg",
    "img2": "product_images/img_4_CKNILV9.jpg",
    "img3": "product_images/img_6_QXL70AZ.jpg",
    "img4": "product_images/img_8.jpg",
    "img5": "product_images/img_10.jpg",
    "created": "2024-07-23T08:17:17.250941Z",
    "publicated": true,
    "user_id": 1,
    "likes_count": 2,
    "comments_count": 0
  }
]
```

### Obtener Producto Específico
```http
GET /api/products/{product_id}
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Barbie Bounce House",
  "description": "",
  "price": "1.00",
  "category": "option1",
  "youtube_url": null,
  "dimensions": "17x30ft",
  "circuits": null,
  "space": null,
  "img": "product_images/img_1.png",
  "img1": "product_images/img_2.jpeg",
  "img2": "product_images/img_1.jpeg",
  "img3": "product_images/img_1.jpg",
  "img4": "product_images/img_2_7GtFMyp.jpeg",
  "img5": "product_images/img_1_9azbb0J.jpeg",
  "created": "2024-07-23T07:43:55.052351Z",
  "publicated": true,
  "user_id": 1,
  "likes_count": 5,
  "comments_count": 1
}
```

### Crear Producto (Requiere Autenticación)
```http
POST /api/products/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Nuevo Producto",
  "description": "Descripción del producto",
  "price": "150.00",
  "category": "option1",
  "youtube_url": "https://youtube.com/watch?v=example",
  "dimensions": "10x10ft",
  "circuits": "2",
  "space": "100sqft"
}
```

### Actualizar Producto (Requiere Autenticación)
```http
PUT /api/products/{product_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Producto Actualizado",
  "price": "200.00",
  "publicated": true
}
```

### Eliminar Producto (Requiere Autenticación)
```http
DELETE /api/products/{product_id}
Authorization: Bearer {token}
```

---

## 💬 API de Comentarios

### Obtener Todos los Comentarios
```http
GET /api/commentaries/
```

**Parámetros de Query:**
- `product_id` (int, opcional): Filtrar por producto

**Ejemplo:**
```http
GET /api/commentaries/?product_id=1
```

**Respuesta:**
```json
[
  {
    "id": 2,
    "comment": "test",
    "user_id": "VfTnuhyZd7PxO8VxkXPftqyEPtk1",
    "product_id": 1
  },
  {
    "id": 3,
    "comment": "❤️❤️❤️❤️",
    "user_id": "NMHm52GuM0QD4Q5OZtjl8JOCmAQ2",
    "product_id": 9
  }
]
```

### Crear Comentario (Requiere Autenticación)
```http
POST /api/commentaries/
Authorization: Bearer {token}
Content-Type: application/json

{
  "comment": "¡Excelente producto!",
  "user_id": "user123",
  "product_id": 1
}
```

### Actualizar Comentario (Requiere Autenticación)
```http
PUT /api/commentaries/{comment_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "comment": "Comentario actualizado"
}
```

### Eliminar Comentario (Requiere Autenticación)
```http
DELETE /api/commentaries/{comment_id}
Authorization: Bearer {token}
```

---

## 📅 API de Eventos

### Obtener Todos los Eventos
```http
GET /api/events/
```

**Respuesta:**
```json
[]
```

### Crear Evento (Requiere Autenticación)
```http
POST /api/events/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Fiesta de Cumpleaños",
  "description": "Evento de cumpleaños infantil",
  "date": "2024-12-25T15:00:00Z",
  "location": "Parque Central"
}
```

### Actualizar Evento (Requiere Autenticación)
```http
PUT /api/events/{event_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Fiesta Actualizada"
}
```

### Eliminar Evento (Requiere Autenticación)
```http
DELETE /api/events/{event_id}
Authorization: Bearer {token}
```

---

## 👥 API de Usuarios

### Obtener Todos los Usuarios (Requiere Autenticación - Solo Admin)
```http
GET /api/users/
Authorization: Bearer {token}
```

### Obtener Usuario Específico (Requiere Autenticación)
```http
GET /api/users/{user_id}
Authorization: Bearer {token}
```

### Actualizar Usuario (Requiere Autenticación)
```http
PUT /api/users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "nuevo@email.com"
}
```

### Eliminar Usuario (Requiere Autenticación - Solo Admin)
```http
DELETE /api/users/{user_id}
Authorization: Bearer {token}
```

---

## ❤️ API de Likes

### Obtener Todos los Likes (Requiere Autenticación)
```http
GET /api/likes/
Authorization: Bearer {token}
```

**Parámetros de Query:**
- `product_id` (int, opcional): Filtrar por producto
- `user_id` (string, opcional): Filtrar por usuario

### Crear/Actualizar Like (Requiere Autenticación)
```http
POST /api/likes/
Authorization: Bearer {token}
Content-Type: application/json

{
  "user": "user123",
  "product": "26",
  "is_favorite": true
}
```

### Eliminar Like (Requiere Autenticación)
```http
DELETE /api/likes/{like_id}
Authorization: Bearer {token}
```

---

## 📋 API de Waivers

### Obtener Waivers del Usuario (Requiere Autenticación)
```http
GET /api/waiver/
Authorization: Bearer {token}
```

### Crear Waiver (Requiere Autenticación)
```http
POST /api/waiver/
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": "user123",
  "user_name": "Juan Pérez",
  "user_email": "juan@ejemplo.com",
  "relatives": [
    {
      "name": "María Pérez",
      "age": 8
    },
    {
      "name": "Carlos Pérez",
      "age": 12
    }
  ]
}
```

### Obtener Waiver por QR (Requiere Autenticación)
```http
GET /api/waiver/{qr_code}
Authorization: Bearer {token}
```

---

## 💬 API de Chat

### Obtener Salas de Chat (Requiere Autenticación)
```http
GET /api/chat/
Authorization: Bearer {token}
```

### Crear Sala de Chat (Requiere Autenticación)
```http
POST /api/chat/
Authorization: Bearer {token}
```

### Obtener Sala Específica (Requiere Autenticación)
```http
GET /api/chat/{room_id}
Authorization: Bearer {token}
```

### Obtener Mensajes de una Sala (Requiere Autenticación)
```http
GET /api/chat/rooms/{room_id}/messages
Authorization: Bearer {token}
```

### Enviar Mensaje (Requiere Autenticación)
```http
POST /api/chat/rooms/{room_id}/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Hola, necesito información sobre sus productos"
}
```

---

## 🚨 Códigos de Error

### Códigos HTTP Comunes

| Código | Descripción |
|--------|-------------|
| 200 | OK - Request exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Autenticación requerida |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Error de validación |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error - Error del servidor |

### Ejemplos de Respuestas de Error

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

#### 429 Rate Limit
```json
{
  "detail": "Rate limit exceeded"
}
```

---

## 💡 Ejemplos de Uso

### JavaScript (Fetch API)

#### Obtener Productos
```javascript
async function getProducts() {
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/products/');
    const products = await response.json();
    console.log('Productos:', products);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### Login y Obtener Token
```javascript
async function login(email, password) {
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
  } catch (error) {
    console.error('Error de login:', error);
  }
}
```

#### Crear Producto con Autenticación
```javascript
async function createProduct(productData) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(productData)
    });
    
    const product = await response.json();
    console.log('Producto creado:', product);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Python (Requests)

#### Obtener Productos
```python
import requests

def get_products():
    url = "https://api.kidsfunyfiestasinfantiles.com/api/products/"
    response = requests.get(url)
    
    if response.status_code == 200:
        products = response.json()
        print(f"Productos obtenidos: {len(products)}")
        return products
    else:
        print(f"Error: {response.status_code}")
        return None
```

#### Login
```python
import requests

def login(email, password):
    url = "https://api.kidsfunyfiestasinfantiles.com/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Error de login: {response.status_code}")
        return None
```

#### Crear Producto
```python
import requests

def create_product(token, product_data):
    url = "https://api.kidsfunyfiestasinfantiles.com/api/products/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=product_data, headers=headers)
    
    if response.status_code == 200:
        product = response.json()
        print("Producto creado exitosamente")
        return product
    else:
        print(f"Error: {response.status_code}")
        return None
```

### cURL

#### Obtener Productos
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/" \
  -H "Content-Type: application/json"
```

#### Login
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
  }'
```

#### Crear Producto
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Nuevo Producto",
    "description": "Descripción del producto",
    "price": "150.00",
    "category": "option1"
  }'
```

---

## 📞 Soporte

Para soporte técnico o preguntas sobre la API, contacta a:
- **Email**: soporte@kidsfunyfiestasinfantiles.com
- **Documentación Interactiva**: https://api.kidsfunyfiestasinfantiles.com/docs

---

## 📝 Notas Importantes

1. **Siempre usa HTTPS** - Las requests HTTP no están permitidas
2. **Respeta el Rate Limiting** - Máximo 10 requests por segundo
3. **Maneja los errores** - Siempre verifica los códigos de estado HTTP
4. **Guarda el token** - El token JWT expira, renóvalo cuando sea necesario
5. **Valida los datos** - Asegúrate de que los datos enviados sean válidos

---

*Última actualización: Agosto 2025*
*Versión de la API: 1.0.0* 