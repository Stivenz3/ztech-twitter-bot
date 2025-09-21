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
    CONTENT_SOURCES = os.getenv('CONTENT_SOURCES', 'rss,reddit,newsapi,youtube,tiktok,instagram,linkedin,medium,devto').split(',')
    
    # Tipos de publicaciones disponibles
    POST_TYPES = [
        'single',      # Una noticia con enlace
        'curated',     # Múltiples noticias
        'hacks',       # Tips y trucos tecnológicos
        'protips',     # Consejos profesionales
        'top_lists',   # Rankings y listas
        'curiosities', # Datos curiosos
        'controversial', # Contenido polémico
        'history',     # Historia de la tecnología
        'trends',      # Trends virales
        'reviews'      # Reseñas y análisis
    ]
    
    # Configuración de tipos de publicaciones
    POST_TYPE_WEIGHTS = {
        'single': 0.25,      # 25% - Noticias principales
        'curated': 0.15,     # 15% - Múltiples noticias
        'hacks': 0.15,       # 15% - Tips y trucos
        'protips': 0.10,     # 10% - Consejos profesionales
        'top_lists': 0.10,   # 10% - Rankings
        'curiosities': 0.10, # 10% - Datos curiosos
        'controversial': 0.05, # 5% - Contenido polémico
        'history': 0.05,     # 5% - Historia
        'trends': 0.03,      # 3% - Trends virales
        'reviews': 0.02      # 2% - Reseñas
    }
    
    # Configuración de engagement
    USE_CONTROVERSIAL_TITLES = os.getenv('USE_CONTROVERSIAL_TITLES', 'true').lower() == 'true'
    USE_IMAGES = os.getenv('USE_IMAGES', 'true').lower() == 'true'
    MIN_CONTENT_LENGTH = int(os.getenv('MIN_CONTENT_LENGTH', '150'))
    
    # Configuración de idiomas por región
    US_LANGUAGE = 'en'
    COLOMBIA_LANGUAGE = 'es'
    
    # Palabras clave para títulos polémicos
    CONTROVERSIAL_KEYWORDS = {
        'en': [
            'shocking', 'breaking', 'exclusive', 'controversial', 'scandal', 
            'revolutionary', 'game-changing', 'unprecedented', 'explosive',
            'leaked', 'exposed', 'revealed', 'outrageous', 'incredible'
        ],
        'es': [
            'impactante', 'exclusivo', 'controversial', 'escándalo', 'revolucionario',
            'cambia el juego', 'sin precedentes', 'explosivo', 'filtrado', 'expuesto',
            'revelado', 'escandaloso', 'increíble', 'sorprendente', 'polémico'
        ]
    }
    
    # URLs de imágenes por categoría
    IMAGE_URLS = {
        'ai': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
        'programming': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=600&fit=crop',
        'startup': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=600&fit=crop',
        'cybersecurity': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=600&fit=crop',
        'blockchain': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&h=600&fit=crop',
        'hardware': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop',
        'mobile': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&h=600&fit=crop',
        'default': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop'
    }
    
    # APIs externas
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    
    # APIs de IA para generación de contenido
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Configuración de IA
    USE_AI_CONTENT = os.getenv('USE_AI_CONTENT', 'false').lower() == 'true'
    AI_MODEL_PREFERENCE = os.getenv('AI_MODEL_PREFERENCE', 'openrouter')  # 'openrouter', 'openai' o 'anthropic'
    
    # Fuentes de YouTube para tecnología
    YOUTUBE_CHANNELS = [
        'UCBJycsmduvYEL83R_U4JriQ',  # Marques Brownlee
        'UCXuqSBlHAE6Xw-yeJA0Tunw',  # Linus Tech Tips
        'UCeeFfhMcJa1kjtfZAGskOCA',  # TechWorld with Nana
        'UCBJycsmduvYEL83R_U4JriQ',  # The Verge
        'UCBJycsmduvYEL83R_U4JriQ',  # TechCrunch
        'UCBJycsmduvYEL83R_U4JriQ',  # Wired
        'UCBJycsmduvYEL83R_U4JriQ',  # Ars Technica
        'UCBJycsmduvYEL83R_U4JriQ',  # Engadget
        'UCBJycsmduvYEL83R_U4JriQ',  # CNET
        'UCBJycsmduvYEL83R_U4JriQ'   # Digital Trends
    ]
    
    # Fuentes de TikTok para trends virales
    TIKTOK_HASHTAGS = [
        '#tech', '#technology', '#programming', '#coding', '#ai', '#artificialintelligence',
        '#machinelearning', '#cybersecurity', '#blockchain', '#crypto', '#startup',
        '#entrepreneur', '#innovation', '#gadgets', '#smartphone', '#laptop', '#gaming',
        '#techhack', '#techtip', '#techreview', '#technews', '#techtrends'
    ]
    
    # Fuentes de Instagram para tech influencers
    INSTAGRAM_HASHTAGS = [
        '#tech', '#technology', '#programming', '#coding', '#ai', '#artificialintelligence',
        '#machinelearning', '#cybersecurity', '#blockchain', '#crypto', '#startup',
        '#entrepreneur', '#innovation', '#gadgets', '#smartphone', '#laptop', '#gaming',
        '#techhack', '#techtip', '#techreview', '#technews', '#techtrends'
    ]
    
    # Fuentes de LinkedIn para artículos profesionales
    LINKEDIN_TOPICS = [
        'artificial-intelligence', 'machine-learning', 'cybersecurity', 'blockchain',
        'cloud-computing', 'data-science', 'programming', 'software-development',
        'startups', 'entrepreneurship', 'innovation', 'technology', 'digital-transformation'
    ]
    
    # Fuentes de Medium para artículos técnicos
    MEDIUM_TAGS = [
        'technology', 'programming', 'artificial-intelligence', 'machine-learning',
        'cybersecurity', 'blockchain', 'startup', 'entrepreneurship', 'innovation',
        'software-development', 'web-development', 'mobile-development', 'data-science'
    ]
    
    # Fuentes de Dev.to para comunidad de desarrolladores
    DEV_TO_TAGS = [
        'javascript', 'python', 'java', 'cpp', 'golang', 'rust', 'react', 'node',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ai', 'machinelearning',
        'cybersecurity', 'blockchain', 'startup', 'programming', 'webdev'
    ]
    
    # Base de datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ztech_bot.db')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/ztech_bot.log')
    
    # URLs de fuentes RSS organizadas por región e idioma
    RSS_FEEDS_US = [
        # Fuentes principales en inglés para Estados Unidos
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
        
        # Fuentes de startups y emprendimiento
        'https://techstartups.com/feed/',
        'https://www.startupgrind.com/blog/feed/',
        'https://www.entrepreneur.com/latest.rss',
        
        # Fuentes de ciberseguridad
        'https://krebsonsecurity.com/feed/',
        'https://www.darkreading.com/rss.xml',
        
        # Fuentes de blockchain y crypto
        'https://cointelegraph.com/rss',
        'https://decrypt.co/feed',
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        
        # Fuentes de hardware
        'https://www.anandtech.com/rss/',
        'https://www.tomshardware.com/feeds/all',
        'https://www.pcworld.com/index.rss'
    ]
    
    RSS_FEEDS_COLOMBIA = [
        # Fuentes en español para Colombia
        'https://www.xataka.com/tag/tecnologia/rss2.xml',
        'https://www.genbeta.com/rss2.xml',
        'https://www.omicrono.com/feed/',
        'https://www.elandroidelibre.com/feed',
        'https://www.applesfera.com/rss2.xml',
        'https://feeds.feedburner.com/eset/blog',
        
        # Fuentes específicas de Colombia
        'https://www.enter.co/feed/',
        'https://www.portafolio.co/rss/tecnologia',
        'https://www.semana.com/rss/tecnologia',
        'https://www.eltiempo.com/rss/tecnologia.xml',
        'https://www.elespectador.com/rss/tecnologia',
        'https://www.pulzo.com/rss/tecnologia',
        'https://www.larepublica.co/rss/tecnologia',
        'https://www.dinero.com/rss/tecnologia',
        
        # Fuentes latinoamericanas
        'https://www.fayerwayer.com/feed/',
        'https://www.tekcrispy.com/feed/',
        'https://www.unocero.com/feed/',
        'https://www.xataka.com.mx/feed',
        'https://www.techbiz.com/feed/',
        
        # Fuentes de startups colombianas
        'https://www.wayra.com/blog/feed/',
        'https://www.rocket.co/blog/feed/',
        'https://www.innpulsacolombia.com/feed/',
        
        # Fuentes de ciberseguridad en español
        'https://www.segu-info.com.ar/feed/',
        'https://www.securitybydefault.com/feed/',
        'https://www.hackplayers.com/feed/'
    ]
    
    # Fuentes generales (para compatibilidad)
    RSS_FEEDS = RSS_FEEDS_US + RSS_FEEDS_COLOMBIA
    
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
