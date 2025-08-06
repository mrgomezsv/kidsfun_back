# 🎪 KidsFun API Documentation

## 📋 Índice
- [Información General](#información-general)
- [Autenticación](#autenticación)
- [Endpoints Públicos](#endpoints-públicos)
- [🎪 API de Productos e Imágenes](#-api-de-productos-e-imágenes)
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

## 🎪 API de Productos e Imágenes

### 📋 Información General

La API de productos permite obtener información completa de todos los productos de KidsFun, incluyendo:
- **Datos del producto**: título, descripción, precio, categoría, dimensiones
- **Imágenes**: hasta 6 imágenes por producto (img, img1, img2, img3, img4, img5)
- **Metadatos**: fecha de creación, estado de publicación, conteos de likes y comentarios
- **URLs de YouTube**: videos relacionados con el producto

### 🖼️ Sistema de Imágenes

#### Estructura de URLs de Imágenes
```
https://api.kidsfunyfiestasinfantiles.com/media/{ruta_imagen}
```

**Ejemplos:**
- Imagen principal: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_5_oO5U4ei.jpg`
- Imagen adicional 1: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_3_sPgiwc8.jpg`
- Imagen adicional 2: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_4_CKNILV9.jpg`

#### Campos de Imágenes por Producto
- `img`: Imagen principal del producto
- `img1`: Imagen adicional 1
- `img2`: Imagen adicional 2
- `img3`: Imagen adicional 3
- `img4`: Imagen adicional 4
- `img5`: Imagen adicional 5

### 🚀 Endpoints de Productos

#### 1. Obtener Todos los Productos
```http
GET /api/products/
```

**Parámetros de Query:**
- `skip` (int, opcional): Número de productos a saltar (default: 0)
- `limit` (int, opcional): Número máximo de productos (default: 100, max: 100)
- `category` (string, opcional): Filtrar por categoría (option1, option2, etc.)
- `search` (string, opcional): Buscar en título del producto
- `publicated` (boolean, opcional): Filtrar por estado de publicación (true/false)

**Ejemplos de uso:**
```bash
# Obtener todos los productos
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/"

# Obtener primeros 10 productos
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?limit=10"

# Buscar productos con "bounce" en el título
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?search=bounce"

# Filtrar por categoría
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=option1"

# Combinar filtros
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=option1&search=bounce&limit=5"
```

**Respuesta:**
```json
[
  {
    "id": 26,
    "title": "Red Mechanical Bull",
    "description": "Saddle up for a rip-roaring good time with our mechanical bulls, the ultimate crowd-pleaser that'll turn your event into a memorable bull-riding hoedown with our mechanical bull rentals!",
    "price": 1.00,
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
  },
  {
    "id": 4,
    "title": "Big Bounce House",
    "description": "A huge bounce house perfect for big parties",
    "price": 1.00,
    "category": "option1",
    "youtube_url": null,
    "dimensions": "30X30ft",
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
]
```

#### 2. Obtener Producto Específico
```http
GET /api/products/{product_id}
```

**Ejemplo:**
```bash
# Obtener producto con ID 26
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/26"
```

**Respuesta:**
```json
{
  "id": 26,
  "title": "Red Mechanical Bull",
  "description": "Saddle up for a rip-roaring good time with our mechanical bulls, the ultimate crowd-pleaser that'll turn your event into a memorable bull-riding hoedown with our mechanical bull rentals!",
  "price": 1.00,
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
```

### 🖼️ Cómo Acceder a las Imágenes

#### URLs Completas de Imágenes
Para obtener las URLs completas de las imágenes, simplemente concatena la base URL con la ruta de la imagen:

```javascript
const baseUrl = "https://api.kidsfunyfiestasinfantiles.com/media/";
const product = {
  "img": "product_images/img_5_oO5U4ei.jpg",
  "img1": "product_images/img_3_sPgiwc8.jpg",
  "img2": "product_images/img_4_CKNILV9.jpg"
};

// URLs completas
const imageUrls = {
  main: baseUrl + product.img,
  additional1: baseUrl + product.img1,
  additional2: baseUrl + product.img2
};
```

#### Ejemplos de URLs de Imágenes
```
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_5_oO5U4ei.jpg
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_3_sPgiwc8.jpg
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_4_CKNILV9.jpg
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_6_QXL70AZ.jpg
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_8.jpg
https://api.kidsfunyfiestasinfantiles.com/media/product_images/img_10.jpg
```

### 💡 Ejemplos de Implementación

#### JavaScript (Fetch API)
```javascript
// Obtener todos los productos
async function getProducts() {
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/products/');
    const products = await response.json();
    
    // Procesar productos y sus imágenes
    products.forEach(product => {
      console.log(`Producto: ${product.title}`);
      console.log(`Precio: $${product.price}`);
      console.log(`Imagen principal: https://api.kidsfunyfiestasinfantiles.com/media/${product.img}`);
      
      // Mostrar todas las imágenes
      const images = [product.img, product.img1, product.img2, product.img3, product.img4, product.img5];
      images.forEach((img, index) => {
        if (img) {
          console.log(`Imagen ${index + 1}: https://api.kidsfunyfiestasinfantiles.com/media/${img}`);
        }
      });
    });
    
    return products;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Obtener producto específico
async function getProduct(productId) {
  try {
    const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/products/${productId}`);
    const product = await response.json();
    
    // Crear URLs completas de imágenes
    const imageUrls = {
      main: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img}`,
      additional1: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img1}`,
      additional2: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img2}`,
      additional3: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img3}`,
      additional4: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img4}`,
      additional5: `https://api.kidsfunyfiestasinfantiles.com/media/${product.img5}`
    };
    
    return { ...product, imageUrls };
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### Python (requests)
```python
import requests
import json

def get_products():
    """Obtener todos los productos"""
    url = "https://api.kidsfunyfiestasinfantiles.com/api/products/"
    response = requests.get(url)
    
    if response.status_code == 200:
        products = response.json()
        
        # Procesar productos y sus imágenes
        for product in products:
            print(f"Producto: {product['title']}")
            print(f"Precio: ${product['price']}")
            print(f"Imagen principal: https://api.kidsfunyfiestasinfantiles.com/media/{product['img']}")
            
            # Mostrar todas las imágenes
            images = [product['img'], product['img1'], product['img2'], 
                     product['img3'], product['img4'], product['img5']]
            
            for i, img in enumerate(images):
                if img:
                    print(f"Imagen {i+1}: https://api.kidsfunyfiestasinfantiles.com/media/{img}")
            
            print("-" * 50)
        
        return products
    else:
        print(f"Error: {response.status_code}")
        return None

def get_product(product_id):
    """Obtener producto específico"""
    url = f"https://api.kidsfunyfiestasinfantiles.com/api/products/{product_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        product = response.json()
        
        # Crear URLs completas de imágenes
        base_url = "https://api.kidsfunyfiestasinfantiles.com/media/"
        image_urls = {
            'main': base_url + product['img'],
            'additional1': base_url + product['img1'],
            'additional2': base_url + product['img2'],
            'additional3': base_url + product['img3'],
            'additional4': base_url + product['img4'],
            'additional5': base_url + product['img5']
        }
        
        product['image_urls'] = image_urls
        return product
    else:
        print(f"Error: {response.status_code}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Obtener todos los productos
    products = get_products()
    
    # Obtener producto específico
    product = get_product(26)
    if product:
        print(json.dumps(product, indent=2))
```

#### cURL
```bash
# Obtener todos los productos
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/" | jq '.[0:3]'

# Obtener producto específico
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/26" | jq '.'

# Obtener solo las imágenes de un producto
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/26" | jq '.img, .img1, .img2, .img3, .img4, .img5'

# Buscar productos con "bounce" en el título
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/?search=bounce" | jq '.[].title'
```

### 🎯 Casos de Uso Comunes

#### 1. Mostrar Galería de Productos
```javascript
async function displayProductGallery() {
  const products = await getProducts();
  const gallery = document.getElementById('product-gallery');
  
  products.forEach(product => {
    const productCard = document.createElement('div');
    productCard.className = 'product-card';
    
    // Imagen principal
    const mainImage = document.createElement('img');
    mainImage.src = `https://api.kidsfunyfiestasinfantiles.com/media/${product.img}`;
    mainImage.alt = product.title;
    
    // Información del producto
    const productInfo = document.createElement('div');
    productInfo.innerHTML = `
      <h3>${product.title}</h3>
      <p>${product.description}</p>
      <p>Precio: $${product.price}</p>
      <p>Categoría: ${product.category}</p>
    `;
    
    productCard.appendChild(mainImage);
    productCard.appendChild(productInfo);
    gallery.appendChild(productCard);
  });
}
```

#### 2. Mostrar Detalle de Producto con Todas las Imágenes
```javascript
async function displayProductDetail(productId) {
  const product = await getProduct(productId);
  const detailContainer = document.getElementById('product-detail');
  
  // Imagen principal
  const mainImage = document.createElement('img');
  mainImage.src = `https://api.kidsfunyfiestasinfantiles.com/media/${product.img}`;
  mainImage.className = 'main-image';
  
  // Galería de imágenes adicionales
  const imageGallery = document.createElement('div');
  imageGallery.className = 'image-gallery';
  
  const additionalImages = [product.img1, product.img2, product.img3, product.img4, product.img5];
  additionalImages.forEach(img => {
    if (img) {
      const thumbnail = document.createElement('img');
      thumbnail.src = `https://api.kidsfunyfiestasinfantiles.com/media/${img}`;
      thumbnail.className = 'thumbnail';
      thumbnail.onclick = () => mainImage.src = thumbnail.src;
      imageGallery.appendChild(thumbnail);
    }
  });
  
  // Información del producto
  const productInfo = document.createElement('div');
  productInfo.innerHTML = `
    <h1>${product.title}</h1>
    <p>${product.description}</p>
    <p>Precio: $${product.price}</p>
    <p>Dimensiones: ${product.dimensions}</p>
    <p>Likes: ${product.likes_count}</p>
    <p>Comentarios: ${product.comments_count}</p>
  `;
  
  detailContainer.appendChild(mainImage);
  detailContainer.appendChild(imageGallery);
  detailContainer.appendChild(productInfo);
}
```

### 📊 Estructura de Datos Completa

#### Campos del Producto
```json
{
  "id": 26,                           // ID único del producto
  "title": "Red Mechanical Bull",     // Título del producto
  "description": "Descripción...",    // Descripción detallada
  "price": 1.00,                      // Precio (número decimal)
  "category": "option2",              // Categoría del producto
  "youtube_url": "https://...",       // URL de video de YouTube
  "dimensions": "15x15x10ft",         // Dimensiones del producto
  "circuits": null,                   // Número de circuitos
  "space": null,                      // Espacio requerido
  "img": "product_images/img_5_oO5U4ei.jpg",      // Imagen principal
  "img1": "product_images/img_3_sPgiwc8.jpg",     // Imagen adicional 1
  "img2": "product_images/img_4_CKNILV9.jpg",     // Imagen adicional 2
  "img3": "product_images/img_6_QXL70AZ.jpg",     // Imagen adicional 3
  "img4": "product_images/img_8.jpg",             // Imagen adicional 4
  "img5": "product_images/img_10.jpg",            // Imagen adicional 5
  "created": "2024-07-23T08:17:17.250941Z",       // Fecha de creación
  "publicated": true,                 // Estado de publicación
  "user_id": 1,                       // ID del usuario creador
  "likes_count": 2,                   // Número de likes
  "comments_count": 0                 // Número de comentarios
}
```

### 🔍 Filtros y Búsqueda

#### Categorías Disponibles
- `option1`: Categoría 1 (ej: Bounce Houses)
- `option2`: Categoría 2 (ej: Mechanical Bulls)
- `option3`: Categoría 3 (ej: Games)

#### Ejemplos de Búsqueda
```bash
# Buscar productos de categoría 1
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=option1"

# Buscar productos con "bounce" en el título
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?search=bounce"

# Obtener solo productos publicados
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?publicated=true"

# Combinar filtros
curl "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=option1&search=bounce&limit=5"
```

### 🚨 Manejo de Errores

#### Códigos de Error Comunes
- `404`: Producto no encontrado
- `429`: Rate limit excedido
- `500`: Error interno del servidor

#### Ejemplo de Manejo de Errores
```javascript
async function getProductWithErrorHandling(productId) {
  try {
    const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/products/${productId}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Producto no encontrado');
      } else if (response.status === 429) {
        throw new Error('Demasiadas requests. Intenta más tarde');
      } else {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
    }
    
    const product = await response.json();
    return product;
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}
```

---

## 🎪 API de Productos (Continuación)

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
  "description": "Nueva descripción",
  "price": "200.00"
}
```

### Eliminar Producto (Requiere Autenticación)
```http
DELETE /api/products/{product_id}
Authorization: Bearer {token}
```

### Subir Imagen de Producto (Requiere Autenticación)
```http
POST /api/products/{product_id}/upload-image
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [archivo de imagen]
```

---

## 💬 API de Comentarios

### Obtener Comentarios
```http
GET /api/commentaries/
```

### Crear Comentario (Requiere Autenticación)
```http
POST /api/commentaries/
Authorization: Bearer {token}
Content-Type: application/json

{
  "comment": "Excelente producto!",
  "product_id": 26
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

## 🎉 API de Eventos

### Obtener Eventos
```http
GET /api/events/
```

### Crear Evento (Requiere Autenticación)
```http
POST /api/events/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Fiesta de Cumpleaños",
  "description": "Fiesta temática",
  "location": "Parque Central",
  "start_datetime": "2024-12-25T15:00:00Z",
  "ticket_price": "50.00",
  "partners": "partner1"
}
```

---

## 👥 API de Usuarios

### Obtener Usuarios (Requiere Autenticación)
```http
GET /api/users/
Authorization: Bearer {token}
```

### Obtener Usuario Específico (Requiere Autenticación)
```http
GET /api/users/{user_id}
Authorization: Bearer {token}
```

### Crear Usuario
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "nuevo@usuario.com",
  "password": "contraseña123",
  "username": "nuevo_usuario",
  "first_name": "Nuevo",
  "last_name": "Usuario"
}
```

### Eliminar Usuario (Requiere Autenticación)
```http
DELETE /api/users/{user_id}
Authorization: Bearer {token}
```

---

## ❤️ API de Likes

### Obtener Likes (Requiere Autenticación)
```http
GET /api/likes/
Authorization: Bearer {token}
```

### Crear Like (Requiere Autenticación)
```http
POST /api/likes/
Authorization: Bearer {token}
Content-Type: application/json

{
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

### Obtener Waivers (Requiere Autenticación)
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
  "participant_name": "Juan Pérez",
  "participant_age": 25,
  "emergency_contact": "María Pérez",
  "emergency_phone": "123-456-7890",
  "medical_conditions": "Ninguna",
  "signature": "Juan Pérez"
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
    return data.access_token;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### Crear Producto con Token
```javascript
async function createProduct(token, productData) {
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
    return product;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Python (requests)

#### Obtener Productos
```python
import requests

def get_products():
    url = "https://api.kidsfunyfiestasinfantiles.com/api/products/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Uso
products = get_products()
if products:
    for product in products:
        print(f"Producto: {product['title']}")
        print(f"Precio: ${product['price']}")
        print(f"Imagen: https://api.kidsfunyfiestasinfantiles.com/media/{product['img']}")
        print("-" * 50)
```

#### Login y Crear Producto
```python
import requests

def login(email, password):
    url = "https://api.kidsfunyfiestasinfantiles.com/api/auth/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error: {response.status_code}")
        return None

def create_product(token, product_data):
    url = "https://api.kidsfunyfiestasinfantiles.com/api/products/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=product_data, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Uso
token = login("usuario@ejemplo.com", "contraseña123")
if token:
    product_data = {
        "title": "Nuevo Producto",
        "description": "Descripción del producto",
        "price": "150.00",
        "category": "option1"
    }
    product = create_product(token, product_data)
    if product:
        print(f"Producto creado: {product['title']}")
```

### cURL

#### Obtener Productos
```bash
curl -s "https://api.kidsfunyfiestasinfantiles.com/api/products/" | jq '.[0:3]'
```

#### Login
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "contraseña123"}'
```

#### Crear Producto
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Nuevo Producto",
    "description": "Descripción del producto",
    "price": "150.00",
    "category": "option1"
  }'
```

---

## 📞 Soporte

### Contacto
- **Email**: soporte@kidsfunyfiestasinfantiles.com
- **Documentación**: https://api.kidsfunyfiestasinfantiles.com/docs
- **Issues**: https://github.com/mrgomezsv/kidsfun_back/issues

### Recursos Útiles
- **[API Documentation](API_DOCUMENTATION.md)** - Guía completa
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Guía técnica
- **[Health Check](https://api.kidsfunyfiestasinfantiles.com/health)** - Estado del sistema

---

**¡Gracias por usar KidsFun API! 🎉** 