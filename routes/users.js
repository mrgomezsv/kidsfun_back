const express = require('express');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const Product = require('../models/Product');
const { authenticateToken, requireRole } = require('../middleware/auth');

const router = express.Router();

// Get all users (admin only)
router.get('/', authenticateToken, requireRole(['staff', 'superuser']), async (req, res) => {
  try {
    const { page = 1, limit = 10, search } = req.query;
    const offset = (page - 1) * limit;
    
    const whereClause = {};
    if (search) {
      whereClause.$or = [
        { username: { $iLike: `%${search}%` } },
        { email: { $iLike: `%${search}%` } },
        { first_name: { $iLike: `%${search}%` } },
        { last_name: { $iLike: `%${search}%` } }
      ];
    }

    const { count, rows: users } = await User.findAndCountAll({
      where: whereClause,
      attributes: { exclude: ['password'] },
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['date_joined', 'DESC']]
    });

    res.json({
      users,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get user by ID
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    // Users can only see their own profile unless they're admin
    if (parseInt(id) !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para ver este perfil'
      });
    }

    const user = await User.findByPk(id, {
      attributes: { exclude: ['password'] },
      include: [
        {
          model: Product,
          as: 'products',
          attributes: ['id', 'title', 'category', 'created', 'publicated']
        }
      ]
    });

    if (!user) {
      return res.status(404).json({
        error: 'User not found',
        message: 'Usuario no encontrado'
      });
    }

    res.json(user);
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Update user profile
router.put('/:id', authenticateToken, [
  body('first_name')
    .optional()
    .isLength({ min: 1, max: 150 })
    .withMessage('First name must be between 1 and 150 characters'),
  body('last_name')
    .optional()
    .isLength({ min: 1, max: 150 })
    .withMessage('Last name must be between 1 and 150 characters'),
  body('email')
    .optional()
    .isEmail()
    .withMessage('Valid email is required')
    .normalizeEmail()
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation error',
        message: 'Error de validación',
        details: errors.array()
      });
    }

    const { id } = req.params;
    
    // Users can only update their own profile unless they're admin
    if (parseInt(id) !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para modificar este perfil'
      });
    }

    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({
        error: 'User not found',
        message: 'Usuario no encontrado'
      });
    }

    const { first_name, last_name, email } = req.body;
    const updateData = {};

    if (first_name) updateData.first_name = first_name;
    if (last_name) updateData.last_name = last_name;
    if (email) {
      // Check if email is already taken by another user
      const existingUser = await User.findOne({ where: { email, id: { $ne: id } } });
      if (existingUser) {
        return res.status(400).json({
          error: 'Email already exists',
          message: 'El email ya existe'
        });
      }
      updateData.email = email;
    }

    await user.update(updateData);

    // Return user without password
    const userResponse = {
      id: user.id,
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      is_staff: user.is_staff,
      is_superuser: user.is_superuser,
      is_active: user.is_active,
      date_joined: user.date_joined,
      last_login: user.last_login
    };

    res.json(userResponse);
  } catch (error) {
    console.error('Update user error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Change password
router.put('/:id/password', authenticateToken, [
  body('current_password')
    .notEmpty()
    .withMessage('Current password is required'),
  body('new_password')
    .isLength({ min: 8 })
    .withMessage('New password must be at least 8 characters long')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('New password must contain at least one uppercase letter, one lowercase letter, and one number')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation error',
        message: 'Error de validación',
        details: errors.array()
      });
    }

    const { id } = req.params;
    const { current_password, new_password } = req.body;

    // Users can only change their own password
    if (parseInt(id) !== req.user.id) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para cambiar esta contraseña'
      });
    }

    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({
        error: 'User not found',
        message: 'Usuario no encontrado'
      });
    }

    // Verify current password
    const isValidPassword = await user.comparePassword(current_password);
    if (!isValidPassword) {
      return res.status(400).json({
        error: 'Invalid current password',
        message: 'Contraseña actual incorrecta'
      });
    }

    // Update password
    user.password = new_password;
    await user.save();

    res.json({
      message: 'Password updated successfully',
      message_es: 'Contraseña actualizada exitosamente'
    });
  } catch (error) {
    console.error('Change password error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Admin: Update user status
router.put('/:id/status', authenticateToken, requireRole(['staff', 'superuser']), [
  body('is_active')
    .isBoolean()
    .withMessage('is_active must be a boolean')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation error',
        message: 'Error de validación',
        details: errors.array()
      });
    }

    const { id } = req.params;
    const { is_active } = req.body;

    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({
        error: 'User not found',
        message: 'Usuario no encontrado'
      });
    }

    await user.update({ is_active });

    res.json({
      message: 'User status updated successfully',
      message_es: 'Estado del usuario actualizado exitosamente',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        is_active: user.is_active
      }
    });
  } catch (error) {
    console.error('Update user status error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

module.exports = router; 