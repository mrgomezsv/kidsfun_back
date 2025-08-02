from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://mrgomez:Karin2100@82.165.210.146:5432/smap_kf")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
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
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "kidsfun.developer@gmail.com")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "Karin2100")
    
    class Config:
        env_file = ".env"

settings = Settings() 