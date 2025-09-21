
"""
Generador de contenido con IA para el bot ZTech
Usa modelos de lenguaje para crear contenido original y creativo
"""
import os
import json
import random
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from config import Config

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("⚠️ OpenAI no disponible. Instala: pip install openai")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("⚠️ Anthropic no disponible. Instala: pip install anthropic")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("⚠️ Requests no disponible. Instala: pip install requests")

class AIContentGenerator:
    """Generador de contenido usando modelos de IA"""
    
    def __init__(self, language: str = 'es'):
        self.language = language
        self.max_length = Config.MAX_TWEET_LENGTH
        
        # Configurar APIs de IA
        self._setup_ai_apis()
        
        # Prompts optimizados para diferentes tipos de contenido
        self._init_prompts()
    
    def _setup_ai_apis(self):
        """Configura las APIs de IA disponibles"""
        self.openai_client = None
        self.anthropic_client = None
        self.qwen_available = False
        
        # Qwen API (prioridad)
        if REQUESTS_AVAILABLE and os.getenv('QWEN_API_KEY'):
            self.qwen_api_key = os.getenv('QWEN_API_KEY')
            self.qwen_available = True
            logger.info("✅ Qwen API configurada")
        
        # OpenAI
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai
            logger.info("✅ OpenAI configurado")
        
        # Anthropic (Claude)
        if ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = anthropic.Anthropic(
                api_key=os.getenv('ANTHROPIC_API_KEY')
            )
            logger.info("✅ Anthropic configurado")
        
        if not self.qwen_available and not self.openai_client and not self.anthropic_client:
            logger.warning("⚠️ No hay APIs de IA configuradas")
    
    def _init_prompts(self):
        """Inicializa los prompts optimizados para diferentes tipos de contenido"""
        
        self.prompts = {
            'hacks': {
                'en': """Create a viral tech hack tweet that will get massive engagement. The tweet should:
- Be 200-280 characters
- Include a practical tech tip or shortcut
- Use engaging emojis
- Have a hook that makes people want to try it
- Include relevant hashtags
- Be written in an exciting, shareable tone
- Include a brief explanation of WHY this hack is useful
- Make people want to save and share it

Examples of good hooks:
- "This will blow your mind!"
- "Game changer!"
- "You won't believe this!"
- "This changes everything!"

Generate 3 different versions.""",
                'es': """Crea un tweet viral de hack tecnológico que genere mucho engagement. El tweet debe:
- Tener 200-280 caracteres
- Incluir un tip o atajo tecnológico práctico
- Usar emojis atractivos
- Tener un gancho que haga que la gente quiera probarlo
- Incluir hashtags relevantes
- Estar escrito en un tono emocionante y compartible
- Incluir una breve explicación de POR QUÉ este hack es útil
- Hacer que la gente quiera guardarlo y compartirlo

Ejemplos de buenos ganchos:
- "¡Esto te va a volar la mente!"
- "¡Cambia el juego!"
- "¡No vas a creer esto!"
- "¡Esto cambia todo!"

Genera 3 versiones diferentes."""
            },
            
            'protips': {
                'en': """Create a professional tech tip tweet that developers and tech professionals will love. The tweet should:
- Be 200-280 characters
- Share valuable professional advice
- Be actionable and practical
- Use professional but engaging tone
- Include relevant hashtags
- Appeal to developers, engineers, or tech workers
- Include a brief explanation of WHY this tip matters
- Provide context about the impact or benefit

Focus on:
- Career advice
- Best practices
- Productivity tips
- Industry insights
- Professional development

Generate 3 different versions.""",
                'es': """Crea un tweet de consejo profesional tecnológico que los desarrolladores y profesionales tech van a amar. El tweet debe:
- Tener 200-280 caracteres
- Compartir consejo profesional valioso
- Ser accionable y práctico
- Usar un tono profesional pero atractivo
- Incluir hashtags relevantes
- Atraer a desarrolladores, ingenieros o trabajadores tech
- Incluir una breve explicación de POR QUÉ este consejo importa
- Proporcionar contexto sobre el impacto o beneficio

Enfócate en:
- Consejos de carrera
- Mejores prácticas
- Tips de productividad
- Insights de la industria
- Desarrollo profesional

Genera 3 versiones diferentes."""
            },
            
            'top_lists': {
                'en': """Create a compelling "Top X" list tweet about technology. The tweet should:
- Be 200-280 characters
- Present a numbered list (Top 3, Top 5, etc.)
- Be about current tech trends, tools, or topics
- Use engaging formatting with numbers and emojis
- Include relevant hashtags
- Make people want to save or share the list

Examples:
- Top 5 Programming Languages 2024
- Top 3 AI Tools Everyone Should Know
- Top 5 Cybersecurity Tips
- Top 3 Tech Trends to Watch

Generate 3 different versions.""",
                'es': """Crea un tweet convincente de lista "Top X" sobre tecnología. El tweet debe:
- Tener 200-280 caracteres
- Presentar una lista numerada (Top 3, Top 5, etc.)
- Ser sobre tendencias, herramientas o temas tech actuales
- Usar formato atractivo con números y emojis
- Incluir hashtags relevantes
- Hacer que la gente quiera guardar o compartir la lista

Ejemplos:
- Top 5 Lenguajes de Programación 2024
- Top 3 Herramientas de IA que Todos Deben Conocer
- Top 5 Tips de Ciberseguridad
- Top 3 Tendencias Tech a Observar

Genera 3 versiones diferentes."""
            },
            
            'curiosities': {
                'en': """Create a fascinating tech curiosity tweet with a detailed explanation. The tweet should have TWO parts:

PART 1 - The Hook (200-280 characters):
- Start with "CURIOSITY:" or "DID YOU KNOW:"
- Share an amazing tech fact or discovery
- Be surprising and educational
- Use engaging emojis
- Include relevant hashtags

PART 2 - The Explanation (500+ characters):
- Provide a detailed paragraph explaining the curiosity
- Include historical context, technical details, and implications
- Explain WHY this fact is important or interesting
- Add additional related information
- Make it educational and comprehensive

Example format:
"CURIOSITY: The first password was created in 1961 at MIT! 🔐

[Detailed 500+ character explanation about the history of passwords, how they evolved, their importance in cybersecurity, and their impact on modern technology]"

Create 1-2 versions of this detailed curiosity tweet.""",
                'es': """Crea un tweet de curiosidad tecnológica fascinante con una explicación detallada. El tweet debe tener DOS partes:

PARTE 1 - El Gancho (200-280 caracteres):
- Comienza con "CURIOSIDAD:" o "¿SABÍAS QUE:"
- Comparte un hecho o descubrimiento tecnológico asombroso
- Sé sorprendente y educativo
- Usa emojis atractivos
- Incluye hashtags relevantes

PARTE 2 - La Explicación (500+ caracteres):
- Proporciona un párrafo detallado explicando la curiosidad
- Incluye contexto histórico, detalles técnicos e implicaciones
- Explica POR QUÉ este hecho es importante o interesante
- Añade información adicional relacionada
- Hazlo educativo y comprensivo

Formato de ejemplo:
"CURIOSIDAD: ¡La primera contraseña fue creada en 1961 en MIT! 🔐

[Explicación detallada de 500+ caracteres sobre la historia de las contraseñas, cómo evolucionaron, su importancia en ciberseguridad y su impacto en la tecnología moderna]"

Crea 1-2 versiones de este tweet de curiosidad detallado."""
            },
            
            'controversial': {
                'en': """Create a controversial tech opinion tweet that will spark debate and discussion. The tweet should:
- Be 200-280 characters
- Present a bold, controversial tech opinion
- Be thought-provoking and debatable
- Use strong, confident language
- Include relevant hashtags
- Encourage people to share their opinions

Focus on:
- Industry controversies
- Bold predictions
- Unpopular opinions
- Challenging common beliefs
- Provocative statements

Generate 3 different versions.""",
                'es': """Crea un tweet de opinión tecnológica controversial que genere debate y discusión. El tweet debe:
- Tener 200-280 caracteres
- Presentar una opinión tech audaz y controversial
- Ser provocativo y debatible
- Usar lenguaje fuerte y confiado
- Incluir hashtags relevantes
- Animar a la gente a compartir sus opiniones

Enfócate en:
- Controversias de la industria
- Predicciones audaces
- Opiniones impopulares
- Desafiar creencias comunes
- Declaraciones provocativas

Genera 3 versiones diferentes."""
            },
            
            'history': {
                'en': """Create an engaging tech history tweet that educates and entertains. The tweet should:
- Be 200-280 characters
- Share an interesting tech historical fact
- Be educational but entertaining
- Use engaging emojis
- Include relevant hashtags
- Make people appreciate tech evolution

Focus on:
- Historical milestones
- Famous tech figures
- Evolution of technology
- Vintage tech facts
- Tech industry history

Generate 3 different versions.""",
                'es': """Crea un tweet de historia tecnológica atractivo que eduque y entretenga. El tweet debe:
- Tener 200-280 caracteres
- Compartir un hecho histórico tecnológico interesante
- Ser educativo pero entretenido
- Usar emojis atractivos
- Incluir hashtags relevantes
- Hacer que la gente aprecie la evolución tech

Enfócate en:
- Hitos históricos
- Figuras tech famosas
- Evolución de la tecnología
- Hechos de tech vintage
- Historia de la industria tech

Genera 3 versiones diferentes."""
            }
        }
    
    def generate_content(self, content_type: str, article_text: str = None) -> Optional[str]:
        """
        Genera contenido usando IA
        
        Args:
            content_type: Tipo de contenido a generar
            article_text: Texto del artículo (opcional, para resúmenes)
            
        Returns:
            Contenido generado o None si no se puede generar
        """
        try:
            if not self.qwen_available and not self.openai_client and not self.anthropic_client:
                logger.warning("⚠️ No hay APIs de IA disponibles")
                return None
            
            # Obtener prompt para el tipo de contenido
            prompt_template = self.prompts.get(content_type, {}).get(self.language)
            if not prompt_template:
                logger.warning(f"⚠️ No hay prompt para {content_type} en {self.language}")
                return None
            
            # Si hay texto de artículo, agregarlo al prompt
            if article_text:
                prompt_template += f"\n\nContexto del artículo:\n{article_text[:1000]}..."
            
            # Generar contenido usando IA (prioridad: OpenRouter > OpenAI > Anthropic)
            if self.qwen_available:
                return self._generate_with_openrouter(prompt_template, content_type)
            elif self.openai_client:
                return self._generate_with_openai(prompt_template, content_type)
            elif self.anthropic_client:
                return self._generate_with_anthropic(prompt_template, content_type)
            
        except Exception as e:
            logger.error(f"❌ Error generando contenido con IA: {e}")
            return None
    
    def _generate_with_openrouter(self, prompt: str, content_type: str) -> Optional[str]:
        """Genera contenido usando OpenRouter API con GPT-OSS-120B"""
        try:
            import requests
            
            # URL de la API de OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.qwen_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/Stivenz3/ztech-twitter-bot",
                "X-Title": "ZTech Twitter Bot",
                "X-User": "ZTech Bot"
            }
            
            data = {
                "model": "openai/gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un experto en marketing digital y creación de contenido viral para redes sociales. Especializado en tecnología y programación. Responde siempre en español."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Seleccionar la mejor versión si hay múltiples
                if "1." in content and "2." in content:
                    versions = content.split("\n\n")
                    content = random.choice(versions)
                
                # Limpiar y formatear
                content = self._clean_content(content)
                
                logger.info(f"✅ Contenido generado con OpenRouter GPT: {content_type}")
                return content
            else:
                logger.error(f"❌ Error con OpenRouter API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error con OpenRouter: {e}")
            return None
    
    def _generate_with_openai(self, prompt: str, content_type: str) -> Optional[str]:
        """Genera contenido usando OpenAI GPT"""
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing digital y creación de contenido viral para redes sociales. Especializado en tecnología y programación."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8,
                top_p=0.9
            )
            
            content = response.choices[0].message.content.strip()
            
            # Seleccionar la mejor versión si hay múltiples
            if "1." in content and "2." in content:
                versions = content.split("\n\n")
                content = random.choice(versions)
            
            # Limpiar y formatear
            content = self._clean_content(content)
            
            logger.info(f"✅ Contenido generado con OpenAI: {content_type}")
            return content
            
        except Exception as e:
            logger.error(f"❌ Error con OpenAI: {e}")
            return None
    
    def _generate_with_anthropic(self, prompt: str, content_type: str) -> Optional[str]:
        """Genera contenido usando Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Seleccionar la mejor versión si hay múltiples
            if "1." in content and "2." in content:
                versions = content.split("\n\n")
                content = random.choice(versions)
            
            # Limpiar y formatear
            content = self._clean_content(content)
            
            logger.info(f"✅ Contenido generado con Anthropic: {content_type}")
            return content
            
        except Exception as e:
            logger.error(f"❌ Error con Anthropic: {e}")
            return None
    
    def _clean_content(self, content: str) -> str:
        """Limpia y formatea el contenido generado"""
        # Remover numeración si existe
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remover numeración (1., 2., etc.)
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                line = line.split('.', 1)[1].strip()
            
            # Remover comillas si están al inicio y final
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            
            # Remover "Versión 1:", "Versión 2:", etc.
            if line.strip().startswith(('Versión 1:', 'Versión 2:', 'Versión 3:')):
                line = line.split(':', 1)[1].strip()
            
            # Remover "**Versión 1:**", "**Versión 2:**", etc.
            if '**Versión' in line:
                line = line.split('**', 2)[2].strip()
            
            cleaned_lines.append(line)
        
        # Unir líneas y limpiar
        content = ' '.join(cleaned_lines)
        content = content.replace('  ', ' ').strip()
        
        # Remover texto adicional después de hashtags
        if 'Versión' in content:
            content = content.split('Versión')[0].strip()
        
        # Asegurar que no exceda el límite de caracteres
        if len(content) > self.max_length:
            content = content[:self.max_length-3] + "..."
        
        return content
    
    def generate_from_article(self, article: Dict) -> Optional[str]:
        """
        Genera contenido basado en un artículo específico
        
        Args:
            article: Diccionario con información del artículo
            
        Returns:
            Contenido generado o None
        """
        try:
            title = article.get('title', '')
            summary = article.get('summary', '')
            content = article.get('content', '')
            
            # Combinar información del artículo
            article_text = f"Título: {title}\n\nResumen: {summary}\n\nContenido: {content}"
            
            # Determinar el tipo de contenido basado en el artículo
            content_type = self._determine_content_type(article)
            
            # Generar contenido
            return self.generate_content(content_type, article_text)
            
        except Exception as e:
            logger.error(f"❌ Error generando contenido desde artículo: {e}")
            return None
    
    def _determine_content_type(self, article: Dict) -> str:
        """Determina el tipo de contenido basado en el artículo"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        content = f"{title} {summary}"
        
        # Palabras clave para cada tipo
        if any(word in content for word in ['hack', 'trick', 'shortcut', 'tip', 'truco', 'atajo']):
            return 'hacks'
        elif any(word in content for word in ['professional', 'career', 'job', 'profesional', 'carrera', 'trabajo']):
            return 'protips'
        elif any(word in content for word in ['top', 'best', 'ranking', 'mejor', 'ranking']):
            return 'top_lists'
        elif any(word in content for word in ['fact', 'curious', 'amazing', 'hecho', 'curioso', 'increíble']):
            return 'curiosities'
        elif any(word in content for word in ['controversial', 'debate', 'opinion', 'controversial', 'debate', 'opinión']):
            return 'controversial'
        elif any(word in content for word in ['history', 'historical', 'vintage', 'historia', 'histórico']):
            return 'history'
        else:
            # Por defecto, usar hacks
            return 'hacks'
    
    def is_available(self) -> bool:
        """Verifica si las APIs de IA están disponibles"""
        return bool(self.qwen_available or self.openai_client or self.anthropic_client)
