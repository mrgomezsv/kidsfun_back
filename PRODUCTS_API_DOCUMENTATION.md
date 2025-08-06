# 🎪 API de Productos - KidsFun Backend

## 📋 **Resumen**

API completa para la gestión de productos de KidsFun, incluyendo imágenes, categorías, precios, dimensiones y metadatos.

### 🎯 **Características Principales**
- ✅ **CRUD Completo** - Create, Read, Update, Delete
- ✅ **Múltiples Imágenes** - Hasta 6 imágenes por producto
- ✅ **Filtros Avanzados** - Por categoría, búsqueda, estado
- ✅ **YouTube Integration** - URLs de videos
- ✅ **Paginación** - Limit y offset
- ✅ **Estadísticas** - Conteos de likes y comentarios
- ✅ **Upload de Imágenes** - Subida de archivos

---

## 🌐 **Información General**

### **Base URL**
```
https://api.kidsfunyfiestasinfantiles.com
```

### **Endpoint Principal**
```
/api/products/
```

### **Versión**
```
v1.0.0
```

---

## 🗄️ **Estructura de la Base de Datos**

### **Tabla: `t_app_product_product`**

```sql
CREATE TABLE t_app_product_product (
    id BIGINT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    category VARCHAR(50) NOT NULL,
    created TIMESTAMP WITH TIME ZONE NOT NULL,
    publicated BOOLEAN NOT NULL,
    user_id INTEGER REFERENCES auth_user(id),
    img VARCHAR(100) NOT NULL,
    img1 VARCHAR(100) NOT NULL,
    img2 VARCHAR(100) NOT NULL,
    img3 VARCHAR(100) NOT NULL,
    img4 VARCHAR(100) NOT NULL,
    img5 VARCHAR(100) NOT NULL,
    dimensions VARCHAR(50),
    youtube_url VARCHAR(255),
    circuits VARCHAR(50),
    space VARCHAR(50)
);
```

### **Campos de la Tabla**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | BIGINT | ID único del producto | ✅ |
| `title` | VARCHAR(100) | Título del producto | ✅ |
| `description` | TEXT | Descripción del producto | ❌ |
| `price` | NUMERIC(10,2) | Precio del producto | ❌ |
| `category` | VARCHAR(50) | Categoría del producto | ✅ |
| `created` | TIMESTAMP | Fecha de creación | ✅ |
| `publicated` | BOOLEAN | Estado de publicación | ✅ |
| `user_id` | INTEGER | ID del usuario creador | ✅ |
| `img` | VARCHAR(100) | Imagen principal | ✅ |
| `img1` | VARCHAR(100) | Imagen secundaria 1 | ✅ |
| `img2` | VARCHAR(100) | Imagen secundaria 2 | ✅ |
| `img3` | VARCHAR(100) | Imagen secundaria 3 | ✅ |
| `img4` | VARCHAR(100) | Imagen secundaria 4 | ✅ |
| `img5` | VARCHAR(100) | Imagen secundaria 5 | ✅ |
| `dimensions` | VARCHAR(50) | Dimensiones del producto | ❌ |
| `youtube_url` | VARCHAR(255) | URL de video de YouTube | ❌ |
| `circuits` | VARCHAR(50) | Circuitos del producto | ❌ |
| `space` | VARCHAR(50) | Espacio requerido | ❌ |

---

## 🚀 **Endpoints**

### **1. Obtener Productos - `GET /api/products/`**

