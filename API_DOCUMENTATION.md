# 📚 Documentación para Consumir la API de KidsFun

## 🌐 **Información General**

- **URL Base:** `https://api.kidsfunyfiestasinfantiles.com`
- **Versión:** 1.0.0
- **Formato:** JSON
- **Autenticación:** JWT Bearer Token

## 🔐 **Autenticación y Seguridad**

### **1. Obtener Token de Acceso**

```bash
# Login para obtener token
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=tu_usuario&password=tu_password"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### **2. Usar Token en Requests**

```bash
# Ejemplo con token
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### **3. Registro de Usuario**

```bash
# Registrar nuevo usuario
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "usuario@ejemplo.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

## 📋 **Endpoints Principales**

### **🔐 Autenticación**

#### **Login**
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=usuario&password=password
```

#### **Registro**
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

#### **Obtener Usuario Actual**
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### **👥 Usuarios**

#### **Listar Usuarios**
```http
GET /api/users/
Authorization: Bearer <token>
```

#### **Obtener Usuario por ID**
```http
GET /api/users/{user_id}
Authorization: Bearer <token>
```

#### **Actualizar Usuario**
```http
PUT /api/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Nuevo Nombre",
  "last_name": "Nuevo Apellido",
  "email": "nuevo@email.com"
}
```

### **🛍️ Productos**

#### **Listar Productos**
```http
GET /api/products/
Authorization: Bearer <token>
```

#### **Obtener Producto por ID**
```http
GET /api/products/{product_id}
Authorization: Bearer <token>
```

#### **Crear Producto**
```http
POST /api/products/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Producto Nuevo",
  "description": "Descripción del producto",
  "price": 99.99,
  "category": "categoria"
}
```

#### **Actualizar Producto**
```http
PUT /api/products/{product_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Producto Actualizado",
  "price": 149.99
}
```

#### **Eliminar Producto**
```http
DELETE /api/products/{product_id}
Authorization: Bearer <token>
```

#### **Subir Imagen de Producto**
```http
POST /api/products/{product_id}/upload-image
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: [archivo de imagen]
```

### **❤️ Likes**

#### **Listar Likes**
```http
GET /api/likes/
Authorization: Bearer <token>
```

#### **Crear/Actualizar Like**
```http
POST /api/likes/
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "user_id": 1
}
```

#### **Eliminar Like**
```http
DELETE /api/likes/{like_id}
Authorization: Bearer <token>
```

### **💬 Comentarios**

#### **Listar Comentarios**
```http
GET /api/commentaries/
Authorization: Bearer <token>
```

#### **Crear Comentario**
```http
POST /api/commentaries/
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "user_id": 1,
  "content": "Excelente producto!"
}
```

#### **Eliminar Comentario**
```http
DELETE /api/commentaries/{commentary_id}
Authorization: Bearer <token>
```

### **🎉 Eventos**

#### **Listar Eventos**
```http
GET /api/events/
Authorization: Bearer <token>
```

#### **Crear Evento**
```http
POST /api/events/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Fiesta de Cumpleaños",
  "description": "Celebración especial",
  "date": "2024-12-25T18:00:00",
  "location": "Salón Principal"
}
```

### **📄 Waivers**

#### **Crear Waiver**
```http
POST /api/waiver/
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,
  "event_id": 1,
  "family_members": [
    {
      "name": "María Pérez",
      "relationship": "Madre",
      "phone": "1234567890"
    }
  ]
}
```

#### **Validar Waiver por QR**
```http
POST /api/waiver/validate
Authorization: Bearer <token>
Content-Type: application/json

{
  "qr_code": "QR_CODE_HERE"
}
```

#### **Obtener Waiver por QR**
```http
GET /api/waiver/{qr_code}
Authorization: Bearer <token>
```

### **💬 Chat**

#### **Obtener Salas de Chat**
```http
GET /api/chat/rooms
Authorization: Bearer <token>
```

#### **Crear Sala de Chat**
```http
POST /api/chat/rooms
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,
  "title": "Soporte Técnico"
}
```

#### **Obtener Mensajes**
```http
GET /api/chat/rooms/{room_id}/messages
Authorization: Bearer <token>
```

