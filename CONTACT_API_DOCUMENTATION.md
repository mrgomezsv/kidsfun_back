# 📞 API de Contacto - KidsFun Backend

## 📋 **Resumen**

API para la gestión de formularios de contacto en el sistema KidsFun, permitiendo a los usuarios enviar mensajes y al equipo administrar las consultas recibidas.

### 🎯 **Características Principales**
- ✅ **Formulario Público** - No requiere autenticación para enviar
- ✅ **Notificaciones por Email** - Envía email automático al recibir formulario
- ✅ **Gestión de Contactos** - Panel de administración para ver y gestionar contactos
- ✅ **Estadísticas** - Resumen de contactos recibidos
- ✅ **Validación de Datos** - Validación automática de campos
- ✅ **Estado de Gestión** - Marcado como leído y respondido

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/contact/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_contact`**

```sql
CREATE TABLE t_app_contact (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_read BOOLEAN DEFAULT FALSE,
    is_responded BOOLEAN DEFAULT FALSE
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | INTEGER | ID único del contacto | ✅ |
| `first_name` | VARCHAR(100) | Nombre del contacto | ✅ |
| `last_name` | VARCHAR(100) | Apellido del contacto | ✅ |
| `contact_number` | VARCHAR(20) | Número de teléfono | ✅ |
| `email` | VARCHAR(255) | Email del contacto | ✅ |
| `reason` | TEXT | Mensaje o razón del contacto | ✅ |
| `created_at` | TIMESTAMP | Fecha de creación | ✅ |
| `is_read` | BOOLEAN | Estado de lectura | ❌ |
| `is_responded` | BOOLEAN | Estado de respuesta | ❌ |

---

## 🚀 **Endpoints**

### **1. Crear Formulario de Contacto - `POST /api/contact/`**

Crea un nuevo formulario de contacto (PÚBLICO - no requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/contact/
```

#### **Headers**
```http
Content-Type: application/json
```

#### **Body**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles. ¿Podrían enviarme un catálogo de productos y precios?"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles. ¿Podrían enviarme un catálogo de productos y precios?",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": false,
  "is_responded": false
}
```

#### **Response Error (422)**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/contact/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "contact_number": "+1 (555) 123-4567",
    "email": "juan.perez@ejemplo.com",
    "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles."
  }'
```

#### **Ejemplo con JavaScript**
```javascript
async function createContact(contactData) {
  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(contactData)
  });
  
  if (response.ok) {
    return await response.json();
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
}

// Uso
const contactData = {
  first_name: 'Juan',
  last_name: 'Pérez',
  contact_number: '+1 (555) 123-4567',
  email: 'juan.perez@ejemplo.com',
  reason: 'Hola, me gustaría obtener información sobre sus servicios.'
};

createContact(contactData)
  .then(contact => console.log('Contacto creado:', contact))
  .catch(error => console.error('Error:', error));
```

---

### **2. Obtener Contactos - `GET /api/contact/`**

Obtiene una lista de contactos (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `skip` | int | Número de contactos a saltar | 0 | ❌ |
| `limit` | int | Número máximo de contactos (1-100) | 100 | ❌ |
| `is_read` | boolean | Filtrar por estado de lectura | - | ❌ |
| `is_responded` | boolean | Filtrar por estado de respuesta | - | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "first_name": "Juan",
    "last_name": "Pérez",
    "contact_number": "+1 (555) 123-4567",
    "email": "juan.perez@ejemplo.com",
    "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles.",
    "created_at": "2024-01-01T00:00:00Z",
    "is_read": false,
    "is_responded": false
  },
  {
    "id": 2,
    "first_name": "María",
    "last_name": "García",
    "contact_number": "+1 (555) 987-6543",
    "email": "maria.garcia@ejemplo.com",
    "reason": "Necesito información sobre precios para una fiesta de cumpleaños.",
    "created_at": "2024-01-02T00:00:00Z",
    "is_read": true,
    "is_responded": true
  }
]
```

#### **Ejemplo con cURL**
```bash
# Obtener todos los contactos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener contactos no leídos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/?is_read=false" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener contactos con paginación
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **3. Obtener Contacto por ID - `GET /api/contact/{contact_id}`**

Obtiene un contacto específico por su ID (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/{contact_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Path**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `contact_id` | int | ID del contacto |

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles.",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": false,
  "is_responded": false
}
```

#### **Response Error (404)**
```json
{
  "detail": "Contact not found"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **4. Actualizar Contacto - `PUT /api/contact/{contact_id}`**

Actualiza un contacto existente (requiere autenticación).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/contact/{contact_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "is_read": true,
  "is_responded": true
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles.",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": true,
  "is_responded": true
}
```

#### **Ejemplo con cURL**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/contact/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_read": true,
    "is_responded": true
  }'
