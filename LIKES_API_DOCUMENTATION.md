# ❤️ API de Likes - KidsFun Backend

## 📋 **Resumen**

API para la gestión de likes/favoritos en productos de KidsFun, permitiendo a los usuarios marcar productos como favoritos.

### 🎯 **Características Principales**
- ✅ **CRUD Completo** - Create, Read, Update, Delete
- ✅ **Filtros por Producto** - Likes específicos por producto
- ✅ **Filtros por Usuario** - Likes específicos por usuario
- ✅ **Autenticación** - Likes vinculados a usuarios
- ✅ **Validación** - Validación de datos
- ✅ **Estadísticas** - Conteos de likes por producto

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/likes/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_like`**

```sql
CREATE TABLE t_app_like (
    id INTEGER PRIMARY KEY,
    product VARCHAR NOT NULL,
    user VARCHAR NOT NULL,
    is_favorite BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | INTEGER | ID único del like | ✅ |
| `product` | VARCHAR | ID del producto (como string) | ✅ |
| `user` | VARCHAR | ID del usuario (como string) | ✅ |
| `is_favorite` | BOOLEAN | Estado del favorito | ✅ |
| `created_at` | TIMESTAMP | Fecha de creación | ✅ |

---

## 🚀 **Endpoints**

### **1. Obtener Likes - `GET /api/likes/`**

Obtiene una lista de likes con filtros opcionales (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/likes/
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `product_id` | int | Filtrar por producto específico | - | ❌ |
| `user_id` | string | Filtrar por usuario específico | - | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "product": "26",
    "user": "1",
    "is_favorite": true,
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "product": "27",
    "user": "1",
    "is_favorite": true,
    "created_at": "2024-01-02T00:00:00Z"
  }
]
```

#### **Ejemplo con cURL**
```bash
# Obtener todos los likes del usuario autenticado
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener likes de un producto específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/?product_id=26" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Ejemplo con JavaScript**
```javascript
async function getLikes(productId = null, userId = null, token) {
  const params = new URLSearchParams();
  if (productId) params.append('product_id', productId);
  if (userId) params.append('user_id', userId);
  
  const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/likes/?${params}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch likes');
  }
}

// Uso
getLikes(26, null, 'YOUR_TOKEN')
  .then(likes => console.log('Likes:', likes))
  .catch(error => console.error('Error:', error));
```

---

### **2. Crear Like - `POST /api/likes/`**

Crea un nuevo like/favorito (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/likes/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "product": "26",
  "is_favorite": true
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "product": "26",
  "user": "1",
  "is_favorite": true,
  "created_at": "2024-01-03T00:00:00Z"
}
```

#### **Response Error (400)**
```json
{
  "detail": "Like already exists for this product and user"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/likes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": "26",
    "is_favorite": true
  }'
```

---

### **3. Actualizar Like - `PUT /api/likes/{like_id}`**

Actualiza un like existente (requiere autenticación).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/likes/{like_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "is_favorite": false
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "product": "26",
  "user": "1",
  "is_favorite": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### **Ejemplo con cURL**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/likes/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_favorite": false
  }'
```

---

### **4. Eliminar Like - `DELETE /api/likes/{like_id}`**

Elimina un like (requiere autenticación).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/likes/{like_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (204)**
```
No Content
```

#### **Ejemplo con cURL**
```bash
curl -X DELETE "https://api.kidsfunyfiestasinfantiles.com/api/likes/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Likes**
```bash
# Obtener todos los likes del usuario autenticado
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener likes de un producto específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/?product_id=26" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Crear Like**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/likes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": "26",
    "is_favorite": true
  }'
```

#### **Actualizar Like**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/likes/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_favorite": false
  }'
```

### **2. Testing con JavaScript**

```javascript
class LikesAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getLikes(productId = null, userId = null, token) {
    const params = new URLSearchParams();
    if (productId) params.append('product_id', productId);
    if (userId) params.append('user_id', userId);
    
    const response = await fetch(`${this.baseURL}/api/likes/?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createLike(likeData, token) {
    const response = await fetch(`${this.baseURL}/api/likes/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(likeData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateLike(id, likeData, token) {
    const response = await fetch(`${this.baseURL}/api/likes/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(likeData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteLike(id, token) {
    const response = await fetch(`${this.baseURL}/api/likes/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }
}

// Uso
const likesAPI = new LikesAPI();

// Obtener likes
likesAPI.getLikes(26, null, 'YOUR_TOKEN')
  .then(likes => console.log('Likes:', likes))
  .catch(error => console.error('Error:', error));

// Crear like
likesAPI.createLike({
  product: "26",
  is_favorite: true
}, 'YOUR_TOKEN')
  .then(like => console.log('Like creado:', like))
  .catch(error => console.error('Error:', error));
```

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Error 401 - "Not authenticated"**
```bash
# Verificar que el token es válido
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **2. Error 404 - "Like not found"**
```bash
# Verificar que el like existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 400 - "Like already exists"**
```bash
# Verificar si ya existe un like para ese producto y usuario
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/likes/?product_id=26&user_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **Comandos de Diagnóstico**

#### **Verificar Likes en Base de Datos**
```sql
-- Ver todos los likes
SELECT id, product, user, is_favorite, created_at 
FROM t_app_like;

-- Ver likes por producto
SELECT id, user, is_favorite, created_at 
FROM t_app_like 
WHERE product = '26';

-- Ver likes por usuario
SELECT id, product, is_favorite, created_at 
FROM t_app_like 
WHERE user = '1';
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Likes**
```sql
-- Total de likes
SELECT COUNT(*) as total_likes FROM t_app_like;

-- Likes por producto
SELECT product, COUNT(*) as like_count 
FROM t_app_like 
WHERE is_favorite = true
GROUP BY product 
ORDER BY like_count DESC;

-- Likes por usuario
SELECT user, COUNT(*) as like_count 
FROM t_app_like 
WHERE is_favorite = true
GROUP BY user 
ORDER BY like_count DESC;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **⭐ Sistema de Calificación**
   - Calificaciones de 1 a 5 estrellas
   - Promedio de calificaciones por producto
   - Filtros por calificación

2. **🔍 Búsqueda Avanzada**
   - Búsqueda en productos favoritos
   - Filtros por fecha
   - Ordenamiento por relevancia

3. **📊 Analytics**
   - Métricas de engagement
   - Reportes de likes
   - Análisis de tendencias

4. **🔄 Sincronización**
   - Sincronización entre dispositivos
   - Backup de favoritos
   - Exportación de datos

---

## 📞 **Soporte**

### **Contacto**
- **📧 Email:** soporte@kidsfunyfiestasinfantiles.com
- **🔗 Documentación:** [API Documentation](./API_DOCUMENTATION.md)
- **🌐 Health Check:** `https://api.kidsfunyfiestasinfantiles.com/health`

### **Recursos Adicionales**
- [API Documentation](./API_DOCUMENTATION.md)
- [Developer Guide](./DEVELOPER_GUIDE.md)
- [Postman Guide](./POSTMAN_GUIDE.md)
- [Auth API Documentation](./AUTH_API_DOCUMENTATION.md)

---

**¡API de Likes lista para usar! ❤️** 