# 🔐 API de Autenticación - KidsFun Backend

## 📋 **Resumen**

Sistema completo de autenticación basado en JWT (JSON Web Tokens) que utiliza la tabla `auth_user` para gestionar usuarios y credenciales.

### 🎯 **Características Principales**
- ✅ **JWT Authentication** - Tokens seguros y temporales
- ✅ **bcrypt Password Hashing** - Contraseñas encriptadas
- ✅ **User Management** - CRUD completo de usuarios
- ✅ **Session Management** - Gestión de sesiones
- ✅ **Security Headers** - Headers de seguridad
- ✅ **Rate Limiting** - Protección contra ataques

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Versión**
```
v1.0.0
```

### **Formato de Respuesta**
Todas las respuestas están en formato JSON con la siguiente estructura:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
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

| Campo | Tipo | Descripción | Requerido | Único |
|-------|------|-------------|-----------|-------|
| `id` | INTEGER | ID único del usuario | ✅ | ✅ |
| `password` | VARCHAR | Contraseña hasheada | ✅ | ❌ |
| `last_login` | TIMESTAMP | Último login del usuario | ❌ | ❌ |
| `is_superuser` | BOOLEAN | Es superusuario | ❌ | ❌ |
| `username` | VARCHAR(150) | Nombre de usuario | ✅ | ✅ |
| `first_name` | VARCHAR(150) | Nombre del usuario | ✅ | ❌ |
| `last_name` | VARCHAR(150) | Apellido del usuario | ✅ | ❌ |
| `email` | VARCHAR(254) | Email del usuario | ✅ | ✅ |
| `is_staff` | BOOLEAN | Es staff | ❌ | ❌ |
| `is_active` | BOOLEAN | Usuario activo | ❌ | ❌ |
| `date_joined` | TIMESTAMP | Fecha de registro | ❌ | ❌ |

---

## 🔐 **Endpoints de Autenticación**

### **1. Login - `POST /api/auth/login`**

Autentica un usuario y devuelve un token JWT.

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/auth/login
```

#### **Headers**
```http
Content-Type: application/x-www-form-urlencoded
```

#### **Body (Form Data)**
```http
username=tu_usuario&password=tu_password
```

#### **Body (JSON - Alternativo)**
```json
{
  "username": "tu_usuario",
  "password": "tu_password"
}
```

#### **Response Exitosa (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0dV91c3VhcmlvIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "tu_usuario",
    "email": "usuario@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_superuser": false,
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

#### **Response Error (401)**
```json
{
  "detail": "Incorrect username or password"
}
```

#### **Response Error (422)**
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### **Ejemplo con JavaScript**
```javascript
async function login(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/login', {
    method: 'POST',
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  } else {
    throw new Error('Login failed');
  }
}

// Uso
login('admin', 'admin123')
  .then(data => console.log('Login exitoso:', data))
  .catch(error => console.error('Error:', error));
```

---

### **2. Register - `POST /api/auth/register`**

Registra un nuevo usuario en el sistema.

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/auth/register
```

#### **Headers**
```http
Content-Type: application/json
```

#### **Body**
```json
{
  "username": "nuevo_usuario",
  "email": "nuevo@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "password": "password123"
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 2,
  "username": "nuevo_usuario",
  "email": "nuevo@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_superuser": false,
  "is_staff": false,
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

#### **Response Error (400)**
```json
{
  "detail": "Username already registered"
}
```

```json
{
  "detail": "Email already registered"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "nuevo@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "password": "password123"
  }'
```

#### **Ejemplo con JavaScript**
```javascript
async function register(userData) {
  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  });

  if (response.ok) {
    return await response.json();
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
}

// Uso
const userData = {
  username: 'nuevo_usuario',
  email: 'nuevo@ejemplo.com',
  first_name: 'Juan',
  last_name: 'Pérez',
  password: 'password123'
};

register(userData)
  .then(user => console.log('Usuario registrado:', user))
  .catch(error => console.error('Error:', error));
```

---

### **3. Me - `GET /api/auth/me`**

Obtiene la información del usuario autenticado.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/auth/me
```

