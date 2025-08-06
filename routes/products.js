const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { body, validationResult, query } = require('express-validator');
const { Op } = require('sequelize');
const Product = require('../models/Product');
const User = require('../models/User');
const Commentary = require('../models/Commentary');
const Like = require('../models/Like');
const { authenticateToken, optionalAuth } = require('../middleware/auth');
const config = require('../config/config');

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = process.env.UPLOAD_DIR || 'media';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: parseInt(process.env.MAX_FILE_SIZE) || 10485760 // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// Validation rules
const productValidation = [
  body('title')
    .isLength({ min: 1, max: 100 })
    .withMessage('Title must be between 1 and 100 characters'),
  body('category')
    .isLength({ min: 1, max: 50 })
    .withMessage('Category must be between 1 and 50 characters'),
  body('price')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Price must be a positive number'),
  body('description')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Description must be less than 1000 characters'),
  body('dimensions')
    .optional()
    .isLength({ max: 50 })
    .withMessage('Dimensions must be less than 50 characters'),
  body('youtube_url')
    .optional()
    .isURL()
    .withMessage('YouTube URL must be a valid URL'),
  body('circuits')
    .optional()
    .isLength({ max: 50 })
    .withMessage('Circuits must be less than 50 characters'),
  body('space')
    .optional()
    .isLength({ max: 50 })
    .withMessage('Space must be less than 50 characters')
];

// Get all products (with pagination and filtering)
router.get('/', optionalAuth, async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      category,
      search,
      min_price,
      max_price,
      publicated = 'true'
    } = req.query;

    const offset = (page - 1) * limit;
    const whereClause = { publicated: publicated === 'true' };

    // Add category filter
    if (category) {
      whereClause.category = category;
    }

    // Add price filters
    if (min_price || max_price) {
      whereClause.price = {};
      if (min_price) whereClause.price[Op.gte] = parseFloat(min_price);
      if (max_price) whereClause.price[Op.lte] = parseFloat(max_price);
    }

    // Add search filter
    if (search) {
      whereClause[Op.or] = [
        { title: { [Op.iLike]: `%${search}%` } },
        { description: { [Op.iLike]: `%${search}%` } }
      ];
    }

    const { count, rows: products } = await Product.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created', 'DESC']]
    });

    // Get likes count for each product
    const productsWithLikes = await Promise.all(
      products.map(async (product) => {
        const likesCount = await Like.count({ where: { product_id: product.id } });
        const commentariesCount = await Commentary.count({ where: { product_id: product.id } });
        
        return {
          ...product.toJSON(),
          likes_count: likesCount,
          commentaries_count: commentariesCount
        };
      })
    );

    res.json({
      products: productsWithLikes,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(count / limit),
        total_items: count,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Get products error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Get single product
router.get('/:id', optionalAuth, async (req, res) => {
  try {
    const { id } = req.params;
    
    const product = await Product.findByPk(id, {
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ]
    });

    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    // Get likes and commentaries count
    const likesCount = await Like.count({ where: { product_id: id } });
    const commentariesCount = await Commentary.count({ where: { product_id: id } });

    // Check if current user liked this product
    let userLiked = false;
    if (req.user) {
      const userLike = await Like.findOne({
        where: { user_id: req.user.id, product_id: id }
      });
      userLiked = !!userLike;
    }

    const productResponse = {
      ...product.toJSON(),
      likes_count: likesCount,
      commentaries_count: commentariesCount,
      user_liked: userLiked
    };

    res.json(productResponse);
  } catch (error) {
    console.error('Get product error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Create product
router.post('/', authenticateToken, upload.fields([
  { name: 'img', maxCount: 1 },
  { name: 'img1', maxCount: 1 },
  { name: 'img2', maxCount: 1 },
  { name: 'img3', maxCount: 1 },
  { name: 'img4', maxCount: 1 },
  { name: 'img5', maxCount: 1 }
]), productValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation error',
        message: 'Error de validación',
        details: errors.array()
      });
    }

    const {
      title,
      description,
      price,
      category,
      dimensions,
      youtube_url,
      circuits,
      space,
      publicated = false
    } = req.body;

    // Check if required images are uploaded
    const requiredImages = ['img', 'img1', 'img2', 'img3', 'img4', 'img5'];
    const uploadedImages = req.files ? Object.keys(req.files) : [];
    
    const missingImages = requiredImages.filter(img => !uploadedImages.includes(img));
    if (missingImages.length > 0) {
      return res.status(400).json({
        error: 'Missing required images',
        message: 'Faltan imágenes requeridas',
        missing_images: missingImages
      });
    }

    // Create product
    const product = await Product.create({
      title,
      description,
      price: price ? parseFloat(price) : null,
      category,
      dimensions,
      youtube_url,
      circuits,
      space,
      publicated: publicated === 'true',
      user_id: req.user.id,
      img: req.files.img[0].filename,
      img1: req.files.img1[0].filename,
      img2: req.files.img2[0].filename,
      img3: req.files.img3[0].filename,
      img4: req.files.img4[0].filename,
      img5: req.files.img5[0].filename
    });

    res.status(201).json(product);
  } catch (error) {
    console.error('Create product error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Update product
router.put('/:id', authenticateToken, upload.fields([
  { name: 'img', maxCount: 1 },
  { name: 'img1', maxCount: 1 },
  { name: 'img2', maxCount: 1 },
  { name: 'img3', maxCount: 1 },
  { name: 'img4', maxCount: 1 },
  { name: 'img5', maxCount: 1 }
]), productValidation, async (req, res) => {
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
    const product = await Product.findByPk(id);

    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    // Check if user owns the product or is admin
    if (product.user_id !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para modificar este producto'
      });
    }

    const updateData = { ...req.body };
    
    // Handle image updates
    if (req.files) {
      Object.keys(req.files).forEach(fieldName => {
        updateData[fieldName] = req.files[fieldName][0].filename;
      });
    }

    await product.update(updateData);

    res.json(product);
  } catch (error) {
    console.error('Update product error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

// Delete product
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const product = await Product.findByPk(id);

    if (!product) {
      return res.status(404).json({
        error: 'Product not found',
        message: 'Producto no encontrado'
      });
    }

    // Check if user owns the product or is admin
    if (product.user_id !== req.user.id && !req.user.is_staff && !req.user.is_superuser) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'No tienes permisos para eliminar este producto'
      });
    }

    await product.destroy();

    res.json({
      message: 'Product deleted successfully',
      message_es: 'Producto eliminado exitosamente'
    });
  } catch (error) {
    console.error('Delete product error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Error interno del servidor'
    });
  }
});

module.exports = router; 