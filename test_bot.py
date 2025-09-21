#!/usr/bin/env python3
"""
Script de prueba para ZTech Twitter Bot
Verifica que todos los componentes funcionen correctamente
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from config import Config
from database import DatabaseManager
from twitter_client import TwitterClient
from content_sources import ContentAggregator
from content_processor import ContentProcessor

def test_config():
    """Prueba la configuración"""
    print("🔍 Probando configuración...")
    
    if Config.validate_config():
        print("✅ Configuración válida")
        return True
    else:
        print("❌ Configuración inválida")
        return False

def test_database():
    """Prueba la base de datos"""
    print("🗄️ Probando base de datos...")
    
    try:
        db = DatabaseManager("test_bot.db")
        print("✅ Base de datos inicializada correctamente")
        
        # Limpiar archivo de prueba
        Path("test_bot.db").unlink(missing_ok=True)
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def test_twitter_connection():
    """Prueba la conexión con Twitter"""
    print("🐦 Probando conexión con Twitter...")
    
    try:
        twitter = TwitterClient()
        if twitter.validate_credentials():
            print("✅ Conexión con Twitter exitosa")
            return True
        else:
            print("❌ Error en credenciales de Twitter")
            return False
    except Exception as e:
        print(f"❌ Error de conexión con Twitter: {e}")
        return False

def test_content_sources():
    """Prueba las fuentes de contenido"""
    print("📚 Probando fuentes de contenido...")
    
    try:
        aggregator = ContentAggregator()
        print(f"✅ {len(aggregator.sources)} fuentes de contenido inicializadas")
        
        # Probar una fuente RSS
        if aggregator.sources:
            content = aggregator.sources[0].fetch_content()
            print(f"✅ Fuente RSS funcionando: {len(content)} artículos obtenidos")
        
        return True
    except Exception as e:
        print(f"❌ Error en fuentes de contenido: {e}")
        return False

def test_content_processor():
    """Prueba el procesador de contenido"""
    print("⚙️ Probando procesador de contenido...")
    
    try:
        processor = ContentProcessor()
        
        # Artículo de prueba
        test_article = {
            'title': 'Nueva tecnología revoluciona la industria',
            'summary': 'Una innovación tecnológica está cambiando la forma en que trabajamos.',
            'link': 'https://example.com/noticia',
            'source': 'test',
            'content_hash': 'test123'
        }
        
        tweet = processor.process_article_to_tweet(test_article)
        
        if tweet and processor.validate_tweet(tweet):
            print("✅ Procesador de contenido funcionando")
            print(f"📝 Tweet generado: {tweet[:100]}...")
            return True
        else:
            print("❌ Error en procesador de contenido")
            return False
    except Exception as e:
        print(f"❌ Error en procesador: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas del ZTech Twitter Bot...")
    print("=" * 50)
    
    tests = [
        ("Configuración", test_config),
        ("Base de datos", test_database),
        ("Conexión Twitter", test_twitter_connection),
        ("Fuentes de contenido", test_content_sources),
        ("Procesador de contenido", test_content_processor)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE LAS PRUEBAS:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Resumen: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El bot está listo para usar.")
        return 0
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
        return 1

if __name__ == "__main__":
    exit(main())
