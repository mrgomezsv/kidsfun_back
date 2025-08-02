from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:4200",
        "https://kidsfunyfiestasinfantiles.com",
        "https://www.kidsfunyfiestasinfantiles.com"
    ]
    
    # File Upload
    upload_dir: str = os.getenv("UPLOAD_DIR", "media")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # Email
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    
    # Production Settings
    workers: int = int(os.getenv("WORKERS", "4"))
    worker_class: str = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    timeout: int = int(os.getenv("TIMEOUT", "30"))
    keepalive: int = int(os.getenv("KEEPALIVE", "2"))
    max_requests: int = int(os.getenv("MAX_REQUESTS", "1000"))
    max_requests_jitter: int = int(os.getenv("MAX_REQUESTS_JITTER", "50"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "info")
    access_log: str = os.getenv("ACCESS_LOG", "logs/access.log")
    error_log: str = os.getenv("ERROR_LOG", "logs/error.log")
    
    # SSL/TLS (optional)
    ssl_keyfile: str = os.getenv("SSL_KEYFILE", "")
    ssl_certfile: str = os.getenv("SSL_CERTFILE", "")
    
    class Config:
        env_file = ".env"

settings = Settings() 