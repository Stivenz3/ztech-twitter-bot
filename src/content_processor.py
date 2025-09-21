"""
Procesador de contenido para el bot ZTech
Convierte artículos en tweets optimizados para Twitter
"""
import re
import random
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from config import Config

class ContentProcessor:
    """Procesador de contenido para generar tweets"""
    
    def __init__(self):
        self.hashtags = Config.HASHTAGS
        self.max_length = Config.MAX_TWEET_LENGTH
    
    def process_article_to_tweet(self, article: Dict) -> Optional[str]:
        """
        Convierte un artículo en un tweet optimizado
        
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
            
            # Generar diferentes tipos de tweets
            tweet_types = [
                self._create_news_tweet,
                self._create_insight_tweet,
                self._create_question_tweet,
                self._create_highlight_tweet
            ]
            
            # Seleccionar tipo aleatorio
            tweet_type = random.choice(tweet_types)
            tweet = tweet_type(title, summary, link, source)
            
            if tweet and len(tweet) <= self.max_length:
                return tweet
            else:
                # Si es muy largo, usar versión simplificada
                return self._create_simple_tweet(title, link, source)
                
        except Exception as e:
            logger.error(f"❌ Error procesando artículo: {e}")
            return None
    
    def _create_news_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """Crea un tweet tipo noticia"""
        # Limpiar y acortar título
        clean_title = self._clean_title(title)
        
        # Crear tweet
        tweet = f"📰 {clean_title}"
        
        # Agregar resumen si cabe
        if summary and len(tweet) + len(summary) + 50 < self.max_length:
            clean_summary = self._clean_summary(summary)
            tweet += f"\n\n{clean_summary}"
        
        # Agregar enlace y hashtags
        tweet += f"\n\n{link}"
        tweet += f"\n\n{self._get_random_hashtags()}"
        
        return tweet
    
    def _create_insight_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """Crea un tweet con insight o análisis"""
        clean_title = self._clean_title(title)
        
        insights = [
            "💡 Interesante perspectiva:",
            "🔍 Análisis destacado:",
            "⚡ Insight tecnológico:",
            "🚀 Innovación notable:",
            "🎯 Punto clave:"
        ]
        
        insight = random.choice(insights)
        tweet = f"{insight}\n\n{clean_title}"
        
        if summary and len(tweet) + len(summary) + 50 < self.max_length:
            clean_summary = self._clean_summary(summary)
            tweet += f"\n\n{clean_summary}"
        
        tweet += f"\n\n{link}"
        tweet += f"\n\n{self._get_random_hashtags()}"
        
        return tweet
    
    def _create_question_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """Crea un tweet con pregunta para engagement"""
        clean_title = self._clean_title(title)
        
        questions = [
            "¿Qué opinas sobre esto?",
            "¿Cómo crees que impactará esto?",
            "¿Has probado algo similar?",
            "¿Cuál es tu experiencia con esto?",
            "¿Qué te parece esta tendencia?"
        ]
        
        question = random.choice(questions)
        tweet = f"🤔 {clean_title}\n\n{question}"
        
        if summary and len(tweet) + len(summary) + 50 < self.max_length:
            clean_summary = self._clean_summary(summary)
            tweet += f"\n\n{clean_summary}"
        
        tweet += f"\n\n{link}"
        tweet += f"\n\n{self._get_random_hashtags()}"
        
        return tweet
    
    def _create_highlight_tweet(self, title: str, summary: str, link: str, source: str) -> str:
        """Crea un tweet destacando puntos clave"""
        clean_title = self._clean_title(title)
        
        highlights = [
            "⭐ Destacado:",
            "🔥 Trending:",
            "📈 Importante:",
            "🎯 Clave:",
            "💎 Joya tecnológica:"
        ]
        
        highlight = random.choice(highlights)
        tweet = f"{highlight}\n\n{clean_title}"
        
        if summary and len(tweet) + len(summary) + 50 < self.max_length:
            clean_summary = self._clean_summary(summary)
            tweet += f"\n\n{clean_summary}"
        
        tweet += f"\n\n{link}"
        tweet += f"\n\n{self._get_random_hashtags()}"
        
        return tweet
    
    def _create_simple_tweet(self, title: str, link: str, source: str) -> str:
        """Crea un tweet simple cuando el contenido es muy largo"""
        clean_title = self._clean_title(title)
        
        # Calcular espacio disponible
        base_length = len(link) + len(self._get_random_hashtags()) + 10
        available_length = self.max_length - base_length
        
        if len(clean_title) > available_length:
            clean_title = clean_title[:available_length-3] + "..."
        
        tweet = f"📰 {clean_title}\n\n{link}\n\n{self._get_random_hashtags()}"
        
        return tweet
    
    def _clean_title(self, title: str) -> str:
        """Limpia y optimiza el título"""
        if not title:
            return ""
        
        # Remover caracteres especiales problemáticos
        title = re.sub(r'[^\w\s.,!?@#:()-]', '', title)
        
        # Remover palabras comunes al inicio
        title = re.sub(r'^(Breaking|News|Update|Latest|New):\s*', '', title, flags=re.IGNORECASE)
        
        # Capitalizar primera letra
        title = title.strip()
        if title:
            title = title[0].upper() + title[1:]
        
        return title
    
    def _clean_summary(self, summary: str) -> str:
        """Limpia y acorta el resumen"""
        if not summary:
            return ""
        
        # Limpiar HTML y caracteres especiales
        summary = re.sub(r'<[^>]+>', '', summary)
        summary = re.sub(r'[^\w\s.,!?@#:()-]', '', summary)
        
        # Limitar longitud
        max_summary_length = 200
        if len(summary) > max_summary_length:
            summary = summary[:max_summary_length-3] + "..."
        
        return summary.strip()
    
    def _get_random_hashtags(self) -> str:
        """Obtiene hashtags aleatorios"""
        # Hashtags base siempre incluidos
        base_hashtags = ['#tecnologia', '#innovacion']
        
        # Hashtags adicionales aleatorios
        additional_hashtags = [
            '#AI', '#programacion', '#desarrollo', '#startup', '#cybersecurity',
            '#datascience', '#machinelearning', '#blockchain', '#cloud', '#devops',
            '#webdev', '#mobile', '#gaming', '#fintech', '#edtech', '#healthtech'
        ]
        
        # Seleccionar 2-3 hashtags adicionales
        selected_additional = random.sample(additional_hashtags, min(3, len(additional_hashtags)))
        
        all_hashtags = base_hashtags + selected_additional
        return ' '.join(all_hashtags)
    
    def create_thread_tweet(self, articles: List[Dict], max_tweets: int = 3) -> List[str]:
        """
        Crea un hilo de tweets con múltiples artículos
        
        Args:
            articles: Lista de artículos
            max_tweets: Número máximo de tweets en el hilo
            
        Returns:
            Lista de tweets para el hilo
        """
        if not articles:
            return []
        
        tweets = []
        
        # Primer tweet (introducción)
        intro_tweet = f"🧵 Hilo de noticias tecnológicas de hoy:\n\n"
        
        # Agregar artículos hasta llenar el primer tweet
        current_tweet = intro_tweet
        article_count = 0
        
        for article in articles[:max_tweets]:
            title = self._clean_title(article.get('title', ''))
            link = article.get('link', '')
            
            if not title or not link:
                continue
            
            # Formato: "1. Título - Enlace"
            article_text = f"{article_count + 1}. {title}\n{link}\n\n"
            
            if len(current_tweet) + len(article_text) + len(self._get_random_hashtags()) < self.max_length:
                current_tweet += article_text
                article_count += 1
            else:
                break
        
        if article_count > 0:
            current_tweet += self._get_random_hashtags()
            tweets.append(current_tweet)
        
        return tweets
    
    def create_curated_tweet(self, articles: List[Dict]) -> Optional[str]:
        """
        Crea un tweet curado con múltiples artículos
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Tweet curado o None
        """
        if not articles:
            return None
        
        # Seleccionar los 3 artículos más relevantes
        selected_articles = articles[:3]
        
        tweet = "📚 Resumen tecnológico del día:\n\n"
        
        for i, article in enumerate(selected_articles, 1):
            title = self._clean_title(article.get('title', ''))
            link = article.get('link', '')
            
            if title and link:
                tweet += f"{i}. {title}\n{link}\n\n"
        
        tweet += self._get_random_hashtags()
        
        if len(tweet) <= self.max_length:
            return tweet
        else:
            # Si es muy largo, usar solo el primer artículo
            return self.process_article_to_tweet(selected_articles[0])
    
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
        if len(tweet.strip()) < 50:
            logger.warning("⚠️ Tweet muy corto")
            return False
        
        return True
