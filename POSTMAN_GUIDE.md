# 🚀 Guía Completa de Postman para KidsFun API

## 📋 Índice
- [Configuración Inicial](#configuración-inicial)
- [Colección de Postman](#colección-de-postman)
- [Autenticación](#autenticación)
- [Endpoints de Productos](#endpoints-de-productos)
- [Endpoints de Usuarios](#endpoints-de-usuarios)
- [Endpoints de Comentarios](#endpoints-de-comentarios)
- [Endpoints de Likes](#endpoints-de-likes)
- [Endpoints de Eventos](#endpoints-de-eventos)
- [Endpoints de Waivers](#endpoints-de-waivers)
- [Endpoints de Chat](#endpoints-de-chat)
- [Endpoints de Contacto](#endpoints-de-contacto)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Configuración Inicial

### 1. Variables de Entorno en Postman

#### Crear Variables de Entorno
1. Abre Postman
2. Haz clic en el ícono de engranaje (⚙️) en la esquina superior derecha
3. Haz clic en "Add" para crear un nuevo entorno
4. Nombra el entorno como "KidsFun API"

#### Variables a Configurar
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `base_url` | `https://api.kidsfunyfiestasinfantiles.com` | URL base de la API |
| `token` | (vacío) | Token JWT (se llenará automáticamente) |
| `user_id` | (vacío) | ID del usuario (se llenará automáticamente) |

### 2. Headers Globales

#### Configurar Headers por Defecto
1. Ve a "Settings" → "General"
2. En "Headers", agrega:
   - `Content-Type`: `application/json`
   - `Accept`: `application/json`

---

## 📁 Colección de Postman

### Importar Colección
1. Descarga el archivo JSON de la colección (se proporciona al final)
2. En Postman, haz clic en "Import"
3. Selecciona el archivo JSON
4. La colección se importará automáticamente

### Estructura de la Colección
```
KidsFun API
├── 🔐 Authentication
│   ├── Login
│   └── Register
├── 🎪 Products
│   ├── Get All Products
│   ├── Get Product by ID
│   ├── Create Product
│   ├── Update Product
│   ├── Delete Product
│   └── Upload Product Image
├── 👥 Users
│   ├── Get All Users
│   ├── Get User by ID
│   └── Delete User
├── 💬 Commentaries
│   ├── Get All Commentaries
│   ├── Create Commentary
│   ├── Update Commentary
│   └── Delete Commentary
├── ❤️ Likes
│   ├── Get All Likes
│   ├── Create Like
│   └── Delete Like
├── 🎉 Events
│   ├── Get All Events
│   └── Create Event
├── 📋 Waivers
│   ├── Get All Waivers
│   ├── Create Waiver
│   └── Get Waiver by QR
├── 💬 Chat
│   ├── Get All Chat Rooms
│   ├── Create Chat Room
│   └── Get Chat Room by ID
└── 📞 Contact
    ├── Create Contact Form
    ├── Get All Contacts
    ├── Get Contact by ID
    ├── Update Contact
    ├── Delete Contact
    └── Contact Statistics
```

---

## 🔐 Autenticación

### 1. Login

#### Request
```http
POST {{base_url}}/api/auth/login
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

#### Response
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

#### Script de Postman (Tests)
```javascript
// Extraer token y user_id automáticamente
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("token", response.access_token);
    pm.environment.set("user_id", response.user.id);
    
    console.log("Token guardado:", response.access_token);
    console.log("User ID guardado:", response.user.id);
}
```

### 2. Register

#### Request
```http
POST {{base_url}}/api/auth/register
Content-Type: application/json

{
  "email": "nuevo@usuario.com",
  "password": "contraseña123",
  "username": "nuevo_usuario",
  "first_name": "Nuevo",
  "last_name": "Usuario"
}
```

---

## 🎪 Endpoints de Productos

### 1. Obtener Todos los Productos

#### Request
```http
GET {{base_url}}/api/products/
```

#### Parámetros de Query (Opcionales)
- `skip`: Número de productos a saltar (default: 0)
- `limit`: Número máximo de productos (default: 100, max: 100)
- `category`: Filtrar por categoría (option1, option2, etc.)
- `search`: Buscar en título
- `publicated`: Filtrar por estado de publicación (true/false)

#### Ejemplos de URLs
```
{{base_url}}/api/products/?limit=10
{{base_url}}/api/products/?category=option1
{{base_url}}/api/products/?search=bounce
{{base_url}}/api/products/?category=option1&search=bounce&limit=5
```

#### Response
```json
[
  {
    "id": 26,
    "title": "Red Mechanical Bull",
    "description": "Saddle up for a rip-roaring good time...",
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
]
```

### 2. Obtener Producto por ID

#### Request
```http
GET {{base_url}}/api/products/26
```

### 3. Crear Producto (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/products/
Authorization: Bearer {{token}}
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

### 4. Actualizar Producto (Requiere Autenticación)

#### Request
```http
PUT {{base_url}}/api/products/26
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Producto Actualizado",
  "description": "Nueva descripción",
  "price": "200.00"
}
```

### 5. Eliminar Producto (Requiere Autenticación)

#### Request
```http
DELETE {{base_url}}/api/products/26
Authorization: Bearer {{token}}
```

### 6. Subir Imagen de Producto (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/products/26/upload-image
Authorization: Bearer {{token}}
Content-Type: multipart/form-data

file: [seleccionar archivo de imagen]
```

---

## 👥 Endpoints de Usuarios

### 1. Obtener Todos los Usuarios (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/users/
Authorization: Bearer {{token}}
```

### 2. Obtener Usuario por ID (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/users/1
Authorization: Bearer {{token}}
```

### 3. Eliminar Usuario (Requiere Autenticación)

#### Request
```http
DELETE {{base_url}}/api/users/1
Authorization: Bearer {{token}}
```

---

## 💬 Endpoints de Comentarios

### 1. Obtener Todos los Comentarios

#### Request
```http
GET {{base_url}}/api/commentaries/
```

### 2. Crear Comentario (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/commentaries/
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "comment": "Excelente producto!",
  "product_id": 26
}
```

### 3. Actualizar Comentario (Requiere Autenticación)

#### Request
```http
PUT {{base_url}}/api/commentaries/1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "comment": "Comentario actualizado"
}
```

### 4. Eliminar Comentario (Requiere Autenticación)

#### Request
```http
DELETE {{base_url}}/api/commentaries/1
Authorization: Bearer {{token}}
```

---

## ❤️ Endpoints de Likes

### 1. Obtener Todos los Likes (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/likes/
Authorization: Bearer {{token}}
```

### 2. Crear Like (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/likes/
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product": "26",
  "is_favorite": true
}
```

### 3. Eliminar Like (Requiere Autenticación)

#### Request
```http
DELETE {{base_url}}/api/likes/1
Authorization: Bearer {{token}}
```

---

## 🎉 Endpoints de Eventos

### 1. Obtener Todos los Eventos

#### Request
```http
GET {{base_url}}/api/events/
```

### 2. Crear Evento (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/events/
Authorization: Bearer {{token}}
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

## 📋 Endpoints de Waivers

### 1. Obtener Todos los Waivers (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/waiver/
Authorization: Bearer {{token}}
```

### 2. Crear Waiver (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/waiver/
Authorization: Bearer {{token}}
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

### 3. Obtener Waiver por QR (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/waiver/QR123456
Authorization: Bearer {{token}}
```

---

## 💬 Endpoints de Chat

### 1. Obtener Todas las Salas de Chat (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/chat/
Authorization: Bearer {{token}}
```

### 2. Crear Sala de Chat (Requiere Autenticación)

#### Request
```http
POST {{base_url}}/api/chat/
Authorization: Bearer {{token}}
```

### 3. Obtener Sala de Chat por ID (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/chat/1
Authorization: Bearer {{token}}
```

---

## 📞 Endpoints de Contacto

### 1. Crear Formulario de Contacto (PÚBLICO)

#### Request
```http
POST {{base_url}}/api/contact/
Content-Type: application/json

{
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles. ¿Podrían enviarme un catálogo de productos y precios?"
}
```

#### Response
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles. ¿Podrían enviarme un catálogo de productos y precios?",
  "created_at": "2025-08-06T02:30:00.000000Z",
  "is_read": false,
  "is_responded": false
}
```

### 2. Obtener Todos los Contactos (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/contact/
Authorization: Bearer {{token}}
```

#### Parámetros de Query
- `skip` (int, opcional): Número de contactos a saltar (default: 0)
- `limit` (int, opcional): Número máximo de contactos (default: 100, max: 100)
- `is_read` (boolean, opcional): Filtrar por estado de lectura
- `is_responded` (boolean, opcional): Filtrar por estado de respuesta

#### Ejemplos
```http
# Obtener contactos no leídos
GET {{base_url}}/api/contact/?is_read=false

# Obtener contactos no respondidos
GET {{base_url}}/api/contact/?is_responded=false

# Obtener primeros 10 contactos
GET {{base_url}}/api/contact/?limit=10
```

### 3. Obtener Contacto Específico (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/contact/1
Authorization: Bearer {{token}}
```

### 4. Actualizar Contacto (Requiere Autenticación)

#### Request
```http
PUT {{base_url}}/api/contact/1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "is_read": true,
  "is_responded": true
}
```

### 5. Eliminar Contacto (Requiere Autenticación)

#### Request
```http
DELETE {{base_url}}/api/contact/1
Authorization: Bearer {{token}}
```

### 6. Estadísticas de Contactos (Requiere Autenticación)

#### Request
```http
GET {{base_url}}/api/contact/stats/summary
Authorization: Bearer {{token}}
```

#### Response
```json
{
  "total_contacts": 25,
  "unread_contacts": 8,
  "responded_contacts": 15,
  "pending_contacts": 10
}
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Obtener Productos y Mostrar Imágenes

#### Request
```http
GET {{base_url}}/api/products/?limit=3
```

#### Script de Tests
```javascript
// Verificar que la respuesta sea exitosa
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Verificar que hay productos
pm.test("Response has products", function () {
    const response = pm.response.json();
    pm.expect(response).to.be.an('array');
    pm.expect(response.length).to.be.greaterThan(0);
});

// Mostrar información de productos e imágenes
const products = pm.response.json();
products.forEach((product, index) => {
    console.log(`Producto ${index + 1}: ${product.title}`);
    console.log(`Precio: $${product.price}`);
    console.log(`Imagen principal: {{base_url}}/media/${product.img}`);
    
    // Mostrar todas las imágenes
    const images = [product.img, product.img1, product.img2, product.img3, product.img4, product.img5];
    images.forEach((img, imgIndex) => {
        if (img) {
            console.log(`  Imagen ${imgIndex + 1}: {{base_url}}/media/${img}`);
        }
    });
    console.log("---");
});
```

### Ejemplo 2: Login y Crear Producto

#### Paso 1: Login
```http
POST {{base_url}}/api/auth/login
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

#### Paso 2: Crear Producto (usando el token del login)
```http
POST {{base_url}}/api/products/
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Nuevo Producto desde Postman",
  "description": "Producto creado usando Postman",
  "price": "250.00",
  "category": "option1",
  "dimensions": "15x15ft"
}
```

### Ejemplo 3: Filtrar Productos

#### Request
```http
GET {{base_url}}/api/products/?category=option1&search=bounce&limit=5
```

#### Script de Tests
```javascript
pm.test("Filtered products", function () {
    const response = pm.response.json();
    
    // Verificar que todos los productos son de la categoría correcta
    response.forEach(product => {
        pm.expect(product.category).to.eql("option1");
    });
    
    // Verificar que todos los títulos contienen "bounce"
    response.forEach(product => {
        pm.expect(product.title.toLowerCase()).to.include("bounce");
    });
    
    // Verificar que no hay más de 5 productos
    pm.expect(response.length).to.be.at.most(5);
});
```

### Ejemplo 4: Enviar Formulario de Contacto

#### Request
```http
POST {{base_url}}/api/contact/
Content-Type: application/json

{
  "first_name": "María",
  "last_name": "García",
  "contact_number": "+1 (555) 987-6543",
  "email": "maria.garcia@ejemplo.com",
  "reason": "Hola, necesito cotización para una fiesta de cumpleaños para 20 niños. ¿Podrían enviarme información sobre sus paquetes y precios?"
}
```

#### Script de Tests
```javascript
pm.test("Contact form submitted successfully", function () {
    pm.response.to.have.status(200);
    
    const response = pm.response.json();
    pm.expect(response).to.have.property('id');
    pm.expect(response).to.have.property('first_name', 'María');
    pm.expect(response).to.have.property('last_name', 'García');
    pm.expect(response).to.have.property('email', 'maria.garcia@ejemplo.com');
    pm.expect(response).to.have.property('is_read', false);
    pm.expect(response).to.have.property('is_responded', false);
});
```

---

## 🔧 Solución de Problemas

### Error 401: Unauthorized
**Problema**: Token expirado o no válido
**Solución**: 
1. Hacer login nuevamente
2. Verificar que el token se guardó correctamente en las variables de entorno
3. Verificar que el header `Authorization` está configurado como `Bearer {{token}}`

### Error 429: Too Many Requests
**Problema**: Rate limit excedido
**Solución**: 
1. Esperar 1 segundo antes de hacer otra request
2. Reducir la frecuencia de requests
3. Implementar delays en los scripts de Postman

### Error 404: Not Found
**Problema**: Endpoint o recurso no encontrado
**Solución**:
1. Verificar que la URL es correcta
2. Verificar que el ID del recurso existe
3. Verificar que el endpoint está disponible

### Error 422: Validation Error
**Problema**: Datos inválidos en el request
**Solución**:
1. Verificar el formato de los datos
2. Verificar que todos los campos requeridos están presentes
3. Verificar que los tipos de datos son correctos

---

## 📊 Headers Importantes

### Headers de Autenticación
```
Authorization: Bearer {{token}}
```

### Headers de Contenido
```
Content-Type: application/json
Accept: application/json
```

### Headers de Rate Limiting
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

---

## 🎯 Consejos de Uso

### 1. Usar Variables de Entorno
- Configura `{{base_url}}` para no repetir la URL base
- Usa `{{token}}` para el token de autenticación
- Usa `{{user_id}}` para el ID del usuario

### 2. Scripts de Tests
- Usa scripts para validar respuestas automáticamente
- Extrae datos de las respuestas para usar en otros requests
- Implementa logging para debug

### 3. Organización
- Agrupa requests relacionados en folders
- Usa nombres descriptivos para los requests
- Documenta los requests con descripciones

### 4. Monitoreo
- Usa la consola de Postman para ver logs
- Revisa los headers de respuesta para información adicional
- Verifica el tiempo de respuesta

---

## 📁 Colección JSON

### Descargar Colección
```json
{
  "info": {
    "name": "KidsFun API",
    "description": "Colección completa para la API de KidsFun",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "https://api.kidsfunyfiestasinfantiles.com"
    },
    {
      "key": "token",
      "value": ""
    },
    {
      "key": "user_id",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "🔐 Authentication",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"usuario@ejemplo.com\",\n  \"password\": \"contraseña123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/auth/login",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "login"]
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "if (pm.response.code === 200) {",
                  "    const response = pm.response.json();",
                  "    pm.environment.set(\"token\", response.access_token);",
                  "    pm.environment.set(\"user_id\", response.user.id);",
                  "    ",
                  "    console.log(\"Token guardado:\", response.access_token);",
                  "    console.log(\"User ID guardado:\", response.user.id);",
                  "}"
                ]
              }
            }
          ]
        }
      ]
    },
    {
      "name": "🎪 Products",
      "item": [
        {
          "name": "Get All Products",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/products/",
              "host": ["{{base_url}}"],
              "path": ["api", "products", ""]
            }
          }
        },
        {
          "name": "Get Product by ID",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/products/26",
              "host": ["{{base_url}}"],
              "path": ["api", "products", "26"]
            }
          }
        }
      ]
    },
    {
      "name": "📞 Contact",
      "item": [
        {
          "name": "Create Contact Form",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"first_name\": \"Juan\",\n  \"last_name\": \"Pérez\",\n  \"contact_number\": \"+1 (555) 123-4567\",\n  \"email\": \"juan.perez@ejemplo.com\",\n  \"reason\": \"Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles.\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/contact/",
              "host": ["{{base_url}}"],
              "path": ["api", "contact", ""]
            }
          }
        },
        {
          "name": "Get All Contacts",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/contact/",
              "host": ["{{base_url}}"],
              "path": ["api", "contact", ""]
            }
          }
        }
      ]
    }
  ]
}
```

---

## 📞 Soporte

### Recursos Útiles
- **Documentación API**: https://api.kidsfunyfiestasinfantiles.com/docs
- **Health Check**: https://api.kidsfunyfiestasinfantiles.com/health
- **Issues**: https://github.com/mrgomezsv/kidsfun_back/issues

### Contacto
- **Email**: soporte@kidsfunyfiestasinfantiles.com

---

**¡Listo para usar Postman con KidsFun API! 🚀** 