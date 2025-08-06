# 💬 API de Chat - KidsFun Backend

## 📋 **Resumen**

API para la gestión de salas de chat y mensajes en tiempo real para el sistema KidsFun, permitiendo comunicación entre usuarios y administradores.

### 🎯 **Características Principales**
- ✅ **Salas de Chat** - Creación y gestión de salas
- ✅ **Mensajes en Tiempo Real** - Comunicación instantánea
- ✅ **Autenticación** - Chat vinculado a usuarios
- ✅ **WebSockets** - Conexiones en tiempo real
- ✅ **Historial** - Mensajes persistentes
- ✅ **Notificaciones** - Alertas de nuevos mensajes

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/chat/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_chat_room`**

```sql
CREATE TABLE t_app_chat_room (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    created_by INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### **Tabla: `t_app_chat_message`**

```sql
CREATE TABLE t_app_chat_message (
    id INTEGER PRIMARY KEY,
    room_id INTEGER REFERENCES t_app_chat_room(id),
    user_id INTEGER REFERENCES auth_user(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Tabla: `t_app_chat_administrator`**

```sql
CREATE TABLE t_app_chat_administrator (
    id INTEGER PRIMARY KEY,
    room_id INTEGER REFERENCES t_app_chat_room(id),
    user_id INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🚀 **Endpoints**

### **1. Obtener Salas de Chat - `GET /api/chat/`**

Obtiene una lista de salas de chat (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/chat/
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "name": "Sala General",
    "created_by": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "is_active": true,
    "administrators": [
      {
        "id": 1,
        "user_id": 1,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  },
  {
    "id": 2,
    "name": "Sala de Soporte",
    "created_by": 1,
    "created_at": "2024-01-02T00:00:00Z",
    "is_active": true,
    "administrators": [
      {
        "id": 2,
        "user_id": 2,
        "created_at": "2024-01-02T00:00:00Z"
      }
    ]
  }
]
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **2. Crear Sala de Chat - `POST /api/chat/`**

Crea una nueva sala de chat (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/chat/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "name": "Nueva Sala de Chat"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "name": "Nueva Sala de Chat",
  "created_by": 1,
  "created_at": "2024-01-03T00:00:00Z",
  "is_active": true
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nueva Sala de Chat"
  }'
```

---

### **3. Obtener Sala Específica - `GET /api/chat/{room_id}`**

Obtiene una sala de chat específica (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/chat/{room_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "name": "Sala General",
  "created_by": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "is_active": true,
  "administrators": [
    {
      "id": 1,
      "user_id": 1,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **4. Obtener Mensajes de una Sala - `GET /api/chat/rooms/{room_id}/messages`**

Obtiene los mensajes de una sala específica (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/{room_id}/messages
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `skip` | int | Número de mensajes a saltar | 0 | ❌ |
| `limit` | int | Número máximo de mensajes (1-100) | 50 | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 1,
    "room_id": 1,
    "user_id": 1,
    "content": "Hola, ¿cómo están todos?",
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
    "room_id": 1,
    "user_id": 2,
    "content": "¡Hola! Todo bien, gracias.",
    "created_at": "2024-01-01T00:01:00Z",
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
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/1/messages" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **5. Enviar Mensaje - `POST /api/chat/rooms/{room_id}/messages`**

Envía un mensaje a una sala específica (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/{room_id}/messages
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "content": "Hola, necesito información sobre sus productos"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "room_id": 1,
  "user_id": 1,
  "content": "Hola, necesito información sobre sus productos",
  "created_at": "2024-01-03T00:00:00Z"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/1/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hola, necesito información sobre sus productos"
  }'
```

---

## 🔌 **WebSockets**

### **Conexión WebSocket**

Para mensajes en tiempo real, conecta al endpoint WebSocket:

```
wss://api.kidsfunyfiestasinfantiles.com/ws/chat/{room_id}
```

### **Ejemplo de Conexión JavaScript**

```javascript
class ChatWebSocket {
  constructor(roomId, token) {
    this.roomId = roomId;
    this.token = token;
    this.ws = null;
    this.messageHandlers = [];
  }

  connect() {
    this.ws = new WebSocket(`wss://api.kidsfunyfiestasinfantiles.com/ws/chat/${this.roomId}`);
    
    this.ws.onopen = () => {
      console.log('Conectado al chat');
      // Enviar token de autenticación
      this.ws.send(JSON.stringify({
        type: 'auth',
        token: this.token
      }));
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messageHandlers.forEach(handler => handler(data));
    };

    this.ws.onclose = () => {
      console.log('Desconectado del chat');
    };

    this.ws.onerror = (error) => {
      console.error('Error en WebSocket:', error);
    };
  }

  sendMessage(content) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'message',
        content: content
      }));
    }
  }

  onMessage(handler) {
    this.messageHandlers.push(handler);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Uso
const chat = new ChatWebSocket(1, 'YOUR_TOKEN');
chat.connect();

chat.onMessage((data) => {
  if (data.type === 'message') {
    console.log('Nuevo mensaje:', data.message);
  }
});

// Enviar mensaje
chat.sendMessage('Hola, ¿cómo están?');
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Salas de Chat**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Crear Sala de Chat**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Chat Room"
  }'
