# 🛠️ KidsFun API - Developer Guide

## 📋 Índice
- [Configuración Inicial](#configuración-inicial)
- [Autenticación Avanzada](#autenticación-avanzada)
- [Manejo de Errores](#manejo-de-errores)
- [Rate Limiting](#rate-limiting)
- [Ejemplos Avanzados](#ejemplos-avanzados)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ⚙️ Configuración Inicial

### Variables de Entorno
```bash
# Configuración del cliente
API_BASE_URL=https://api.kidsfunyfiestasinfantiles.com
API_VERSION=v1.0.0
API_TIMEOUT=10000
API_RATE_LIMIT=10
```

### Headers Comunes
```javascript
const commonHeaders = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'User-Agent': 'KidsFun-Client/1.0.0'
};
```

---

## 🔐 Autenticación Avanzada

### Clase de Autenticación (JavaScript)
```javascript
class KidsFunAuth {
  constructor() {
    this.baseURL = 'https://api.kidsfunyfiestasinfantiles.com';
    this.token = localStorage.getItem('kidsfun_token');
    this.refreshToken = localStorage.getItem('kidsfun_refresh_token');
  }

  async login(email, password) {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
      }

      const data = await response.json();
      this.setTokens(data.access_token, data.refresh_token);
      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async refreshAccessToken() {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: this.refreshToken })
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();
      this.setTokens(data.access_token, data.refresh_token);
      return data.access_token;
    } catch (error) {
      this.logout();
      throw error;
    }
  }

  setTokens(accessToken, refreshToken) {
    this.token = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('kidsfun_token', accessToken);
    localStorage.setItem('kidsfun_refresh_token', refreshToken);
  }

  logout() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('kidsfun_token');
    localStorage.removeItem('kidsfun_refresh_token');
  }

  isAuthenticated() {
    return !!this.token;
  }

  getAuthHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
  }
}
```

### Cliente API Base (JavaScript)
```javascript
class KidsFunAPI {
  constructor() {
    this.baseURL = 'https://api.kidsfunyfiestasinfantiles.com';
    this.auth = new KidsFunAuth();
    this.retryAttempts = 3;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        ...this.auth.getAuthHeaders(),
        ...options.headers
      },
      ...options
    };

    for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
      try {
        const response = await fetch(url, config);
        
        if (response.status === 401 && attempt < this.retryAttempts) {
          // Token expirado, intentar renovar
          await this.auth.refreshAccessToken();
          config.headers = this.auth.getAuthHeaders();
          continue;
        }

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
      } catch (error) {
        if (attempt === this.retryAttempts) {
          throw error;
        }
        // Esperar antes de reintentar
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }
  }

  // Métodos para productos
  async getProducts(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/products/?${queryString}`);
  }

  async getProduct(id) {
    return this.request(`/api/products/${id}`);
  }

  async createProduct(productData) {
    return this.request('/api/products/', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  }

  async updateProduct(id, productData) {
    return this.request(`/api/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(productData)
    });
  }

  async deleteProduct(id) {
    return this.request(`/api/products/${id}`, {
      method: 'DELETE'
    });
  }

  // Métodos para comentarios
  async getComments(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/commentaries/?${queryString}`);
  }

  async createComment(commentData) {
    return this.request('/api/commentaries/', {
      method: 'POST',
      body: JSON.stringify(commentData)
    });
  }

  // Métodos para likes
  async getLikes(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/likes/?${queryString}`);
  }

  async toggleLike(productId, isFavorite = true) {
    return this.request('/api/likes/', {
      method: 'POST',
      body: JSON.stringify({
        product: productId.toString(),
        is_favorite: isFavorite
      })
    });
  }
}
```

---

## 🚨 Manejo de Errores

### Clase de Manejo de Errores
```javascript
class APIError extends Error {
  constructor(message, status, code, details = null) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

class ErrorHandler {
  static handle(error) {
    if (error instanceof APIError) {
      switch (error.status) {
        case 400:
          console.error('Bad Request:', error.details);
          return 'Datos inválidos. Verifica la información enviada.';
        
        case 401:
          console.error('Unauthorized');
          // Redirigir al login
          window.location.href = '/login';
          return 'Sesión expirada. Inicia sesión nuevamente.';
        
        case 403:
          console.error('Forbidden');
          return 'No tienes permisos para realizar esta acción.';
        
        case 404:
          console.error('Not Found');
          return 'El recurso solicitado no existe.';
        
        case 422:
          console.error('Validation Error:', error.details);
          return 'Error de validación. Verifica los datos enviados.';
        
        case 429:
          console.error('Rate Limit Exceeded');
          return 'Demasiadas peticiones. Intenta más tarde.';
        
        case 500:
          console.error('Server Error');
          return 'Error del servidor. Intenta más tarde.';
        
        default:
          console.error('Unknown Error:', error);
          return 'Error inesperado. Intenta más tarde.';
      }
    } else {
      console.error('Network Error:', error);
      return 'Error de conexión. Verifica tu internet.';
    }
  }

  static async handleResponse(response) {
    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: response.statusText };
      }

      throw new APIError(
        errorData.detail || 'Error desconocido',
        response.status,
        errorData.code,
        errorData.detail
      );
    }
    return response;
  }
}
```

### Interceptor para Axios
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.kidsfunyfiestasinfantiles.com',
  timeout: 10000
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('kidsfun_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('kidsfun_refresh_token');
        const response = await axios.post('/api/auth/refresh', {
          refresh_token: refreshToken
        });

        const { access_token } = response.data;
        localStorage.setItem('kidsfun_token', access_token);
        api.defaults.headers.Authorization = `Bearer ${access_token}`;

        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('kidsfun_token');
        localStorage.removeItem('kidsfun_refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
```

---

## ⏱️ Rate Limiting

### Cliente con Rate Limiting
```javascript
class RateLimitedAPI {
  constructor() {
    this.requestQueue = [];
    this.lastRequestTime = 0;
    this.minInterval = 100; // 100ms entre requests (10 por segundo)
  }

  async makeRequest(endpoint, options = {}) {
    return new Promise((resolve, reject) => {
      this.requestQueue.push({
        endpoint,
        options,
        resolve,
        reject
      });
      this.processQueue();
    });
  }

  async processQueue() {
    if (this.requestQueue.length === 0) return;

    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;

    if (timeSinceLastRequest < this.minInterval) {
      setTimeout(() => this.processQueue(), this.minInterval - timeSinceLastRequest);
      return;
    }

    const request = this.requestQueue.shift();
    this.lastRequestTime = Date.now();

    try {
      const response = await fetch(request.endpoint, request.options);
      request.resolve(response);
    } catch (error) {
      request.reject(error);
    }

    // Procesar siguiente request
    if (this.requestQueue.length > 0) {
      setTimeout(() => this.processQueue(), this.minInterval);
    }
  }
}
```

---

## 💡 Ejemplos Avanzados

### React Hook para Productos
```javascript
import { useState, useEffect, useCallback } from 'react';

const useProducts = (filters = {}) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    total: 0,
    hasMore: true
  });

  const api = new KidsFunAPI();

  const fetchProducts = useCallback(async (page = 1, append = false) => {
    try {
      setLoading(true);
      setError(null);

      const params = {
        ...filters,
        skip: (page - 1) * 20,
        limit: 20
      };

      const data = await api.getProducts(params);
      
      if (append) {
        setProducts(prev => [...prev, ...data]);
      } else {
        setProducts(data);
      }

      setPagination(prev => ({
        ...prev,
        page,
        hasMore: data.length === 20
      }));
    } catch (err) {
      setError(ErrorHandler.handle(err));
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const loadMore = useCallback(() => {
    if (!loading && pagination.hasMore) {
      fetchProducts(pagination.page + 1, true);
    }
  }, [loading, pagination, fetchProducts]);

  useEffect(() => {
    fetchProducts(1, false);
  }, [fetchProducts]);

  return {
    products,
    loading,
    error,
    pagination,
    refetch: () => fetchProducts(1, false),
    loadMore
  };
};
```

### Componente de Productos con Infinite Scroll
```javascript
import React from 'react';
import { useProducts } from './hooks/useProducts';

const ProductList = ({ category, search }) => {
  const { products, loading, error, loadMore, hasMore } = useProducts({
    category,
    search
  });

  const handleScroll = (e) => {
    const { scrollTop, scrollHeight, clientHeight } = e.target;
    if (scrollTop + clientHeight >= scrollHeight - 100) {
      loadMore();
    }
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="product-list" onScroll={handleScroll}>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
      
      {loading && <div className="loading">Cargando...</div>}
      
      {!hasMore && products.length > 0 && (
        <div className="no-more">No hay más productos</div>
      )}
    </div>
  );
};
```

### Gestión de Estado Global (Redux/Zustand)
```javascript
import create from 'zustand';

const useStore = create((set, get) => ({
  // Estado
  products: [],
  cart: [],
  user: null,
  loading: false,
  error: null,

  // Acciones
  setProducts: (products) => set({ products }),
  addToCart: (product) => set((state) => ({
    cart: [...state.cart, product]
  })),
  removeFromCart: (productId) => set((state) => ({
    cart: state.cart.filter(item => item.id !== productId)
  })),
  setUser: (user) => set({ user }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  // Acciones asíncronas
  fetchProducts: async (filters = {}) => {
    const api = new KidsFunAPI();
    set({ loading: true, error: null });

    try {
      const products = await api.getProducts(filters);
      set({ products, loading: false });
    } catch (error) {
      set({ error: ErrorHandler.handle(error), loading: false });
    }
  },

  login: async (email, password) => {
    const auth = new KidsFunAuth();
    set({ loading: true, error: null });

    try {
      const userData = await auth.login(email, password);
      set({ user: userData.user, loading: false });
    } catch (error) {
      set({ error: ErrorHandler.handle(error), loading: false });
    }
  }
}));
```

---

## 🧪 Testing

### Tests con Jest
```javascript
import { KidsFunAPI } from './api';

// Mock fetch
global.fetch = jest.fn();

describe('KidsFunAPI', () => {
  let api;

  beforeEach(() => {
    api = new KidsFunAPI();
    fetch.mockClear();
  });

  test('should fetch products successfully', async () => {
    const mockProducts = [
      { id: 1, title: 'Test Product', price: '100.00' }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockProducts
    });

    const products = await api.getProducts();
    expect(products).toEqual(mockProducts);
    expect(fetch).toHaveBeenCalledWith(
      'https://api.kidsfunyfiestasinfantiles.com/api/products/',
      expect.any(Object)
    );
  });

  test('should handle authentication errors', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: 'Unauthorized'
    });

    await expect(api.getProducts()).rejects.toThrow('HTTP 401');
  });
});
```

### Tests de Integración
```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { ProductList } from './ProductList';

test('renders products list', async () => {
  render(<ProductList />);

  await waitFor(() => {
    expect(screen.getByText('Red Mechanical Bull')).toBeInTheDocument();
  });
});
```

---

## 🚀 Deployment

### Configuración de Producción
```javascript
// config/production.js
export const config = {
  api: {
    baseURL: 'https://api.kidsfunyfiestasinfantiles.com',
    timeout: 15000,
    retryAttempts: 3
  },
  auth: {
    tokenExpiry: 30 * 60 * 1000, // 30 minutos
    refreshThreshold: 5 * 60 * 1000 // 5 minutos antes
  },
  features: {
    enableCache: true,
    enableOffline: false,
    enableAnalytics: true
  }
};
```

### Service Worker para Cache
```javascript
// sw.js
const CACHE_NAME = 'kidsfun-api-v1';
const API_CACHE_NAME = 'kidsfun-api-cache';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      caches.open(API_CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response) {
            return response;
          }
          return fetch(event.request).then((response) => {
            cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
  }
});
```

---

## 📊 Monitoreo y Analytics

### Cliente de Analytics
```javascript
class APIAnalytics {
  constructor() {
    this.events = [];
  }

  trackRequest(endpoint, method, status, duration) {
    const event = {
      timestamp: new Date().toISOString(),
      endpoint,
      method,
      status,
      duration,
      userAgent: navigator.userAgent
    };

    this.events.push(event);
    this.sendToAnalytics(event);
  }

  trackError(error, context) {
    const event = {
      timestamp: new Date().toISOString(),
      type: 'error',
      message: error.message,
      stack: error.stack,
      context
    };

    this.sendToAnalytics(event);
  }

  async sendToAnalytics(event) {
    try {
      await fetch('/api/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event)
      });
    } catch (error) {
      console.error('Analytics error:', error);
    }
  }
}
```

---

## 🔧 Herramientas de Desarrollo

### Debug Helper
```javascript
class APIDebugger {
  static enable() {
    if (process.env.NODE_ENV === 'development') {
      window.kidsfunDebug = {
        api: new KidsFunAPI(),
        auth: new KidsFunAuth(),
        clearCache: () => {
          localStorage.clear();
          sessionStorage.clear();
        },
        mockResponse: (endpoint, response) => {
          // Mock responses for testing
        }
      };
    }
  }
}
```

---

*Esta guía está diseñada para desarrolladores que necesitan integrar la API de KidsFun en sus aplicaciones. Para más información, consulta la documentación principal.* 