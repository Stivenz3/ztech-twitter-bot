"""
Script de prueba para el generador de IA mejorado
"""
import os
import sys
from pathlib import Path
from loguru import logger

sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from ai_content_generator_improved import AIContentGeneratorImproved

def test_improved_ai():
    """Prueba el generador de IA mejorado"""
    print("🤖 Probando Generador de IA Mejorado...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar API key
    api_key = os.getenv('QWEN_API_KEY')
    if not api_key:
        print("❌ QWEN_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:20]}...")
    
    # Crear generador
    generator = AIContentGeneratorImproved()
    
    # Verificar disponibilidad
    if not generator.is_available():
        print("❌ OpenRouter API no está disponible")
        return False
    
    print("✅ OpenRouter API está disponible")
    
    # Probar generación de contenido
    print("\n🧪 Probando generación de contenido mejorado...")
    
    # Probar diferentes tipos
    content_types_to_test = ['hacks', 'protips', 'curiosities', 'controversial']
    
    for content_type in content_types_to_test:
        print(f"\n📝 Generando {content_type}...")
        generated_content = generator.generate_content(content_type)
        if generated_content:
            print(f"✅ {content_type} generado:")
            print(f"   {generated_content}")
            print(f"   Longitud: {len(generated_content)} caracteres")
        else:
            print(f"❌ Error generando {content_type}")
    
    return True

if __name__ == "__main__":
    test_improved_ai()
