const express = require('express');
const Like = require('../models/Like');
const Product = require('../models/Product');
const User = require('../models/User');
const { authenticateToken } = require('../middleware/auth');

const router = express.Router();

// Get likes for a product
router.get('/product/:productId', async (req, res) => {
  try {
    const { productId } = req.params;
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    const { count, rows: likes } = await Like.findAndCountAll({
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
      likes,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get likes error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get likes by user
router.get('/user/:userId', authenticateToken, async (req, res) => {
  try {
    const { userId } = req.params;
    const { page = 1, limit = 10 } = req.query;
    const offset = (page - 1) * limit;

    // Users can only see their own likes unless they're admin
    if (parseInt(userId) !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para ver estos likes'
      });
    }

    const { count, rows: likes } = await Like.findAndCountAll({
      where: { user_id: userId },
      include: [
        {
          model: Product,
          as: 'product',
          attributes: ['id', 'title', 'category', 'img', 'price']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    });

    res.json({
      likes,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get user likes error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Toggle like (create or delete)
router.post('/toggle/:productId', authenticateToken, async (req, res) => {
  try {
    const { productId } = req.params;
    const userId = req.user.id;

    // Check if product exists
    const product = await Product.findByPk(productId);
    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    // Check if user already liked the product
    const existingLike = await Like.findOne({
      where: { user_id: userId, product_id: productId }
    });

    if (existingLike) {
      // Remove like
      await existingLike.destroy();
      
      // Get updated likes count
      const likesCount = await Like.count({ where: { product_id: productId } });
      
      res.json({
        message: 'Like removed successfully',
        message_es: 'Like eliminado exitosamente',
        liked: false,
        likes_count: likesCount
      });
    } else {
      // Add like
      await Like.create({
        user_id: userId,
        product_id: productId
      });
      
      // Get updated likes count
      const likesCount = await Like.count({ where: { product_id: productId } });
      
      res.status(201).json({
        message: 'Like added successfully',
        message_es: 'Like agregado exitosamente',
        liked: true,
        likes_count: likesCount
      });
    }
  } catch (error) {
    console.error('Toggle like error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Check if user liked a product
router.get('/check/:productId', authenticateToken, async (req, res) => {
  try {
    const { productId } = req.params;
    const userId = req.user.id;

    const like = await Like.findOne({
      where: { user_id: userId, product_id: productId }
    });

    res.json({
      liked: !!like,
      like_id: like ? like.id : null
    });
  } catch (error) {
    console.error('Check like error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get total likes count for a product
router.get('/count/:productId', async (req, res) => {
  try {
    const { productId } = req.params;

    const count = await Like.count({
      where: { product_id: productId }
    });

    res.json({ count });
  } catch (error) {
    console.error('Get likes count error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

module.exports = router; 