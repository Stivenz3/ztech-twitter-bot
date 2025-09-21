"""
Configuración centralizada para el bot de Twitter ZTech
"""
import os
from typing import List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # Twitter API Credentials
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # Configuración de la aplicación
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', 'ztech')
    POSTING_SCHEDULE = os.getenv('POSTING_SCHEDULE', '09:00,18:00').split(',')
    TIMEZONE = os.getenv('TIMEZONE', 'America/Mexico_City')
    
    # Configuración de contenido
    MAX_TWEET_LENGTH = int(os.getenv('MAX_TWEET_LENGTH', '280'))
    HASHTAGS = os.getenv('HASHTAGS', '#tecnologia #innovacion #AI #programacion').split()
    CONTENT_SOURCES = os.getenv('CONTENT_SOURCES', 'rss,reddit,newsapi').split(',')
    
    # APIs externas
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    
    # Base de datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ztech_bot.db')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/ztech_bot.log')
    
    # URLs de fuentes RSS de tecnología
    RSS_FEEDS = [
        'https://feeds.feedburner.com/oreilly/radar',
        'https://techcrunch.com/feed/',
        'https://www.wired.com/feed/rss',
        'https://feeds.arstechnica.com/arstechnica/index/',
        'https://www.theverge.com/rss/index.xml',
        'https://feeds.feedburner.com/venturebeat/SZYF',
        'https://www.engadget.com/rss.xml',
        'https://feeds.feedburner.com/oreilly/radar',
        'https://www.zdnet.com/topic/artificial-intelligence/rss.xml',
        'https://feeds.feedburner.com/venturebeat/SZYF'
    ]
    
    # Subreddits de tecnología
    REDDIT_SUBREDDITS = [
        'technology',
        'programming',
        'MachineLearning',
        'artificial',
        'Futurology',
        'gadgets',
        'technews',
        'cybersecurity',
        'webdev',
        'datascience'
    ]
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida que todas las credenciales necesarias estén configuradas"""
        required_vars = [
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_BEARER_TOKEN'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
            print("📝 Copia el archivo env.example a .env y completa las credenciales")
            return False
        
        return True
