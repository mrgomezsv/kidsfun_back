from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.routers import products, users, likes, commentaries, events, auth, waiver, chat, contact
from app.middleware import add_security_middleware, add_security_headers

# Create FastAPI app
app = FastAPI(
    title="KidsFun API",
    description="API para el sistema de gestión de KidsFun",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Agregar middleware de seguridad
app = add_security_middleware(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists(settings.upload_dir):
    app.mount("/media", StaticFiles(directory=settings.upload_dir), name="media")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(likes.router, prefix="/api/likes", tags=["Likes"])
app.include_router(commentaries.router, prefix="/api/commentaries", tags=["Commentaries"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(waiver.router, prefix="/api/waiver", tags=["Waiver"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])

@app.get("/")
async def root():
    return {
        "message": "KidsFun API",
        "version": "1.0.0",
        "docs": "/docs",
        "security": {
            "rate_limit": "10 requests/second",
            "ssl_required": True,
            "cors_enabled": True
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/security-info")
async def security_info():
    """Información sobre las medidas de seguridad implementadas"""
    return {
        "security_features": {
            "rate_limiting": "10 requests per second per IP",
            "input_validation": "XSS and SQL injection protection",
            "cors": "Configured for specific domains",
            "trusted_hosts": "Only allowed hosts accepted",
            "security_headers": "HSTS, CSP, X-Frame-Options, etc.",
            "ssl_required": True,
            "jwt_authentication": True,
            "request_logging": True
        },
        "rate_limits": {
            "requests_per_second": 10,
            "window_size": "1 second",
            "storage": "In-memory (Redis recommended for production)"
        },
        "allowed_origins": settings.allowed_origins,
        "max_file_size": f"{settings.max_file_size} bytes"
    }

@app.middleware("http")
async def add_security_headers_middleware(request: Request, call_next):
    """Middleware para agregar headers de seguridad a todas las respuestas"""
    response = await call_next(request)
    return add_security_headers(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 