```

---

### **5. Eliminar Contacto - `DELETE /api/contact/{contact_id}`**

Elimina un contacto (requiere autenticación).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/contact/{contact_id}
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
curl -X DELETE "https://api.kidsfunyfiestasinfantiles.com/api/contact/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **6. Obtener Estadísticas - `GET /api/contact/stats/summary`**

Obtiene estadísticas resumidas de contactos (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/stats/summary
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (200)**
```json
{
  "total_contacts": 150,
  "unread_contacts": 25,
  "unresponded_contacts": 30,
  "contacts_this_month": 45,
  "contacts_this_week": 12,
  "average_response_time": "2.5 days"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/stats/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📧 **Sistema de Notificaciones por Email**

### **Configuración Automática**

Cuando se recibe un formulario de contacto, el sistema automáticamente:

1. **Guarda el contacto** en la base de datos
2. **Envía email de notificación** al equipo
3. **Registra el estado** del envío

### **Formato del Email**

```
Asunto: Nuevo formulario de contacto - {nombre} {apellido}

Se ha recibido un nuevo formulario de contacto:

**Información del Contacto:**
- Nombre: {nombre} {apellido}
- Email: {email}
- Teléfono: {teléfono}
- Fecha: {fecha}

**Mensaje:**
{mensaje}

---
Este mensaje fue enviado automáticamente desde el formulario de contacto de KidsFun.
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Crear Contacto**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/contact/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "contact_number": "+1 (555) 123-4567",
    "email": "test@ejemplo.com",
    "reason": "Test contact message"
  }'
```

#### **Obtener Contactos**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Actualizar Contacto**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/contact/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_read": true,
    "is_responded": true
  }'
```

#### **Obtener Estadísticas**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/stats/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **2. Testing con JavaScript**

```javascript
class ContactAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async createContact(contactData) {
    const response = await fetch(`${this.baseURL}/api/contact/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contactData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getContacts(token, filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/api/contact/?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getContact(id, token) {
    const response = await fetch(`${this.baseURL}/api/contact/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateContact(id, contactData, token) {
    const response = await fetch(`${this.baseURL}/api/contact/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contactData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteContact(id, token) {
    const response = await fetch(`${this.baseURL}/api/contact/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  async getStats(token) {
    const response = await fetch(`${this.baseURL}/api/contact/stats/summary`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }
}

// Uso
const contactAPI = new ContactAPI();

// Crear contacto
contactAPI.createContact({
  first_name: 'Test',
  last_name: 'User',
  contact_number: '+1 (555) 123-4567',
  email: 'test@ejemplo.com',
  reason: 'Test contact message'
})
  .then(contact => console.log('Contacto creado:', contact))
  .catch(error => console.error('Error:', error));

// Obtener contactos
contactAPI.getContacts('YOUR_TOKEN', { is_read: false })
  .then(contacts => console.log('Contactos:', contacts))
  .catch(error => console.error('Error:', error));
```

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Error 422 - "Validation error"**
```bash
# Verificar que todos los campos requeridos están presentes
# Campos requeridos: first_name, last_name, contact_number, email, reason
# Verificar que el email tiene formato válido
```

#### **2. Error 401 - "Not authenticated"**
```bash
# Verificar que el token es válido para endpoints protegidos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 404 - "Contact not found"**
```bash
# Verificar que el contacto existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **Comandos de Diagnóstico**

#### **Verificar Contactos en Base de Datos**
```sql
-- Ver todos los contactos
SELECT id, first_name, last_name, email, created_at, is_read, is_responded 
FROM t_app_contact;

-- Ver contactos no leídos
SELECT id, first_name, last_name, email, created_at 
FROM t_app_contact 
WHERE is_read = false;

-- Ver contactos no respondidos
SELECT id, first_name, last_name, email, created_at 
FROM t_app_contact 
WHERE is_responded = false;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Contactos**
```sql
-- Total de contactos
SELECT COUNT(*) as total_contacts FROM t_app_contact;

-- Contactos por estado
SELECT is_read, is_responded, COUNT(*) as contact_count 
FROM t_app_contact 
GROUP BY is_read, is_responded;

-- Contactos por mes
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as contact_count
FROM t_app_contact 
GROUP BY month 
ORDER BY month DESC;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **📧 Notificaciones Avanzadas**
   - Notificaciones push
   - Emails personalizados
   - Plantillas de respuesta

2. **📊 Analytics**
   - Métricas de engagement
   - Reportes de contactos
   - Análisis de tendencias

3. **🤖 Automatización**
   - Respuestas automáticas
   - Clasificación de contactos
   - Enrutamiento inteligente

4. **📱 Integración**
   - App móvil
   - CRM integration
   - Slack notifications

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

**¡API de Contacto lista para usar! 📞** 