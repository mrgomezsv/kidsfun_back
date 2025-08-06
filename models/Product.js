const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const User = require('./User');

const Product = sequelize.define('Product', {
  id: {
    type: DataTypes.BIGINT,
    primaryKey: true,
    autoIncrement: true,
    field: 'id'
  },
  title: {
    type: DataTypes.STRING(100),
    allowNull: false,
    validate: {
      len: [1, 100]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  price: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: true,
    validate: {
      min: 0
    }
  },
  category: {
    type: DataTypes.STRING(50),
    allowNull: false,
    validate: {
      len: [1, 50]
    }
  },
  created: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  },
  publicated: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
    defaultValue: false
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'auth_user',
      key: 'id'
    }
  },
  img: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img1: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img2: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img3: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img4: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  img5: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  dimensions: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  youtube_url: {
    type: DataTypes.STRING(255),
    allowNull: true,
    validate: {
      isUrl: true
    }
  },
  circuits: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  space: {
    type: DataTypes.STRING(50),
    allowNull: true
  }
}, {
  tableName: 't_app_product_product',
  timestamps: false
});

// Associations
Product.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
User.hasMany(Product, { foreignKey: 'user_id', as: 'products' });

// Instance method to get formatted price
Product.prototype.getFormattedPrice = function() {
  return this.price ? `$${parseFloat(this.price).toFixed(2)}` : 'N/A';
};

// Instance method to get all images
Product.prototype.getAllImages = function() {
  return [this.img, this.img1, this.img2, this.img3, this.img4, this.img5].filter(Boolean);
};

module.exports = Product; 