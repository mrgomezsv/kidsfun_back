#!/usr/bin/env python3
"""
Script para diagnosticar productos específicos que no devuelven información
Uso: python3 diagnose_specific_product.py [product_id]
"""

import os
import sys
import json
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

def diagnose_product(engine, product_id):
    """Diagnosticar un producto específico"""
    try:
        with engine.connect() as connection:
            print(f"\n🔍 Diagnosticando producto ID: {product_id}")
            print("=" * 50)
            
            # Verificar si el producto existe
            result = connection.execute(text("""
                SELECT id, title, description, category, publicated, created, 
                       img, img1, img2, img3, img4, img5, dimensions, circuits, space,
                       youtube_url, user_id, price
                FROM t_app_product_product 
                WHERE id = :product_id
            """), {"product_id": product_id})
            
            product = result.fetchone()
            
            if not product:
                print(f"❌ Producto con ID {product_id} no encontrado")
                return False
            
            print(f"✅ Producto encontrado: {product.title}")
            print(f"   - Categoría: {product.category}")
            print(f"   - Publicado: {'✅ Sí' if product.publicated else '❌ No'}")
            print(f"   - Creado: {product.created}")
            print(f"   - Usuario ID: {product.user_id}")
            print(f"   - Precio: {product.price}")
            print(f"   - Dimensiones: {product.dimensions}")
            print(f"   - Circuitos: {product.circuits}")
            print(f"   - Espacio: {product.space}")
            print(f"   - YouTube URL: {product.youtube_url}")
            
            # Verificar imágenes
            print(f"\n🖼️  Imágenes:")
            images = [product.img, product.img1, product.img2, product.img3, product.img4, product.img5]
            for i, img in enumerate(images, 1):
                if img and img.strip():
                    print(f"   - img{i}: {img}")
                else:
                    print(f"   - img{i}: ❌ Vacía o nula")
            
            # Verificar si hay likes (si la tabla existe)
            try:
                result = connection.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM t_app_like_like 
                    WHERE product = :product_id AND is_favorite = true
                """), {"product_id": str(product_id)})
                likes_count = result.fetchone()[0]
                print(f"\n❤️  Likes: {likes_count}")
            except Exception as e:
                print(f"\n❤️  Likes: Tabla no existe o error - {e}")
            
            # Verificar si hay comentarios (si la tabla existe)
            try:
                result = connection.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM t_app_commentary_commentary 
                    WHERE product_id = :product_id
                """), {"product_id": product_id})
                comments_count = result.fetchone()[0]
                print(f"💬 Comentarios: {comments_count}")
            except Exception as e:
                print(f"💬 Comentarios: Tabla no existe o error - {e}")
            
            # Verificar si el producto está publicado
            if not product.publicated:
                print(f"\n⚠️  ADVERTENCIA: El producto NO está publicado")
                print(f"   Esto puede ser la razón por la que no se muestra en el frontend")
            
            # Verificar si tiene imágenes
            valid_images = [img for img in images if img and img.strip()]
            if not valid_images:
                print(f"\n⚠️  ADVERTENCIA: El producto no tiene imágenes")
                print(f"   Esto puede causar problemas en el frontend")
            
            # Verificar si tiene descripción
            if not product.description or not product.description.strip():
                print(f"\n⚠️  ADVERTENCIA: El producto no tiene descripción")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al diagnosticar producto: {e}")
        return False

def list_problematic_products(engine):
    """Listar productos que pueden tener problemas"""
    try:
        with engine.connect() as connection:
            print(f"\n🔍 Buscando productos problemáticos...")
            print("=" * 50)
            
            # Productos no publicados
            result = connection.execute(text("""
                SELECT id, title, category, created
                FROM t_app_product_product 
                WHERE publicated = false
                ORDER BY created DESC
            """))
            
            unpublished = result.fetchall()
            if unpublished:
                print(f"\n❌ Productos NO publicados ({len(unpublished)}):")
                for product in unpublished:
                    print(f"   - ID: {product.id}, Título: {product.title}, Categoría: {product.category}")
            else:
                print(f"\n✅ Todos los productos están publicados")
            
            # Productos sin imágenes
            result = connection.execute(text("""
                SELECT id, title, category, created
                FROM t_app_product_product 
                WHERE (img IS NULL OR img = '' OR img = 'default_product_image.jpg')
                AND (img1 IS NULL OR img1 = '' OR img1 = 'default_product_image.jpg')
                AND (img2 IS NULL OR img2 = '' OR img2 = 'default_product_image.jpg')
                AND (img3 IS NULL OR img3 = '' OR img3 = 'default_product_image.jpg')
                AND (img4 IS NULL OR img4 = '' OR img4 = 'default_product_image.jpg')
                AND (img5 IS NULL OR img5 = '' OR img5 = 'default_product_image.jpg')
                ORDER BY created DESC
            """))
            
            no_images = result.fetchall()
            if no_images:
                print(f"\n⚠️  Productos sin imágenes ({len(no_images)}):")
                for product in no_images:
                    print(f"   - ID: {product.id}, Título: {product.title}, Categoría: {product.category}")
            else:
                print(f"\n✅ Todos los productos tienen imágenes")
            
            # Productos sin descripción
            result = connection.execute(text("""
                SELECT id, title, category, created
                FROM t_app_product_product 
                WHERE description IS NULL OR description = '' OR description = 'None'
                ORDER BY created DESC
            """))
            
            no_description = result.fetchall()
            if no_description:
                print(f"\n⚠️  Productos sin descripción ({len(no_description)}):")
                for product in no_description:
                    print(f"   - ID: {product.id}, Título: {product.title}, Categoría: {product.category}")
            else:
                print(f"\n✅ Todos los productos tienen descripción")
            
    except Exception as e:
        print(f"❌ Error al listar productos problemáticos: {e}")

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        product_id = int(sys.argv[1])
        print(f"🔍 Diagnóstico de producto específico - ID: {product_id}")
    else:
        print("🔍 Diagnóstico general de productos problemáticos")
    
    print("=" * 60)
    
    # Verificar conexión a la base de datos
    engine = check_database_connection()
    
    if len(sys.argv) > 1:
        # Diagnosticar producto específico
        diagnose_product(engine, product_id)
    else:
        # Listar productos problemáticos
        list_problematic_products(engine)
    
    print("\n✨ Diagnóstico completado")

if __name__ == "__main__":
    main() 