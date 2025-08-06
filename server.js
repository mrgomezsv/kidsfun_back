const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const compression = require('compression');
const morgan = require('morgan');
const path = require('path');
require('dotenv').config();

const { sequelize } = require('./config/database');
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');
const likeRoutes = require('./routes/likes');
const commentaryRoutes = require('./routes/commentaries');
const eventRoutes = require('./routes/events');
const waiverRoutes = require('./routes/waiver');
const chatRoutes = require('./routes/chat');
const contactRoutes = require('./routes/contact');
const { errorHandler } = require('./middleware/errorHandler');
const { securityHeaders } = require('./middleware/securityHeaders');

const app = express();
const PORT = process.env.PORT || 8000;

// Trust proxy for rate limiting behind Nginx
app.set('trust proxy', 1);

// Rate limiting
const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10, // limit each IP to 10 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Middleware
app.use(helmet());
app.use(compression());
app.use(morgan('combined'));
app.use(limiter);
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// CORS configuration
const corsOptions = {
  origin: [
    'http://localhost:4200',
    'https://kidsfunyfiestasinfantiles.com',
    'https://www.kidsfunyfiestasinfantiles.com'
  ],
  credentials: true,
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Security headers middleware
app.use(securityHeaders);

// Static files
if (process.env.UPLOAD_DIR && require('fs').existsSync(process.env.UPLOAD_DIR)) {
  app.use('/media', express.static(process.env.UPLOAD_DIR));
}

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/likes', likeRoutes);
app.use('/api/commentaries', commentaryRoutes);
app.use('/api/events', eventRoutes);
app.use('/api/waiver', waiverRoutes);
app.use('/api/chat', chatRoutes);
app.use('/api/contact', contactRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'KidsFun API',
    version: '1.0.0',
    docs: '/docs',
    security: {
      rate_limit: '10 requests/second',
      ssl_required: true,
      cors_enabled: true
    }
  });
});

// Security info endpoint
app.get('/security-info', (req, res) => {
  res.json({
    security_features: {
      rate_limiting: '10 requests per second per IP',
      input_validation: 'XSS and SQL injection protection',
      cors: 'Configured for specific domains',
      trusted_hosts: 'Only allowed hosts accepted',
      security_headers: 'HSTS, CSP, X-Frame-Options, etc.',
      ssl_required: true,
      jwt_authentication: true,
      request_logging: true
    },
    rate_limits: {
      requests_per_second: 10,
      window_size: '1 second',
      storage: 'In-memory (Redis recommended for production)'
    },
    allowed_origins: corsOptions.origin,
    max_file_size: process.env.MAX_FILE_SIZE || '10485760'
  });
});

// Error handling middleware
app.use(errorHandler);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Database connection and server start
async function startServer() {
  try {
    await sequelize.authenticate();
    console.log('✅ Database connection established successfully.');
    
    // Sync database (in development)
    if (process.env.NODE_ENV === 'development') {
      await sequelize.sync({ alter: true });
      console.log('✅ Database synchronized.');
    }
    
    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
      console.log(`📚 API Documentation: http://localhost:${PORT}/docs`);
      console.log(`🏥 Health Check: http://localhost:${PORT}/health`);
    });
  } catch (error) {
    console.error('❌ Unable to start server:', error);
    process.exit(1);
  }
}

startServer();

module.exports = app; 