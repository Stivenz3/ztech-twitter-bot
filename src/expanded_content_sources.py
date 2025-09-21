"""
Agregador de fuentes expandido para el bot ZTech
Incluye YouTube, TikTok, Instagram, LinkedIn, Medium, Dev.to
"""
import requests
import json
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from config import Config

class ExpandedContentSources:
    """Agregador de fuentes expandido para contenido diverso"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_youtube_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de YouTube (simulado - requiere API key)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de YouTube
        """
        try:
            # Simulación de contenido de YouTube
            # En producción, usarías la YouTube Data API
            youtube_content = [
                {
                    'title': '🚀 10 Tech Hacks That Will Blow Your Mind!',
                    'summary': 'Amazing technology hacks that will make your life easier and more productive.',
                    'link': 'https://youtube.com/watch?v=example1',
                    'source': 'YouTube',
                    'content_type': 'hacks',
                    'published_date': datetime.now() - timedelta(hours=2),
                    'content_hash': f"youtube_{hash('hacks_video_1')}"
                },
                {
                    'title': '💻 Top 5 Programming Languages to Learn in 2024',
                    'summary': 'The most in-demand programming languages that will boost your career.',
                    'link': 'https://youtube.com/watch?v=example2',
                    'source': 'YouTube',
                    'content_type': 'top_lists',
                    'published_date': datetime.now() - timedelta(hours=4),
                    'content_hash': f"youtube_{hash('top_lists_video_1')}"
                },
                {
                    'title': '🤖 AI Revolution: What You Need to Know',
                    'summary': 'Everything about artificial intelligence and how it will change the world.',
                    'link': 'https://youtube.com/watch?v=example3',
                    'source': 'YouTube',
                    'content_type': 'controversial',
                    'published_date': datetime.now() - timedelta(hours=6),
                    'content_hash': f"youtube_{hash('controversial_video_1')}"
                }
            ]
            
            return youtube_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de YouTube: {e}")
            return []
    
    def get_tiktok_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de TikTok (simulado - requiere API)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de TikTok
        """
        try:
            # Simulación de contenido de TikTok
            tiktok_content = [
                {
                    'title': '🔥 Tech Hack: Double Your Phone Battery Life!',
                    'summary': 'Simple trick to extend your phone battery life significantly.',
                    'link': 'https://tiktok.com/@techhacker/video/example1',
                    'source': 'TikTok',
                    'content_type': 'hacks',
                    'published_date': datetime.now() - timedelta(hours=1),
                    'content_hash': f"tiktok_{hash('hacks_tiktok_1')}"
                },
                {
                    'title': '💡 Programming Tip: Use This Shortcut!',
                    'summary': 'Keyboard shortcut that will make you code 10x faster.',
                    'link': 'https://tiktok.com/@coder/video/example2',
                    'source': 'TikTok',
                    'content_type': 'protips',
                    'published_date': datetime.now() - timedelta(hours=3),
                    'content_hash': f"tiktok_{hash('protips_tiktok_1')}"
                },
                {
                    'title': '🤯 Tech Fact: You Wont Believe This!',
                    'summary': 'Mind-blowing technology fact that will surprise you.',
                    'link': 'https://tiktok.com/@techfacts/video/example3',
                    'source': 'TikTok',
                    'content_type': 'curiosities',
                    'published_date': datetime.now() - timedelta(hours=5),
                    'content_hash': f"tiktok_{hash('curiosities_tiktok_1')}"
                }
            ]
            
            return tiktok_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de TikTok: {e}")
            return []
    
    def get_instagram_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de Instagram (simulado - requiere API)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de Instagram
        """
        try:
            # Simulación de contenido de Instagram
            instagram_content = [
                {
                    'title': '📱 Tech Review: New iPhone vs Samsung Galaxy',
                    'summary': 'Detailed comparison of the latest smartphones from Apple and Samsung.',
                    'link': 'https://instagram.com/p/example1',
                    'source': 'Instagram',
                    'content_type': 'reviews',
                    'published_date': datetime.now() - timedelta(hours=2),
                    'content_hash': f"instagram_{hash('reviews_insta_1')}"
                },
                {
                    'title': '🚀 Startup Story: From Zero to Million',
                    'summary': 'Inspiring story of a tech startup that made it big.',
                    'link': 'https://instagram.com/p/example2',
                    'source': 'Instagram',
                    'content_type': 'trends',
                    'published_date': datetime.now() - timedelta(hours=4),
                    'content_hash': f"instagram_{hash('trends_insta_1')}"
                }
            ]
            
            return instagram_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de Instagram: {e}")
            return []
    
    def get_linkedin_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de LinkedIn (simulado - requiere API)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de LinkedIn
        """
        try:
            # Simulación de contenido de LinkedIn
            linkedin_content = [
                {
                    'title': '💼 Professional Tip: How to Land Your Dream Tech Job',
                    'summary': 'Expert advice on getting hired in the technology industry.',
                    'link': 'https://linkedin.com/posts/example1',
                    'source': 'LinkedIn',
                    'content_type': 'protips',
                    'published_date': datetime.now() - timedelta(hours=3),
                    'content_hash': f"linkedin_{hash('protips_linkedin_1')}"
                },
                {
                    'title': '🏢 Industry Analysis: Tech Market Trends 2024',
                    'summary': 'Comprehensive analysis of technology market trends and predictions.',
                    'link': 'https://linkedin.com/posts/example2',
                    'source': 'LinkedIn',
                    'content_type': 'trends',
                    'published_date': datetime.now() - timedelta(hours=6),
                    'content_hash': f"linkedin_{hash('trends_linkedin_1')}"
                }
            ]
            
            return linkedin_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de LinkedIn: {e}")
            return []
    
    def get_medium_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de Medium (simulado - requiere API)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de Medium
        """
        try:
            # Simulación de contenido de Medium
            medium_content = [
                {
                    'title': '📚 The Complete Guide to Machine Learning',
                    'summary': 'Comprehensive guide to understanding and implementing machine learning.',
                    'link': 'https://medium.com/@author/example1',
                    'source': 'Medium',
                    'content_type': 'protips',
                    'published_date': datetime.now() - timedelta(hours=4),
                    'content_hash': f"medium_{hash('protips_medium_1')}"
                },
                {
                    'title': '🔒 Cybersecurity: Protecting Your Digital Life',
                    'summary': 'Essential cybersecurity practices for individuals and businesses.',
                    'link': 'https://medium.com/@author/example2',
                    'source': 'Medium',
                    'content_type': 'hacks',
                    'published_date': datetime.now() - timedelta(hours=8),
                    'content_hash': f"medium_{hash('hacks_medium_1')}"
                }
            ]
            
            return medium_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de Medium: {e}")
            return []
    
    def get_devto_content(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido de Dev.to (simulado - requiere API)
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido de Dev.to
        """
        try:
            # Simulación de contenido de Dev.to
            devto_content = [
                {
                    'title': '💻 10 JavaScript Tricks Every Developer Should Know',
                    'summary': 'Advanced JavaScript techniques that will make you a better developer.',
                    'link': 'https://dev.to/author/example1',
                    'source': 'Dev.to',
                    'content_type': 'hacks',
                    'published_date': datetime.now() - timedelta(hours=2),
                    'content_hash': f"devto_{hash('hacks_devto_1')}"
                },
                {
                    'title': '🚀 Building Scalable Web Applications',
                    'summary': 'Best practices for creating web applications that can handle millions of users.',
                    'link': 'https://dev.to/author/example2',
                    'source': 'Dev.to',
                    'content_type': 'protips',
                    'published_date': datetime.now() - timedelta(hours=5),
                    'content_hash': f"devto_{hash('protips_devto_1')}"
                }
            ]
            
            return devto_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido de Dev.to: {e}")
            return []
    
    def get_all_expanded_content(self, max_results_per_source: int = 3) -> List[Dict]:
        """
        Obtiene contenido de todas las fuentes expandidas
        
        Args:
            max_results_per_source: Número máximo de resultados por fuente
            
        Returns:
            Lista combinada de contenido de todas las fuentes
        """
        try:
            all_content = []
            
            # Obtener contenido de cada fuente
            if 'youtube' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_youtube_content(max_results_per_source))
            
            if 'tiktok' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_tiktok_content(max_results_per_source))
            
            if 'instagram' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_instagram_content(max_results_per_source))
            
            if 'linkedin' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_linkedin_content(max_results_per_source))
            
            if 'medium' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_medium_content(max_results_per_source))
            
            if 'devto' in Config.CONTENT_SOURCES:
                all_content.extend(self.get_devto_content(max_results_per_source))
            
            # Mezclar y retornar
            random.shuffle(all_content)
            return all_content
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido expandido: {e}")
            return []
    
    def get_content_by_type(self, content_type: str, max_results: int = 5) -> List[Dict]:
        """
        Obtiene contenido filtrado por tipo
        
        Args:
            content_type: Tipo de contenido a buscar
            max_results: Número máximo de resultados
            
        Returns:
            Lista de contenido filtrado por tipo
        """
        try:
            all_content = self.get_all_expanded_content(max_results * 2)
            filtered_content = [item for item in all_content if item.get('content_type') == content_type]
            
            return filtered_content[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo contenido por tipo: {e}")
            return []
