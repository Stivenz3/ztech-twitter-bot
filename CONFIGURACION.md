# 🔧 Configuración de ZTech Twitter Bot

## 📋 Pasos para configurar tu bot

### 1. Crear archivo de configuración

Copia el archivo `env.example` a `.env`:

```bash
copy env.example .env
```

### 2. Configurar credenciales de Twitter

Edita el archivo `.env` con tus credenciales reales:

```env
# Twitter API Credentials - ZTech Bot
TWITTER_API_KEY=0GfOX57m3C280ZqC4JbR24K
TWITTER_API_SECRET=S4EaL3yZSk9UVLI3fETkJOHzAHMDYQtez6RUFPm7rFFVxW
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAJc84QEAAAAAA6nfgnzIIHwYHb%2B0Yqzu6juHhKI%3D73l46nQSUuPVf7F6gYSL8axJGIHWbXVXt4kFXaG7UqH3vicAWa
TWITTER_ACCESS_TOKEN=tu_access_token_aqui
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui

# Configuración de la aplicación
TWITTER_USERNAME=ztech
POSTING_SCHEDULE=09:00,18:00
TIMEZONE=America/Mexico_City

# Configuración de contenido
MAX_TWEET_LENGTH=280
HASHTAGS=#tecnologia #innovacion #AI #programacion #ztech
CONTENT_SOURCES=rss,reddit,newsapi

# Base de datos
DATABASE_URL=sqlite:///ztech_bot.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/ztech_bot.log
```

### 3. Obtener Access Token y Access Token Secret

**IMPORTANTE**: Necesitas obtener el Access Token y Access Token Secret desde Twitter Developer Portal:

1. Ve a [Twitter Developer Portal](https://developer.twitter.com/)
2. Selecciona tu app "1969821075761684480ztechub"
3. Ve a "Keys and tokens"
4. En la sección "Access Token and Secret", haz clic en "Generate"
5. Copia los valores a tu archivo `.env`

### 4. Configurar APIs opcionales (recomendado)

#### NewsAPI (Gratuito)

1. Regístrate en [NewsAPI](https://newsapi.org/)
2. Obtén tu API key gratuita
3. Agrega al `.env`:

```env
NEWS_API_KEY=tu_news_api_key_aqui
```

#### Reddit API (Gratuito)

1. Ve a [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Crea una nueva aplicación (script)
3. Obtén Client ID y Client Secret
4. Agrega al `.env`:

```env
REDDIT_CLIENT_ID=tu_client_id_aqui
REDDIT_CLIENT_SECRET=tu_client_secret_aqui
```

## 🚀 Instalación y ejecución

### Instalación automática (Windows)

```cmd
scripts\install.bat
```

### Instalación manual

```cmd
pip install -r requirements.txt
mkdir logs
mkdir data
```

### Verificar configuración

```cmd
python main.py --config-check
```

### Ejecutar prueba

```cmd
python main.py --mode test
```

### Ejecutar bot

```cmd
python main.py --mode continuous
```

## 📊 Comandos útiles

```cmd
# Publicación única
python main.py --mode single

# Tweet curado
python main.py --mode single --post-type curated

# Ver estadísticas
python main.py --mode stats

# Limpiar datos antiguos
python main.py --mode cleanup
```

## 🔧 Configuración avanzada

### Horarios de publicación

Modifica `POSTING_SCHEDULE` en `.env`:

```env
POSTING_SCHEDULE=09:00,15:00,21:00  # 3 publicaciones al día
```

### Hashtags personalizados

```env
HASHTAGS=#tecnologia #innovacion #AI #programacion #ztech #startup
```

### Fuentes de contenido

```env
CONTENT_SOURCES=rss,newsapi  # Solo RSS y NewsAPI
```

## 🚨 Solución de problemas

### Error de autenticación

- Verifica que todas las credenciales estén correctas
- Asegúrate de que la app tenga permisos de escritura
- Verifica que no hay espacios extra en las credenciales

### Error de rate limit

- El bot maneja automáticamente los rate limits
- Si persiste, reduce la frecuencia de publicaciones

### No hay contenido

- Verifica la conexión a internet
- Revisa que las fuentes RSS estén funcionando
- Considera agregar NewsAPI o Reddit

## 📱 Deployment en GitHub Actions

1. Sube tu código a GitHub
2. Ve a Settings > Secrets and variables > Actions
3. Agrega estos secrets:

   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_BEARER_TOKEN`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `NEWS_API_KEY` (opcional)
   - `REDDIT_CLIENT_ID` (opcional)
   - `REDDIT_CLIENT_SECRET` (opcional)

4. El bot se ejecutará automáticamente según el cron configurado

## 🎯 Próximos pasos

1. ✅ Configura las credenciales
2. ✅ Prueba la conexión
3. ✅ Ejecuta una publicación de prueba
4. ✅ Configura el deployment automático
5. ✅ Monitorea las estadísticas

¡Tu bot ZTech estará listo para publicar contenido sobre tecnología automáticamente! 🚀
