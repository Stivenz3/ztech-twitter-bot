"""
Módulo de fuentes de contenido para el bot ZTech
Integra RSS feeds, APIs de noticias y otras fuentes de contenido tecnológico
"""
import requests
import feedparser
import hashlib
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from loguru import logger
from config import Config

class ContentSource:
    """Clase base para fuentes de contenido"""
    
    def __init__(self, name: str):
        self.name = name
        self.last_fetch = None
    
    def fetch_content(self) -> List[Dict]:
        """
        Obtiene contenido de la fuente
        
        Returns:
            Lista de artículos/contenidos
        """
        raise NotImplementedError
    
    def generate_content_hash(self, content: str) -> str:
        """
        Genera hash único para el contenido
        
        Args:
            content: Contenido a hashear
            
        Returns:
            Hash MD5 del contenido
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def clean_text(self, text: str) -> str:
        """
        Limpia y normaliza texto
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not text:
            return ""
        
        # Remover HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remover caracteres especiales
        text = re.sub(r'[^\w\s.,!?@#]', '', text)
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

class RSSContentSource(ContentSource):
    """Fuente de contenido RSS"""
    
    def __init__(self, feed_url: str, name: str = None):
        super().__init__(name or f"RSS_{feed_url.split('/')[-1]}")
        self.feed_url = feed_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ZTech Bot 1.0 (Educational Content Aggregator)'
        })
    
    def fetch_content(self) -> List[Dict]:
        """
        Obtiene contenido del feed RSS
        
        Returns:
            Lista de artículos del RSS
        """
        try:
            logger.info(f"📡 Obteniendo contenido de RSS: {self.name}")
            
            response = self.session.get(self.feed_url, timeout=30)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                logger.warning(f"⚠️ Feed RSS con problemas: {self.name}")
            
            articles = []
            for entry in feed.entries[:10]:  # Limitar a 10 artículos más recientes
                try:
                    article = {
                        'title': self.clean_text(entry.get('title', '')),
                        'summary': self.clean_text(entry.get('summary', '')),
                        'link': entry.get('link', ''),
                        'published': self._parse_date(entry.get('published')),
                        'source': self.name,
                        'source_url': self.feed_url,
                        'content_hash': self.generate_content_hash(
                            entry.get('title', '') + entry.get('summary', '')
                        )
                    }
                    
                    if article['title'] and article['link']:
                        articles.append(article)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error procesando artículo RSS: {e}")
                    continue
            
            self.last_fetch = datetime.now()
            logger.info(f"✅ Obtenidos {len(articles)} artículos de {self.name}")
            return articles
            
        except requests.RequestException as e:
            logger.error(f"❌ Error al obtener RSS {self.name}: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error inesperado en RSS {self.name}: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parsea fecha de string a datetime
        
        Args:
            date_str: String de fecha
            
        Returns:
            Objeto datetime o None si no se puede parsear
        """
        if not date_str:
            return None
        
        try:
            # Intentar parsear con diferentes formatos
            formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%d %H:%M:%S'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Si no funciona, usar feedparser
            import feedparser
            parsed = feedparser._parse_date(date_str)
            if parsed:
                return datetime(*parsed[:6])
            
            return None
            
        except Exception:
            return None

class NewsAPIContentSource(ContentSource):
    """Fuente de contenido usando NewsAPI"""
    
    def __init__(self, api_key: str):
        super().__init__("NewsAPI")
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'User-Agent': 'ZTech Bot 1.0'
        })
    
    def fetch_content(self) -> List[Dict]:
        """
        Obtiene noticias de tecnología de NewsAPI
        
        Returns:
            Lista de artículos de noticias
        """
        if not self.api_key:
            logger.warning("⚠️ NewsAPI key no configurada")
            return []
        
        try:
            logger.info("📰 Obteniendo noticias de NewsAPI")
            
            # Parámetros de búsqueda
            params = {
                'q': 'technology OR programming OR AI OR artificial intelligence',
                'language': 'es,en',
                'sortBy': 'publishedAt',
                'pageSize': 20,
                'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            }
            
            response = self.session.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.error(f"❌ Error en NewsAPI: {data.get('message')}")
                return []
            
            articles = []
            for article in data.get('articles', []):
                try:
                    processed_article = {
                        'title': self.clean_text(article.get('title', '')),
                        'summary': self.clean_text(article.get('description', '')),
                        'link': article.get('url', ''),
                        'published': self._parse_newsapi_date(article.get('publishedAt')),
                        'source': f"NewsAPI_{article.get('source', {}).get('name', 'Unknown')}",
                        'source_url': article.get('url', ''),
                        'content_hash': self.generate_content_hash(
                            article.get('title', '') + article.get('description', '')
                        )
                    }
                    
                    if processed_article['title'] and processed_article['link']:
                        articles.append(processed_article)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error procesando artículo NewsAPI: {e}")
                    continue
            
            self.last_fetch = datetime.now()
            logger.info(f"✅ Obtenidos {len(articles)} artículos de NewsAPI")
            return articles
            
        except requests.RequestException as e:
            logger.error(f"❌ Error al obtener noticias de NewsAPI: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error inesperado en NewsAPI: {e}")
            return []
    
    def _parse_newsapi_date(self, date_str: str) -> Optional[datetime]:
        """
        Parsea fecha de NewsAPI
        
        Args:
            date_str: String de fecha de NewsAPI
            
        Returns:
            Objeto datetime o None
        """
        if not date_str:
            return None
        
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            return None

class RedditContentSource(ContentSource):
    """Fuente de contenido de Reddit"""
    
    def __init__(self, client_id: str, client_secret: str):
        super().__init__("Reddit")
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = None
        self.session = requests.Session()
    
    def _get_access_token(self) -> bool:
        """
        Obtiene token de acceso de Reddit
        
        Returns:
            True si se obtuvo el token, False en caso contrario
        """
        try:
            auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
            data = {
                'grant_type': 'client_credentials'
            }
            headers = {
                'User-Agent': 'ZTech Bot 1.0'
            }
            
            response = requests.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data['access_token']
            self.token_expires = datetime.now() + timedelta(seconds=token_data['expires_in'])
            
            logger.info("✅ Token de Reddit obtenido")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al obtener token de Reddit: {e}")
            return False
    
    def fetch_content(self) -> List[Dict]:
        """
        Obtiene contenido de subreddits de tecnología
        
        Returns:
            Lista de posts de Reddit
        """
        if not self.client_id or not self.client_secret:
            logger.warning("⚠️ Credenciales de Reddit no configuradas")
            return []
        
        # Verificar/obtener token
        if not self.access_token or (self.token_expires and datetime.now() >= self.token_expires):
            if not self._get_access_token():
                return []
        
        try:
            logger.info("🔴 Obteniendo contenido de Reddit")
            
            headers = {
                'Authorization': f'bearer {self.access_token}',
                'User-Agent': 'ZTech Bot 1.0'
            }
            
            posts = []
            for subreddit in Config.REDDIT_SUBREDDITS[:5]:  # Limitar a 5 subreddits
                try:
                    url = f'https://oauth.reddit.com/r/{subreddit}/hot'
                    params = {'limit': 5}
                    
                    response = self.session.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=30
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    for post in data.get('data', {}).get('children', []):
                        post_data = post.get('data', {})
                        
                        # Filtrar posts relevantes
                        if self._is_relevant_post(post_data):
                            processed_post = {
                                'title': self.clean_text(post_data.get('title', '')),
                                'summary': self.clean_text(post_data.get('selftext', '')[:500]),
                                'link': f"https://reddit.com{post_data.get('permalink', '')}",
                                'published': datetime.fromtimestamp(post_data.get('created_utc', 0)),
                                'source': f"Reddit_r/{subreddit}",
                                'source_url': f"https://reddit.com/r/{subreddit}",
                                'content_hash': self.generate_content_hash(
                                    post_data.get('title', '') + post_data.get('selftext', '')
                                )
                            }
                            
                            if processed_post['title']:
                                posts.append(processed_post)
                                
                except Exception as e:
                    logger.warning(f"⚠️ Error obteniendo posts de r/{subreddit}: {e}")
                    continue
            
            self.last_fetch = datetime.now()
            logger.info(f"✅ Obtenidos {len(posts)} posts de Reddit")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en Reddit: {e}")
            return []
    
    def _is_relevant_post(self, post_data: Dict) -> bool:
        """
        Verifica si un post es relevante para tecnología
        
        Args:
            post_data: Datos del post de Reddit
            
        Returns:
            True si es relevante, False en caso contrario
        """
        title = post_data.get('title', '').lower()
        selftext = post_data.get('selftext', '').lower()
        
        # Palabras clave de tecnología
        tech_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'programming',
            'software', 'hardware', 'tech', 'technology', 'innovation',
            'startup', 'coding', 'developer', 'python', 'javascript',
            'blockchain', 'crypto', 'cybersecurity', 'data science'
        ]
        
        content = f"{title} {selftext}"
        return any(keyword in content for keyword in tech_keywords)

class ContentAggregator:
    """Agregador de contenido de múltiples fuentes"""
    
    def __init__(self):
        self.sources = []
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Inicializa todas las fuentes de contenido configuradas"""
        # Fuentes RSS
        for feed_url in Config.RSS_FEEDS:
            self.sources.append(RSSContentSource(feed_url))
        
        # NewsAPI si está configurado
        if Config.NEWS_API_KEY:
            self.sources.append(NewsAPIContentSource(Config.NEWS_API_KEY))
        
        # Reddit si está configurado
        if Config.REDDIT_CLIENT_ID and Config.REDDIT_CLIENT_SECRET:
            self.sources.append(RedditContentSource(
                Config.REDDIT_CLIENT_ID,
                Config.REDDIT_CLIENT_SECRET
            ))
        
        logger.info(f"📚 Inicializadas {len(self.sources)} fuentes de contenido")
    
    def fetch_all_content(self) -> List[Dict]:
        """
        Obtiene contenido de todas las fuentes
        
        Returns:
            Lista combinada de contenido de todas las fuentes
        """
        all_content = []
        
        for source in self.sources:
            try:
                content = source.fetch_content()
                all_content.extend(content)
            except Exception as e:
                logger.error(f"❌ Error en fuente {source.name}: {e}")
                continue
        
        # Ordenar por fecha de publicación (más recientes primero)
        all_content.sort(key=lambda x: x.get('published', datetime.min), reverse=True)
        
        logger.info(f"📊 Total de contenido obtenido: {len(all_content)} artículos")
        return all_content
    
    def get_fresh_content(self, hours: int = 24) -> List[Dict]:
        """
        Obtiene contenido fresco (de las últimas horas)
        
        Args:
            hours: Número de horas hacia atrás
            
        Returns:
            Lista de contenido fresco
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_content = self.fetch_all_content()
        
        fresh_content = [
            article for article in all_content
            if article.get('published') and article['published'] >= cutoff_time
        ]
        
        logger.info(f"🆕 Contenido fresco ({hours}h): {len(fresh_content)} artículos")
        return fresh_content