#### **Headers**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### **Response Exitosa (200)**
```json
{
  "id": 1,
  "username": "tu_usuario",
  "email": "usuario@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_superuser": false,
  "is_staff": false,
  "is_active": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

#### **Response Error (401)**
```json
{
  "detail": "Could not validate credentials"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

#### **Ejemplo con JavaScript**
```javascript
async function getProfile() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    throw new Error('No token available');
  }

  const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to get profile');
  }
}

// Uso
getProfile()
  .then(profile => console.log('Perfil:', profile))
  .catch(error => console.error('Error:', error));
```

---

## 🔧 **Implementación Técnica**

### **Archivos Principales**

#### **1. Modelo de Usuario - `app/models/user.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "auth_user"
    
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_superuser = Column(Boolean, default=False)
    username = Column(String(150), unique=True, index=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="user")
```

#### **2. Router de Autenticación - `app/routers/auth.py`**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserLogin, Token, UserCreate, UserResponse
from ..config import settings

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

#### **3. Esquemas Pydantic - `app/schemas/user.py`**
```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=150)
    last_name: str = Field(..., min_length=1, max_length=150)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=150)
    last_name: Optional[str] = Field(None, min_length=1, max_length=150)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
```

---

## 🔒 **Seguridad**

### **Características de Seguridad Implementadas**

1. **🔐 Hash de Contraseñas**
   - Algoritmo: bcrypt
   - Salt automático
   - Costo configurable

2. **🎫 JWT Tokens**
   - Algoritmo: HS256
   - Expiración: 30 minutos (configurable)
   - Payload seguro

3. **🛡️ Rate Limiting**
   - Límite: 10 requests/segundo por IP
   - Ventana: 1 segundo
   - Protección contra ataques

4. **🔒 Headers de Seguridad**
   - HSTS
   - CSP
   - X-Frame-Options
   - X-Content-Type-Options

5. **✅ Validación de Datos**
   - Pydantic schemas
   - Validación de email
   - Longitud de contraseñas

### **Configuración de Seguridad**

```python
# app/config.py
class Settings(BaseSettings):
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:4200",
        "https://kidsfunyfiestasinfantiles.com",
        "https://www.kidsfunyfiestasinfantiles.com"
    ]
```

---

## 📊 **Ejemplos de Uso Completo**

### **1. Flujo Completo de Autenticación**

#### **Paso 1: Registro**
```javascript
// Registrar un nuevo usuario
const userData = {
  username: 'nuevo_usuario',
  email: 'nuevo@ejemplo.com',
  first_name: 'Juan',
  last_name: 'Pérez',
  password: 'password123'
};

const response = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(userData)
});

const user = await response.json();
console.log('Usuario registrado:', user);
```

#### **Paso 2: Login**
```javascript
// Hacer login
const formData = new FormData();
formData.append('username', 'nuevo_usuario');
formData.append('password', 'password123');

const loginResponse = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/login', {
  method: 'POST',
  body: formData
});

