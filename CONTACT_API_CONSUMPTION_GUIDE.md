# 📞 Guía de Consumo - API de Contacto KidsFun

## 🎯 **Información Rápida**

- **🌐 Base URL:** `https://api.kidsfunyfiestasinfantiles.com`
- **📞 Endpoint Principal:** `/api/contact/`
- **🔓 Acceso Público:** Sí (para enviar formularios)
- **🔐 Autenticación:** Solo para gestión (admin)

---

## 🚀 **Endpoint Principal - Enviar Formulario**

### **POST** `/api/contact/` (PÚBLICO)

#### **Request**
```http
POST https://api.kidsfunyfiestasinfantiles.com/api/contact/
Content-Type: application/json

{
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles."
}
```

#### **Response (200 OK)**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "contact_number": "+1 (555) 123-4567",
  "email": "juan.perez@ejemplo.com",
  "reason": "Hola, me gustaría obtener información sobre sus servicios de fiestas infantiles.",
  "created_at": "2025-08-06T03:57:42.000000Z",
  "is_read": false,
  "is_responded": false
}
```

---

## 💻 **Ejemplos de Código**

### **JavaScript (Fetch API)**
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
      console.log('✅ Formulario enviado:', result);
      return { success: true, data: result };
    } else {
      const error = await response.json();
      console.error('❌ Error:', error);
      return { success: false, error: error };
    }
  } catch (error) {
    console.error('❌ Error de red:', error);
    return { success: false, error: error };
  }
}

// Ejemplo de uso
const formData = {
  firstName: "Juan",
  lastName: "Pérez",
  contactNumber: "+1 (555) 123-4567",
  email: "juan.perez@ejemplo.com",
  reason: "Hola, me gustaría obtener información sobre sus servicios."
};

submitContactForm(formData).then(result => {
  if (result.success) {
    alert('¡Formulario enviado exitosamente!');
  } else {
    alert('Error al enviar el formulario. Por favor, inténtalo de nuevo.');
  }
});
```

### **JavaScript (Axios)**
```javascript
import axios from 'axios';

async function submitContactForm(formData) {
  try {
    const response = await axios.post('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
      first_name: formData.firstName,
      last_name: formData.lastName,
      contact_number: formData.contactNumber,
      email: formData.email,
      reason: formData.reason
    });

    console.log('✅ Formulario enviado:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
    return { success: false, error: error.response?.data || error.message };
  }
}
```

### **Python (requests)**
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
            print("✅ Formulario enviado exitosamente:", result)
            return {"success": True, "data": result}
        else:
            error = response.json()
            print("❌ Error al enviar formulario:", error)
            return {"success": False, "error": error}
            
    except Exception as e:
        print("❌ Error de red:", str(e))
        return {"success": False, "error": str(e)}

# Ejemplo de uso
result = submit_contact_form(
    first_name="Juan",
    last_name="Pérez",
    contact_number="+1 (555) 123-4567",
    email="juan.perez@ejemplo.com",
    reason="Hola, me gustaría obtener información sobre sus servicios."
)

if result["success"]:
    print("¡Formulario enviado exitosamente!")
else:
    print("Error al enviar el formulario.")
```

### **cURL**
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

---

## 🎨 **Integración Frontend**

### **HTML Formulario Completo**
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

### **React Component**
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

## 🔐 **Endpoints de Administración (Requieren Autenticación)**

### **Obtener Todos los Contactos**
```http
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/
Authorization: Bearer YOUR_TOKEN
```

### **Obtener Contacto Específico**
```http
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/1
Authorization: Bearer YOUR_TOKEN
```

### **Actualizar Contacto**
```http
PUT https://api.kidsfunyfiestasinfantiles.com/api/contact/1
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "is_read": true,
  "is_responded": true
}
```

### **Eliminar Contacto**
```http
DELETE https://api.kidsfunyfiestasinfantiles.com/api/contact/1
Authorization: Bearer YOUR_TOKEN
```

### **Estadísticas de Contactos**
```http
GET https://api.kidsfunyfiestasinfantiles.com/api/contact/stats/summary
Authorization: Bearer YOUR_TOKEN
```

---

## 🚨 **Códigos de Error**

| Código | Descripción | Solución |
|--------|-------------|----------|
| `200` | OK - Request exitosa | - |
| `201` | Created - Contacto creado | - |
| `400` | Bad Request - Datos inválidos | Verificar formato de datos |
| `401` | Unauthorized - Autenticación requerida | Agregar token de autorización |
| `422` | Unprocessable Entity - Error de validación | Verificar campos requeridos |
| `500` | Internal Server Error - Error del servidor | Contactar soporte |

---

## 📊 **Estructura de Datos**

### **Request Body**
```json
{
  "first_name": "string (1-100 chars, required)",
  "last_name": "string (1-100 chars, required)",
  "contact_number": "string (1-20 chars, required)",
  "email": "email (valid format, required)",
  "reason": "string (1+ chars, required)"
}
```

### **Response Body**
```json
{
  "id": "integer (auto-generated)",
  "first_name": "string",
  "last_name": "string",
  "contact_number": "string",
  "email": "string",
  "reason": "string",
  "created_at": "datetime (ISO format)",
  "is_read": "boolean (default: false)",
  "is_responded": "boolean (default: false)"
}
```

---

## 🎯 **Ejemplos de Uso Rápido**

### **JavaScript (Una línea)**
```javascript
fetch('https://api.kidsfunyfiestasinfantiles.com/api/contact/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    first_name: "Juan", last_name: "Pérez", 
    contact_number: "+1 (555) 123-4567", 
    email: "juan@ejemplo.com", 
    reason: "Hola, necesito información."
  })
}).then(r => r.json()).then(console.log);
```

### **cURL (Una línea)**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/contact/" -H "Content-Type: application/json" -d '{"first_name":"Juan","last_name":"Pérez","contact_number":"+1 (555) 123-4567","email":"juan@ejemplo.com","reason":"Hola, necesito información."}'
```

---

## 📞 **Soporte**

- **🌐 Documentación completa:** [CONTACT_API_DOCUMENTATION.md](./CONTACT_API_DOCUMENTATION.md)
- **🔗 Health check:** `https://api.kidsfunyfiestasinfantiles.com/health`
- **📧 Soporte:** soporte@kidsfunyfiestasinfantiles.com

---

**¡Listo para usar la API de Contacto! 🚀** 