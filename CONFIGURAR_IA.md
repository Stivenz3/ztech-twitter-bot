# 🤖 Configuración de APIs de IA para ZTech Bot

## 📋 APIs de IA Soportadas

El bot ZTech soporta múltiples APIs de IA para generar contenido original y creativo:

### 1. **OpenAI GPT** (Recomendado)

- **Modelo**: GPT-3.5-turbo o GPT-4
- **Costo**: ~$0.002 por tweet
- **Calidad**: Excelente
- **Configuración**:
  ```env
  OPENAI_API_KEY=sk-...
  AI_MODEL_PREFERENCE=openai
  ```

### 2. **Anthropic Claude**

- **Modelo**: Claude-3-sonnet
- **Costo**: ~$0.003 por tweet
- **Calidad**: Excelente
- **Configuración**:
  ```env
  ANTHROPIC_API_KEY=sk-ant-...
  AI_MODEL_PREFERENCE=anthropic
  ```

### 3. **Qwen (Alibaba Cloud)**

- **Modelo**: qwen-plus
- **Costo**: Variable
- **Calidad**: Buena
- **Configuración**:
  ```env
  QWEN_API_KEY=sk-...
  AI_MODEL_PREFERENCE=qwen
  ```

## 🚀 Cómo Obtener API Keys

### OpenAI

1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en el menú
4. Crea una nueva API key
5. Copia la key (empieza con `sk-`)

### Anthropic

1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys"
4. Crea una nueva API key
5. Copia la key (empieza con `sk-ant-`)

### Qwen (Alibaba Cloud)

1. Ve a [dashscope.aliyun.com](https://dashscope.aliyun.com)
2. Crea una cuenta de Alibaba Cloud
3. Activa el servicio DashScope
4. Crea una API key
5. Copia la key

## ⚙️ Configuración en el Bot

### 1. Actualizar .env

```env
# APIs de IA para generación de contenido
OPENAI_API_KEY=tu_openai_api_key_aqui
ANTHROPIC_API_KEY=tu_anthropic_api_key_aqui
QWEN_API_KEY=tu_qwen_api_key_aqui
USE_AI_CONTENT=true
AI_MODEL_PREFERENCE=openai
```

### 2. Configurar GitHub Secrets

Para GitHub Actions, agrega estos secrets en tu repositorio:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `QWEN_API_KEY`

### 3. Instalar Dependencias

```bash
pip install openai anthropic requests
```

## 🧪 Probar la Configuración

### Prueba Local

```bash
python test_qwen.py
```

### Prueba con GitHub Actions

1. Ve a tu repositorio en GitHub
2. Actions > ZTech Twitter Bot
3. Run workflow
4. Selecciona el tipo de publicación
5. Verifica los logs

## 💡 Tipos de Contenido Generados

Con IA habilitada, el bot genera:

- **Hacks**: Tips tecnológicos con explicaciones detalladas
- **Protips**: Consejos profesionales con contexto
- **Top Lists**: Rankings con justificaciones
- **Curiosities**: Datos curiosos con contexto histórico
- **Controversial**: Opiniones polémicas para generar debate
- **History**: Hechos históricos con contexto

## 📊 Ejemplos de Contenido

### Con IA (Mejorado):

```
🚀 HACK: ¡Usa Ctrl+Shift+T para reabrir pestañas cerradas al instante!
Esto te salva de perder trabajo importante y hace la navegación 10x más rápida.
¡Pruébalo ahora!

#tecnologia #hack #productividad #ztech
```

### Sin IA (Básico):

```
🎨 PROTIP: Sigue patrones de diseño - existen por una razón!

#tecnologia #tech #ztech #protip #profesional
```

## 🔧 Solución de Problemas

### Error: "No hay APIs de IA disponibles"

- Verifica que la API key esté en el archivo .env
- Asegúrate de que `USE_AI_CONTENT=true`
- Revisa que la API key sea válida

### Error: "Incorrect API key provided"

- Verifica que la API key sea correcta
- Asegúrate de que no haya espacios extra
- Confirma que la API key no haya expirado

### Error: "Failed to resolve host"

- Verifica tu conexión a internet
- Revisa que la URL de la API sea correcta
- Prueba con una VPN si es necesario

## 💰 Costos Estimados

Para un bot que publica 4 tweets por día:

- **OpenAI GPT-3.5**: ~$2.40/mes
- **Anthropic Claude**: ~$3.60/mes
- **Qwen**: Variable según el plan

## 🎯 Recomendación

Para empezar, te recomiendo **OpenAI GPT-3.5-turbo**:

- Fácil de configurar
- Costo razonable
- Excelente calidad
- Documentación completa

¿Necesitas ayuda configurando alguna API específica?
