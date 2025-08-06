# 🎉 API de Eventos - KidsFun Backend

## 📋 **Resumen**

API para la gestión de eventos de KidsFun, permitiendo crear, gestionar y consultar eventos de fiestas infantiles.

### 🎯 **Características Principales**
- ✅ **CRUD Completo** - Create, Read, Update, Delete
- ✅ **Filtros por Estado** - Eventos publicados/privados
- ✅ **Autenticación** - Eventos vinculados a organizadores
- ✅ **Validación** - Validación de fechas y datos
- ✅ **Precios** - Gestión de precios de entradas
- ✅ **Ubicaciones** - Gestión de ubicaciones de eventos

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/events/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_event`**

```sql
CREATE TABLE t_app_event (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(200) NOT NULL,
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    organizer_id INTEGER REFERENCES auth_user(id),
    ticket_price NUMERIC(10,2) DEFAULT 0.00,
    published BOOLEAN DEFAULT FALSE,
    partners VARCHAR(50) NOT NULL
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | INTEGER | ID único del evento | ✅ |
| `title` | VARCHAR(200) | Título del evento | ✅ |
| `description` | TEXT | Descripción del evento | ✅ |
| `location` | VARCHAR(200) | Ubicación del evento | ✅ |
| `start_datetime` | TIMESTAMP | Fecha y hora de inicio | ✅ |
| `organizer_id` | INTEGER | ID del organizador | ✅ |
| `ticket_price` | NUMERIC(10,2) | Precio de la entrada | ❌ |
| `published` | BOOLEAN | Estado de publicación | ❌ |
| `partners` | VARCHAR(50) | Socios/colaboradores | ✅ |

---

## 🚀 **Endpoints**

### **1. Obtener Eventos - `GET /api/events/`**

Obtiene una lista de eventos con filtros opcionales.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/events/
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `skip` | int | Número de eventos a saltar | 0 | ❌ |
| `limit` | int | Número máximo de eventos (1-100) | 100 | ❌ |
| `published` | boolean | Filtrar por estado de publicación | - | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "title": "Fiesta de Cumpleaños Temática",
    "description": "Fiesta de cumpleaños con tema de superhéroes",
    "location": "Parque Central",
    "start_datetime": "2024-12-25T15:00:00Z",
    "organizer_id": 1,
    "ticket_price": "50.00",
    "published": true,
    "partners": "partner1"
  },
  {
    "id": 2,
    "title": "Evento de Verano",
    "description": "Evento especial de verano para niños",
    "location": "Playa del Sol",
    "start_datetime": "2024-07-15T10:00:00Z",
    "organizer_id": 1,
    "ticket_price": "30.00",
    "published": false,
    "partners": "partner2"
  }
]
```

#### **Ejemplo con cURL**
```bash
# Obtener todos los eventos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/"

# Obtener solo eventos publicados
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/?published=true"

# Obtener eventos con paginación
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/?skip=0&limit=10"
```

#### **Ejemplo con JavaScript**
```javascript
async function getEvents(filters = {}) {
  const params = new URLSearchParams(filters);
  const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/events/?${params}`);
  
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch events');
  }
}

// Uso
getEvents({ published: true, limit: 10 })
  .then(events => console.log('Eventos:', events))
  .catch(error => console.error('Error:', error));
```

---

### **2. Obtener Evento por ID - `GET /api/events/{event_id}`**

Obtiene un evento específico por su ID.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/events/{event_id}
```

#### **Parámetros de Path**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `event_id` | int | ID del evento |

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "title": "Fiesta de Cumpleaños Temática",
  "description": "Fiesta de cumpleaños con tema de superhéroes",
  "location": "Parque Central",
  "start_datetime": "2024-12-25T15:00:00Z",
  "organizer_id": 1,
  "ticket_price": "50.00",
  "published": true,
  "partners": "partner1"
}
```

#### **Response Error (404)**
```json
{
  "detail": "Event not found"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/1"
```

---

### **3. Crear Evento - `POST /api/events/`**

Crea un nuevo evento (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/events/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "title": "Nuevo Evento",
  "description": "Descripción del nuevo evento",
  "location": "Nueva Ubicación",
  "start_datetime": "2024-12-25T15:00:00Z",
  "ticket_price": "75.00",
  "published": true,
  "partners": "partner1"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "title": "Nuevo Evento",
  "description": "Descripción del nuevo evento",
  "location": "Nueva Ubicación",
  "start_datetime": "2024-12-25T15:00:00Z",
  "organizer_id": 1,
  "ticket_price": "75.00",
  "published": true,
  "partners": "partner1"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/events/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nuevo Evento",
    "description": "Descripción del nuevo evento",
    "location": "Nueva Ubicación",
    "start_datetime": "2024-12-25T15:00:00Z",
    "ticket_price": "75.00",
    "published": true,
    "partners": "partner1"
  }'
```

---

### **4. Actualizar Evento - `PUT /api/events/{event_id}`**

Actualiza un evento existente (requiere autenticación).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/events/{event_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "title": "Evento Actualizado",
  "description": "Nueva descripción del evento",
  "location": "Nueva Ubicación",
  "start_datetime": "2024-12-25T16:00:00Z",
  "ticket_price": "100.00",
  "published": true
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "title": "Evento Actualizado",
  "description": "Nueva descripción del evento",
  "location": "Nueva Ubicación",
  "start_datetime": "2024-12-25T16:00:00Z",
  "organizer_id": 1,
  "ticket_price": "100.00",
  "published": true,
  "partners": "partner1"
}
```

#### **Ejemplo con cURL**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/events/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evento Actualizado",
    "description": "Nueva descripción del evento",
    "location": "Nueva Ubicación",
    "start_datetime": "2024-12-25T16:00:00Z",
    "ticket_price": "100.00",
    "published": true
  }'