#### **Enviar Mensaje**
```http
POST /api/chat/rooms/{room_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,
  "content": "Hola, necesito ayuda"
}
```

## 🔒 **Mejores Prácticas de Seguridad**

### **1. Manejo de Tokens**

```javascript
// ✅ CORRECTO - Guardar token en localStorage
const token = localStorage.getItem('auth_token');

// ✅ CORRECTO - Usar en headers
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};

// ❌ INCORRECTO - No exponer token en URLs
fetch('/api/users?token=abc123'); // MALO
```

### **2. Renovación de Tokens**

```javascript
// Verificar si el token está próximo a expirar
const checkTokenExpiration = () => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expirationTime = payload.exp * 1000;
    const currentTime = Date.now();
    
    if (currentTime > expirationTime - 300000) { // 5 minutos antes
      refreshToken();
    }
  }
};
```

### **3. Manejo de Errores**

```javascript
// Interceptor para manejar errores de autenticación
const handleApiError = (error) => {
  if (error.status === 401) {
    // Token expirado o inválido
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
  } else if (error.status === 403) {
    // Sin permisos
    alert('No tienes permisos para realizar esta acción');
  } else if (error.status === 429) {
    // Rate limit excedido
    alert('Demasiadas peticiones. Intenta más tarde.');
  }
};
```

### **4. Validación de Datos**

```javascript
// Validar datos antes de enviar
const validateProductData = (product) => {
  const errors = [];
  
  if (!product.name || product.name.length < 3) {
    errors.push('El nombre debe tener al menos 3 caracteres');
  }
  
  if (!product.price || product.price <= 0) {
    errors.push('El precio debe ser mayor a 0');
  }
  
  if (product.description && product.description.length > 500) {
    errors.push('La descripción no puede exceder 500 caracteres');
  }
  
  return errors;
};
```

## 📱 **Ejemplos por Tecnología**

### **JavaScript/Fetch**

```javascript
// Configuración base
const API_BASE = 'https://api.kidsfunyfiestasinfantiles.com';

// Función para hacer requests
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('auth_token');
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  };
  
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Ejemplos de uso
const getProducts = () => apiRequest('/api/products/');
const createProduct = (product) => apiRequest('/api/products/', {
  method: 'POST',
  body: JSON.stringify(product)
});
const updateProduct = (id, product) => apiRequest(`/api/products/${id}`, {
  method: 'PUT',
  body: JSON.stringify(product)
});
```

### **Axios**

```javascript
import axios from 'axios';

// Configuración base
const api = axios.create({
  baseURL: 'https://api.kidsfunyfiestasinfantiles.com',
  timeout: 10000
});

// Interceptor para agregar token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Ejemplos de uso
const getProducts = () => api.get('/api/products/');
const createProduct = (product) => api.post('/api/products/', product);
const updateProduct = (id, product) => api.put(`/api/products/${id}`, product);
```

### **React Hook**

```javascript
import { useState, useEffect } from 'react';

const useApi = (endpoint, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth_token');
      
      const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com${endpoint}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  return { data, loading, error, refetch: fetchData };
};

// Uso en componente
const ProductList = () => {
  const { data: products, loading, error } = useApi('/api/products/');
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      {products?.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
};
```

## 🚨 **Limitaciones y Rate Limiting**

- **Rate Limit:** 10 requests por segundo por IP
- **Tamaño máximo de archivo:** 10MB
- **Tiempo de expiración del token:** 30 minutos
- **Máximo de productos por página:** 100

## 📞 **Soporte**

Para problemas o consultas:
- **Documentación:** https://api.kidsfunyfiestasinfantiles.com/docs
- **Health Check:** https://api.kidsfunyfiestasinfantiles.com/health
- **Logs del servidor:** Contactar al administrador

## 🔄 **Webhooks (Próximamente)**

```javascript
// Ejemplo de webhook para notificaciones
const webhookUrl = 'https://tu-servidor.com/webhook';

// Configurar webhook
const setupWebhook = async () => {
  await api.post('/api/webhooks/', {
    url: webhookUrl,
    events: ['product.created', 'order.completed']
  });
};
``` 