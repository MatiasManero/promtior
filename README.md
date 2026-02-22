# Chatbot de Promtior

Chatbot con **arquitectura RAG** (Retrieval-Augmented Generation) sobre LangChain: responde preguntas sobre el **contenido del sitio web de Promtior** ([promtior.ai](https://www.promtior.ai)), recuperando fragmentos relevantes e integrándolos en la respuesta.

## Funcionalidades

- **RAG**: índice del sitio Promtior (carga, fragmentación, embeddings con OpenAI, vector store Chroma). Cada pregunta recupera los fragmentos más relevantes y el LLM responde en base a ese contexto.
- Si no hay API key de OpenAI, se usa un **contexto estático** (fallback) para que la app siga funcionando.
- Respuestas sobre servicios, GenAI, casos de uso, contacto, etc., basadas en el contenido real del sitio.

## Tecnologías

- **LangChain**: cadenas, prompts, integración con LLMs y vector stores
- **RAG**: WebBaseLoader (sitio Promtior) → RecursiveCharacterTextSplitter → OpenAI Embeddings → Chroma → retriever → prompt + LLM
- **LangServe**: API del chatbot
- **FastAPI**: servidor web
- **OpenAI**: embeddings (RAG) y opcionalmente LLM
- **Ollama + LLaMA2**: alternativa como LLM si no usás OpenAI

## Instalación

1. Clona el repositorio o descarga los archivos

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno (copia `.env.example` a `.env`):

   **Para RAG (recomendado)**  
   Los embeddings del RAG pueden ser:
   - **OpenAI**: configurá `PROMTIOR_CHAIN_OPENAI_API_KEY`. La primera vez se indexa el sitio y se guarda en `./data/chroma_promtior/openai`.
   - **Ollama** (sin API key): instalá Ollama, ejecutá `ollama pull nomic-embed-text` y dejá Ollama corriendo. El índice se guarda en `./data/chroma_promtior/ollama`.

   **Solo LLM (sin RAG)**  
   Si no hay API key ni Ollama disponible, el chatbot usa contexto estático. Para el LLM: misma key de OpenAI o Ollama (`ollama pull llama2` y Ollama en marcha).

## Uso

### Ejecutar el servidor

```bash
python app.py
```

O usando uvicorn directamente:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Consola interactiva (CLI)

Para chatear desde la terminal:

```bash
python -m cli.console
```

Escribe tu pregunta y pulsa Enter. Para salir: `salir`, `exit` o Ctrl+C.

### Demo web

Con el servidor en marcha, abrí en el navegador:

**http://localhost:8000/demo/**

Ahí podés escribir preguntas y ver las respuestas del chatbot (una página sencilla para demostración).

### Probar el chatbot

1. **LangServe (POST /chat/invoke):**
   ```bash
   curl -X POST "http://localhost:8000/chat/invoke" \
     -H "Content-Type: application/json" \
     -d '{"input": "¿Qué servicios ofrece Promtior?"}'
   ```

2. **Documentación interactiva:**
   - Abre http://localhost:8000/docs y prueba `/chat/invoke`.

3. **Script de prueba:**
   ```bash
   python chatbot.py
   ```

## Despliegue

### Docker

Se incluye un `Dockerfile` para facilitar el despliegue:

```bash
# Construir la imagen
docker build -t promtior-chatbot .

# Ejecutar el contenedor
docker run -p 8000:8000 --env-file .env promtior-chatbot
```

### AWS (EC2 / ECS / Lambda)

1. **EC2:**
   - Crea una instancia EC2
   - Instala Docker
   - Ejecuta el contenedor Docker

2. **ECS:**
   - Crea un cluster ECS
   - Crea una definición de tarea con el Dockerfile
   - Despliega el servicio

3. **Lambda:**
   - Usa AWS Lambda con contenedores Docker
   - Empaqueta la aplicación en un contenedor compatible con Lambda

### Azure (App Service / Container Instances)

1. **App Service:**
   - Crea un App Service
   - Configura el despliegue desde Docker Hub o Azure Container Registry
   - Establece las variables de entorno

2. **Container Instances:**
   - Crea una instancia de contenedor
   - Usa el Dockerfile proporcionado
   - Configura las variables de entorno

### Variables de entorno en producción

Asegúrate de configurar las variables de entorno según tu proveedor de nube:
- `OPENAI_API_KEY`: Si usas OpenAI
- O asegúrate de que Ollama esté disponible si usas esa opción

## Estructura del Proyecto

```
promtior/
├── app.py                 # Aplicación FastAPI con LangServe
├── chatbot.py             # Script de prueba del chatbot
├── promtior_info.py       # Información sobre Promtior
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración Docker
├── .env.example          # Ejemplo de variables de entorno
└── README.md             # Este archivo
```

## Endpoints de la API

- `GET /`: Información sobre la API
- `GET /health`: Verificación de salud del servicio
- `POST /chat/invoke`: Endpoint principal para chatear con el bot
- `GET /docs`: Documentación interactiva (Swagger UI)

## Notas

- El chatbot está configurado para responder solo preguntas sobre Promtior basándose en la información proporcionada en `promtior_info.py`
- Puedes modificar la información en `promtior_info.py` para actualizar el conocimiento del chatbot
- Para producción, considera agregar autenticación, rate limiting y logging adicional
