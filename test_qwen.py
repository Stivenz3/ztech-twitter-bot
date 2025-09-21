#!/usr/bin/env python3
"""
Script de prueba para verificar que Qwen API esté funcionando
"""
import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from ai_content_generator import AIContentGenerator

def test_openrouter():
    """Prueba la API de OpenRouter"""
    print("🤖 Probando OpenRouter API...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar API key
    api_key = os.getenv('QWEN_API_KEY')
    if not api_key:
        print("❌ QWEN_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:20]}...")
    
    # Crear generador
    generator = AIContentGenerator()
    
    # Verificar disponibilidad
    if not generator.is_available():
        print("❌ OpenRouter API no está disponible")
        return False
    
    print("✅ OpenRouter API está disponible")
    
    # Probar generación de contenido
    print("\n🧪 Probando generación de contenido...")
    
    # Probar diferentes tipos
    content_types = ['hacks', 'protips', 'curiosities', 'controversial']
    
    for content_type in content_types:
        print(f"\n📝 Generando {content_type}...")
        content = generator.generate_content(content_type)
        
        if content:
            print(f"✅ {content_type} generado:")
            print(f"   {content}")
            print(f"   Longitud: {len(content)} caracteres")
        else:
            print(f"❌ Error generando {content_type}")
    
    return True

if __name__ == "__main__":
    test_openrouter()
