# 📋 API de Waivers - KidsFun Backend

## 📋 **Resumen**

API para la gestión de waivers (formularios de consentimiento) en el sistema KidsFun, permitiendo crear, gestionar y validar formularios de consentimiento para participantes.

### 🎯 **Características Principales**
- ✅ **CRUD Completo** - Create, Read, Update, Delete
- ✅ **Códigos QR** - Generación automática de códigos QR
- ✅ **Validación** - Validación de datos y firmas
- ✅ **PDF** - Generación automática de PDFs
- ✅ **Email** - Envío automático de waivers por email
- ✅ **Búsqueda** - Búsqueda por código QR

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/waiver/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_waiver_data`**

```sql
CREATE TABLE t_app_waiver_data (
    id INTEGER PRIMARY KEY,
    participant_name VARCHAR(200) NOT NULL,
    participant_age INTEGER NOT NULL,
    emergency_contact VARCHAR(200) NOT NULL,
    emergency_phone VARCHAR(50) NOT NULL,
    medical_conditions TEXT,
    signature VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    qr_code VARCHAR(255) UNIQUE,
    is_valid BOOLEAN DEFAULT TRUE
);
```

### **Tabla: `t_app_waiver_validator`**

```sql
CREATE TABLE t_app_waiver_validator (
    id INTEGER PRIMARY KEY,
    waiver_id INTEGER REFERENCES t_app_waiver_data(id),
    validated_by INTEGER REFERENCES auth_user(id),
    validated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT
);
```

---

## 🚀 **Endpoints**

### **1. Obtener Waivers - `GET /api/waiver/`**

Obtiene una lista de waivers (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/waiver/
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
    "participant_name": "Juan Pérez",
    "participant_age": 25,
    "emergency_contact": "María Pérez",
    "emergency_phone": "123-456-7890",
    "medical_conditions": "Ninguna",
    "signature": "Juan Pérez",
    "created_at": "2024-01-01T00:00:00Z",
    "qr_code": "waiver_123456",
    "is_valid": true
  },
  {
    "id": 2,
    "participant_name": "Ana García",
    "participant_age": 30,
    "emergency_contact": "Carlos García",
    "emergency_phone": "098-765-4321",
    "medical_conditions": "Alergia a polen",
    "signature": "Ana García",
    "created_at": "2024-01-02T00:00:00Z",
    "qr_code": "waiver_789012",
    "is_valid": true
  }
]
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **2. Crear Waiver - `POST /api/waiver/`**

Crea un nuevo waiver (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/waiver/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "participant_name": "Nuevo Participante",
  "participant_age": 28,
  "emergency_contact": "Contacto de Emergencia",
  "emergency_phone": "555-123-4567",
  "medical_conditions": "Ninguna condición médica",
  "signature": "Nuevo Participante"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 3,
  "participant_name": "Nuevo Participante",
  "participant_age": 28,
  "emergency_contact": "Contacto de Emergencia",
  "emergency_phone": "555-123-4567",
  "medical_conditions": "Ninguna condición médica",
  "signature": "Nuevo Participante",
  "created_at": "2024-01-03T00:00:00Z",
  "qr_code": "waiver_345678",
  "is_valid": true
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/waiver/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "Nuevo Participante",
    "participant_age": 28,
    "emergency_contact": "Contacto de Emergencia",
    "emergency_phone": "555-123-4567",
    "medical_conditions": "Ninguna condición médica",
    "signature": "Nuevo Participante"
  }'
```

---

### **3. Obtener Waiver por QR - `GET /api/waiver/{qr_code}`**

Obtiene un waiver específico por su código QR (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/waiver/{qr_code}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "participant_name": "Juan Pérez",
  "participant_age": 25,
  "emergency_contact": "María Pérez",
  "emergency_phone": "123-456-7890",
  "medical_conditions": "Ninguna",
  "signature": "Juan Pérez",
  "created_at": "2024-01-01T00:00:00Z",
  "qr_code": "waiver_123456",
  "is_valid": true
}
```

#### **Response Error (404)**
```json
{
  "detail": "Waiver not found"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/waiver_123456" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **4. Validar Waiver - `POST /api/waiver/{waiver_id}/validate`**

Valida un waiver existente (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/waiver/{waiver_id}/validate
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "notes": "Waiver validado correctamente"
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "waiver_id": 1,
  "validated_by": 1,
  "validated_at": "2024-01-03T00:00:00Z",
  "notes": "Waiver validado correctamente"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/waiver/1/validate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Waiver validado correctamente"
  }'
```

---

### **5. Generar PDF - `GET /api/waiver/{waiver_id}/pdf`**

Genera un PDF del waiver (requiere autenticación).

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/waiver/{waiver_id}/pdf
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (200)**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="waiver_1.pdf"

[Contenido del PDF]
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/1/pdf" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o waiver_1.pdf
```

---

### **6. Enviar Email - `POST /api/waiver/{waiver_id}/email`**

Envía el waiver por email (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/waiver/{waiver_id}/email
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "email": "participante@ejemplo.com",
  "subject": "Tu Waiver de KidsFun"
}
```

#### **Response Exitosa (200)**
```json
{
  "message": "Waiver enviado por email correctamente",
  "email": "participante@ejemplo.com"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/waiver/1/email" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "participante@ejemplo.com",
    "subject": "Tu Waiver de KidsFun"
  }'
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Waivers**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Crear Waiver**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/waiver/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "Test Participant",
    "participant_age": 25,
    "emergency_contact": "Test Emergency Contact",
    "emergency_phone": "555-123-4567",
    "medical_conditions": "None",
    "signature": "Test Participant"
  }'
