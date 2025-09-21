# 🤖 ZTech Twitter Bot

Bot automatizado para publicar contenido sobre tecnología en Twitter. Obtiene información de múltiples fuentes (RSS, APIs de noticias, Reddit) y publica tweets optimizados de forma programada.

## ✨ Características

- **📰 Múltiples fuentes de contenido**: RSS feeds, NewsAPI, Reddit
- **⏰ Publicación programada**: Configura horarios personalizados
- **🎯 Contenido optimizado**: Diferentes tipos de tweets para mayor engagement
- **📊 Base de datos**: Historial de tweets y estadísticas
- **🔄 Automatización completa**: Funciona 24/7 sin intervención
- **📈 Análisis de engagement**: Métricas de Twitter API
- **🛡️ Manejo de errores**: Sistema robusto de recuperación

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de desarrollador de Twitter
- (Opcional) API keys de NewsAPI y Reddit

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ztech-twitter-bot.git
cd ztech-twitter-bot
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar con tus credenciales
nano .env
```

### 4. Configurar credenciales de Twitter

1. Ve a [Twitter Developer Portal](https://developer.twitter.com/)
2. Crea una nueva aplicación
3. Obtén las siguientes credenciales:

   - API Key
   - API Secret
   - Bearer Token
   - Access Token
   - Access Token Secret

4. Actualiza el archivo `.env`:

```env
TWITTER_API_KEY=tu_api_key_aqui
TWITTER_API_SECRET=tu_api_secret_aqui
TWITTER_BEARER_TOKEN=tu_bearer_token_aqui
TWITTER_ACCESS_TOKEN=tu_access_token_aqui
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui
```

## 🎯 Uso

### Modos de ejecución

#### 1. Modo continuo (recomendado)

```bash
python main.py --mode continuous
```

#### 2. Publicación única

```bash
# Tweet simple
python main.py --mode single --post-type single

# Tweet curado (múltiples artículos)
python main.py --mode single --post-type curated
```

#### 3. Modo de prueba

```bash
python main.py --mode test
```

#### 4. Ver estadísticas

```bash
python main.py --mode stats
```

#### 5. Limpiar datos antiguos

```bash
python main.py --mode cleanup
```

### Verificar configuración

```bash
python main.py --config-check
```

## ⚙️ Configuración

### Variables de entorno principales

```env
# Twitter API
TWITTER_API_KEY=tu_api_key
TWITTER_API_SECRET=tu_api_secret
TWITTER_BEARER_TOKEN=tu_bearer_token
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret

# Configuración del bot
TWITTER_USERNAME=ztech
POSTING_SCHEDULE=09:00,18:00  # Horarios de publicación
TIMEZONE=America/Mexico_City

# Contenido
HASHTAGS=#tecnologia #innovacion #AI #programacion
MAX_TWEET_LENGTH=280
```

### APIs opcionales

#### NewsAPI

1. Regístrate en [NewsAPI](https://newsapi.org/)
2. Obtén tu API key
3. Agrega al `.env`:

```env
NEWS_API_KEY=tu_news_api_key
```

#### Reddit

1. Crea una aplicación en [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Obtén Client ID y Client Secret
3. Agrega al `.env`:

```env
REDDIT_CLIENT_ID=tu_client_id
REDDIT_CLIENT_SECRET=tu_client_secret
```

## 📁 Estructura del proyecto

```
ztech-twitter-bot/
├── src/
│   ├── __init__.py
│   ├── bot.py                 # Bot principal
│   ├── config.py              # Configuración
│   ├── database.py            # Gestión de base de datos
│   ├── twitter_client.py      # Cliente de Twitter API
│   ├── content_sources.py     # Fuentes de contenido
│   └── content_processor.py   # Procesamiento de contenido
├── logs/                      # Archivos de log
├── main.py                    # Punto de entrada
├── config.py                  # Configuración global
├── requirements.txt           # Dependencias
├── env.example               # Ejemplo de configuración
└── README.md                 # Este archivo
```

## 🔧 Funcionalidades

### Fuentes de contenido

- **RSS Feeds**: TechCrunch, Wired, Ars Technica, The Verge, etc.
- **NewsAPI**: Noticias de tecnología en tiempo real
- **Reddit**: Subreddits de tecnología y programación

### Tipos de tweets

1. **Noticias**: Publicación directa de noticias
2. **Insights**: Análisis y perspectivas
3. **Preguntas**: Para aumentar engagement
4. **Destacados**: Contenido trending
5. **Curados**: Múltiples artículos en un tweet

### Programación automática

- Publicaciones diarias en horarios configurados
- Publicaciones curadas los viernes
- Evita contenido duplicado
- Manejo inteligente de rate limits

## 📊 Monitoreo

### Logs

Los logs se guardan en `logs/ztech_bot.log` con rotación diaria.

### Estadísticas

```bash
python main.py --mode stats
```

Muestra:

- Tweets publicados por día
- Contenido procesado
- Errores
- Rate limits de Twitter API

### Base de datos

SQLite con las siguientes tablas:

- `published_tweets`: Historial de tweets
- `processed_content`: Contenido procesado
- `bot_stats`: Estadísticas diarias
- `bot_config`: Configuración

## 🚀 Deployment

### GitHub Actions (Recomendado)

1. Crea un repositorio en GitHub
2. Agrega tus credenciales como secrets:

   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_BEARER_TOKEN`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`

3. El workflow se ejecutará automáticamente según el cron configurado.

### VPS/Cloud

```bash
# Instalar como servicio systemd
sudo cp ztech-bot.service /etc/systemd/system/
sudo systemctl enable ztech-bot
sudo systemctl start ztech-bot
```

### Docker

```bash
# Construir imagen
docker build -t ztech-bot .

# Ejecutar
docker run -d --env-file .env ztech-bot
```

## 🛠️ Desarrollo

### Estructura de código

- **Modular**: Cada funcionalidad en su propio módulo
- **Configurable**: Todo configurable via variables de entorno
- **Extensible**: Fácil agregar nuevas fuentes de contenido
- **Testeable**: Código preparado para testing

### Agregar nuevas fuentes

1. Crear nueva clase heredando de `ContentSource`
2. Implementar método `fetch_content()`
3. Agregar a `ContentAggregator`

### Agregar nuevos tipos de tweets

1. Crear método en `ContentProcessor`
2. Agregar a la lista de tipos en `process_article_to_tweet()`

## 📝 Límites y consideraciones

### Twitter API

- **Plan gratuito**: 500 tweets/mes
- **Rate limits**: 300 requests/15min para posting
- **Contenido**: No spam, contenido original/atribuido

### Recomendaciones

- 1-2 tweets por día máximo
- Siempre atribuir fuentes
- Evitar contenido duplicado
- Monitorear engagement

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ztech-twitter-bot/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/ztech-twitter-bot/wiki)
- **Twitter**: [@ztech](https://twitter.com/ztech)

## 🙏 Agradecimientos

- Twitter API v2
- Tweepy library
- NewsAPI
- Reddit API
- Todas las fuentes RSS de tecnología

---

**⚠️ Importante**: Este bot es para fines educativos y de difusión de información tecnológica. Respeta los términos de servicio de todas las APIs utilizadas y las mejores prácticas de Twitter.