Obtiene una lista de productos con filtros opcionales.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/products/
```

#### **Parámetros de Query**
| Parámetro | Tipo | Descripción | Default | Requerido |
|-----------|------|-------------|---------|-----------|
| `skip` | int | Número de productos a saltar | 0 | ❌ |
| `limit` | int | Número máximo de productos (1-100) | 100 | ❌ |
| `category` | string | Filtrar por categoría | - | ❌ |
| `search` | string | Buscar en título | - | ❌ |
| `publicated` | boolean | Filtrar por estado de publicación | - | ❌ |

#### **Response Exitosa (200)**
```json
[
  {
    "id": 26,
    "title": "Castillo Inflable",
    "description": "Castillo inflable para fiestas infantiles",
    "price": "150.00",
    "category": "Inflables",
    "created": "2024-01-01T00:00:00Z",
    "publicated": true,
    "user_id": 1,
    "youtube_url": "https://youtube.com/watch?v=example",
    "img": "product_images/castillo_principal.jpg",
    "img1": "product_images/castillo_1.jpg",
    "img2": "product_images/castillo_2.jpg",
    "img3": "product_images/castillo_3.jpg",
    "img4": "product_images/castillo_4.jpg",
    "img5": "product_images/castillo_5.jpg",
    "dimensions": "5x5m",
    "circuits": "2",
    "space": "25m²",
    "likes_count": 15,
    "comments_count": 8
  }
]
```

#### **Ejemplo con cURL**
```bash
# Obtener todos los productos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/"

# Obtener productos con filtros
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=Inflables&limit=10&skip=0"

# Buscar productos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?search=castillo"
```

#### **Ejemplo con JavaScript**
```javascript
async function getProducts(filters = {}) {
  const params = new URLSearchParams(filters);
  const response = await fetch(`https://api.kidsfunyfiestasinfantiles.com/api/products/?${params}`);
  
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch products');
  }
}

// Uso
getProducts({ category: 'Inflables', limit: 10 })
  .then(products => console.log('Productos:', products))
  .catch(error => console.error('Error:', error));
```

---

### **2. Obtener Producto por ID - `GET /api/products/{product_id}`**

Obtiene un producto específico por su ID.

#### **URL**
```
GET https://api.kidsfunyfiestasinfantiles.com/api/products/{product_id}
```

#### **Parámetros de Path**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `product_id` | int | ID del producto |

#### **Response Exitosa (200)**
```json
{
  "id": 26,
  "title": "Castillo Inflable",
  "description": "Castillo inflable para fiestas infantiles",
  "price": "150.00",
  "category": "Inflables",
  "created": "2024-01-01T00:00:00Z",
  "publicated": true,
  "user_id": 1,
  "youtube_url": "https://youtube.com/watch?v=example",
  "img": "product_images/castillo_principal.jpg",
  "img1": "product_images/castillo_1.jpg",
  "img2": "product_images/castillo_2.jpg",
  "img3": "product_images/castillo_3.jpg",
  "img4": "product_images/castillo_4.jpg",
  "img5": "product_images/castillo_5.jpg",
  "dimensions": "5x5m",
  "circuits": "2",
  "space": "25m²",
  "likes_count": 15,
  "comments_count": 8
}
```

#### **Response Error (404)**
```json
{
  "detail": "Product not found"
}
```

#### **Ejemplo con cURL**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/26"
```

---

### **3. Crear Producto - `POST /api/products/`**

Crea un nuevo producto (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/products/
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "title": "Nuevo Producto",
  "description": "Descripción del nuevo producto",
  "price": "200.00",
  "category": "Inflables",
  "publicated": true,
  "youtube_url": "https://youtube.com/watch?v=example",
  "dimensions": "6x6m",
  "circuits": "3",
  "space": "36m²"
}
```

#### **Response Exitosa (201)**
```json
{
  "id": 27,
  "title": "Nuevo Producto",
  "description": "Descripción del nuevo producto",
  "price": "200.00",
  "category": "Inflables",
  "created": "2024-01-01T00:00:00Z",
  "publicated": true,
  "user_id": 1,
  "youtube_url": "https://youtube.com/watch?v=example",
  "img": "product_images/default.jpg",
  "img1": "product_images/default.jpg",
  "img2": "product_images/default.jpg",
  "img3": "product_images/default.jpg",
  "img4": "product_images/default.jpg",
  "img5": "product_images/default.jpg",
  "dimensions": "6x6m",
  "circuits": "3",
  "space": "36m²"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/products/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nuevo Producto",
    "description": "Descripción del nuevo producto",
    "price": "200.00",
    "category": "Inflables",
    "publicated": true
  }'
