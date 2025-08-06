const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const User = require('./User');
const Product = require('./Product');

const Commentary = sequelize.define('Commentary', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  content: {
    type: DataTypes.TEXT,
    allowNull: false
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
  tableName: 'commentaries',
  timestamps: false
});

// Associations
Commentary.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
Commentary.belongsTo(Product, { foreignKey: 'product_id', as: 'product' });
User.hasMany(Commentary, { foreignKey: 'user_id', as: 'commentaries' });
Product.hasMany(Commentary, { foreignKey: 'product_id', as: 'commentaries' });

module.exports = Commentary; 