"""
Script de debug para verificar por qué la IA no está funcionando
"""
import os
import sys
from pathlib import Path
from loguru import logger

sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from ai_content_generator_improved import AIContentGeneratorImproved
from config import Config

def debug_ai():
    """Debug de la configuración de IA"""
    print("🔍 Debug de configuración de IA...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables de entorno
    print(f"\n📋 Variables de entorno:")
    print(f"   QWEN_API_KEY: {'✅ Configurada' if os.getenv('QWEN_API_KEY') else '❌ No configurada'}")
    print(f"   USE_AI_CONTENT: {os.getenv('USE_AI_CONTENT', 'No configurada')}")
    print(f"   AI_MODEL_PREFERENCE: {os.getenv('AI_MODEL_PREFERENCE', 'No configurada')}")
    
    # Verificar configuración
    print(f"\n⚙️ Configuración:")
    print(f"   Config.USE_AI_CONTENT: {Config.USE_AI_CONTENT}")
    print(f"   Config.AI_MODEL_PREFERENCE: {Config.AI_MODEL_PREFERENCE}")
    
    # Crear generador
    print(f"\n🤖 Creando generador de IA...")
    generator = AIContentGeneratorImproved()
    
    # Verificar disponibilidad
    print(f"   IA disponible: {generator.is_available()}")
    
    if generator.is_available():
        print(f"\n🧪 Probando generación...")
        content = generator.generate_content('curiosities')
        if content:
            print(f"✅ Contenido generado:")
            print(f"   Longitud: {len(content)} caracteres")
            print(f"   Contenido: {content[:200]}...")
        else:
            print(f"❌ No se pudo generar contenido")
    else:
        print(f"❌ IA no está disponible")
        print(f"   OpenRouter: {generator.openrouter_available}")
        print(f"   OpenAI: {generator.openai_client is not None}")
        print(f"   Anthropic: {generator.anthropic_client is not None}")

if __name__ == "__main__":
    debug_ai()