```

---

### **4. Actualizar Producto - `PUT /api/products/{product_id}`**

Actualiza un producto existente (requiere autenticación).

#### **URL**
```
PUT https://api.kidsfunyfiestasinfantiles.com/api/products/{product_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: application/json
```

#### **Body**
```json
{
  "title": "Producto Actualizado",
  "description": "Nueva descripción",
  "price": "250.00",
  "category": "Inflables",
  "publicated": true
}
```

#### **Response Exitosa (200)**
```json
{
  "id": 26,
  "title": "Producto Actualizado",
  "description": "Nueva descripción",
  "price": "250.00",
  "category": "Inflables",
  "created": "2024-01-01T00:00:00Z",
  "publicated": true,
  "user_id": 1,
  "youtube_url": "https://youtube.com/watch?v=example",
  "img": "product_images/castillo_principal.jpg",
  "img1": "product_images/castillo_1.jpg",
  "img2": "product_images/castillo_2.jpg",
  "img3": "product_images/castillo_3.jpg",
  "img4": "product_images/castillo_4.jpg",
  "img5": "product_images/castillo_5.jpg",
  "dimensions": "5x5m",
  "circuits": "2",
  "space": "25m²"
}
```

---

### **5. Eliminar Producto - `DELETE /api/products/{product_id}`**

Elimina un producto (requiere autenticación).

#### **URL**
```
DELETE https://api.kidsfunyfiestasinfantiles.com/api/products/{product_id}
```

#### **Headers**
```http
Authorization: Bearer {token}
```

#### **Response Exitosa (204)**
```
No Content
```

---

### **6. Subir Imagen de Producto - `POST /api/products/{product_id}/upload-image`**

Sube una imagen para un producto específico (requiere autenticación).

#### **URL**
```
POST https://api.kidsfunyfiestasinfantiles.com/api/products/{product_id}/upload-image
```

#### **Headers**
```http
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

#### **Body (Form Data)**
```
image: [archivo]
position: 0 (0=principal, 1-5=secundarias)
```

#### **Response Exitosa (200)**
```json
{
  "message": "Image uploaded successfully",
  "image_path": "product_images/product_26_img_0.jpg"
}
```

#### **Ejemplo con cURL**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/products/26/upload-image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@/path/to/image.jpg" \
  -F "position=0"
```

---

## 🖼️ **Sistema de Imágenes**

### **Estructura de URLs de Imágenes**

```
https://api.kidsfunyfiestasinfantiles.com/media/{ruta_imagen}
```

### **Ejemplos de URLs**

- **Imagen principal**: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/castillo_principal.jpg`
- **Imagen secundaria 1**: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/castillo_1.jpg`
- **Imagen secundaria 2**: `https://api.kidsfunyfiestasinfantiles.com/media/product_images/castillo_2.jpg`

### **Formatos Soportados**
- **Imágenes**: JPG, JPEG, PNG, GIF
- **Tamaño máximo**: 10MB
- **Resolución recomendada**: 1920x1080

---

## 🔍 **Filtros y Búsqueda**

### **Filtros Disponibles**

#### **Por Categoría**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=Inflables"
```

#### **Por Estado de Publicación**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?publicated=true"
```

#### **Búsqueda por Título**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?search=castillo"
```

#### **Paginación**
```bash
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?skip=20&limit=10"
```

---

## 📊 **Estadísticas**

### **Conteos Incluidos**

Cada producto incluye automáticamente:
- **`likes_count`**: Número de likes del producto
- **`comments_count`**: Número de comentarios del producto

### **Ejemplo de Respuesta con Estadísticas**
```json
{
  "id": 26,
  "title": "Castillo Inflable",
  "description": "Castillo inflable para fiestas infantiles",
  "price": "150.00",
  "category": "Inflables",
  "likes_count": 15,
  "comments_count": 8
}
```

---

## 🧪 **Testing**

### **1. Testing con cURL**

#### **Obtener Productos**
```bash
# Obtener todos los productos
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/"

# Obtener producto específico
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/26"

