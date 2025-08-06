const { sequelize } = require('../config/database');
const User = require('../models/User');
const Product = require('../models/Product');
const Commentary = require('../models/Commentary');
const Like = require('../models/Like');

async function migrate() {
  try {
    console.log('🔄 Starting database migration...');
    
    // Sync all models
    await sequelize.sync({ force: false, alter: true });
    
    console.log('✅ Database migration completed successfully!');
    console.log('📊 Tables created/updated:');
    console.log('   - auth_user (Users)');
    console.log('   - t_app_product_product (Products)');
    console.log('   - commentaries (Commentaries)');
    console.log('   - likes (Likes)');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  }
}

migrate(); 