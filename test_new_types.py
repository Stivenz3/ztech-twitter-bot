"""
Script de prueba para los nuevos tipos trends y reviews
"""
import sys
from pathlib import Path
from loguru import logger

sys.path.append(str(Path(__file__).parent / "src"))

from content_generator import ContentGenerator

def test_new_types():
    """Prueba los nuevos tipos trends y reviews"""
    print("🧪 Probando nuevos tipos: trends y reviews...")
    
    # Crear generador
    generator = ContentGenerator(language='es')
    
    # Probar trends
    print(f"\n📝 Generando trends...")
    trends_content = generator.generate_content('trends')
    if trends_content:
        print(f"✅ trends generado:")
        print(f"   {trends_content}")
        print(f"   Longitud: {len(trends_content)} caracteres")
    else:
        print(f"❌ Error generando trends")
    
    # Probar reviews
    print(f"\n📝 Generando reviews...")
    reviews_content = generator.generate_content('reviews')
    if reviews_content:
        print(f"✅ reviews generado:")
        print(f"   {reviews_content}")
        print(f"   Longitud: {len(reviews_content)} caracteres")
    else:
        print(f"❌ Error generando reviews")

if __name__ == "__main__":
    test_new_types()
