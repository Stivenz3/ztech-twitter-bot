"""
Bot principal de Twitter ZTech
Orquesta todas las funcionalidades del bot automatizado
"""
import schedule
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
from pathlib import Path

from config import Config
from database import DatabaseManager
from twitter_client import TwitterClient
from content_sources import ContentAggregator
from content_processor import ContentProcessor

class ZTechBot:
    """Bot principal de Twitter ZTech"""
    
    def __init__(self):
        """Inicializa el bot con todos sus componentes"""
        self.db = DatabaseManager()
        self.twitter = TwitterClient()
        self.content_aggregator = ContentAggregator()
        self.content_processor = ContentProcessor()
        
        # Configurar logging
        self._setup_logging()
        
        # Estadísticas del bot
        self.stats = {
            'tweets_published': 0,
            'content_processed': 0,
            'errors_count': 0,
            'last_run': None
        }
        
        logger.info("🤖 Bot ZTech inicializado correctamente")
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configurar loguru
        logger.remove()  # Remover handler por defecto
        
        # Handler para archivo
        logger.add(
            Config.LOG_FILE,
            rotation="1 day",
            retention="30 days",
            level=Config.LOG_LEVEL,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            encoding="utf-8"
        )
        
        # Handler para consola
        logger.add(
            lambda msg: print(msg, end=""),
            level=Config.LOG_LEVEL,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
            colorize=True
        )
    
    def run_single_post(self) -> bool:
        """
        Ejecuta una sola publicación de tweet
        
        Returns:
            True si se publicó exitosamente, False en caso contrario
        """
        try:
            logger.info("🚀 Iniciando publicación de tweet...")
            
            # Obtener contenido fresco
            fresh_content = self.content_aggregator.get_fresh_content(hours=24)
            
            if not fresh_content:
                logger.warning("⚠️ No hay contenido fresco disponible")
                return False
            
            # Filtrar contenido ya procesado
            unprocessed_content = []
            for article in fresh_content:
                content_hash = article.get('content_hash')
                if content_hash and not self.db.is_content_processed(content_hash):
                    unprocessed_content.append(article)
            
            if not unprocessed_content:
                logger.info("ℹ️ Todo el contenido ya fue procesado")
                return False
            
            # Seleccionar artículo aleatorio
            selected_article = unprocessed_content[0]  # Tomar el más reciente
            
            # Procesar artículo a tweet
            tweet_content = self.content_processor.process_article_to_tweet(selected_article)
            
            if not tweet_content:
                logger.warning("⚠️ No se pudo procesar el artículo a tweet")
                return False
            
            # Validar tweet
            if not self.content_processor.validate_tweet(tweet_content):
                logger.warning("⚠️ Tweet no válido")
                return False
            
            # Publicar tweet
            tweet_result = self.twitter.post_tweet(tweet_content)
            
            if tweet_result:
                # Guardar en base de datos
                self.db.save_published_tweet(
                    tweet_id=tweet_result['id'],
                    content=tweet_content,
                    source=selected_article.get('source'),
                    source_url=selected_article.get('source_url'),
                    engagement_data=tweet_result.get('public_metrics')
                )
                
                # Marcar contenido como procesado
                self.db.save_processed_content(
                    content_hash=selected_article.get('content_hash'),
                    source=selected_article.get('source'),
                    source_url=selected_article.get('source_url'),
                    title=selected_article.get('title'),
                    summary=selected_article.get('summary')
                )
                
                # Actualizar estadísticas
                self.stats['tweets_published'] += 1
                self.stats['content_processed'] += 1
                
                logger.info(f"✅ Tweet publicado exitosamente: {tweet_result['id']}")
                return True
            else:
                self.stats['errors_count'] += 1
                logger.error("❌ Error al publicar tweet")
                return False
                
        except Exception as e:
            self.stats['errors_count'] += 1
            logger.error(f"❌ Error en publicación: {e}")
            return False
    
    def run_curated_post(self) -> bool:
        """
        Ejecuta una publicación curada con múltiples artículos
        
        Returns:
            True si se publicó exitosamente, False en caso contrario
        """
        try:
            logger.info("📚 Iniciando publicación curada...")
            
            # Obtener contenido fresco
            fresh_content = self.content_aggregator.get_fresh_content(hours=24)
            
            if len(fresh_content) < 3:
                logger.warning("⚠️ No hay suficiente contenido para publicación curada")
                return self.run_single_post()  # Fallback a publicación simple
            
            # Crear tweet curado
            curated_tweet = self.content_processor.create_curated_tweet(fresh_content)
            
            if not curated_tweet:
                logger.warning("⚠️ No se pudo crear tweet curado")
                return False
            
            # Validar tweet
            if not self.content_processor.validate_tweet(curated_tweet):
                logger.warning("⚠️ Tweet curado no válido")
                return False
            
            # Publicar tweet
            tweet_result = self.twitter.post_tweet(curated_tweet)
            
            if tweet_result:
                # Guardar en base de datos
                self.db.save_published_tweet(
                    tweet_id=tweet_result['id'],
                    content=curated_tweet,
                    source="curated",
                    source_url="",
                    engagement_data=tweet_result.get('public_metrics')
                )
                
                # Marcar artículos como procesados
                for article in fresh_content[:3]:
                    if article.get('content_hash'):
                        self.db.save_processed_content(
                            content_hash=article.get('content_hash'),
                            source=article.get('source'),
                            source_url=article.get('source_url'),
                            title=article.get('title'),
                            summary=article.get('summary')
                        )
                
                self.stats['tweets_published'] += 1
                self.stats['content_processed'] += 3
                
                logger.info(f"✅ Tweet curado publicado: {tweet_result['id']}")
                return True
            else:
                self.stats['errors_count'] += 1
                logger.error("❌ Error al publicar tweet curado")
                return False
                
        except Exception as e:
            self.stats['errors_count'] += 1
            logger.error(f"❌ Error en publicación curada: {e}")
            return False
    
    def schedule_posts(self):
        """Configura el horario de publicaciones automáticas"""
        logger.info("⏰ Configurando horarios de publicación...")
        
        for schedule_time in Config.POSTING_SCHEDULE:
            # Publicación simple
            schedule.every().day.at(schedule_time).do(self._scheduled_post)
            logger.info(f"📅 Publicación programada a las {schedule_time}")
        
        # Publicación curada los viernes a las 17:00
        schedule.every().friday.at("17:00").do(self._scheduled_curated_post)
        logger.info("📅 Publicación curada programada los viernes a las 17:00")
    
    def _scheduled_post(self):
        """Ejecuta publicación programada"""
        logger.info("⏰ Ejecutando publicación programada...")
        success = self.run_single_post()
        
        if success:
            logger.info("✅ Publicación programada completada")
        else:
            logger.warning("⚠️ Publicación programada falló")
        
        self._update_daily_stats()
    
    def _scheduled_curated_post(self):
        """Ejecuta publicación curada programada"""
        logger.info("⏰ Ejecutando publicación curada programada...")
        success = self.run_curated_post()
        
        if success:
            logger.info("✅ Publicación curada programada completada")
        else:
            logger.warning("⚠️ Publicación curada programada falló")
        
        self._update_daily_stats()
    
    def _update_daily_stats(self):
        """Actualiza estadísticas diarias en la base de datos"""
        self.db.update_daily_stats(
            tweets_published=self.stats['tweets_published'],
            content_processed=self.stats['content_processed'],
            errors_count=self.stats['errors_count']
        )
        
        # Resetear estadísticas del día
        self.stats['tweets_published'] = 0
        self.stats['content_processed'] = 0
        self.stats['errors_count'] = 0
        self.stats['last_run'] = datetime.now()
    
    def run_continuous(self):
        """Ejecuta el bot en modo continuo"""
        logger.info("🔄 Iniciando bot en modo continuo...")
        
        # Configurar horarios
        self.schedule_posts()
        
        # Ejecutar una publicación inicial si es la primera vez del día
        if not self._has_posted_today():
            logger.info("🌅 Primera ejecución del día, publicando...")
            self.run_single_post()
            self._update_daily_stats()
        
        # Loop principal
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar cada minuto
                
        except KeyboardInterrupt:
            logger.info("⏹️ Bot detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error en loop principal: {e}")
        finally:
            self._update_daily_stats()
            logger.info("📊 Estadísticas finales guardadas")
    
    def _has_posted_today(self) -> bool:
        """Verifica si ya se publicó algo hoy"""
        try:
            today = datetime.now().date()
            recent_tweets = self.db.get_published_tweets(limit=10)
            
            for tweet in recent_tweets:
                tweet_date = datetime.fromisoformat(tweet['published_at']).date()
                if tweet_date == today:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error verificando publicaciones del día: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del bot"""
        try:
            daily_stats = self.db.get_daily_stats(days=7)
            recent_tweets = self.db.get_published_tweets(limit=5)
            
            return {
                'daily_stats': daily_stats,
                'recent_tweets': recent_tweets,
                'current_stats': self.stats,
                'rate_limits': self.twitter.get_rate_limit_status()
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Twitter API"""
        try:
            logger.info("🔍 Probando conexión con Twitter API...")
            
            if self.twitter.validate_credentials():
                logger.info("✅ Conexión con Twitter API exitosa")
                return True
            else:
                logger.error("❌ Error en conexión con Twitter API")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error probando conexión: {e}")
            return False
    
    def cleanup_old_data(self):
        """Limpia datos antiguos de la base de datos"""
        try:
            logger.info("🧹 Iniciando limpieza de datos antiguos...")
            self.db.cleanup_old_data(days_to_keep=30)
            logger.info("✅ Limpieza completada")
            
        except Exception as e:
            logger.error(f"❌ Error en limpieza: {e}")