```

#### **Obtener Waiver por QR**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/waiver_123456" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Validar Waiver**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/waiver/1/validate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Test validation"
  }'
```

### **2. Testing con JavaScript**

```javascript
class WaiverAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getWaivers(token) {
    const response = await fetch(`${this.baseURL}/api/waiver/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createWaiver(waiverData, token) {
    const response = await fetch(`${this.baseURL}/api/waiver/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(waiverData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getWaiverByQR(qrCode, token) {
    const response = await fetch(`${this.baseURL}/api/waiver/${qrCode}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async validateWaiver(waiverId, validationData, token) {
    const response = await fetch(`${this.baseURL}/api/waiver/${waiverId}/validate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(validationData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async generatePDF(waiverId, token) {
    const response = await fetch(`${this.baseURL}/api/waiver/${waiverId}/pdf`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.blob();
  }

  async sendEmail(waiverId, emailData, token) {
    const response = await fetch(`${this.baseURL}/api/waiver/${waiverId}/email`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(emailData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }
}

// Uso
const waiverAPI = new WaiverAPI();

// Obtener waivers
waiverAPI.getWaivers('YOUR_TOKEN')
  .then(waivers => console.log('Waivers:', waivers))
  .catch(error => console.error('Error:', error));

// Crear waiver
waiverAPI.createWaiver({
  participant_name: 'Test Participant',
  participant_age: 25,
  emergency_contact: 'Test Emergency Contact',
  emergency_phone: '555-123-4567',
  medical_conditions: 'None',
  signature: 'Test Participant'
}, 'YOUR_TOKEN')
  .then(waiver => console.log('Waiver creado:', waiver))
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

#### **2. Error 404 - "Waiver not found"**
```bash
# Verificar que el waiver existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/waiver/waiver_999999" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 422 - "Validation error"**
```bash
# Verificar que todos los campos requeridos están presentes
# Campos requeridos: participant_name, participant_age, emergency_contact, emergency_phone, signature
```

### **Comandos de Diagnóstico**

#### **Verificar Waivers en Base de Datos**
```sql
-- Ver todos los waivers
SELECT id, participant_name, participant_age, qr_code, is_valid 
FROM t_app_waiver_data;

-- Ver waivers válidos
SELECT id, participant_name, qr_code 
FROM t_app_waiver_data 
WHERE is_valid = true;

-- Ver validaciones
SELECT id, waiver_id, validated_by, validated_at 
FROM t_app_waiver_validator;
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Estadísticas de Waivers**
```sql
-- Total de waivers
SELECT COUNT(*) as total_waivers FROM t_app_waiver_data;

-- Waivers por estado
SELECT is_valid, COUNT(*) as waiver_count 
FROM t_app_waiver_data 
GROUP BY is_valid;

-- Waivers por edad
SELECT 
  CASE 
    WHEN participant_age < 18 THEN 'Menor de 18'
    WHEN participant_age BETWEEN 18 AND 30 THEN '18-30'
    WHEN participant_age BETWEEN 31 AND 50 THEN '31-50'
    ELSE 'Mayor de 50'
  END as age_group,
  COUNT(*) as count
FROM t_app_waiver_data 
GROUP BY age_group;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **📱 App Móvil**
   - Escáner de códigos QR
   - Firma digital
   - Notificaciones push

2. **📊 Analytics**
   - Métricas de uso
   - Reportes de waivers
   - Análisis de tendencias

3. **🛡️ Seguridad**
   - Encriptación de datos
   - Auditoría de cambios
   - Backup automático

4. **🔔 Notificaciones**
   - Recordatorios de waivers
   - Notificaciones de validación
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

**¡API de Waivers lista para usar! 📋** 