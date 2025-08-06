"""Add performance indexes

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Agregar índices para mejorar el rendimiento de las consultas
    op.create_index('idx_product_category', 't_app_product_product', ['category'])
    op.create_index('idx_product_publicated', 't_app_product_product', ['publicated'])
    op.create_index('idx_product_user_id', 't_app_product_product', ['user_id'])
    op.create_index('idx_product_title', 't_app_product_product', ['title'])
    
    # Índices para likes
    op.create_index('idx_like_product', 't_app_like_like', ['product'])
    op.create_index('idx_like_is_favorite', 't_app_like_like', ['is_favorite'])
    op.create_index('idx_like_product_favorite', 't_app_like_like', ['product', 'is_favorite'])
    
    # Índices para comentarios
    op.create_index('idx_commentary_product_id', 't_app_commentary_commentary', ['product_id'])
    op.create_index('idx_commentary_created', 't_app_commentary_commentary', ['created'])

def downgrade():
    # Remover índices
    op.drop_index('idx_product_category', table_name='t_app_product_product')
    op.drop_index('idx_product_publicated', table_name='t_app_product_product')
    op.drop_index('idx_product_user_id', table_name='t_app_product_product')
    op.drop_index('idx_product_title', table_name='t_app_product_product')
    
    op.drop_index('idx_like_product', table_name='t_app_like_like')
    op.drop_index('idx_like_is_favorite', table_name='t_app_like_like')
    op.drop_index('idx_like_product_favorite', table_name='t_app_like_like')
    
    op.drop_index('idx_commentary_product_id', table_name='t_app_commentary_commentary')
    op.drop_index('idx_commentary_created', table_name='t_app_commentary_commentary') 