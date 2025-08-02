from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Dict, List
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting storage (en producción usar Redis)
rate_limit_storage: Dict[str, List[float]] = {}

class SecurityMiddleware:
    """Middleware para mejorar la seguridad de la API"""
    
    def __init__(self, app):
        self.app = app
        self.rate_limit_requests = 10  # requests por segundo
        self.rate_limit_window = 1  # ventana en segundos
        
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Verificar rate limiting
            if not self._check_rate_limit(request):
                return await self._rate_limit_response(send)
            
            # Verificar headers de seguridad
            if not self._check_security_headers(request):
                return await self._security_error_response(send)
            
            # Log de requests
            await self._log_request(request)
        
        await self.app(scope, receive, send)
    
    def _check_rate_limit(self, request: Request) -> bool:
        """Verificar rate limiting por IP"""
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip not in rate_limit_storage:
            rate_limit_storage[client_ip] = []
        
        # Limpiar requests antiguos
        rate_limit_storage[client_ip] = [
            req_time for req_time in rate_limit_storage[client_ip]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Verificar si excede el límite
        if len(rate_limit_storage[client_ip]) >= self.rate_limit_requests:
            return False
        
        # Agregar request actual
        rate_limit_storage[client_ip].append(current_time)
        return True
    
    def _check_security_headers(self, request: Request) -> bool:
        """Verificar headers de seguridad"""
        # Verificar User-Agent
        user_agent = request.headers.get("user-agent", "")
        if not user_agent or len(user_agent) > 500:
            return False
        
        # Verificar Content-Length para prevenir ataques de tamaño
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
            return False
        
        return True
    
    async def _log_request(self, request: Request):
        """Log de requests para auditoría"""
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host} "
            f"User-Agent: {request.headers.get('user-agent', 'Unknown')}"
        )
    
    async def _rate_limit_response(self, send):
        """Respuesta para rate limit excedido"""
        response = JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "retry_after": self.rate_limit_window
            }
        )
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": response.headers.raw
        })
        await send({
            "type": "http.response.body",
            "body": response.body
        })
    
    async def _security_error_response(self, send):
        """Respuesta para errores de seguridad"""
        response = JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Security violation",
                "message": "Request blocked for security reasons"
            }
        )
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": response.headers.raw
        })
        await send({
            "type": "http.response.body",
            "body": response.body
        })

class InputValidationMiddleware:
    """Middleware para validación de entrada"""
    
    def __init__(self, app):
        self.app = app
        self.suspicious_patterns = [
            r"<script.*?>.*?</script>",  # XSS
            r"javascript:",  # XSS
            r"on\w+\s*=",  # XSS events
            r"union\s+select",  # SQL injection
            r"drop\s+table",  # SQL injection
            r"exec\s*\(",  # Command injection
            r"system\s*\(",  # Command injection
        ]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Validar parámetros de query
            if not self._validate_query_params(request):
                return await self._validation_error_response(send)
            
            # Validar headers
            if not self._validate_headers(request):
                return await self._validation_error_response(send)
        
        await self.app(scope, receive, send)
    
    def _validate_query_params(self, request: Request) -> bool:
        """Validar parámetros de query"""
        for param_name, param_value in request.query_params.items():
            if not self._is_safe_input(param_value):
                logger.warning(f"Suspicious query parameter: {param_name}={param_value}")
                return False
        return True
    
    def _validate_headers(self, request: Request) -> bool:
        """Validar headers"""
        for header_name, header_value in request.headers.items():
            if not self._is_safe_input(header_value):
                logger.warning(f"Suspicious header: {header_name}={header_value}")
                return False
        return True
    
    def _is_safe_input(self, value: str) -> bool:
        """Verificar si el input es seguro"""
        if not value:
            return True
        
        value_lower = value.lower()
        
        # Verificar patrones sospechosos
        for pattern in self.suspicious_patterns:
            if re.search(pattern, value_lower, re.IGNORECASE):
                return False
        
        # Verificar longitud
        if len(value) > 10000:  # Máximo 10KB por campo
            return False
        
        return True
    
    async def _validation_error_response(self, send):
        """Respuesta para errores de validación"""
        response = JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Invalid input",
                "message": "Request contains invalid or suspicious data"
            }
        )
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": response.headers.raw
        })
        await send({
            "type": "http.response.body",
            "body": response.body
        })

def add_security_middleware(app):
    """Agregar middleware de seguridad a la aplicación"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "https://kidsfunyfiestasinfantiles.com",
            "https://www.kidsfunyfiestasinfantiles.com",
            "https://api.kidsfunyfiestasinfantiles.com"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page-Count"]
    )
    
    # Trusted Host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "api.kidsfunyfiestasinfantiles.com",
            "localhost",
            "127.0.0.1"
        ]
    )
    
    # Security middleware personalizado
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(InputValidationMiddleware)
    
    return app

# Headers de seguridad adicionales
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}

def add_security_headers(response):
    """Agregar headers de seguridad a la respuesta"""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response 