"""
Generador de contenido propio para el bot ZTech
Crea hacks, protips, top lists, curiosidades y contenido polémico
"""
import random
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from config import Config

class ContentGenerator:
    """Generador de contenido propio para diferentes tipos de publicaciones"""
    
    def __init__(self, language: str = 'es'):
        self.language = language
        self.max_length = Config.MAX_TWEET_LENGTH
        
        # Base de datos de contenido
        self._init_content_database()
    
    def _init_content_database(self):
        """Inicializa la base de datos de contenido"""
        
        # Hacks tecnológicos
        self.tech_hacks = {
            'en': [
                "💡 HACK: Use Ctrl+Shift+T to reopen closed browser tabs instantly!",
                "🚀 HACK: Windows key + L locks your computer in seconds!",
                "⚡ HACK: Ctrl+Shift+N opens incognito mode in any browser!",
                "🔒 HACK: Use 2FA on ALL your accounts - it's not optional anymore!",
                "📱 HACK: Double-tap space bar to add period and space on mobile!",
                "💻 HACK: Alt+Tab switches between open applications instantly!",
                "🌐 HACK: Use Ctrl+F to find any text on any webpage!",
                "📧 HACK: Use BCC when sending emails to multiple people!",
                "🔍 HACK: Use Ctrl+Shift+Delete to clear browser data quickly!",
                "⌨️ HACK: Use Ctrl+C and Ctrl+V to copy and paste anything!"
            ],
            'es': [
                "💡 HACK: Usa Ctrl+Shift+T para reabrir pestañas cerradas al instante!",
                "🚀 HACK: Tecla Windows + L bloquea tu computadora en segundos!",
                "⚡ HACK: Ctrl+Shift+N abre modo incógnito en cualquier navegador!",
                "🔒 HACK: Usa 2FA en TODAS tus cuentas - ya no es opcional!",
                "📱 HACK: Doble toque en espacio agrega punto y espacio en móvil!",
                "💻 HACK: Alt+Tab cambia entre aplicaciones abiertas al instante!",
                "🌐 HACK: Usa Ctrl+F para encontrar cualquier texto en cualquier página!",
                "📧 HACK: Usa CCO al enviar emails a múltiples personas!",
                "🔍 HACK: Usa Ctrl+Shift+Supr para limpiar datos del navegador rápido!",
                "⌨️ HACK: Usa Ctrl+C y Ctrl+V para copiar y pegar cualquier cosa!"
            ]
        }
        
        # Protips profesionales
        self.professional_tips = {
            'en': [
                "🎯 PROTIP: Always backup your code before making major changes!",
                "💼 PROTIP: Document your code - your future self will thank you!",
                "🚀 PROTIP: Use version control (Git) for every project, no matter how small!",
                "🔒 PROTIP: Never commit passwords or API keys to version control!",
                "📊 PROTIP: Test your code before deploying to production!",
                "🌐 PROTIP: Use HTTPS everywhere - security is not optional!",
                "📱 PROTIP: Design mobile-first - most users are on mobile!",
                "⚡ PROTIP: Optimize images before uploading - size matters!",
                "🔍 PROTIP: Use meaningful variable names - code should be self-documenting!",
                "🎨 PROTIP: Follow design patterns - they exist for a reason!"
            ],
            'es': [
                "🎯 PROTIP: Siempre respalda tu código antes de hacer cambios importantes!",
                "💼 PROTIP: Documenta tu código - tu yo futuro te lo agradecerá!",
                "🚀 PROTIP: Usa control de versiones (Git) para cada proyecto, sin importar qué tan pequeño!",
                "🔒 PROTIP: Nunca subas contraseñas o API keys al control de versiones!",
                "📊 PROTIP: Prueba tu código antes de desplegarlo a producción!",
                "🌐 PROTIP: Usa HTTPS en todas partes - la seguridad no es opcional!",
                "📱 PROTIP: Diseña mobile-first - la mayoría de usuarios están en móvil!",
                "⚡ PROTIP: Optimiza imágenes antes de subirlas - el tamaño importa!",
                "🔍 PROTIP: Usa nombres de variables significativos - el código debe ser auto-documentado!",
                "🎨 PROTIP: Sigue patrones de diseño - existen por una razón!"
            ]
        }
        
        # Top lists
        self.top_lists = {
            'en': [
                "🏆 TOP 5 Programming Languages in 2024:\n1. Python 🐍\n2. JavaScript 📜\n3. Java ☕\n4. C# 🔷\n5. Go 🐹",
                "🚀 TOP 5 Tech Trends 2024:\n1. AI & Machine Learning 🤖\n2. Cloud Computing ☁️\n3. Cybersecurity 🔒\n4. IoT 🌐\n5. Blockchain ⛓️",
                "💻 TOP 5 IDEs for Developers:\n1. Visual Studio Code 📝\n2. IntelliJ IDEA 🧠\n3. PyCharm 🐍\n4. Sublime Text ✨\n5. Atom ⚛️",
                "📱 TOP 5 Mobile Apps for Productivity:\n1. Notion 📝\n2. Todoist ✅\n3. Slack 💬\n4. Trello 📋\n5. Evernote 📄",
                "🔒 TOP 5 Cybersecurity Tips:\n1. Use strong passwords 🔑\n2. Enable 2FA 📱\n3. Keep software updated 🔄\n4. Use VPN 🌐\n5. Be cautious with emails 📧"
            ],
            'es': [
                "🏆 TOP 5 Lenguajes de Programación 2024:\n1. Python 🐍\n2. JavaScript 📜\n3. Java ☕\n4. C# 🔷\n5. Go 🐹",
                "🚀 TOP 5 Tendencias Tech 2024:\n1. IA & Machine Learning 🤖\n2. Cloud Computing ☁️\n3. Ciberseguridad 🔒\n4. IoT 🌐\n5. Blockchain ⛓️",
                "💻 TOP 5 IDEs para Desarrolladores:\n1. Visual Studio Code 📝\n2. IntelliJ IDEA 🧠\n3. PyCharm 🐍\n4. Sublime Text ✨\n5. Atom ⚛️",
                "📱 TOP 5 Apps Móviles para Productividad:\n1. Notion 📝\n2. Todoist ✅\n3. Slack 💬\n4. Trello 📋\n5. Evernote 📄",
                "🔒 TOP 5 Tips de Ciberseguridad:\n1. Usa contraseñas fuertes 🔑\n2. Activa 2FA 📱\n3. Mantén software actualizado 🔄\n4. Usa VPN 🌐\n5. Sé cauteloso con emails 📧"
            ]
        }
        
        # Curiosidades tecnológicas
        self.tech_curiosities = {
            'en': [
                "🤯 CURIOSITY: The first computer bug was an actual bug! A moth got stuck in a Harvard Mark II computer in 1947!",
                "💡 CURIOSITY: The first domain name ever registered was symbolics.com in 1985!",
                "🚀 CURIOSITY: The first email was sent in 1971 by Ray Tomlinson to himself!",
                "📱 CURIOSITY: The first smartphone was created by IBM in 1994, not Apple!",
                "🌐 CURIOSITY: The internet was originally designed to survive nuclear attacks!",
                "💻 CURIOSITY: The first computer virus was created in 1983 and was called 'Elk Cloner'!",
                "🔒 CURIOSITY: The first password was created in 1961 at MIT!",
                "📊 CURIOSITY: The first website is still online at info.cern.ch!",
                "⚡ CURIOSITY: The first computer mouse was made of wood in 1964!",
                "🎮 CURIOSITY: The first video game was created in 1958 and was called 'Tennis for Two'!"
            ],
            'es': [
                "🤯 CURIOSIDAD: ¡El primer bug de computadora fue un bicho real! ¡Una polilla se quedó atrapada en una computadora Harvard Mark II en 1947!",
                "💡 CURIOSIDAD: ¡El primer dominio registrado fue symbolics.com en 1985!",
                "🚀 CURIOSIDAD: ¡El primer email fue enviado en 1971 por Ray Tomlinson a sí mismo!",
                "📱 CURIOSIDAD: ¡El primer smartphone fue creado por IBM en 1994, no por Apple!",
                "🌐 CURIOSIDAD: ¡Internet fue diseñado originalmente para sobrevivir ataques nucleares!",
                "💻 CURIOSIDAD: ¡El primer virus de computadora fue creado en 1983 y se llamaba 'Elk Cloner'!",
                "🔒 CURIOSIDAD: ¡La primera contraseña fue creada en 1961 en MIT!",
                "📊 CURIOSIDAD: ¡El primer sitio web sigue en línea en info.cern.ch!",
                "⚡ CURIOSIDAD: ¡El primer mouse de computadora fue hecho de madera en 1964!",
                "🎮 CURIOSIDAD: ¡El primer videojuego fue creado en 1958 y se llamaba 'Tennis for Two'!"
            ]
        }
        
        # Contenido polémico
        self.controversial_content = {
            'en': [
                "🔥 CONTROVERSIAL: Is AI going to replace all developers? The truth might shock you!",
                "💥 CONTROVERSIAL: Why most startups fail - the harsh reality nobody talks about!",
                "🚨 CONTROVERSIAL: The dark side of social media algorithms - they're controlling your mind!",
                "⚡ CONTROVERSIAL: Why traditional education is failing the tech industry!",
                "🎯 CONTROVERSIAL: The biggest lie in tech: 'We care about your privacy'!",
                "💀 CONTROVERSIAL: Why most programming bootcamps are scams!",
                "🔥 CONTROVERSIAL: The truth about remote work - it's not what you think!",
                "🚨 CONTROVERSIAL: Why most tech companies are toxic workplaces!",
                "💥 CONTROVERSIAL: The biggest mistake developers make - and it's not technical!",
                "⚡ CONTROVERSIAL: Why most tech products are designed to be addictive!"
            ],
            'es': [
                "🔥 CONTROVERSIAL: ¿La IA va a reemplazar a todos los desarrolladores? ¡La verdad podría sorprenderte!",
                "💥 CONTROVERSIAL: Por qué la mayoría de startups fallan - ¡la dura realidad de la que nadie habla!",
                "🚨 CONTROVERSIAL: El lado oscuro de los algoritmos de redes sociales - ¡están controlando tu mente!",
                "⚡ CONTROVERSIAL: Por qué la educación tradicional está fallando a la industria tech!",
                "🎯 CONTROVERSIAL: La mentira más grande en tech: 'Nos importa tu privacidad'!",
                "💀 CONTROVERSIAL: Por qué la mayoría de bootcamps de programación son estafas!",
                "🔥 CONTROVERSIAL: La verdad sobre el trabajo remoto - ¡no es lo que piensas!",
                "🚨 CONTROVERSIAL: Por qué la mayoría de empresas tech son lugares de trabajo tóxicos!",
                "💥 CONTROVERSIAL: El error más grande que cometen los desarrolladores - ¡y no es técnico!",
                "⚡ CONTROVERSIAL: Por qué la mayoría de productos tech están diseñados para ser adictivos!"
            ]
        }
        
        # Historia de la tecnología
        self.tech_history = {
            'en': [
                "📚 HISTORY: On this day in 1975, Microsoft was founded by Bill Gates and Paul Allen!",
                "🏛️ HISTORY: The first computer, ENIAC, weighed 30 tons and filled an entire room!",
                "📖 HISTORY: The first programming language, FORTRAN, was created in 1957!",
                "🗓️ HISTORY: The first computer virus was created in 1983 by a 15-year-old!",
                "📜 HISTORY: The first website went live on August 6, 1991!",
                "🏆 HISTORY: The first computer game, 'Spacewar!', was created in 1962!",
                "📱 HISTORY: The first mobile phone call was made in 1973!",
                "🌐 HISTORY: The first email was sent in 1971 - it was just a test message!",
                "💻 HISTORY: The first laptop computer was created in 1981 and weighed 24 pounds!",
                "🔒 HISTORY: The first computer password was created in 1961 at MIT!"
            ],
            'es': [
                "📚 HISTORIA: ¡En este día en 1975, Microsoft fue fundada por Bill Gates y Paul Allen!",
                "🏛️ HISTORIA: ¡La primera computadora, ENIAC, pesaba 30 toneladas y llenaba una habitación entera!",
                "📖 HISTORIA: ¡El primer lenguaje de programación, FORTRAN, fue creado en 1957!",
                "🗓️ HISTORIA: ¡El primer virus de computadora fue creado en 1983 por un joven de 15 años!",
                "📜 HISTORIA: ¡El primer sitio web se puso en línea el 6 de agosto de 1991!",
                "🏆 HISTORIA: ¡El primer juego de computadora, 'Spacewar!', fue creado en 1962!",
                "📱 HISTORIA: ¡La primera llamada de teléfono móvil se hizo en 1973!",
                "🌐 HISTORIA: ¡El primer email fue enviado en 1971 - ¡solo era un mensaje de prueba!",
                "💻 HISTORIA: ¡La primera computadora portátil fue creada en 1981 y pesaba 24 libras!",
                "🔒 HISTORIA: ¡La primera contraseña de computadora fue creada en 1961 en MIT!"
            ]
        }
    
    def generate_content(self, content_type: str) -> Optional[str]:
        """
        Genera contenido según el tipo especificado
        
        Args:
            content_type: Tipo de contenido a generar
            
        Returns:
            Contenido generado o None si no se puede generar
        """
        try:
            if content_type == 'hacks':
                return self._generate_hack()
            elif content_type == 'protips':
                return self._generate_protip()
            elif content_type == 'top_lists':
                return self._generate_top_list()
            elif content_type == 'curiosities':
                return self._generate_curiosity()
            elif content_type == 'controversial':
                return self._generate_controversial()
            elif content_type == 'history':
                return self._generate_history()
            else:
                logger.warning(f"⚠️ Tipo de contenido no soportado: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error generando contenido: {e}")
            return None
    
    def _generate_hack(self) -> str:
        """Genera un hack tecnológico"""
        hacks = self.tech_hacks.get(self.language, self.tech_hacks['es'])
        hack = random.choice(hacks)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('hacks')
        return f"{hack}\n\n{hashtags}"
    
    def _generate_protip(self) -> str:
        """Genera un protip profesional"""
        tips = self.professional_tips.get(self.language, self.professional_tips['es'])
        tip = random.choice(tips)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('protips')
        return f"{tip}\n\n{hashtags}"
    
    def _generate_top_list(self) -> str:
        """Genera una lista top"""
        lists = self.top_lists.get(self.language, self.top_lists['es'])
        top_list = random.choice(lists)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('top_lists')
        return f"{top_list}\n\n{hashtags}"
    
    def _generate_curiosity(self) -> str:
        """Genera una curiosidad tecnológica"""
        curiosities = self.tech_curiosities.get(self.language, self.tech_curiosities['es'])
        curiosity = random.choice(curiosities)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('curiosities')
        return f"{curiosity}\n\n{hashtags}"
    
    def _generate_controversial(self) -> str:
        """Genera contenido polémico"""
        controversial = self.controversial_content.get(self.language, self.controversial_content['es'])
        content = random.choice(controversial)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('controversial')
        return f"{content}\n\n{hashtags}"
    
    def _generate_history(self) -> str:
        """Genera contenido histórico"""
        history = self.tech_history.get(self.language, self.tech_history['es'])
        content = random.choice(history)
        
        # Agregar hashtags
        hashtags = self._get_hashtags_for_type('history')
        return f"{content}\n\n{hashtags}"
    
    def _get_hashtags_for_type(self, content_type: str) -> str:
        """Obtiene hashtags específicos para el tipo de contenido"""
        base_hashtags = {
            'en': ['#tech', '#technology', '#ztech'],
            'es': ['#tecnologia', '#tech', '#ztech']
        }
        
        specific_hashtags = {
            'hacks': {
                'en': ['#hack', '#tip', '#productivity'],
                'es': ['#hack', '#tip', '#productividad']
            },
            'protips': {
                'en': ['#protip', '#professional', '#career'],
                'es': ['#protip', '#profesional', '#carrera']
            },
            'top_lists': {
                'en': ['#top', '#list', '#ranking'],
                'es': ['#top', '#lista', '#ranking']
            },
            'curiosities': {
                'en': ['#curiosity', '#fact', '#interesting'],
                'es': ['#curiosidad', '#dato', '#interesante']
            },
            'controversial': {
                'en': ['#controversial', '#debate', '#opinion'],
                'es': ['#controversial', '#debate', '#opinion']
            },
            'history': {
                'en': ['#history', '#techhistory', '#vintage'],
                'es': ['#historia', '#historiatech', '#vintage']
            }
        }
        
        base = base_hashtags.get(self.language, base_hashtags['es'])
        specific = specific_hashtags.get(content_type, {}).get(self.language, [])
        
        all_hashtags = base + specific
        return ' '.join(all_hashtags[:5])  # Máximo 5 hashtags
    
    def get_random_content_type(self) -> str:
        """Obtiene un tipo de contenido aleatorio basado en los pesos"""
        import random
        
        types = list(Config.POST_TYPE_WEIGHTS.keys())
        weights = list(Config.POST_TYPE_WEIGHTS.values())
        
        # Filtrar solo los tipos que podemos generar
        generatable_types = ['hacks', 'protips', 'top_lists', 'curiosities', 'controversial', 'history']
        filtered_types = [t for t in types if t in generatable_types]
        filtered_weights = [Config.POST_TYPE_WEIGHTS[t] for t in filtered_types]
        
        return random.choices(filtered_types, weights=filtered_weights)[0]
