const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const bcrypt = require('bcryptjs');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    field: 'id'
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false
  },
  last_login: {
    type: DataTypes.DATE,
    allowNull: true
  },
  is_superuser: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  username: {
    type: DataTypes.STRING(150),
    unique: true,
    allowNull: false,
    validate: {
      len: [1, 150]
    }
  },
  first_name: {
    type: DataTypes.STRING(150),
    allowNull: false,
    validate: {
      len: [1, 150]
    }
  },
  last_name: {
    type: DataTypes.STRING(150),
    allowNull: false,
    validate: {
      len: [1, 150]
    }
  },
  email: {
    type: DataTypes.STRING(254),
    unique: true,
    allowNull: false,
    validate: {
      isEmail: true,
      len: [1, 254]
    }
  },
  is_staff: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  date_joined: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  }
}, {
  tableName: 'auth_user',
  timestamps: false,
  hooks: {
    beforeCreate: async (user) => {
      if (user.password) {
        user.password = await bcrypt.hash(user.password, 12);
      }
    },
    beforeUpdate: async (user) => {
      if (user.changed('password')) {
        user.password = await bcrypt.hash(user.password, 12);
      }
    }
  }
});

// Instance method to compare password
User.prototype.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Instance method to get full name
User.prototype.getFullName = function() {
  return `${this.first_name} ${this.last_name}`;
};

module.exports = User; 