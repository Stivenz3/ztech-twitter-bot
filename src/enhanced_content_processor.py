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
        Crea un tweet con más contenido y engagement para generar más clicks
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            link: Enlace del artículo
            source: Fuente del artículo
            
        Returns:
            Tweet mejorado con más contenido
        """
        # Emojis según el tipo de contenido
        emoji = self._get_content_emoji(title, summary)
        
        # Crear tweet base con título polémico
        tweet = f"{emoji} {title}\n\n"
        
        # Agregar resumen expandido con más detalles
        if summary:
            expanded_summary = self._expand_summary(summary)
            tweet += f"{expanded_summary}\n\n"
        
        # Agregar información adicional para generar interés
        additional_info = self._get_additional_info(title, summary)
        if additional_info and len(tweet) + len(additional_info) + 100 < self.max_length:
            tweet += f"{additional_info}\n\n"
        
        # Agregar call-to-action más atractivo
        cta = self._get_enhanced_call_to_action()
        if len(tweet) + len(cta) + 50 < self.max_length:
            tweet += f"{cta}\n\n"
        
        # Agregar enlace con descripción
        link_description = self._get_link_description()
        tweet += f"🔗 {link_description}\n{link}\n\n"
        
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
        Expande el resumen para hacerlo más atractivo y generar más clicks
        
        Args:
            summary: Resumen original
            
        Returns:
            Resumen expandido con más detalles
        """
        if not summary:
            return ""
        
        # Limpiar y expandir el resumen
        expanded = summary.strip()
        
        # Agregar conectores y detalles adicionales
        connectors = {
            'en': [
                'This revolutionary technology', 'The groundbreaking innovation', 
                'This game-changing breakthrough', 'The unprecedented development',
                'This cutting-edge advancement', 'The industry-disrupting technology'
            ],
            'es': [
                'Esta tecnología revolucionaria', 'La innovación revolucionaria', 
                'Este avance que cambia el juego', 'El desarrollo sin precedentes',
                'Esta tecnología de vanguardia', 'La tecnología que está revolucionando'
            ]
        }
        
        # Agregar detalles adicionales para generar más interés
        additional_details = {
            'en': [
                'Experts predict this will transform the industry completely.',
                'This could be the biggest breakthrough of the year.',
                'Industry leaders are calling this a game-changer.',
                'This technology is already being adopted by major companies.',
                'The implications of this development are enormous.',
                'This could revolutionize how we work and live.'
            ],
            'es': [
                'Los expertos predicen que esto transformará la industria completamente.',
                'Este podría ser el avance más grande del año.',
                'Los líderes de la industria lo llaman un cambio de juego.',
                'Esta tecnología ya está siendo adoptada por grandes empresas.',
                'Las implicaciones de este desarrollo son enormes.',
                'Esto podría revolucionar cómo trabajamos y vivimos.'
            ]
        }
        
        # Construir resumen expandido
        if len(expanded) < self.min_content_length:
            connector = random.choice(connectors.get(self.language, connectors['es']))
            expanded = f"{connector} {expanded.lower()}"
        
        # Agregar detalles adicionales si hay espacio
        if len(expanded) < 200:
            detail = random.choice(additional_details.get(self.language, additional_details['es']))
            expanded += f" {detail}"
        
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
    
    def _get_enhanced_call_to_action(self) -> str:
        """
        Obtiene un call-to-action más atractivo para generar clicks
        
        Returns:
            Call-to-action mejorado
        """
        ctas = {
            'en': [
                "🚀 This is HUGE! What's your take?",
                "💡 Game-changer alert! Thoughts?",
                "🔥 This will blow your mind! Agree?",
                "⚡ Revolutionary stuff! Your opinion?",
                "🎯 This changes everything! What do you think?",
                "💥 Mind-blowing! Share your thoughts!",
                "🌟 Incredible breakthrough! Your take?",
                "🚨 This is massive! What's your view?"
            ],
            'es': [
                "🚀 ¡Esto es ENORME! ¿Qué opinas?",
                "💡 ¡Alerta de cambio de juego! ¿Pensamientos?",
                "🔥 ¡Esto te va a volar la mente! ¿Estás de acuerdo?",
                "⚡ ¡Cosas revolucionarias! ¿Tu opinión?",
                "🎯 ¡Esto cambia todo! ¿Qué piensas?",
                "💥 ¡Alucinante! ¡Comparte tus pensamientos!",
                "🌟 ¡Avance increíble! ¿Tu punto de vista?",
                "🚨 ¡Esto es masivo! ¿Cuál es tu visión?"
            ]
        }
        
        return random.choice(ctas.get(self.language, ctas['es']))
    
    def _get_additional_info(self, title: str, summary: str) -> str:
        """
        Obtiene información adicional para hacer el tweet más atractivo
        
        Args:
            title: Título del artículo
            summary: Resumen del artículo
            
        Returns:
            Información adicional
        """
        content = f"{title} {summary}".lower()
        
        additional_info = {
            'en': [
                "The implications are enormous and could reshape entire industries.",
                "This breakthrough has been years in the making and is finally here.",
                "Industry experts are calling this the most significant development yet.",
                "The technology behind this is truly revolutionary and game-changing.",
                "This could be the breakthrough we've all been waiting for.",
                "The potential applications are endless and incredibly exciting.",
                "This development marks a new era in technology and innovation."
            ],
            'es': [
                "Las implicaciones son enormes y podrían reestructurar industrias enteras.",
                "Este avance lleva años en desarrollo y finalmente está aquí.",
                "Los expertos de la industria lo llaman el desarrollo más significativo hasta ahora.",
                "La tecnología detrás de esto es verdaderamente revolucionaria y cambia el juego.",
                "Este podría ser el avance que todos hemos estado esperando.",
                "Las aplicaciones potenciales son infinitas e increíblemente emocionantes.",
                "Este desarrollo marca una nueva era en tecnología e innovación."
            ]
        }
        
        return random.choice(additional_info.get(self.language, additional_info['es']))
    
    def _get_link_description(self) -> str:
        """
        Obtiene una descripción atractiva para el enlace
        
        Returns:
            Descripción del enlace
        """
        descriptions = {
            'en': [
                "Read the full story here:",
                "Get all the details:",
                "Full article here:",
                "Complete coverage:",
                "Deep dive into this:",
                "Full report:",
                "Complete analysis:"
            ],
            'es': [
                "Lee la historia completa aquí:",
                "Obtén todos los detalles:",
                "Artículo completo aquí:",
                "Cobertura completa:",
                "Análisis profundo aquí:",
                "Reporte completo:",
                "Análisis completo:"
            ]
        }
        
        return random.choice(descriptions.get(self.language, descriptions['es']))
    
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
