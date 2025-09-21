"""
Procesador de contenido mejorado para el bot ZTech
Incluye títulos polémicos, imágenes automáticas y contenido más largo
"""
import re
import random
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from config import Config

class EnhancedContentProcessor:
    """Procesador de contenido mejorado con engagement optimizado"""
    
    def __init__(self, language: str = 'es'):
        self.language = language
        self.hashtags = Config.HASHTAGS
        self.max_length = Config.MAX_TWEET_LENGTH
        self.use_controversial = Config.USE_CONTROVERSIAL_TITLES
        self.use_images = Config.USE_IMAGES
        self.min_content_length = Config.MIN_CONTENT_LENGTH
        
        # Configurar hashtags por idioma
        if language == 'en':
            self.hashtags = [
                '#technology', '#innovation', '#AI', '#programming', '#tech',
                '#startup', '#cybersecurity', '#blockchain', '#hardware', '#mobile'
            ]
        else:
            self.hashtags = [
                '#tecnologia', '#innovacion', '#IA', '#programacion', '#tech',
                '#startup', '#ciberseguridad', '#blockchain', '#hardware', '#mobile'
            ]
    
    def process_article_to_tweet(self, article: Dict) -> Optional[str]:
        """
        Convierte un artículo en un tweet optimizado con más contenido
        
        Args:
            article: Diccionario con información del artículo
            
        Returns:
            Texto del tweet o None si no se puede procesar
        """
        try:
            title = article.get('title', '').strip()
            summary = article.get('summary', '').strip()
            link = article.get('link', '').strip()
            source = article.get('source', '')
            
            if not title or not link:
                logger.warning("⚠️ Artículo sin título o enlace, saltando...")
                return None
            
            # Generar título polémico si está habilitado
            if self.use_controversial:
                title = self._make_controversial_title(title)
            
            # Crear tweet con más contenido
            tweet = self._create_enhanced_tweet(title, summary, link, source)
            
            if tweet and len(tweet) <= self.max_length:
                return tweet
            else:
                # Si es muy largo, usar versión optimizada
                return self._create_optimized_tweet(title, summary, link, source)
                
        except Exception as e:
            logger.error(f"❌ Error procesando artículo: {e}")
            return None
    
    def _make_controversial_title(self, title: str) -> str:
        """
        Hace el título más polémico para generar engagement
        
        Args:
            title: Título original
            
        Returns:
            Título polémico
        """
        if not self.use_controversial:
            return title
        
        # Obtener palabras clave polémicas según el idioma
        controversial_words = Config.CONTROVERSIAL_KEYWORDS.get(self.language, [])
        
        if not controversial_words:
            return title
        
        # Seleccionar palabra polémica aleatoria
        controversial_word = random.choice(controversial_words)
        
        # Patrones para insertar la palabra polémica
        patterns = [
            f"{controversial_word.upper()}: {title}",
            f"{title} - {controversial_word.upper()}",
            f"🚨 {controversial_word.upper()}: {title}",
            f"⚡ {controversial_word.upper()}: {title}",
            f"🔥 {controversial_word.upper()}: {title}",
            f"💥 {controversial_word.upper()}: {title}"
        ]
        
        return random.choice(patterns)
    
    def _create_enhanced_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """
        Crea un tweet con más contenido y engagement
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            link: Enlace del artículo
            source: Fuente del artículo
            
        Returns:
            Tweet mejorado
        """
        # Emojis según el tipo de contenido
        emoji = self._get_content_emoji(title, summary)
        
        # Crear tweet base
        tweet = f"{emoji} {title}\n\n"
        
        # Agregar resumen expandido si hay espacio
        if summary and len(tweet) + len(summary) + 100 < self.max_length:
            expanded_summary = self._expand_summary(summary)
            tweet += f"{expanded_summary}\n\n"
        
        # Agregar call-to-action
        cta = self._get_call_to_action()
        if len(tweet) + len(cta) + 50 < self.max_length:
            tweet += f"{cta}\n\n"
        
        # Agregar enlace
        tweet += f"🔗 {link}\n\n"
        
        # Agregar hashtags optimizados
        hashtags = self._get_optimized_hashtags(title, summary)
        tweet += hashtags
        
        return tweet
    
    def _create_optimized_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """
        Crea un tweet optimizado cuando el contenido es muy largo
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            link: Enlace del artículo
            source: Fuente del artículo
            
        Returns:
            Tweet optimizado
        """
        emoji = self._get_content_emoji(title, summary)
        
        # Calcular espacio disponible
        base_length = len(link) + len(self._get_optimized_hashtags(title, summary)) + 50
        available_length = self.max_length - base_length
        
        # Truncar título si es necesario
        if len(title) > available_length:
            title = title[:available_length-3] + "..."
        
        tweet = f"{emoji} {title}\n\n"
        tweet += f"🔗 {link}\n\n"
        tweet += self._get_optimized_hashtags(title, summary)
        
        return tweet
    
    def _get_content_emoji(self, title: str, summary: str) -> str:
        """
        Obtiene emoji según el tipo de contenido
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            
        Returns:
            Emoji apropiado
        """
        content = f"{title} {summary}".lower()
        
        if any(word in content for word in ['ai', 'artificial intelligence', 'machine learning', 'ia', 'inteligencia artificial']):
            return "🤖"
        elif any(word in content for word in ['programming', 'code', 'developer', 'programación', 'código', 'desarrollador']):
            return "💻"
        elif any(word in content for word in ['startup', 'entrepreneur', 'business', 'emprendimiento', 'negocio']):
            return "🚀"
        elif any(word in content for word in ['security', 'hack', 'cyber', 'seguridad', 'hackeo', 'ciber']):
            return "🔒"
        elif any(word in content for word in ['blockchain', 'crypto', 'bitcoin', 'ethereum']):
            return "⛓️"
        elif any(word in content for word in ['hardware', 'cpu', 'gpu', 'hardware', 'procesador']):
            return "🔧"
        elif any(word in content for word in ['mobile', 'smartphone', 'android', 'ios', 'móvil', 'celular']):
            return "📱"
        else:
            return "📰"
    
    def _expand_summary(self, summary: str) -> str:
        """
        Expande el resumen para hacerlo más atractivo
        
        Args:
            summary: Resumen original
            
        Returns:
            Resumen expandido
        """
        if not summary:
            return ""
        
        # Limpiar y expandir el resumen
        expanded = summary.strip()
        
        # Agregar conectores para hacerlo más fluido
        connectors = {
            'en': ['This technology', 'The innovation', 'This breakthrough', 'The development'],
            'es': ['Esta tecnología', 'La innovación', 'Este avance', 'El desarrollo']
        }
        
        if len(expanded) < self.min_content_length:
            connector = random.choice(connectors.get(self.language, connectors['es']))
            expanded = f"{connector} {expanded.lower()}"
        
        return expanded
    
    def _get_call_to_action(self) -> str:
        """
        Obtiene un call-to-action según el idioma
        
        Returns:
            Call-to-action
        """
        ctas = {
            'en': [
                "What do you think about this?",
                "How will this impact the industry?",
                "Share your thoughts below!",
                "This is game-changing!",
                "Your opinion matters!"
            ],
            'es': [
                "¿Qué opinas sobre esto?",
                "¿Cómo impactará esto a la industria?",
                "¡Comparte tu opinión!",
                "¡Esto cambia todo!",
                "Tu opinión importa!"
            ]
        }
        
        return random.choice(ctas.get(self.language, ctas['es']))
    
    def _get_optimized_hashtags(self, title: str, summary: str) -> str:
        """
        Obtiene hashtags optimizados según el contenido
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            
        Returns:
            String con hashtags optimizados
        """
        content = f"{title} {summary}".lower()
        
        # Hashtags base
        base_hashtags = self.hashtags[:3]  # Tomar los primeros 3
        
        # Hashtags específicos según contenido
        specific_hashtags = []
        
        if any(word in content for word in ['ai', 'artificial intelligence', 'ia', 'inteligencia artificial']):
            specific_hashtags.extend(['#AI', '#MachineLearning'] if self.language == 'en' else ['#IA', '#MachineLearning'])
        
        if any(word in content for word in ['programming', 'code', 'programación', 'código']):
            specific_hashtags.extend(['#Programming', '#Code'] if self.language == 'en' else ['#Programacion', '#Codigo'])
        
        if any(word in content for word in ['startup', 'emprendimiento']):
            specific_hashtags.extend(['#Startup', '#Entrepreneur'] if self.language == 'en' else ['#Startup', '#Emprendimiento'])
        
        # Combinar hashtags
        all_hashtags = base_hashtags + specific_hashtags[:2]  # Máximo 5 hashtags
        
        return ' '.join(all_hashtags)
    
    def get_image_url(self, title: str, summary: str) -> Optional[str]:
        """
        Obtiene URL de imagen según el tipo de contenido
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            
        Returns:
            URL de imagen o None
        """
        if not self.use_images:
            return None
        
        content = f"{title} {summary}".lower()
        
        # Determinar categoría del contenido
        if any(word in content for word in ['ai', 'artificial intelligence', 'ia', 'inteligencia artificial']):
            return Config.IMAGE_URLS.get('ai')
        elif any(word in content for word in ['programming', 'code', 'programación', 'código']):
            return Config.IMAGE_URLS.get('programming')
        elif any(word in content for word in ['startup', 'emprendimiento']):
            return Config.IMAGE_URLS.get('startup')
        elif any(word in content for word in ['security', 'hack', 'cyber', 'seguridad', 'hackeo']):
            return Config.IMAGE_URLS.get('cybersecurity')
        elif any(word in content for word in ['blockchain', 'crypto', 'bitcoin']):
            return Config.IMAGE_URLS.get('blockchain')
        elif any(word in content for word in ['hardware', 'cpu', 'gpu', 'hardware']):
            return Config.IMAGE_URLS.get('hardware')
        elif any(word in content for word in ['mobile', 'smartphone', 'android', 'ios', 'móvil']):
            return Config.IMAGE_URLS.get('mobile')
        else:
            return Config.IMAGE_URLS.get('default')
    
    def validate_tweet(self, tweet: str) -> bool:
        """
        Valida que un tweet cumpla con los requisitos
        
        Args:
            tweet: Texto del tweet
            
        Returns:
            True si es válido, False en caso contrario
        """
        if not tweet or not tweet.strip():
            return False
        
        if len(tweet) > self.max_length:
            logger.warning(f"⚠️ Tweet muy largo: {len(tweet)} caracteres")
            return False
        
        # Verificar que tenga contenido mínimo
        if len(tweet.strip()) < 100:
            logger.warning("⚠️ Tweet muy corto")
            return False
        
        return True
