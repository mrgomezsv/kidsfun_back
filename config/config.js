require('dotenv').config();

module.exports = {
  // Database
  database: {
    url: process.env.DATABASE_URL || 'postgresql://localhost:5432/kidsfun'
  },
  
  // Security
  jwt: {
    secret: process.env.SECRET_KEY || 'your-secret-key-change-in-production',
    algorithm: process.env.ALGORITHM || 'HS256',
    expiresIn: process.env.ACCESS_TOKEN_EXPIRE_MINUTES || '30m'
  },
  
  // Server
  server: {
    port: process.env.PORT || 8000,
    host: process.env.HOST || '0.0.0.0',
    nodeEnv: process.env.NODE_ENV || 'development'
  },
  
  // CORS
  cors: {
    allowedOrigins: [
      'http://localhost:4200',
      'https://kidsfunyfiestasinfantiles.com',
      'https://www.kidsfunyfiestasinfantiles.com'
    ]
  },
  
  // File Upload
  upload: {
    dir: process.env.UPLOAD_DIR || 'media',
    maxSize: parseInt(process.env.MAX_FILE_SIZE) || 10485760 // 10MB
  },
  
  // Email
  email: {
    host: process.env.SMTP_HOST || '',
    port: parseInt(process.env.SMTP_PORT) || 587,
    user: process.env.SMTP_USER || '',
    password: process.env.SMTP_PASSWORD || '',
    secure: process.env.SMTP_SECURE === 'true'
  },
  
  // Production Settings
  production: {
    workers: parseInt(process.env.WORKERS) || 4,
    timeout: parseInt(process.env.TIMEOUT) || 30,
    keepalive: parseInt(process.env.KEEPALIVE) || 2,
    maxRequests: parseInt(process.env.MAX_REQUESTS) || 1000,
    maxRequestsJitter: parseInt(process.env.MAX_REQUESTS_JITTER) || 50
  },
  
  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    accessLog: process.env.ACCESS_LOG || 'logs/access.log',
    errorLog: process.env.ERROR_LOG || 'logs/error.log'
  },
  
  // SSL/TLS
  ssl: {
    keyFile: process.env.SSL_KEYFILE || '',
    certFile: process.env.SSL_CERTFILE || ''
  }
}; 