```

#### **Obtener Mensajes**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/1/messages" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Enviar Mensaje**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/chat/rooms/1/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Test message"
  }'
```

### **2. Testing con JavaScript**

```javascript
class ChatAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getChatRooms(token) {
    const response = await fetch(`${this.baseURL}/api/chat/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createChatRoom(roomData, token) {
    const response = await fetch(`${this.baseURL}/api/chat/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(roomData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getChatRoom(roomId, token) {
    const response = await fetch(`${this.baseURL}/api/chat/${roomId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getMessages(roomId, token, filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/api/chat/rooms/${roomId}/messages?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async sendMessage(roomId, messageData, token) {
    const response = await fetch(`${this.baseURL}/api/chat/rooms/${roomId}/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(messageData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }
}

// Uso
const chatAPI = new ChatAPI();

// Obtener salas de chat
chatAPI.getChatRooms('YOUR_TOKEN')
  .then(rooms => console.log('Salas de chat:', rooms))
  .catch(error => console.error('Error:', error));

// Crear sala de chat
chatAPI.createChatRoom({
  name: 'Test Chat Room'
}, 'YOUR_TOKEN')
  .then(room => console.log('Sala creada:', room))
  .catch(error => console.error('Error:', error));

// Enviar mensaje
chatAPI.sendMessage(1, {
  content: 'Test message'
}, 'YOUR_TOKEN')
  .then(message => console.log('Mensaje enviado:', message))
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

#### **2. Error 404 - "Chat room not found"**
```bash
# Verificar que la sala existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 403 - "Access denied"**
```bash
# Verificar permisos de acceso a la sala
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/chat/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **Comandos de Diagnóstico**

#### **Verificar Salas de Chat en Base de Datos**
```sql
-- Ver todas las salas
SELECT id, name, created_by, created_at, is_active 
FROM t_app_chat_room;

-- Ver mensajes por sala
SELECT id, room_id, user_id, content, created_at 
FROM t_app_chat_message 
WHERE room_id = 1;

-- Ver administradores
SELECT id, room_id, user_id, created_at 
FROM t_app_chat_administrator;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Chat**
```sql
-- Total de salas
SELECT COUNT(*) as total_rooms FROM t_app_chat_room;

-- Total de mensajes
SELECT COUNT(*) as total_messages FROM t_app_chat_message;

-- Mensajes por sala
SELECT room_id, COUNT(*) as message_count 
FROM t_app_chat_message 
GROUP BY room_id 
ORDER BY message_count DESC;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **🔔 Notificaciones**
   - Notificaciones push
   - Emails de nuevos mensajes
   - Alertas en tiempo real

2. **📊 Analytics**
   - Métricas de uso
   - Reportes de chat
   - Análisis de conversaciones

3. **🛡️ Moderación**
   - Filtros de contenido
   - Sistema de reportes
   - Moderación automática

4. **📱 Móvil**
   - App móvil
   - Notificaciones push
   - Sincronización offline

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

**¡API de Chat lista para usar! 💬** 