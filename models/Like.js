const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const User = require('./User');
const Product = require('./Product');

const Like = sequelize.define('Like', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'auth_user',
      key: 'id'
    }
  },
  product_id: {
    type: DataTypes.BIGINT,
    allowNull: false,
    references: {
      model: 't_app_product_product',
      key: 'id'
    }
  },
  created_at: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 'likes',
  timestamps: false,
  indexes: [
    {
      unique: true,
      fields: ['user_id', 'product_id']
    }
  ]
});

// Associations
Like.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
Like.belongsTo(Product, { foreignKey: 'product_id', as: 'product' });
User.hasMany(Like, { foreignKey: 'user_id', as: 'likes' });
Product.hasMany(Like, { foreignKey: 'product_id', as: 'likes' });

module.exports = Like; 