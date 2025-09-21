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
    
    # OAuth 2.0 Credentials
    TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')
    
    # Configuración de la aplicación
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', 'ztech')
    POSTING_SCHEDULE = os.getenv('POSTING_SCHEDULE', '12:00,18:00').split(',')
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
    
    # URLs de fuentes RSS de tecnología (expandidas)
    RSS_FEEDS = [
        # Fuentes principales en inglés
        'https://techcrunch.com/feed/',
        'https://www.wired.com/feed/rss',
        'https://feeds.arstechnica.com/arstechnica/index/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.engadget.com/rss.xml',
        'https://www.zdnet.com/topic/artificial-intelligence/rss.xml',
        'https://feeds.feedburner.com/venturebeat/SZYF',
        'https://www.digitaltrends.com/feed/',
        'https://www.cnet.com/rss/news/',
        'https://feeds.feedburner.com/oreilly/radar',
        
        # Fuentes de programación y desarrollo
        'https://stackoverflow.blog/feed/',
        'https://dev.to/feed',
        'https://hackernoon.com/feed',
        'https://www.freecodecamp.org/news/rss/',
        'https://blog.codinghorror.com/rss/',
        
        # Fuentes de IA y Machine Learning
        'https://openai.com/blog/rss.xml',
        'https://blog.google/technology/ai/rss/',
        'https://www.artificialintelligence-news.com/feed/',
        'https://machinelearningmastery.com/feed/',
        
        # Fuentes en español
        'https://www.xataka.com/tag/tecnologia/rss2.xml',
        'https://www.genbeta.com/rss2.xml',
        'https://www.omicrono.com/feed/',
        'https://www.elandroidelibre.com/feed',
        'https://www.applesfera.com/rss2.xml',
        
        # Fuentes de startups y emprendimiento
        'https://techstartups.com/feed/',
        'https://www.startupgrind.com/blog/feed/',
        'https://www.entrepreneur.com/latest.rss',
        
        # Fuentes de ciberseguridad
        'https://krebsonsecurity.com/feed/',
        'https://www.darkreading.com/rss.xml',
        'https://feeds.feedburner.com/eset/blog',
        
        # Fuentes de blockchain y crypto
        'https://cointelegraph.com/rss',
        'https://decrypt.co/feed',
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        
        # Fuentes de hardware
        'https://www.anandtech.com/rss/',
        'https://www.tomshardware.com/feeds/all',
        'https://www.pcworld.com/index.rss'
    ]
    
    # Subreddits de tecnología (expandidos)
    REDDIT_SUBREDDITS = [
        # Tecnología general
        'technology',
        'technews',
        'gadgets',
        'Futurology',
        'tech',
        
        # Programación y desarrollo
        'programming',
        'webdev',
        'javascript',
        'Python',
        'reactjs',
        'node',
        'MachineLearning',
        'datascience',
        'artificial',
        
        # Startups y emprendimiento
        'startups',
        'entrepreneur',
        'SaaS',
        'productivity',
        
        # Ciberseguridad
        'cybersecurity',
        'netsec',
        'privacy',
        'hacking',
        
        # Blockchain y crypto
        'cryptocurrency',
        'Bitcoin',
        'ethereum',
        'blockchain',
        
        # Hardware
        'hardware',
        'buildapc',
        'Amd',
        'nvidia',
        
        # Mobile y apps
        'android',
        'iOS',
        'mobile',
        
        # Gaming tech
        'gaming',
        'pcgaming',
        'Steam'
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
