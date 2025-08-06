const express = require('express');
const { body, validationResult } = require('express-validator');
const Commentary = require('../models/Commentary');
const Product = require('../models/Product');
const User = require('../models/User');
const { authenticateToken } = require('../middleware/auth');

const router = express.Router();

// Get commentaries for a product
router.get('/product/:productId', async (req, res) => {
  try {
    const { productId } = req.params;
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    // Check if product exists
    const product = await Product.findByPk(productId);
    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    const { count, rows: commentaries } = await Commentary.findAndCountAll({
      where: { product_id: productId },
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    });

    res.json({
      commentaries,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get commentaries error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get commentaries by user
router.get('/user/:userId', authenticateToken, async (req, res) => {
  try {
    const { userId } = req.params;
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    // Users can only see their own commentaries unless they're admin
    if (parseInt(userId) !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para ver estos comentarios'
      });
    }

    const { count, rows: commentaries } = await Commentary.findAndCountAll({
      where: { user_id: userId },
      include: [
        {
          model: Product,
          as: 'product',
          attributes: ['id', 'title', 'category', 'img']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    });

    res.json({
      commentaries,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get user commentaries error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Create commentary
router.post('/', authenticateToken, [
  body('content')
    .isLength({ min: 1, max: 1000 })
    .withMessage('Content must be between 1 and 1000 characters'),
  body('product_id')
    .isInt({ min: 1 })
    .withMessage('Valid product_id is required')
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

    const { content, product_id } = req.body;
    const user_id = req.user.id;

    // Check if product exists
    const product = await Product.findByPk(product_id);
    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    // Create commentary
    const commentary = await Commentary.create({
      content,
      user_id,
      product_id
    });

    // Get commentary with user info
    const commentaryWithUser = await Commentary.findByPk(commentary.id, {
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ]
    });

    res.status(201).json(commentaryWithUser);
  } catch (error) {
    console.error('Create commentary error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Update commentary
router.put('/:id', authenticateToken, [
  body('content')
    .isLength({ min: 1, max: 1000 })
    .withMessage('Content must be between 1 and 1000 characters')
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
    const { content } = req.body;
    const user_id = req.user.id;

    const commentary = await Commentary.findByPk(id);
    if (!commentary) {
      return res.status(404).json({
        error: 'Commentary not found',
        message: 'Comentario no encontrado'
      });
    }

    // Check if user owns the commentary or is admin
    if (commentary.user_id !== user_id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para modificar este comentario'
      });
    }

    await commentary.update({ content });

    // Get updated commentary with user info
    const updatedCommentary = await Commentary.findByPk(id, {
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ]
    });

    res.json(updatedCommentary);
  } catch (error) {
    console.error('Update commentary error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Delete commentary
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const user_id = req.user.id;

    const commentary = await Commentary.findByPk(id);
    if (!commentary) {
      return res.status(404).json({
        error: 'Commentary not found',
        message: 'Comentario no encontrado'
      });
    }

    // Check if user owns the commentary or is admin
    if (commentary.user_id !== user_id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para eliminar este comentario'
      });
    }

    await commentary.destroy();

    res.json({
      message: 'Commentary deleted successfully',
      message_es: 'Comentario eliminado exitosamente'
    });
  } catch (error) {
    console.error('Delete commentary error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get commentary by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const commentary = await Commentary.findByPk(id, {
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        },
        {
          model: Product,
          as: 'product',
          attributes: ['id', 'title', 'category']
        }
      ]
    });

    if (!commentary) {
      return res.status(404).json({
        error: 'Commentary not found',
        message: 'Comentario no encontrado'
      });
    }

    res.json(commentary);
  } catch (error) {
    console.error('Get commentary error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

module.exports = router; 