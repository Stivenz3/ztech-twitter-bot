"""
Cliente de Twitter API v2 para el bot ZTech
Maneja la autenticación y publicación de tweets
"""
import tweepy
from typing import Dict, Optional, List
from loguru import logger
from config import Config

class TwitterClient:
    """Cliente para interactuar con Twitter API v2"""
    
    def __init__(self):
        """Inicializa el cliente de Twitter"""
        self.client = None
        self.api = None
        self.authenticate()
    
    def authenticate(self):
        """
        Autentica con Twitter API usando las credenciales configuradas
        """
        try:
            # Validar configuración
            if not Config.validate_config():
                raise ValueError("Configuración de Twitter API incompleta")
            
            # Crear cliente de Twitter API v2
            self.client = tweepy.Client(
                bearer_token=Config.TWITTER_BEARER_TOKEN,
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            # Crear cliente de API v1.1 para funcionalidades adicionales
            auth = tweepy.OAuth1UserHandler(
                Config.TWITTER_API_KEY,
                Config.TWITTER_API_SECRET,
                Config.TWITTER_ACCESS_TOKEN,
                Config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Verificar autenticación
            user = self.client.get_me()
            if user.data:
                logger.info(f"✅ Autenticado como @{user.data.username}")
            else:
                raise Exception("No se pudo verificar la autenticación")
                
        except Exception as e:
            logger.error(f"❌ Error en autenticación de Twitter: {e}")
            raise
    
    def post_tweet(self, content: str, reply_to: Optional[str] = None) -> Optional[Dict]:
        """
        Publica un tweet
        
        Args:
            content: Contenido del tweet
            reply_to: ID del tweet al que responder (opcional)
            
        Returns:
            Diccionario con información del tweet publicado o None si falla
        """
        try:
            # Validar longitud del tweet
            if len(content) > Config.MAX_TWEET_LENGTH:
                logger.warning(f"⚠️ Tweet muy largo ({len(content)} chars), truncando...")
                content = content[:Config.MAX_TWEET_LENGTH-3] + "..."
            
            # Publicar tweet
            response = self.client.create_tweet(
                text=content,
                in_reply_to_tweet_id=reply_to
            )
            
            if response.data:
                tweet_info = {
                    'id': response.data['id'],
                    'text': content,
                    'created_at': response.data.get('created_at'),
                    'public_metrics': response.data.get('public_metrics', {})
                }
                
                logger.info(f"✅ Tweet publicado: {tweet_info['id']}")
                logger.debug(f"Contenido: {content[:100]}...")
                
                return tweet_info
            else:
                logger.error("❌ No se recibió respuesta del tweet")
                return None
                
        except tweepy.TooManyRequests:
            logger.warning("⚠️ Límite de rate limit alcanzado, esperando...")
            return None
        except tweepy.Unauthorized:
            logger.error("❌ Error de autorización - verifica las credenciales")
            return None
        except tweepy.Forbidden:
            logger.error("❌ Tweet prohibido - posible contenido duplicado o spam")
            return None
        except Exception as e:
            logger.error(f"❌ Error al publicar tweet: {e}")
            return None
    
    def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict]:
        """
        Obtiene métricas de un tweet
        
        Args:
            tweet_id: ID del tweet
            
        Returns:
            Diccionario con métricas del tweet
        """
        try:
            tweet = self.client.get_tweet(
                tweet_id,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if tweet.data:
                return {
                    'id': tweet.data.id,
                    'metrics': tweet.data.public_metrics,
                    'created_at': tweet.data.created_at
                }
            return None
            
        except Exception as e:
            logger.error(f"❌ Error al obtener métricas del tweet {tweet_id}: {e}")
            return None
    
    def search_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Busca tweets con una consulta específica
        
        Args:
            query: Consulta de búsqueda
            max_results: Número máximo de resultados
            
        Returns:
            Lista de tweets encontrados
        """
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )
            
            if tweets.data:
                return [
                    {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author_id': tweet.author_id,
                        'metrics': tweet.public_metrics
                    }
                    for tweet in tweets.data
                ]
            return []
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda de tweets: {e}")
            return []
    
    def get_user_timeline(self, username: str, max_tweets: int = 20) -> List[Dict]:
        """
        Obtiene timeline de un usuario
        
        Args:
            username: Nombre de usuario (sin @)
            max_tweets: Número máximo de tweets
            
        Returns:
            Lista de tweets del usuario
        """
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                logger.error(f"❌ Usuario @{username} no encontrado")
                return []
            
            tweets = self.client.get_users_tweets(
                id=user.data.id,
                max_results=min(max_tweets, 100),
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if tweets.data:
                return [
                    {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'metrics': tweet.public_metrics
                    }
                    for tweet in tweets.data
                ]
            return []
            
        except Exception as e:
            logger.error(f"❌ Error al obtener timeline de @{username}: {e}")
            return []
    
    def get_rate_limit_status(self) -> Dict:
        """
        Obtiene el estado de los límites de rate limit
        
        Returns:
            Diccionario con información de rate limits
        """
        try:
            # Obtener límites de la API v1.1
            limits = self.api.get_rate_limit_status()
            
            # Extraer información relevante
            relevant_limits = {}
            for endpoint, info in limits.items():
                if 'tweets' in endpoint.lower() or 'search' in endpoint.lower():
                    relevant_limits[endpoint] = {
                        'limit': info.limit,
                        'remaining': info.remaining,
                        'reset': info.reset
                    }
            
            return relevant_limits
            
        except Exception as e:
            logger.error(f"❌ Error al obtener estado de rate limits: {e}")
            return {}
    
    def validate_credentials(self) -> bool:
        """
        Valida que las credenciales funcionen correctamente
        
        Returns:
            True si las credenciales son válidas, False en caso contrario
        """
        try:
            user = self.client.get_me()
            return user.data is not None
        except Exception as e:
            logger.error(f"❌ Error al validar credenciales: {e}")
            return False
