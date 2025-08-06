# 👥 API de Usuarios - KidsFun Backend

## 📋 **Resumen**

API para la gestión de usuarios del sistema KidsFun, incluyendo perfiles, permisos y administración.

### 🎯 **Características Principales**
- ✅ **Gestión de Perfiles** - Ver y actualizar información de usuarios
- ✅ **Control de Acceso** - Permisos basados en roles
- ✅ **Administración** - Gestión completa para superusuarios
- ✅ **Validación** - Validación de datos y emails
- ✅ **Seguridad** - Contraseñas hasheadas y tokens JWT

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/users/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `auth_user`**

```sql
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY,
    password VARCHAR NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | INTEGER | ID único del usuario | ✅ |
| `password` | VARCHAR | Contraseña hasheada | ✅ |
| `last_login` | TIMESTAMP | Último login | ❌ |
| `is_superuser` | BOOLEAN | Es superusuario | ❌ |
| `username` | VARCHAR(150) | Nombre de usuario | ✅ |
| `first_name` | VARCHAR(150) | Nombre | ✅ |
| `last_name` | VARCHAR(150) | Apellido | ✅ |
| `email` | VARCHAR(254) | Email | ✅ |
| `is_staff` | BOOLEAN | Es staff | ❌ |
| `is_active` | BOOLEAN | Usuario activo | ❌ |
| `date_joined` | TIMESTAMP | Fecha de registro | ❌ |

---

## 🚀 **Endpoints**

### **1. Obtener Usuarios - `GET /api/users/`**

Obtiene una lista de usuarios (requiere permisos de superusuario).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/users/
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `skip` | int | Número de usuarios a saltar | 0 | ❌ |
| `limit` | int | Número máximo de usuarios (1-100) | 100 | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@kidsfun.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_superuser": true,
    "is_staff": true,
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "username": "usuario1",
    "email": "usuario1@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-01-02T00:00:00Z"
  }
]
```

#### **Response Error (403)**
```json
{
  "detail": "Not enough permissions"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **2. Obtener Usuario por ID - `GET /api/users/{user_id}`**

Obtiene un usuario específico por su ID (requiere permisos de superusuario).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/users/{user_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Path**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `user_id` | int | ID del usuario |

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@kidsfun.com",
  "first_name": "Admin",
  "last_name": "User",
  "is_superuser": true,
  "is_staff": true,
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

#### **Response Error (404)**
```json
{
  "detail": "User not found"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **3. Actualizar Usuario - `PUT /api/users/{user_id}`**

Actualiza un usuario existente (requiere permisos de superusuario).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/users/{user_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "username": "usuario_actualizado",
  "email": "nuevo@email.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_active": true
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "username": "usuario_actualizado",
  "email": "nuevo@email.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_superuser": false,
  "is_staff": false,
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

#### **Ejemplo con cURL**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_actualizado",
    "email": "nuevo@email.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_active": true
  }'
```

---

### **4. Eliminar Usuario - `DELETE /api/users/{user_id}`**

Elimina un usuario (requiere permisos de superusuario).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/users/{user_id}
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
curl -X DELETE "https://api.kidsfunyfiestasinfantiles.com/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🔐 **Permisos y Roles**

### **Tipos de Usuario**

#### **1. Superusuario (`is_superuser: true`)**
- ✅ Acceso completo a todas las funcionalidades
- ✅ Gestión de usuarios
- ✅ Configuración del sistema
- ✅ Acceso a logs y métricas

#### **2. Staff (`is_staff: true`)**
- ✅ Acceso a panel de administración
- ✅ Gestión de contenido
- ✅ Moderación de comentarios

#### **3. Usuario Regular (`is_active: true`)**
- ✅ Acceso a funcionalidades básicas
- ✅ Crear y gestionar contenido propio
- ✅ Comentar y dar likes

#### **4. Usuario Inactivo (`is_active: false`)**
- ❌ Acceso limitado
- ❌ No puede crear contenido
- ❌ No puede comentar

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Usuarios**
```bash
# Obtener todos los usuarios
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener usuario específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Actualizar Usuario**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@ejemplo.com",
    "first_name": "Test",
    "last_name": "User",
    "is_active": true
  }'
```

### **2. Testing con JavaScript**

```javascript
class UsersAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getUsers(token, filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/api/users/?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getUser(id, token) {
    const response = await fetch(`${this.baseURL}/api/users/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateUser(id, userData, token) {
    const response = await fetch(`${this.baseURL}/api/users/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteUser(id, token) {
    const response = await fetch(`${this.baseURL}/api/users/${id}`, {
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
const usersAPI = new UsersAPI();

// Obtener usuarios
usersAPI.getUsers('YOUR_TOKEN')
  .then(users => console.log('Usuarios:', users))
  .catch(error => console.error('Error:', error));

// Obtener usuario específico
usersAPI.getUser(1, 'YOUR_TOKEN')
  .then(user => console.log('Usuario:', user))
  .catch(error => console.error('Error:', error));
```

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Error 403 - "Not enough permissions"**
```bash
# Verificar que el usuario es superusuario
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **2. Error 404 - "User not found"**
```bash
# Verificar que el usuario existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/users/999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 422 - "Validation error"**
```bash
# Verificar que todos los campos requeridos están presentes
# Campos requeridos: username, email, first_name, last_name
```

### **Comandos de Diagnóstico**

#### **Verificar Usuarios en Base de Datos**
```sql
-- Ver todos los usuarios
SELECT id, username, email, is_superuser, is_active FROM auth_user;

-- Ver superusuarios
SELECT id, username, email FROM auth_user WHERE is_superuser = true;

-- Ver usuarios activos
SELECT id, username, email FROM auth_user WHERE is_active = true;
```

#### **Verificar Permisos**
```sql
-- Verificar permisos de un usuario específico
SELECT username, is_superuser, is_staff, is_active 
FROM auth_user 
WHERE id = 1;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Usuarios**
```sql
-- Total de usuarios
SELECT COUNT(*) as total_users FROM auth_user;

-- Usuarios activos
SELECT COUNT(*) as active_users FROM auth_user WHERE is_active = true;

-- Usuarios por tipo
SELECT 
  CASE 
    WHEN is_superuser THEN 'Superusuario'
    WHEN is_staff THEN 'Staff'
    ELSE 'Usuario Regular'
  END as user_type,
  COUNT(*) as count
FROM auth_user 
GROUP BY is_superuser, is_staff;
```

#### **Últimos Registros**
```sql
SELECT username, email, date_joined 
FROM auth_user 
ORDER BY date_joined DESC 
LIMIT 10;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **👥 Gestión de Roles**
   - Roles personalizados
   - Permisos granulares
   - Grupos de usuarios

2. **📧 Notificaciones**
   - Emails de bienvenida
   - Notificaciones de cambios
   - Recordatorios

3. **🔐 Seguridad Avanzada**
   - Autenticación de dos factores
   - Historial de logins
   - Detección de actividad sospechosa

4. **📊 Analytics**
   - Métricas de uso
   - Reportes de actividad
   - Dashboard de administración

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

**¡API de Usuarios lista para usar! 👥** 