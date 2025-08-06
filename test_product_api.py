#!/usr/bin/env python3
"""
Script para probar la API de productos específicos
Uso: python3 test_product_api.py [product_id]
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_product_api(product_id=None):
    """Probar la API de productos"""
    base_url = "https://api.kidsfunyfiestasinfantiles.com/api"
    
    print("🔍 Probando API de productos...")
    print("=" * 50)
    
    if product_id:
        # Probar producto específico
        url = f"{base_url}/products/{product_id}"
        print(f"📡 Probando: GET {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                product = response.json()
                print(f"✅ Producto encontrado: {product.get('title', 'Sin título')}")
                print(f"   - ID: {product.get('id')}")
                print(f"   - Categoría: {product.get('category')}")
                print(f"   - Publicado: {product.get('publicated')}")
                print(f"   - Precio: {product.get('price')}")
                print(f"   - Dimensiones: {product.get('dimensions')}")
                print(f"   - Likes: {product.get('likes_count', 0)}")
                print(f"   - Comentarios: {product.get('comments_count', 0)}")
                
                # Verificar imágenes
                images = [
                    product.get('img'),
                    product.get('img1'),
                    product.get('img2'),
                    product.get('img3'),
                    product.get('img4'),
                    product.get('img5')
                ]
                
                valid_images = [img for img in images if img and img.strip()]
                print(f"   - Imágenes válidas: {len(valid_images)}/6")
                
                if not valid_images:
                    print("   ⚠️  ADVERTENCIA: No hay imágenes válidas")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Mensaje: {error_data.get('detail', 'Sin mensaje')}")
                except:
                    print(f"   Respuesta: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False
    else:
        # Probar lista de productos
        url = f"{base_url}/products/"
        print(f"📡 Probando: GET {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                products = response.json()
                print(f"✅ Productos encontrados: {len(products)}")
                
                # Mostrar algunos productos
                for i, product in enumerate(products[:5]):
                    print(f"   {i+1}. ID: {product.get('id')}, Título: {product.get('title')}, Publicado: {product.get('publicated')}")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Mensaje: {error_data.get('detail', 'Sin mensaje')}")
                except:
                    print(f"   Respuesta: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        try:
            product_id = int(sys.argv[1])
            print(f"🔍 Probando producto específico - ID: {product_id}")
        except ValueError:
            print("❌ Error: El ID del producto debe ser un número")
            sys.exit(1)
    else:
        product_id = None
        print("🔍 Probando lista de productos")
    
    print("=" * 60)
    
    success = test_product_api(product_id)
    
    if success:
        print("\n✅ Prueba completada exitosamente")
    else:
        print("\n❌ Prueba falló")
        sys.exit(1)

if __name__ == "__main__":
    main() 