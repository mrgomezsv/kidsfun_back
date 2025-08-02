# Configuración de Gunicorn para KidsFun Backend
import multiprocessing
import os

# Configuración básica
bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
timeout = int(os.getenv("TIMEOUT", 30))
keepalive = int(os.getenv("KEEPALIVE", 2))
max_requests = int(os.getenv("MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))

# Configuración de logs
accesslog = os.getenv("ACCESS_LOG", "logs/access.log")
errorlog = os.getenv("ERROR_LOG", "logs/error.log")
loglevel = os.getenv("LOG_LEVEL", "info")

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de rendimiento
preload_app = True
worker_connections = 1000
backlog = 2048

# Configuración de reinicio
graceful_timeout = 30
worker_tmp_dir = "/dev/shm"

# Configuración de usuario
user = os.getenv("GUNICORN_USER", "kidsfun")
group = os.getenv("GUNICORN_GROUP", "kidsfun")

# Configuración de SSL (opcional)
keyfile = os.getenv("SSL_KEYFILE", None)
certfile = os.getenv("SSL_CERTFILE", None)

if keyfile and certfile:
    bind = "0.0.0.0:8443"
    ssl_version = "TLSv1_2" 