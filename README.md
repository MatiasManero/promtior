# Chatbot de Promtior

Chatbot con **arquitectura RAG** (Retrieval-Augmented Generation) sobre LangChain: responde preguntas sobre el **contenido del sitio web de Promtior** ([promtior.ai](https://www.promtior.ai)), recuperando fragmentos relevantes e integrándolos en la respuesta.

## Funcionalidades

- **RAG**: índice del sitio Promtior (carga, fragmentación, embeddings con OpenAI u Ollama, vector store Chroma). Cada pregunta recupera los fragmentos más relevantes y el LLM responde en base a ese contexto.
- **Traducción de consultas**: si el usuario pregunta en otro idioma (ej. inglés) y los embeddings están en español, la pregunta se traduce al español para el retriever y el LLM responde en el idioma del usuario.
- Respuestas sobre servicios, GenAI, casos de uso, contacto, etc., basadas en el contenido real del sitio.

## Tecnologías

- **LangChain**: cadenas, prompts, integración con LLMs y vector stores
- **RAG**: WebBaseLoader (sitio Promtior) → RecursiveCharacterTextSplitter → Embeddings (OpenAI u Ollama) → Chroma → retriever → prompt + LLM
- **LangServe**: API del chatbot
- **FastAPI**: servidor web
- **OpenAI** u **Ollama**: LLM y embeddings (configurable por variables de entorno)

## Instalación

1. Clona el repositorio o descarga los archivos.

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno (copia `.env.example` a `.env`):
   - **OpenAI**: configurá `PROMTIOR_OPENAI_API_KEY` para usar OpenAI como LLM y para embeddings. El índice se guarda en `./data/chroma_promtior/openai`.
   - **Ollama** (sin API key): instalá Ollama, ejecutá `ollama pull nomic-embed-text` (y opcionalmente `ollama pull llama2` para el chat) y dejá Ollama corriendo. El índice se guarda en `./data/chroma_promtior/ollama`.

## Uso

### Ejecutar el servidor

```bash
python app.py
```

O con uvicorn directamente:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Página web para interactuar con el chat

Existe una **página `index.html`** para usar el chatbot desde el navegador. Con el servidor en marcha, abrí:

**http://localhost:8000/demo/**

Ahí se sirve la interfaz (`static/index.html`) donde podés escribir preguntas y ver las respuestas del chatbot en tiempo real.

### Versión pública

La página para uso público está disponible en [promtior-production-cc0b.up.railway.app](https://promtior-production-cc0b.up.railway.app/). Se recomienda acceder a [/demo](https://promtior-production-cc0b.up.railway.app/demo) para usar el chat.

### Probar el chatbot por API

1. **LangServe (POST /chat/invoke):**
   ```bash
   curl -X POST "http://localhost:8000/chat/invoke" \
     -H "Content-Type: application/json" \
     -d '{"input": "¿Qué servicios ofrece Promtior?"}'
   ```

2. **Documentación interactiva:**  
   Abrí http://localhost:8000/docs y probá `/chat/invoke`.

## Estructura del proyecto

```
├── app.py                    # Punto de entrada (uvicorn)
├── app/                      # FastAPI y LangServe
├── rag/                      # RAG, prompts, proveedores (OpenAI/Ollama), vector stores
├── config/                   # Configuración (PROMTIOR_*)
├── logger/                   # Logging (structlog, console / 12fa)
├── static/
│   └── index.html            # Página para interactuar con el chat (/demo/)
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Endpoints de la API

- `GET /`: Información sobre la API
- `GET /health`: Verificación de salud del servicio
- `GET /demo/`: Página web para chatear (index.html)
- `POST /chat/invoke`: Endpoint principal para chatear con el bot
- `GET /docs`: Documentación interactiva (Swagger UI)

## Documentación

- **Project Overview y diagrama de componentes**: ver [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)
- **Diagrama Draw.io**: `docs/architecture.drawio` (abrir con [Draw.io](https://app.diagrams.net/), exportable a Lucidchart)

## Notas

- El conocimiento del chatbot proviene del **contenido indexado** del sitio de Promtior (URLs en `PROMTIOR_WEB_*`).