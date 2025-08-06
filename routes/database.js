const express = require('express');
const { Sequelize, DataTypes, Op } = require('sequelize');
const { body, validationResult } = require('express-validator');
require('dotenv').config();

const router = express.Router();

// Configuración de la base de datos
const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: false,
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
  dialectOptions: {
    ssl: process.env.NODE_ENV === 'production' ? {
      require: true,
      rejectUnauthorized: false
    } : false
  }
});

// Modelos para acceso directo a la base de datos
const Product = sequelize.define('Product', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  title: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: false
  },
  price: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  },
  category: {
    type: DataTypes.STRING(50),
    allowNull: false
  },
  youtube_url: {
    type: DataTypes.STRING(200),
    allowNull: true
  },
  dimensions: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  circuits: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  space: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  img: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img1: {
    type: DataTypes.STRING(100),
    allowNull: true
  },
  img2: {
    type: DataTypes.STRING(100),
    allowNull: true
  },
  img3: {
    type: DataTypes.STRING(100),
    allowNull: true
  },
  img4: {
    type: DataTypes.STRING(100),
    allowNull: true
  },
  img5: {
    type: DataTypes.STRING(100),
    allowNull: true
  },
  created: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  publicated: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    defaultValue: true
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false
  }
}, {
  tableName: 't_app_product_product',
  timestamps: false
});

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING(150),
    allowNull: false,
    unique: true
  },
  first_name: {
    type: DataTypes.STRING(150),
    allowNull: false
  },
  last_name: {
    type: DataTypes.STRING(150),
    allowNull: false
  },
  email: {
    type: DataTypes.STRING(254),
    allowNull: false,
    unique: true
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    defaultValue: true
  },
  date_joined: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 'auth_user',
  timestamps: false
});

const Comment = sequelize.define('Comment', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  comment: {
    type: DataTypes.TEXT,
    allowNull: false
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  product_id: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  created: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 't_app_commentary',
  timestamps: false
});

const Like = sequelize.define('Like', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  product_id: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  created: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 't_app_like',
  timestamps: false
});

// Definir relaciones
Product.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
User.hasMany(Product, { foreignKey: 'user_id', as: 'products' });

Product.hasMany(Comment, { foreignKey: 'product_id', as: 'comments' });
Comment.belongsTo(Product, { foreignKey: 'product_id', as: 'product' });

Product.hasMany(Like, { foreignKey: 'product_id', as: 'likes' });
Like.belongsTo(Product, { foreignKey: 'product_id', as: 'product' });

// Middleware para manejar errores de base de datos
const handleDatabaseError = (res, error) => {
  console.error('Database error:', error);
  res.status(500).json({
    error: 'Error de base de datos',
    message: error.message
  });
};

// GET /db/products - Obtener todos los productos
router.get('/products', async (req, res) => {
  try {
    const {
      category,
      search,
      min_price,
      max_price,
      publicated = 'true',
      limit = 100,
      offset = 0
    } = req.query;

    const whereClause = { publicated: publicated === 'true' };

    if (category) {
      whereClause.category = category;
    }

    if (min_price || max_price) {
      whereClause.price = {};
      if (min_price) whereClause.price[Op.gte] = parseFloat(min_price);
      if (max_price) whereClause.price[Op.lte] = parseFloat(max_price);
    }

    if (search) {
      whereClause[Op.or] = [
        { title: { [Op.iLike]: `%${search}%` } },
        { description: { [Op.iLike]: `%${search}%` } }
      ];
    }

    const products = await Product.findAll({
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

    res.json({ products });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/products/:id - Obtener un producto específico
router.get('/products/:id', async (req, res) => {
  try {
    const product = await Product.findByPk(req.params.id, {
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'username', 'first_name', 'last_name']
        }
      ]
    });

    if (!product) {
      return res.status(404).json({ error: 'Producto no encontrado' });
    }

    res.json(product);
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/products/:id/comments - Obtener comentarios de un producto
router.get('/products/:id/comments', async (req, res) => {
  try {
    const comments = await Comment.findAll({
      where: { product_id: req.params.id },
      order: [['created', 'DESC']]
    });

    res.json({ comments });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/products/:id/likes - Obtener likes de un producto
router.get('/products/:id/likes', async (req, res) => {
  try {
    const likes = await Like.findAll({
      where: { product_id: req.params.id },
      order: [['created', 'DESC']]
    });

    res.json({ likes });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/users - Obtener todos los usuarios
router.get('/users', async (req, res) => {
  try {
    const users = await User.findAll({
      attributes: ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined'],
      order: [['date_joined', 'DESC']]
    });

    res.json({ users });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/stats - Obtener estadísticas de la base de datos
router.get('/stats', async (req, res) => {
  try {
    const [totalProducts, totalUsers, totalComments, totalLikes] = await Promise.all([
      Product.count(),
      User.count(),
      Comment.count(),
      Like.count()
    ]);

    res.json({
      total_products: totalProducts,
      total_users: totalUsers,
      total_comments: totalComments,
      total_likes: totalLikes
    });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/tables - Obtener información de las tablas
router.get('/tables', async (req, res) => {
  try {
    const tables = await sequelize.query(`
      SELECT table_name, table_type 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
      ORDER BY table_name
    `, { type: Sequelize.QueryTypes.SELECT });

    res.json(tables);
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// GET /db/tables/:tableName/structure - Obtener estructura de una tabla
router.get('/tables/:tableName/structure', async (req, res) => {
  try {
    const structure = await sequelize.query(`
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns 
      WHERE table_name = :tableName
      ORDER BY ordinal_position
    `, {
      replacements: { tableName: req.params.tableName },
      type: Sequelize.QueryTypes.SELECT
    });

    res.json(structure);
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

// POST /db/query - Ejecutar consulta SQL personalizada (solo para desarrollo)
router.post('/query', [
  body('query').notEmpty().withMessage('Query es requerida')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Solo permitir consultas SELECT para seguridad
    const query = req.body.query.trim();
    if (!query.toLowerCase().startsWith('select')) {
      return res.status(403).json({ error: 'Solo se permiten consultas SELECT' });
    }

    const result = await sequelize.query(query, {
      type: Sequelize.QueryTypes.SELECT
    });

    res.json({ result });
  } catch (error) {
    handleDatabaseError(res, error);
  }
});

module.exports = router; 