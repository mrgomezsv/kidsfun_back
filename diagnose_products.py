#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de los productos en la base de datos
Uso: python3 diagnose_products.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_database_url():
    """Obtener la URL de la base de datos desde las variables de entorno"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurada en el archivo .env")
        sys.exit(1)
    return database_url

def check_database_connection():
    """Verificar la conexión a la base de datos"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)
        
        # Probar la conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            return engine
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        sys.exit(1)

def check_products_table(engine):
    """Verificar la tabla de productos"""
    try:
        with engine.connect() as connection:
            # Verificar si la tabla existe
            result = connection.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name = 't_app_product_product'
            """))
            table_exists = result.fetchone()[0] > 0
            
            if not table_exists:
                print("❌ La tabla t_app_product_product no existe")
                return False
            
            print("✅ Tabla t_app_product_product existe")
            
            # Contar productos
            result = connection.execute(text("SELECT COUNT(*) as count FROM t_app_product_product"))
            product_count = result.fetchone()[0]
            print(f"📊 Total de productos en la base de datos: {product_count}")
            
            # Verificar productos publicados
            result = connection.execute(text("SELECT COUNT(*) as count FROM t_app_product_product WHERE publicated = true"))
            published_count = result.fetchone()[0]
            print(f"📊 Productos publicados: {published_count}")
            
            # Mostrar algunos productos de ejemplo
            result = connection.execute(text("""
                SELECT id, title, category, publicated, created 
                FROM t_app_product_product 
                ORDER BY created DESC 
                LIMIT 5
            """))
            
            products = result.fetchall()
            if products:
                print("\n📋 Últimos 5 productos:")
                for product in products:
                    status = "✅ Publicado" if product.publicated else "❌ No publicado"
                    print(f"   - ID: {product.id}, Título: {product.title}, Categoría: {product.category}, {status}")
            else:
                print("⚠️  No hay productos en la base de datos")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar la tabla de productos: {e}")
        return False

def check_indexes(engine):
    """Verificar si los índices están creados"""
    try:
        with engine.connect() as connection:
            # Verificar índices de productos
            result = connection.execute(text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = 't_app_product_product' 
                AND indexname LIKE 'idx_%'
            """))
            
            indexes = [row[0] for row in result.fetchall()]
            print(f"\n🔍 Índices encontrados en t_app_product_product: {len(indexes)}")
            
            expected_indexes = [
                'idx_product_category',
                'idx_product_publicated', 
                'idx_product_user_id',
                'idx_product_title'
            ]
            
            for expected_index in expected_indexes:
                if expected_index in indexes:
                    print(f"   ✅ {expected_index}")
                else:
                    print(f"   ❌ {expected_index} (faltante)")
            
            return len(indexes) >= len(expected_indexes)
            
    except Exception as e:
        print(f"❌ Error al verificar índices: {e}")
        return False

def check_likes_table(engine):
    """Verificar la tabla de likes"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) as count FROM t_app_like_like"))
            likes_count = result.fetchone()[0]
            print(f"📊 Total de likes en la base de datos: {likes_count}")
            return True
    except Exception as e:
        print(f"❌ Error al verificar tabla de likes: {e}")
        return False

def check_comments_table(engine):
    """Verificar la tabla de comentarios"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) as count FROM t_app_commentary_commentary"))
            comments_count = result.fetchone()[0]
            print(f"📊 Total de comentarios en la base de datos: {comments_count}")
            return True
    except Exception as e:
        print(f"❌ Error al verificar tabla de comentarios: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Diagnóstico del sistema de productos - KidsFun Backend")
    print("=" * 60)
    
    # Verificar conexión a la base de datos
    engine = check_database_connection()
    
    # Verificar tabla de productos
    products_ok = check_products_table(engine)
    
    # Verificar índices
    indexes_ok = check_indexes(engine)
    
    # Verificar tablas relacionadas
    likes_ok = check_likes_table(engine)
    comments_ok = check_comments_table(engine)
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL DIAGNÓSTICO:")
    
    if products_ok:
        print("✅ Tabla de productos: OK")
    else:
        print("❌ Tabla de productos: PROBLEMA")
    
    if indexes_ok:
        print("✅ Índices de rendimiento: OK")
    else:
        print("❌ Índices de rendimiento: PROBLEMA")
    
    if likes_ok:
        print("✅ Tabla de likes: OK")
    else:
        print("❌ Tabla de likes: PROBLEMA")
    
    if comments_ok:
        print("✅ Tabla de comentarios: OK")
    else:
        print("❌ Tabla de comentarios: PROBLEMA")
    
    print("\n🎯 RECOMENDACIONES:")
    
    if not indexes_ok:
        print("   - Ejecutar migraciones: alembic upgrade head")
    
    if not products_ok:
        print("   - Verificar la estructura de la base de datos")
        print("   - Revisar las migraciones")
    
    print("\n✨ Diagnóstico completado")

if __name__ == "__main__":
    main() 