const authData = await loginResponse.json();
localStorage.setItem('token', authData.access_token);
localStorage.setItem('user', JSON.stringify(authData.user));
```

#### **Paso 3: Usar Token**
```javascript
// Obtener perfil del usuario
const token = localStorage.getItem('token');
const profileResponse = await fetch('https://api.kidsfunyfiestasinfantiles.com/api/auth/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const profile = await profileResponse.json();
console.log('Perfil:', profile);
```

### **2. Clase de Autenticación**

```javascript
class KidsFunAuth {
  constructor() {
    this.baseURL = 'https://api.kidsfunyfiestasinfantiles.com';
    this.token = localStorage.getItem('kidsfun_token');
    this.user = JSON.parse(localStorage.getItem('kidsfun_user') || 'null');
  }

  async login(username, password) {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${this.baseURL}/api/auth/login`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
      }

      const data = await response.json();
      this.setTokens(data.access_token, data.user);
      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
      }

      return await response.json();
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  }

  async getProfile() {
    if (!this.token) {
      throw new Error('No token available');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to get profile');
      }

      return await response.json();
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  }

  setTokens(accessToken, user) {
    this.token = accessToken;
    this.user = user;
    localStorage.setItem('kidsfun_token', accessToken);
    localStorage.setItem('kidsfun_user', JSON.stringify(user));
  }

  logout() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('kidsfun_token');
    localStorage.removeItem('kidsfun_user');
  }

  isAuthenticated() {
    return !!this.token;
  }

  getToken() {
    return this.token;
  }

  getUser() {
    return this.user;
  }
}

// Uso
const auth = new KidsFunAuth();

// Login
auth.login('admin', 'admin123')
  .then(data => console.log('Login exitoso:', data))
  .catch(error => console.error('Error:', error));

// Verificar si está autenticado
if (auth.isAuthenticated()) {
  console.log('Usuario autenticado:', auth.getUser());
}
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Test de Login**
```bash
# Test de login exitoso
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" \
  -v

# Test de login fallido
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=wrongpassword" \
  -v
```

#### **Test de Registro**
```bash
# Test de registro exitoso
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@ejemplo.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123"
  }' \
  -v
```

#### **Test de Perfil**
```bash
# Test de perfil (requiere token)
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -v
```

### **2. Testing con Postman**

#### **Collection de Postman**
```json
{
  "info": {
    "name": "KidsFun Auth API",
    "description": "API de autenticación para KidsFun Backend"
  },
  "item": [
    {
      "name": "🔐 Authentication",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/x-www-form-urlencoded"
              }
            ],
            "body": {
              "mode": "urlencoded",
              "urlencoded": [
                {
                  "key": "username",
                  "value": "admin",
                  "type": "text"
                },
                {
                  "key": "password",
                  "value": "admin123",
                  "type": "text"
                }
              ]
            },
            "url": {
              "raw": "{{base_url}}/api/auth/login",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "login"]
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "if (pm.response.code === 200) {",
                  "    const response = pm.response.json();",
                  "    pm.environment.set('token', response.access_token);",
                  "    pm.environment.set('user_id', response.user.id);",
                  "    ",
                  "    console.log('Token guardado:', response.access_token);",
                  "    console.log('User ID guardado:', response.user.id);",
                  "}"
                ]
              }
            }
          ]
        },
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"nuevo_usuario\",\n  \"email\": \"nuevo@ejemplo.com\",\n  \"first_name\": \"Juan\",\n  \"last_name\": \"Pérez\",\n  \"password\": \"password123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/auth/register",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "register"]
            }
          }
        },
        {
          "name": "Get Profile",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/auth/me",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "me"]
            }
          }
        }
      ]
    }
  ]
}
```

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Error 401 - "Incorrect username or password"**
```bash
# Verificar que el usuario existe
psql -U kidsfun -d kidsfun_db -c "SELECT username, email FROM auth_user WHERE username = 'tu_usuario';"

# Verificar que la contraseña es correcta
# Las contraseñas están hasheadas con bcrypt
```

#### **2. Error 422 - "field required"**
```bash
# Verificar que todos los campos requeridos están presentes
# Para login: username y password
# Para register: username, email, first_name, last_name, password
```

#### **3. Error 400 - "Username already registered"**
```bash
# Verificar si el usuario ya existe
psql -U kidsfun -d kidsfun_db -c "SELECT username FROM auth_user WHERE username = 'nuevo_usuario';"
```

#### **4. Error 400 - "Email already registered"**
```bash
# Verificar si el email ya existe
psql -U kidsfun -d kidsfun_db -c "SELECT email FROM auth_user WHERE email = 'nuevo@ejemplo.com';"
```

### **Comandos de Diagnóstico**

#### **Verificar Tabla auth_user**
```sql
-- Ver estructura de la tabla
\d auth_user

-- Ver usuarios existentes
SELECT id, username, email, is_active, date_joined FROM auth_user;

-- Ver último login
SELECT username, last_login FROM auth_user WHERE last_login IS NOT NULL;
```

#### **Verificar Logs**
```bash
# Ver logs del backend
sudo journalctl -u kidsfun-backend -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/kidsfun-backend-access.log
sudo tail -f /var/log/nginx/kidsfun-backend-error.log
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Security Info**
```bash
curl https://api.kidsfunyfiestasinfantiles.com/security-info
```

### **Métricas de Uso**

#### **Usuarios Activos**
```sql
SELECT COUNT(*) as active_users FROM auth_user WHERE is_active = true;
```

#### **Últimos Logins**
```sql
SELECT username, last_login 
FROM auth_user 
WHERE last_login IS NOT NULL 
ORDER BY last_login DESC 
LIMIT 10;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **🔄 Refresh Tokens**
   - Implementar refresh tokens para renovación automática
   - Mejorar la experiencia de usuario

2. **📧 Email Verification**
   - Verificación de email al registrarse
   - Recuperación de contraseña

3. **🔐 Two-Factor Authentication**
   - Autenticación de dos factores
   - Códigos SMS/Email

4. **📊 Analytics**
   - Tracking de logins
   - Métricas de uso

5. **🛡️ Advanced Security**
   - Rate limiting por usuario
   - Detección de ataques
   - Logs de seguridad

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
- [Backend Deployment Guide](./BACKEND_DEPLOYMENT_GUIDE.md)

---

**¡API de Autenticación lista para usar! 🔐** 