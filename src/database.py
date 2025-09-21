"""
Módulo de base de datos para el bot de Twitter ZTech
Maneja el almacenamiento de tweets publicados y contenido procesado
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from loguru import logger
from pathlib import Path

class DatabaseManager:
    """Gestor de base de datos SQLite para el bot"""
    
    def __init__(self, db_path: str = "ztech_bot.db"):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa las tablas de la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabla de tweets publicados
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS published_tweets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tweet_id TEXT UNIQUE,
                        content TEXT NOT NULL,
                        source TEXT,
                        source_url TEXT,
                        published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        engagement_data TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabla de contenido procesado
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS processed_content (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content_hash TEXT UNIQUE,
                        source TEXT NOT NULL,
                        source_url TEXT,
                        title TEXT,
                        summary TEXT,
                        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        used BOOLEAN DEFAULT FALSE
                    )
                """)
                
                # Tabla de configuración
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bot_config (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabla de estadísticas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bot_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE,
                        tweets_published INTEGER DEFAULT 0,
                        content_processed INTEGER DEFAULT 0,
                        errors_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("✅ Base de datos inicializada correctamente")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al inicializar la base de datos: {e}")
            raise
    
    def save_published_tweet(self, tweet_id: str, content: str, source: str = None, 
                           source_url: str = None, engagement_data: Dict = None):
        """
        Guarda un tweet publicado en la base de datos
        
        Args:
            tweet_id: ID del tweet en Twitter
            content: Contenido del tweet
            source: Fuente del contenido
            source_url: URL de la fuente
            engagement_data: Datos de engagement del tweet
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO published_tweets 
                    (tweet_id, content, source, source_url, engagement_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    tweet_id, 
                    content, 
                    source, 
                    source_url, 
                    json.dumps(engagement_data) if engagement_data else None
                ))
                conn.commit()
                logger.info(f"✅ Tweet guardado en BD: {tweet_id}")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al guardar tweet: {e}")
            raise
    
    def save_processed_content(self, content_hash: str, source: str, 
                             source_url: str = None, title: str = None, 
                             summary: str = None):
        """
        Guarda contenido procesado para evitar duplicados
        
        Args:
            content_hash: Hash único del contenido
            source: Fuente del contenido
            source_url: URL de la fuente
            title: Título del contenido
            summary: Resumen del contenido
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO processed_content 
                    (content_hash, source, source_url, title, summary)
                    VALUES (?, ?, ?, ?, ?)
                """, (content_hash, source, source_url, title, summary))
                conn.commit()
                logger.debug(f"Contenido procesado guardado: {content_hash}")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al guardar contenido procesado: {e}")
            raise
    
    def is_content_processed(self, content_hash: str) -> bool:
        """
        Verifica si el contenido ya fue procesado
        
        Args:
            content_hash: Hash del contenido o enlace a verificar
            
        Returns:
            True si ya fue procesado, False en caso contrario
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar por hash del contenido
                cursor.execute("""
                    SELECT COUNT(*) FROM processed_content 
                    WHERE content_hash = ?
                """, (content_hash,))
                count = cursor.fetchone()[0]
                
                if count > 0:
                    return True
                
                # Verificar por enlace (para evitar duplicados de enlaces)
                cursor.execute("""
                    SELECT COUNT(*) FROM processed_content 
                    WHERE content_url = ?
                """, (content_hash,))
                count = cursor.fetchone()[0]
                
                return count > 0
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al verificar contenido procesado: {e}")
            return False
    
    def get_published_tweets(self, limit: int = 100) -> List[Dict]:
        """
        Obtiene tweets publicados recientes
        
        Args:
            limit: Número máximo de tweets a obtener
            
        Returns:
            Lista de diccionarios con información de tweets
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM published_tweets 
                    ORDER BY published_at DESC 
                    LIMIT ?
                """, (limit,))
                
                tweets = []
                for row in cursor.fetchall():
                    tweet = dict(row)
                    if tweet['engagement_data']:
                        tweet['engagement_data'] = json.loads(tweet['engagement_data'])
                    tweets.append(tweet)
                
                return tweets
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al obtener tweets publicados: {e}")
            return []
    
    def update_daily_stats(self, tweets_published: int = 0, 
                          content_processed: int = 0, errors_count: int = 0):
        """
        Actualiza las estadísticas diarias del bot
        
        Args:
            tweets_published: Número de tweets publicados hoy
            content_processed: Número de contenidos procesados hoy
            errors_count: Número de errores hoy
        """
        try:
            today = datetime.now().date()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar si ya existe registro para hoy
                cursor.execute("""
                    SELECT id FROM bot_stats WHERE date = ?
                """, (today,))
                
                if cursor.fetchone():
                    # Actualizar registro existente
                    cursor.execute("""
                        UPDATE bot_stats 
                        SET tweets_published = tweets_published + ?,
                            content_processed = content_processed + ?,
                            errors_count = errors_count + ?
                        WHERE date = ?
                    """, (tweets_published, content_processed, errors_count, today))
                else:
                    # Crear nuevo registro
                    cursor.execute("""
                        INSERT INTO bot_stats 
                        (date, tweets_published, content_processed, errors_count)
                        VALUES (?, ?, ?, ?)
                    """, (today, tweets_published, content_processed, errors_count))
                
                conn.commit()
                logger.info(f"📊 Estadísticas actualizadas para {today}")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al actualizar estadísticas: {e}")
    
    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """
        Obtiene estadísticas de los últimos días
        
        Args:
            days: Número de días hacia atrás
            
        Returns:
            Lista de estadísticas diarias
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM bot_stats 
                    ORDER BY date DESC 
                    LIMIT ?
                """, (days,))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error al obtener estadísticas: {e}")
            return []
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """
        Limpia datos antiguos de la base de datos
        
        Args:
            days_to_keep: Días de datos a mantener
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Limpiar contenido procesado antiguo
                cursor.execute("""
                    DELETE FROM processed_content 
                    WHERE processed_at < ?
                """, (cutoff_date,))
                
                deleted_content = cursor.rowcount
                
                # Limpiar estadísticas antiguas
                cursor.execute("""
                    DELETE FROM bot_stats 
                    WHERE date < date('now', '-{} days')
                """.format(days_to_keep))
                
                deleted_stats = cursor.rowcount
                
                conn.commit()
                logger.info(f"🧹 Limpieza completada: {deleted_content} contenidos, {deleted_stats} estadísticas")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Error en limpieza de datos: {e}")
