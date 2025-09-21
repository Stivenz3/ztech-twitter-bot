#!/usr/bin/env python3
"""
Script de prueba para el generador de contenido mejorado
"""
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from content_generator import ContentGenerator

def test_improved_generator():
    """Prueba el generador de contenido mejorado"""
    print("📝 Probando generador de contenido mejorado...")
    
    # Crear generador
    generator = ContentGenerator()
    
    # Probar diferentes tipos
    content_types = ['hacks', 'protips', 'top_lists', 'curiosities', 'controversial']
    
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
    test_improved_generator()
