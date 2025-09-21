"""
Generador de contenido con IA mejorado para tweets largos y detallados
"""
import os
import random
from typing import Optional, Dict
from loguru import logger

# Importar configuraciones
try:
    from config import Config
except ImportError:
    logger.warning("⚠️ No se pudo importar Config, usando valores por defecto")
    class Config:
        USE_AI_CONTENT = True
        AI_MODEL_PREFERENCE = 'openrouter'

# Verificar disponibilidad de librerías
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("⚠️ Requests no disponible. Instala: pip install requests")

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


class AIContentGeneratorImproved:
    """Generador de contenido con IA mejorado para tweets largos y detallados"""
    
    def __init__(self, language: str = 'es'):
        self.language = language
        self.max_length = 280
        self._setup_ai_apis()
        self._init_prompts()
    
    def _setup_ai_apis(self):
        """Configura las APIs de IA disponibles"""
        self.openai_client = None
        self.anthropic_client = None
        self.openrouter_available = False
        
        # OpenRouter (usando la variable QWEN_API_KEY)
        if REQUESTS_AVAILABLE and os.getenv('QWEN_API_KEY'):
            self.openrouter_api_key = os.getenv('QWEN_API_KEY')
            self.openrouter_available = True
            logger.info("✅ OpenRouter API configurada")
        
        # OpenAI
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            logger.info("✅ OpenAI API configurada")
        
        # Anthropic
        if ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            logger.info("✅ Anthropic API configurada")
    
    def is_available(self) -> bool:
        """Verifica si hay alguna API de IA disponible"""
        return self.openrouter_available or self.openai_client or self.anthropic_client
    
    def _init_prompts(self):
        """Inicializa los prompts mejorados para contenido largo"""
        self.prompts = {
            'hacks': {
                'en': """Create a viral tech hack tweet with a detailed explanation. The tweet should have TWO parts:

PART 1 - The Hook (200-280 characters):
- Start with "HACK:" or "PRO TIP:"
- Include a practical tech tip or shortcut
- Use engaging emojis
- Have a hook that makes people want to try it
- Include relevant hashtags

PART 2 - The Explanation (500+ characters):
- Provide a detailed explanation of HOW to use the hack
- Explain WHY this hack is useful and when to use it
- Include step-by-step instructions or context
- Add additional related tips or variations
- Make it educational and actionable

Example format:
"HACK: Use Ctrl+Shift+T to reopen closed browser tabs! 🚀

[Detailed 500+ character explanation about how this works, why it's useful, when to use it, and additional related browser shortcuts]"

Create 1-2 versions of this detailed hack tweet.""",
                'es': """Crea un tweet viral de hack tecnológico con una explicación detallada. El tweet debe tener DOS partes:

PARTE 1 - El Gancho (200-280 caracteres):
- Comienza con "HACK:" o "PRO TIP:"
- Incluye un tip o atajo tecnológico práctico
- Usa emojis atractivos
- Tiene un gancho que haga que la gente quiera probarlo
- Incluye hashtags relevantes

PARTE 2 - La Explicación (500+ caracteres):
- Proporciona una explicación detallada de CÓMO usar el hack
- Explica POR QUÉ este hack es útil y cuándo usarlo
- Incluye instrucciones paso a paso o contexto
- Añade tips adicionales relacionados o variaciones
- Hazlo educativo y accionable

Formato de ejemplo:
"HACK: ¡Usa Ctrl+Shift+T para reabrir pestañas cerradas del navegador! 🚀

[Explicación detallada de 500+ caracteres sobre cómo funciona esto, por qué es útil, cuándo usarlo y atajos adicionales del navegador]"

Crea 1-2 versiones de este tweet de hack detallado."""
            },
            
            'protips': {
                'en': """Create a professional tech tip tweet with a detailed explanation. The tweet should have TWO parts:

PART 1 - The Hook (200-280 characters):
- Start with "PRO TIP:" or "CAREER ADVICE:"
- Share valuable professional advice
- Use professional but engaging tone
- Include relevant hashtags
- Appeal to developers, engineers, or tech workers

PART 2 - The Explanation (500+ characters):
- Provide a detailed explanation of WHY this tip matters
- Include specific examples or scenarios
- Explain the impact or benefit in detail
- Add context about when and how to apply it
- Make it actionable and comprehensive

Example format:
"PRO TIP: Always backup your code before major changes! 💾

[Detailed 500+ character explanation about version control, best practices, disaster recovery, and the importance of backups in professional development]"

Create 1-2 versions of this detailed pro tip tweet.""",
                'es': """Crea un tweet de consejo profesional tecnológico con una explicación detallada. El tweet debe tener DOS partes:

PARTE 1 - El Gancho (200-280 caracteres):
- Comienza con "PRO TIP:" o "CONSEJO PROFESIONAL:"
- Comparte consejo profesional valioso
- Usa un tono profesional pero atractivo
- Incluye hashtags relevantes
- Atrae a desarrolladores, ingenieros o trabajadores tech

PARTE 2 - La Explicación (500+ caracteres):
- Proporciona una explicación detallada de POR QUÉ este consejo importa
- Incluye ejemplos específicos o escenarios
- Explica el impacto o beneficio en detalle
- Añade contexto sobre cuándo y cómo aplicarlo
- Hazlo accionable y comprensivo

Formato de ejemplo:
"PRO TIP: ¡Siempre respalda tu código antes de cambios importantes! 💾

[Explicación detallada de 500+ caracteres sobre control de versiones, mejores prácticas, recuperación de desastres y la importancia de respaldos en desarrollo profesional]"

Crea 1-2 versiones de este tweet de consejo profesional detallado."""
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
                'en': """Create a controversial tech opinion tweet with a detailed explanation. The tweet should have TWO parts:

PART 1 - The Hook (200-280 characters):
- Start with "CONTROVERSIAL:" or "UNPOPULAR OPINION:"
- Present a bold, controversial tech opinion
- Be thought-provoking and debatable
- Use strong, confident language
- Include relevant hashtags

PART 2 - The Explanation (500+ characters):
- Provide a detailed explanation of WHY you hold this opinion
- Include specific examples, data, or evidence
- Explain the implications and consequences
- Address potential counterarguments
- Make it educational and thought-provoking

Example format:
"CONTROVERSIAL: AI will replace most developers within 5 years! 🤖

[Detailed 500+ character explanation about AI development trends, automation capabilities, job market analysis, and the future of software development]"

Create 1-2 versions of this detailed controversial tweet.""",
                'es': """Crea un tweet de opinión tecnológica controversial con una explicación detallada. El tweet debe tener DOS partes:

PARTE 1 - El Gancho (200-280 caracteres):
- Comienza con "CONTROVERSIAL:" o "OPINIÓN IMPOPULAR:"
- Presenta una opinión tech audaz y controversial
- Sé provocativo y debatible
- Usa lenguaje fuerte y confiado
- Incluye hashtags relevantes

PARTE 2 - La Explicación (500+ caracteres):
- Proporciona una explicación detallada de POR QUÉ sostienes esta opinión
- Incluye ejemplos específicos, datos o evidencia
- Explica las implicaciones y consecuencias
- Aborda contraargumentos potenciales
- Hazlo educativo y provocativo

Formato de ejemplo:
"CONTROVERSIAL: ¡La IA reemplazará a la mayoría de desarrolladores en 5 años! 🤖

[Explicación detallada de 500+ caracteres sobre tendencias de desarrollo de IA, capacidades de automatización, análisis del mercado laboral y el futuro del desarrollo de software]"

Crea 1-2 versiones de este tweet controversial detallado."""
            }
        }
    
    def generate_content(self, content_type: str, article_text: str = None) -> Optional[str]:
        """
        Genera contenido usando IA
        
        Args:
            content_type: Tipo de contenido a generar
            article_text: Texto del artículo (opcional)
            
        Returns:
            Contenido generado o None si hay error
        """
        try:
            if not self.is_available():
                logger.warning("⚠️ No hay APIs de IA disponibles")
                return None
            
            prompt_template = self.prompts.get(content_type, {}).get(self.language)
            if not prompt_template:
                logger.warning(f"⚠️ No hay prompt para {content_type} en {self.language}")
                return None
            
            # Si hay texto de artículo, agregarlo al prompt
            if article_text:
                prompt_template += f"\n\nContexto del artículo:\n{article_text[:1000]}..."
            
            # Generar contenido usando IA (prioridad: OpenRouter > OpenAI > Anthropic)
            if self.openrouter_available:
                return self._generate_with_openrouter(prompt_template, content_type)
            elif self.openai_client:
                return self._generate_with_openai(prompt_template, content_type)
            elif self.anthropic_client:
                return self._generate_with_anthropic(prompt_template, content_type)
            
        except Exception as e:
            logger.error(f"❌ Error generando contenido con IA: {e}")
            return None
    
    def _generate_with_openrouter(self, prompt: str, content_type: str) -> Optional[str]:
        """Genera contenido usando OpenRouter API con GPT-4o"""
        try:
            import requests
            
            # URL de la API de OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
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
                "max_tokens": 1000,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
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
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en marketing digital y creación de contenido viral para redes sociales. Especializado en tecnología y programación. Responde siempre en español."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.8,
                top_p=0.9
            )
            
            content = response.choices[0].message.content.strip()
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
                max_tokens=1000,
                temperature=0.8,
                system="Eres un experto en marketing digital y creación de contenido viral para redes sociales. Especializado en tecnología y programación. Responde siempre en español.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text.strip()
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
            
            # Remover "**PARTE 1**", "**PARTE 2**", etc.
            if '**PARTE' in line:
                line = line.split('**', 2)[2].strip()
            
            # Remover "PARTE 1:", "PARTE 2:", etc.
            if line.strip().startswith(('PARTE 1:', 'PARTE 2:', 'PARTE 3:')):
                line = line.split(':', 1)[1].strip()
            
            cleaned_lines.append(line)
        
        # Unir líneas y limpiar
        content = ' '.join(cleaned_lines)
        content = content.replace('  ', ' ').strip()
        
        # Remover texto adicional después de hashtags
        if 'Versión' in content:
            content = content.split('Versión')[0].strip()
        
        # Para contenido mejorado, permitir más caracteres
        if len(content) > 1000:
            content = content[:1000-3] + "..."
        
        return content