```

---

### **5. Eliminar Evento - `DELETE /api/events/{event_id}`**

Elimina un evento (requiere autenticación).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/events/{event_id}
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
curl -X DELETE "https://api.kidsfunyfiestasinfantiles.com/api/events/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Eventos**
```bash
# Obtener todos los eventos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/"

# Obtener solo eventos publicados
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/?published=true"

# Obtener evento específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/1"
```

#### **Crear Evento**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/events/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Event",
    "description": "Test event description",
    "location": "Test Location",
    "start_datetime": "2024-12-25T15:00:00Z",
    "ticket_price": "50.00",
    "published": true,
    "partners": "test_partner"
  }'
```

#### **Actualizar Evento**
```bash
curl -X PUT "https://api.kidsfunyfiestasinfantiles.com/api/events/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Test Event",
    "description": "Updated test event description",
    "location": "Updated Test Location",
    "start_datetime": "2024-12-25T16:00:00Z",
    "ticket_price": "75.00",
    "published": true
  }'
```

### **2. Testing con JavaScript**

```javascript
class EventsAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getEvents(filters = {}, token = null) {
    const params = new URLSearchParams(filters);
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    
    const response = await fetch(`${this.baseURL}/api/events/?${params}`, {
      headers
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getEvent(id, token = null) {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    
    const response = await fetch(`${this.baseURL}/api/events/${id}`, {
      headers
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createEvent(eventData, token) {
    const response = await fetch(`${this.baseURL}/api/events/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(eventData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateEvent(id, eventData, token) {
    const response = await fetch(`${this.baseURL}/api/events/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(eventData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteEvent(id, token) {
    const response = await fetch(`${this.baseURL}/api/events/${id}`, {
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
const eventsAPI = new EventsAPI();

// Obtener eventos
eventsAPI.getEvents({ published: true })
  .then(events => console.log('Eventos:', events))
  .catch(error => console.error('Error:', error));

// Crear evento
eventsAPI.createEvent({
  title: 'Test Event',
  description: 'Test event description',
  location: 'Test Location',
  start_datetime: '2024-12-25T15:00:00Z',
  ticket_price: '50.00',
  published: true,
  partners: 'test_partner'
}, 'YOUR_TOKEN')
  .then(event => console.log('Evento creado:', event))
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

#### **2. Error 404 - "Event not found"**
```bash
# Verificar que el evento existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/events/999"
```

#### **3. Error 422 - "Validation error"**
```bash
# Verificar que todos los campos requeridos están presentes
# Campos requeridos: title, description, location, start_datetime, partners
```

### **Comandos de Diagnóstico**

#### **Verificar Eventos en Base de Datos**
```sql
-- Ver todos los eventos
SELECT id, title, location, start_datetime, published 
FROM t_app_event;

-- Ver eventos publicados
SELECT id, title, location, start_datetime 
FROM t_app_event 
WHERE published = true;

-- Ver eventos por organizador
SELECT id, title, location, start_datetime 
FROM t_app_event 
WHERE organizer_id = 1;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Eventos**
```sql
-- Total de eventos
SELECT COUNT(*) as total_events FROM t_app_event;

-- Eventos por estado
SELECT published, COUNT(*) as event_count 
FROM t_app_event 
GROUP BY published;

-- Eventos por organizador
SELECT organizer_id, COUNT(*) as event_count 
FROM t_app_event 
GROUP BY organizer_id 
ORDER BY event_count DESC;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **📅 Calendario**
   - Vista de calendario de eventos
   - Filtros por fecha
   - Eventos recurrentes

2. **🎫 Sistema de Entradas**
   - Compra de entradas
   - Gestión de asistentes
   - Códigos QR

3. **📊 Analytics**
   - Métricas de asistencia
   - Reportes de eventos
   - Análisis de tendencias

4. **🔔 Notificaciones**
   - Recordatorios de eventos
   - Notificaciones push
   - Emails automáticos

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

**¡API de Eventos lista para usar! 🎉** 