const jwt = require('jsonwebtoken');
const config = require('../config/config');
const User = require('../models/User');

const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required',
      message: 'Token de acceso requerido'
    });
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret);
    const user = await User.findByPk(decoded.sub);
    
    if (!user) {
      return res.status(401).json({ 
        error: 'Invalid token',
        message: 'Token inválido'
      });
    }

    if (!user.is_active) {
      return res.status(401).json({ 
        error: 'User account is disabled',
        message: 'Cuenta de usuario deshabilitada'
      });
    }

    req.user = user;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ 
        error: 'Token expired',
        message: 'Token expirado'
      });
    }
    
    return res.status(403).json({ 
      error: 'Invalid token',
      message: 'Token inválido'
    });
  }
};

const requireRole = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ 
        error: 'Authentication required',
        message: 'Autenticación requerida'
      });
    }

    const userRoles = [];
    if (req.user.is_superuser) userRoles.push('superuser');
    if (req.user.is_staff) userRoles.push('staff');
    userRoles.push('user');

    const hasRequiredRole = roles.some(role => userRoles.includes(role));
    
    if (!hasRequiredRole) {
      return res.status(403).json({ 
        error: 'Insufficient permissions',
        message: 'Permisos insuficientes'
      });
    }

    next();
  };
};

const optionalAuth = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return next();
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret);
    const user = await User.findByPk(decoded.sub);
    
    if (user && user.is_active) {
      req.user = user;
    }
  } catch (error) {
    // Token is invalid, but we continue without authentication
  }

  next();
};

module.exports = {
  authenticateToken,
  requireRole,
  optionalAuth
}; 