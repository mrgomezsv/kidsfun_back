# 💬 API de Comentarios - KidsFun Backend

## 📋 **Resumen**

API para la gestión de comentarios en productos de KidsFun, permitiendo a los usuarios expresar sus opiniones y experiencias.

### 🎯 **Características Principales**
- ✅ **CRUD Completo** - Create, Read, Update, Delete
- ✅ **Filtros por Producto** - Comentarios específicos por producto
- ✅ **Autenticación** - Comentarios vinculados a usuarios
- ✅ **Validación** - Validación de contenido y longitud
- ✅ **Moderación** - Gestión de comentarios inapropiados

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/commentaries/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_commentary`**

```sql
CREATE TABLE t_app_commentary (
    id INTEGER PRIMARY KEY,
    comment TEXT NOT NULL,
    product_id INTEGER REFERENCES t_app_product_product(id),
    user_id INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | INTEGER | ID único del comentario | ✅ |
| `comment` | TEXT | Contenido del comentario | ✅ |
| `product_id` | INTEGER | ID del producto | ✅ |
| `user_id` | INTEGER | ID del usuario | ✅ |
| `created_at` | TIMESTAMP | Fecha de creación | ✅ |

---

## 🚀 **Endpoints**

### **1. Obtener Comentarios - `GET /api/commentaries/`**

Obtiene una lista de comentarios con filtros opcionales.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/commentaries/
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `product_id` | int | Filtrar por producto específico | - | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "comment": "Excelente producto! Muy divertido para los niños.",
    "product_id": 26,
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "user": {
      "id": 1,
      "username": "usuario1",
      "first_name": "Juan",
      "last_name": "Pérez"
    }
  },
  {
    "id": 2,
    "comment": "Muy buena calidad, lo recomiendo.",
    "product_id": 26,
    "user_id": 2,
    "created_at": "2024-01-02T00:00:00Z",
    "user": {
      "id": 2,
      "username": "usuario2",
      "first_name": "María",
      "last_name": "García"
    }
  }
]
```

#### **Ejemplo con cURL**
```bash
# Obtener todos los comentarios
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/"

# Obtener comentarios de un producto específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/?product_id=26"
```

#### **Ejemplo con JavaScript**
```javascript
async function getCommentaries(productId = null) {
  const params = productId ? `?product_id=${productId}` : '';
  const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/commentaries/${params}`);
  
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch commentaries');
  }
}

// Uso
getCommentaries(26)
  .then(commentaries => console.log('Comentarios:', commentaries))
  .catch(error => console.error('Error:', error));
```

---

### **2. Crear Comentario - `POST /api/commentaries/`**

Crea un nuevo comentario (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/commentaries/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "comment": "Excelente producto! Muy divertido para los niños.",
  "product_id": 26
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "comment": "Excelente producto! Muy divertido para los niños.",
  "product_id": 26,
  "user_id": 1,
  "created_at": "2024-01-03T00:00:00Z"
}
```

#### **Response Error (400)**
```json
{
  "detail": "Comment cannot be empty"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Excelente producto! Muy divertido para los niños.",
    "product_id": 26
  }'
```

---

### **3. Actualizar Comentario - `PUT /api/commentaries/{comment_id}`**

Actualiza un comentario existente (requiere autenticación).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/commentaries/{comment_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "comment": "Comentario actualizado con nueva información."
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "comment": "Comentario actualizado con nueva información.",
  "product_id": 26,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### **Ejemplo con cURL**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Comentario actualizado con nueva información."
  }'
```

---

### **4. Eliminar Comentario - `DELETE /api/commentaries/{comment_id}`**

Elimina un comentario (requiere autenticación).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/commentaries/{comment_id}
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
curl -X DELETE "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Comentarios**
```bash
# Obtener todos los comentarios
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/"

# Obtener comentarios de un producto específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/?product_id=26"
```

#### **Crear Comentario**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Test comment",
    "product_id": 26
  }'
```

#### **Actualizar Comentario**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Updated test comment"
  }'
```

### **2. Testing con JavaScript**

```javascript
class CommentariesAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getCommentaries(productId = null, token = null) {
    const params = productId ? `?product_id=${productId}` : '';
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    
    const response = await fetch(`${this.baseURL}/api/commentaries/${params}`, {
      headers
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createCommentary(commentData, token) {
    const response = await fetch(`${this.baseURL}/api/commentaries/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(commentData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateCommentary(id, commentData, token) {
    const response = await fetch(`${this.baseURL}/api/commentaries/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(commentData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteCommentary(id, token) {
    const response = await fetch(`${this.baseURL}/api/commentaries/${id}`, {
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
const commentariesAPI = new CommentariesAPI();

// Obtener comentarios
commentariesAPI.getCommentaries(26)
  .then(commentaries => console.log('Comentarios:', commentaries))
  .catch(error => console.error('Error:', error));

// Crear comentario
commentariesAPI.createCommentary({
  comment: 'Test comment',
  product_id: 26
}, 'YOUR_TOKEN')
  .then(commentary => console.log('Comentario creado:', commentary))
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

#### **2. Error 404 - "Comment not found"**
```bash
# Verificar que el comentario existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/commentaries/999"
```

#### **3. Error 400 - "Comment cannot be empty"**
```bash
# Verificar que el comentario no esté vacío
# El comentario debe tener al menos 1 carácter
```

### **Comandos de Diagnóstico**

#### **Verificar Comentarios en Base de Datos**
```sql
-- Ver todos los comentarios
SELECT id, comment, product_id, user_id, created_at 
FROM t_app_commentary;

-- Ver comentarios por producto
SELECT id, comment, user_id, created_at 
FROM t_app_commentary 
WHERE product_id = 26;

-- Ver comentarios por usuario
SELECT id, comment, product_id, created_at 
FROM t_app_commentary 
WHERE user_id = 1;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Comentarios**
```sql
-- Total de comentarios
SELECT COUNT(*) as total_commentaries FROM t_app_commentary;

-- Comentarios por producto
SELECT product_id, COUNT(*) as comment_count 
FROM t_app_commentary 
GROUP BY product_id 
ORDER BY comment_count DESC;

-- Comentarios por usuario
SELECT user_id, COUNT(*) as comment_count 
FROM t_app_commentary 
GROUP BY user_id 
ORDER BY comment_count DESC;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **⭐ Sistema de Calificación**
   - Calificaciones de 1 a 5 estrellas
   - Promedio de calificaciones por producto
   - Filtros por calificación

2. **🔍 Búsqueda Avanzada**
   - Búsqueda en contenido de comentarios
   - Filtros por fecha
   - Ordenamiento por relevancia

3. **🛡️ Moderación**
   - Filtros de contenido inapropiado
   - Sistema de reportes
   - Moderación automática

4. **📊 Analytics**
   - Métricas de engagement
   - Reportes de comentarios
   - Análisis de sentimientos

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

**¡API de Comentarios lista para usar! 💬** 