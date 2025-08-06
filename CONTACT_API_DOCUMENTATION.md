# 📞 API de Formulario de Contacto - KidsFun

## 📋 Índice
- [Información General](#información-general)
- [Endpoints](#endpoints)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Integración con Frontend](#integración-con-frontend)
- [Notificaciones por Email](#notificaciones-por-email)

---

## 🌐 Información General

### Base URL
```
https://api.kidsfunyfiestasinfantiles.com
```

### Endpoint Principal
```
/api/contact/
```

### Características
- ✅ **Formulario público** - No requiere autenticación para enviar
- ✅ **Notificaciones por email** - Envía email automático al recibir formulario
- ✅ **Gestión de contactos** - Panel de administración para ver y gestionar contactos
- ✅ **Estadísticas** - Resumen de contactos recibidos
- ✅ **Validación de datos** - Validación automática de campos

---

## 🚀 Endpoints

### 1. Crear Formulario de Contacto (PÚBLICO)

#### Request
```http
POST /api/contact/
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
GET /api/contact/
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
GET /api/contact/?is_read=false

# Obtener contactos no respondidos
GET /api/contact/?is_responded=false

# Obtener primeros 10 contactos
GET /api/contact/?limit=10
```

#### Response
```json
[
  {
    "id": 1,
    "first_name": "Juan",
    "last_name": "Pérez",
    "contact_number": "+1 (555) 123-4567",
    "email": "juan.perez@ejemplo.com",
    "reason": "Hola, me gustaría obtener información sobre sus servicios...",
    "created_at": "2025-08-06T02:30:00.000000Z",
    "is_read": false,
    "is_responded": false
  },
  {
    "id": 2,
    "first_name": "María",
    "last_name": "García",
    "contact_number": "+1 (555) 987-6543",
    "email": "maria.garcia@ejemplo.com",
    "reason": "Necesito cotización para una fiesta de cumpleaños...",
    "created_at": "2025-08-06T01:15:00.000000Z",
    "is_read": true,
    "is_responded": false
  }
]
```

### 3. Obtener Contacto Específico (Requiere Autenticación)

#### Request
```http
GET /api/contact/1
Authorization: Bearer {{token}}
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

### 4. Actualizar Contacto (Requiere Autenticación)

#### Request
```http
PUT /api/contact/1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "is_read": true,
  "is_responded": true
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
  "is_read": true,
  "is_responded": true
}
```

### 5. Eliminar Contacto (Requiere Autenticación)

#### Request
```http
DELETE /api/contact/1
Authorization: Bearer {{token}}
```

#### Response
```json
{
  "message": "Contacto eliminado exitosamente"
}
```

### 6. Estadísticas de Contactos (Requiere Autenticación)

#### Request
```http
GET /api/contact/stats/summary
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

## 💡 Ejemplos de Uso

### JavaScript (Fetch API)

#### Enviar Formulario de Contacto
```javascript
async function submitContactForm(formData) {
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        first_name: formData.firstName,
        last_name: formData.lastName,
        contact_number: formData.contactNumber,
        email: formData.email,
        reason: formData.reason
      })
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Formulario enviado exitosamente:', result);
      return { success: true, data: result };
    } else {
      const error = await response.json();
      console.error('Error al enviar formulario:', error);
      return { success: false, error: error };
    }
  } catch (error) {
    console.error('Error de red:', error);
    return { success: false, error: error };
  }
}

// Ejemplo de uso
const formData = {
  firstName: "Juan",
  lastName: "Pérez",
  contactNumber: "+1 (555) 123-4567",
  email: "juan.perez@ejemplo.com",
  reason: "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles."
};

submitContactForm(formData).then(result => {
  if (result.success) {
    alert('¡Formulario enviado exitosamente!');
  } else {
    alert('Error al enviar el formulario. Por favor, inténtalo de nuevo.');
  }
});
```

#### Obtener Contactos (Admin)
```javascript
async function getContacts(token) {
  try {
    const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const contacts = await response.json();
      console.log('Contactos obtenidos:', contacts);
      return contacts;
    } else {
      console.error('Error al obtener contactos');
      return null;
    }
  } catch (error) {
    console.error('Error de red:', error);
    return null;
  }
}
```

### Python (requests)

#### Enviar Formulario de Contacto
```python
import requests
import json

def submit_contact_form(first_name, last_name, contact_number, email, reason):
    url = "https://api.kidsfunyfiestasinfantiles.com/api/contact/"
    
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email": email,
        "reason": reason
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("Formulario enviado exitosamente:", result)
            return {"success": True, "data": result}
        else:
            error = response.json()
            print("Error al enviar formulario:", error)
            return {"success": False, "error": error}
            
    except Exception as e:
        print("Error de red:", str(e))
        return {"success": False, "error": str(e)}

# Ejemplo de uso
result = submit_contact_form(
    first_name="Juan",
    last_name="Pérez",
    contact_number="+1 (555) 123-4567",
    email="juan.perez@ejemplo.com",
    reason="Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles."
)

if result["success"]:
    print("¡Formulario enviado exitosamente!")
else:
    print("Error al enviar el formulario.")
```

### cURL

#### Enviar Formulario de Contacto
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

#### Obtener Contactos (Admin)
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/contact/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🎨 Integración con Frontend

### HTML Formulario de Contacto
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Contacto - KidsFun</title>
    <style>
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-row {
            display: flex;
            gap: 15px;
        }
        
        .form-row .form-group {
            flex: 1;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        
        textarea {
            height: 120px;
            resize: vertical;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="contact-form">
        <h2>📞 Contáctanos</h2>
        <p>¿Tienes alguna pregunta? ¡Nos encantaría escucharte!</p>
        
        <form id="contactForm">
            <div class="form-row">
                <div class="form-group">
                    <label for="firstName">First name</label>
                    <input type="text" id="firstName" name="firstName" required>
                </div>
                <div class="form-group">
                    <label for="lastName">Last name</label>
                    <input type="text" id="lastName" name="lastName" required>
                </div>
            </div>
            
            <div class="form-group">
                <label for="contactNumber">Your Contact Number</label>
                <input type="tel" id="contactNumber" name="contactNumber" 
                       placeholder="+1 (000) 000 - 0000" required>
            </div>
            
            <div class="form-group">
                <label for="email">Your Email</label>
                <input type="email" id="email" name="email" 
                       placeholder="example@mail.com" required>
            </div>
            
            <div class="form-group">
                <label for="reason">Reason</label>
                <textarea id="reason" name="reason" 
                          placeholder="Cuéntanos cómo podemos ayudarte..." required></textarea>
            </div>
            
            <button type="submit" class="submit-btn">Submit</button>
        </form>
        
        <div id="message"></div>
    </div>

    <script>
        document.getElementById('contactForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                first_name: document.getElementById('firstName').value,
                last_name: document.getElementById('lastName').value,
                contact_number: document.getElementById('contactNumber').value,
                email: document.getElementById('email').value,
                reason: document.getElementById('reason').value
            };
            
            try {
                const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('message').innerHTML = 
                        '<div class="success-message">¡Gracias por contactarnos! Te responderemos pronto.</div>';
                    document.getElementById('contactForm').reset();
                } else {
                    document.getElementById('message').innerHTML = 
                        '<div class="error-message">Error al enviar el formulario. Por favor, inténtalo de nuevo.</div>';
                }
            } catch (error) {
                document.getElementById('message').innerHTML = 
                    '<div class="error-message">Error de conexión. Por favor, inténtalo de nuevo.</div>';
            }
        });
    </script>
</body>
</html>
```

### React Component
```jsx
import React, { useState } from 'react';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    contact_number: '',
    email: '',
    reason: ''
  });
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
      const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (response.ok) {
        setMessage('¡Gracias por contactarnos! Te responderemos pronto.');
        setFormData({
          first_name: '',
          last_name: '',
          contact_number: '',
          email: '',
          reason: ''
        });
      } else {
        setMessage('Error al enviar el formulario. Por favor, inténtalo de nuevo.');
      }
    } catch (error) {
      setMessage('Error de conexión. Por favor, inténtalo de nuevo.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="contact-form">
      <h2>📞 Contáctanos</h2>
      <p>¿Tienes alguna pregunta? ¡Nos encantaría escucharte!</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="first_name">First name</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="last_name">Last name</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="contact_number">Your Contact Number</label>
          <input
            type="tel"
            id="contact_number"
            name="contact_number"
            value={formData.contact_number}
            onChange={handleChange}
            placeholder="+1 (000) 000 - 0000"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">Your Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="example@mail.com"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="reason">Reason</label>
          <textarea
            id="reason"
            name="reason"
            value={formData.reason}
            onChange={handleChange}
            placeholder="Cuéntanos cómo podemos ayudarte..."
            required
          />
        </div>
        
        <button type="submit" className="submit-btn" disabled={isSubmitting}>
          {isSubmitting ? 'Enviando...' : 'Submit'}
        </button>
      </form>
      
      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default ContactForm;
```

---

## 📧 Notificaciones por Email

### Configuración Automática
Cuando se envía un formulario de contacto, el sistema automáticamente:

1. **Guarda el contacto** en la base de datos
2. **Envía email de notificación** al administrador
3. **Registra la fecha y hora** del contacto
4. **Marca como no leído** por defecto

### Email de Notificación
```
Asunto: Nuevo formulario de contacto - Juan Pérez

Se ha recibido un nuevo formulario de contacto:

**Información del Contacto:**
- Nombre: Juan Pérez
- Email: juan.perez@ejemplo.com
- Teléfono: +1 (555) 123-4567
- Fecha: 2025-08-06 02:30:00

**Mensaje:**
Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles. ¿Podrían enviarme un catálogo de productos y precios?

---
Este mensaje fue enviado automáticamente desde el formulario de contacto de KidsFun.
```

---

## 🔧 Configuración

### Variables de Entorno
```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### CORS Configuration
```python
# En app/config.py
allowed_origins: List[str] = [
    "http://localhost:4200",
    "https://kidsfunyfiestasinfantiles.com",
    "https://www.kidsfunyfiestasinfantiles.com",
    "https://api.kidsfunyfiestasinfantiles.com"
]
```

---

## 🚨 Códigos de Error

### Códigos HTTP Comunes
- `200` - OK - Request exitosa
- `201` - Created - Contacto creado exitosamente
- `400` - Bad Request - Datos inválidos
- `401` - Unauthorized - Autenticación requerida
- `422` - Unprocessable Entity - Error de validación
- `500` - Internal Server Error - Error del servidor

### Ejemplos de Respuestas de Error
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

---

## 📞 Soporte

### Recursos Útiles
- **Documentación API**: https://api.kidsfunyfiestasinfantiles.com/docs
- **Health Check**: https://api.kidsfunyfiestasinfantiles.com/health
- **Issues**: https://github.com/mrgomezsv/kidsfun_back/issues

### Contacto
- **Email**: soporte@kidsfunyfiestasinfantiles.com

---

**¡Listo para usar la API de Contacto! 🎉** 