# Filtrar por categoría
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/?category=Inflables"
```

#### **Crear Producto**
```bash
curl -X POST "https://api.kidsfunyfiestasinfantiles.com/api/products/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Product",
    "description": "Test description",
    "price": "100.00",
    "category": "Test",
    "publicated": true
  }'
```

### **2. Testing con JavaScript**

```javascript
class ProductsAPI {
  constructor(baseURL = 'https://api.kidsfunyfiestasinfantiles.com') {
    this.baseURL = baseURL;
  }

  async getProducts(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/api/products/?${params}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async getProduct(id) {
    const response = await fetch(`${this.baseURL}/api/products/${id}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async createProduct(productData, token) {
    const response = await fetch(`${this.baseURL}/api/products/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async updateProduct(id, productData, token) {
    const response = await fetch(`${this.baseURL}/api/products/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async deleteProduct(id, token) {
    const response = await fetch(`${this.baseURL}/api/products/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  async uploadImage(productId, imageFile, position, token) {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('position', position);

    const response = await fetch(`${this.baseURL}/api/products/${productId}/upload-image`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }
}

// Uso
const productsAPI = new ProductsAPI();

// Obtener productos
productsAPI.getProducts({ category: 'Inflables', limit: 10 })
  .then(products => console.log('Productos:', products))
  .catch(error => console.error('Error:', error));

// Obtener producto específico
productsAPI.getProduct(26)
  .then(product => console.log('Producto:', product))
  .catch(error => console.error('Error:', error));
```

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Error 404 - "Product not found"**
```bash
# Verificar que el producto existe
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/products/999"
```

#### **2. Error 401 - "Not authenticated"**
```bash
# Verificar que el token es válido
curl -X GET "https://api.kidsfunyfiestasinfantiles.com/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Error 422 - "Validation error"**
```bash
# Verificar que todos los campos requeridos están presentes
# Campos requeridos: title, category, publicated
```

#### **4. Error 413 - "File too large"**
```bash
# Verificar que la imagen no excede 10MB
ls -lh /path/to/image.jpg
```

### **Comandos de Diagnóstico**

#### **Verificar Productos en Base de Datos**
```sql
-- Ver todos los productos
SELECT id, title, category, publicated FROM t_app_product_product;

-- Ver productos por categoría
SELECT id, title FROM t_app_product_product WHERE category = 'Inflables';

-- Ver productos publicados
SELECT id, title FROM t_app_product_product WHERE publicated = true;
```

#### **Verificar Imágenes**
```bash
# Verificar que las imágenes existen
ls -la /opt/kidsfun-backend/media/product_images/

# Verificar permisos
sudo chown -R www-data:www-data /opt/kidsfun-backend/media/
sudo chmod -R 755 /opt/kidsfun-backend/media/
```

---

## 📊 **Métricas y Monitoreo**

### **Endpoints de Monitoreo**

#### **Health Check**
```bash
curl -I https://api.kidsfunyfiestasinfantiles.com/health
```

#### **Productos por Categoría**
```sql
SELECT category, COUNT(*) as count 
FROM t_app_product_product 
GROUP BY category 
ORDER BY count DESC;
```

#### **Productos Más Populares**
```sql
SELECT p.id, p.title, COUNT(l.id) as likes_count
FROM t_app_product_product p
LEFT JOIN t_app_like l ON l.product = p.id::text AND l.is_favorite = true
GROUP BY p.id, p.title
ORDER BY likes_count DESC
LIMIT 10;
```

---

## 🎯 **Próximos Pasos**

### **Mejoras Sugeridas**

1. **🖼️ Optimización de Imágenes**
   - Compresión automática
   - Redimensionamiento
   - Formatos WebP

2. **🔍 Búsqueda Avanzada**
   - Búsqueda por descripción
   - Filtros por precio
   - Ordenamiento

3. **📊 Analytics**
   - Vistas de productos
   - Métricas de engagement
   - Reportes

4. **🛡️ Seguridad**
   - Validación de archivos
   - Escaneo de malware
   - Rate limiting por usuario

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

**¡API de Productos lista para usar! 🎪** 