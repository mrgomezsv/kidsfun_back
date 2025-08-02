#!/usr/bin/env python3
"""
Script de pruebas para KidsFun Backend API
Autor: KidsFun Development Team
Fecha: 2024
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Colores para output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_status(message, color=Colors.BLUE):
    print(f"{color}[INFO]{Colors.END} {message}")

def print_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.END} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {message}")

def test_health_check():
    """Probar endpoint de health check"""
    print_status("Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("Health check OK")
            return True
        else:
            print_error(f"Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error en health check: {e}")
        return False

def test_auth():
    """Probar endpoints de autenticación"""
    print_status("Probando autenticación...")
    
    # Datos de prueba
    test_user = {
        "username": "test_user",
        "email": "test@kidsfun.com",
        "password": "test123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        # Registrar usuario
        print_status("  - Registrando usuario de prueba...")
        response = requests.post(f"{API_BASE}/auth/register", json=test_user)
        if response.status_code in [200, 201, 400]:  # 400 si ya existe
            print_success("  - Registro completado")
        else:
            print_error(f"  - Error en registro: {response.status_code}")
            return False
        
        # Login
        print_status("  - Probando login...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = requests.post(f"{API_BASE}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            if token:
                print_success("  - Login exitoso")
                return token
            else:
                print_error("  - No se recibió token")
                return False
        else:
            print_error(f"  - Error en login: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error en autenticación: {e}")
        return False

def test_products(token):
    """Probar endpoints de productos"""
    print_status("Probando productos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Listar productos
        print_status("  - Listando productos...")
        response = requests.get(f"{API_BASE}/products/", headers=headers)
        if response.status_code == 200:
            products = response.json()
            print_success(f"  - {len(products)} productos encontrados")
        else:
            print_error(f"  - Error listando productos: {response.status_code}")
            return False
        
        # Crear producto de prueba
        print_status("  - Creando producto de prueba...")
        test_product = {
            "title": "Producto de Prueba",
            "description": "Descripción de prueba",
            "price": 100.0,
            "category": "test",
            "circuits": 1,
            "dimensions": "10x10",
            "space": "100m2"
        }
        response = requests.post(f"{API_BASE}/products/", json=test_product, headers=headers)
        if response.status_code == 200:
            product_data = response.json()
            product_id = product_data.get("id")
            print_success(f"  - Producto creado con ID: {product_id}")
            return product_id
        else:
            print_error(f"  - Error creando producto: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error en productos: {e}")
        return False

def test_waiver():
    """Probar endpoints de waiver"""
    print_status("Probando sistema de waivers...")
    
    try:
        # Crear waiver de prueba
        print_status("  - Creando waiver de prueba...")
        test_waiver = {
            "user_id": "test_user_123",
            "user_name": "Usuario de Prueba",
            "user_email": "test@kidsfun.com",
            "relatives": [
                {"name": "Hijo 1", "age": 8},
                {"name": "Hija 1", "age": 6}
            ]
        }
        response = requests.post(f"{API_BASE}/waiver/", json=test_waiver)
        if response.status_code == 200:
            waiver_data = response.json()
            qr_code = waiver_data.get("waiver", {}).get("qr_code")
            print_success(f"  - Waiver creado con QR: {qr_code}")
            
            # Validar waiver
            print_status("  - Validando waiver...")
            validation_data = {"qr_code": qr_code}
            response = requests.post(f"{API_BASE}/waiver/validate", json=validation_data)
            if response.status_code == 200:
                validation_result = response.json()
                if validation_result.get("valid"):
                    print_success("  - Waiver válido")
                else:
                    print_warning("  - Waiver no válido")
            else:
                print_error(f"  - Error validando waiver: {response.status_code}")
            
            return qr_code
        else:
            print_error(f"  - Error creando waiver: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error en waivers: {e}")
        return False

def test_chat(token):
    """Probar endpoints de chat"""
    print_status("Probando sistema de chat...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Crear sala de chat
        print_status("  - Creando sala de chat...")
        response = requests.post(f"{API_BASE}/chat/rooms", headers=headers)
        if response.status_code == 200:
            room_data = response.json()
            room_id = room_data.get("id")
            print_success(f"  - Sala creada con ID: {room_id}")
            
            # Enviar mensaje
            print_status("  - Enviando mensaje de prueba...")
            message_data = {"content": "Mensaje de prueba desde script"}
            response = requests.post(f"{API_BASE}/chat/rooms/{room_id}/messages", 
                                   json=message_data, headers=headers)
            if response.status_code == 200:
                print_success("  - Mensaje enviado")
            else:
                print_error(f"  - Error enviando mensaje: {response.status_code}")
            
            # Obtener mensajes
            print_status("  - Obteniendo mensajes...")
            response = requests.get(f"{API_BASE}/chat/rooms/{room_id}/messages", headers=headers)
            if response.status_code == 200:
                messages = response.json()
                print_success(f"  - {len(messages)} mensajes encontrados")
            else:
                print_error(f"  - Error obteniendo mensajes: {response.status_code}")
            
            return room_id
        else:
            print_error(f"  - Error creando sala: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error en chat: {e}")
        return False

def test_likes_and_comments(token, product_id):
    """Probar likes y comentarios"""
    print_status("Probando likes y comentarios...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Crear like
        print_status("  - Creando like...")
        like_data = {
            "product": str(product_id),
            "is_favorite": True
        }
        response = requests.post(f"{API_BASE}/likes/", json=like_data, headers=headers)
        if response.status_code == 200:
            print_success("  - Like creado")
        else:
            print_error(f"  - Error creando like: {response.status_code}")
        
        # Crear comentario
        print_status("  - Creando comentario...")
        comment_data = {
            "product_id": product_id,
            "content": "Comentario de prueba"
        }
        response = requests.post(f"{API_BASE}/commentaries/", json=comment_data, headers=headers)
        if response.status_code == 200:
            print_success("  - Comentario creado")
        else:
            print_error(f"  - Error creando comentario: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error en likes y comentarios: {e}")

def main():
    """Función principal de pruebas"""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 60)
    print("🧪 PRUEBAS DE KIDSFUN BACKEND API")
    print("=" * 60)
    print(f"{Colors.END}")
    
    print_status(f"Iniciando pruebas en: {BASE_URL}")
    print_status(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Contador de pruebas
    total_tests = 0
    passed_tests = 0
    
    # Test 1: Health Check
    total_tests += 1
    if test_health_check():
        passed_tests += 1
    print()
    
    # Test 2: Autenticación
    total_tests += 1
    token = test_auth()
    if token:
        passed_tests += 1
    print()
    
    # Test 3: Productos
    total_tests += 1
    product_id = None
    if token:
        product_id = test_products(token)
        if product_id:
            passed_tests += 1
    print()
    
    # Test 4: Waivers
    total_tests += 1
    if test_waiver():
        passed_tests += 1
    print()
    
    # Test 5: Chat
    total_tests += 1
    if token and test_chat(token):
        passed_tests += 1
    print()
    
    # Test 6: Likes y Comentarios
    total_tests += 1
    if token and product_id:
        test_likes_and_comments(token, product_id)
        passed_tests += 1
    print()
    
    # Resumen final
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"{Colors.END}")
    
    print_status(f"Pruebas totales: {total_tests}")
    print_status(f"Pruebas exitosas: {passed_tests}")
    print_status(f"Pruebas fallidas: {total_tests - passed_tests}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print_status(f"Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print_success("🎉 ¡Backend listo para producción!")
    elif success_rate >= 60:
        print_warning("⚠️  Backend funcional pero requiere revisión")
    else:
        print_error("❌ Backend requiere correcciones antes del despliegue")
    
    print()
    print_status("📚 Documentación disponible en:")
    print_status(f"   • Swagger UI: {BASE_URL}/docs")
    print_status(f"   • ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main() 