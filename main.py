from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.routers import products, users, likes, commentaries, events, auth, waiver, chat

# Create FastAPI app
app = FastAPI(
    title="KidsFun API",
    description="API para el sistema de gestión de KidsFun",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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

@app.get("/")
async def root():
    return {
        "message": "KidsFun API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 