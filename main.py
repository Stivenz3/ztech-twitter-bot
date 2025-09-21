#!/usr/bin/env python3
"""
ZTech Twitter Bot - Bot automatizado para publicar contenido sobre tecnología
Autor: ZTech
Versión: 1.0.0

Este bot automatiza la publicación de contenido sobre tecnología en Twitter,
obteniendo información de múltiples fuentes RSS, APIs de noticias y Reddit.
"""

import sys
import argparse
from pathlib import Path
from loguru import logger

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from config import Config
from bot import ZTechBot

def main():
    """Función principal del bot"""
    parser = argparse.ArgumentParser(
        description="ZTech Twitter Bot - Automatización de publicaciones sobre tecnología"
    )
    
    parser.add_argument(
        '--mode',
        choices=['single', 'continuous', 'test', 'stats', 'cleanup'],
        default='continuous',
        help='Modo de ejecución del bot'
    )
    
    parser.add_argument(
        '--post-type',
        choices=['single', 'curated'],
        default='single',
        help='Tipo de publicación (solo para modo single)'
    )
    
    parser.add_argument(
        '--config-check',
        action='store_true',
        help='Verificar configuración sin ejecutar el bot'
    )
    
    args = parser.parse_args()
    
    # Verificar configuración
    if not Config.validate_config():
        logger.error("❌ Configuración inválida. Revisa el archivo .env")
        return 1
    
    if args.config_check:
        logger.info("✅ Configuración válida")
        return 0
    
    try:
        # Inicializar bot
        bot = ZTechBot()
        
        if args.mode == 'test':
            # Modo de prueba
            logger.info("🧪 Modo de prueba - verificando conexiones...")
            
            if bot.test_connection():
                logger.info("✅ Todas las conexiones funcionan correctamente")
                return 0
            else:
                logger.error("❌ Error en las conexiones")
                return 1
        
        elif args.mode == 'single':
            # Modo de publicación única
            logger.info(f"📝 Modo de publicación única ({args.post_type})")
            
            if args.post_type == 'curated':
                success = bot.run_curated_post()
            else:
                success = bot.run_single_post()
            
            if success:
                logger.info("✅ Publicación completada exitosamente")
                return 0
            else:
                logger.error("❌ Error en la publicación")
                return 1
        
        elif args.mode == 'stats':
            # Mostrar estadísticas
            logger.info("📊 Obteniendo estadísticas del bot...")
            stats = bot.get_stats()
            
            if stats:
                print("\n" + "="*50)
                print("📊 ESTADÍSTICAS DEL BOT ZTECH")
                print("="*50)
                
                # Estadísticas diarias
                daily_stats = stats.get('daily_stats', [])
                if daily_stats:
                    print("\n📅 Estadísticas de los últimos 7 días:")
                    for day_stat in daily_stats:
                        print(f"  {day_stat['date']}: {day_stat['tweets_published']} tweets, "
                              f"{day_stat['content_processed']} contenidos, "
                              f"{day_stat['errors_count']} errores")
                
                # Tweets recientes
                recent_tweets = stats.get('recent_tweets', [])
                if recent_tweets:
                    print(f"\n🐦 Últimos {len(recent_tweets)} tweets:")
                    for tweet in recent_tweets:
                        print(f"  {tweet['published_at']}: {tweet['content'][:50]}...")
                
                # Rate limits
                rate_limits = stats.get('rate_limits', {})
                if rate_limits:
                    print("\n⏱️ Estado de rate limits:")
                    for endpoint, limit_info in rate_limits.items():
                        print(f"  {endpoint}: {limit_info['remaining']}/{limit_info['limit']}")
                
                print("="*50)
                return 0
            else:
                logger.error("❌ Error obteniendo estadísticas")
                return 1
        
        elif args.mode == 'cleanup':
            # Limpiar datos antiguos
            logger.info("🧹 Limpiando datos antiguos...")
            bot.cleanup_old_data()
            logger.info("✅ Limpieza completada")
            return 0
        
        else:  # continuous
            # Modo continuo
            logger.info("🔄 Iniciando bot en modo continuo...")
            bot.run_continuous()
            return 0
    
    except KeyboardInterrupt:
        logger.info("⏹️ Bot detenido por el usuario")
        return 0
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
