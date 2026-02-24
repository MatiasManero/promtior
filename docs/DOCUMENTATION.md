# Documentación del Chatbot Promtior

## Project Overview

El chatbot de Promtior es una solución RAG (Retrieval-Augmented Generation) que responde preguntas sobre el contenido del sitio web de Promtior. El conocimiento se obtiene indexando el sitio, fragmentándolo en chunks y almacenándolo en un vector store para recuperación semántica.

### Arquitectura: Strategy Pattern con clases abstractas

La solución utiliza el **Strategy Pattern** (patrón estrategia) mediante clases abstractas que permiten elegir en tiempo de ejecución:

- **Provider** (LLM y embeddings): `BaseProvider` con implementaciones `OpenAIProvider` y `OllamaProvider`. Se selecciona por configuración (`use_openai`, `api_key`).
- **Vector Store**: `BaseVectorStore` con implementación `ChromaVectorStore` (extensible a pgvector, Qdrant). Se selecciona por `settings.vector_store`.

Ambos usan registro automático vía `__init_subclass__` y factory `from_config()` para instanciar la implementación correcta según la configuración.

### Desafío del idioma y solución

El contexto indexado está en español, pero los usuarios pueden preguntar en otros idiomas (ej. inglés). Sin tratamiento, el retriever no recuperaba el contexto correcto porque la query en inglés no coincidía semánticamente con los chunks en español.

**Solución implementada:**
1. **Traducción de la query**: Si la pregunta no está en español, se traduce al español antes de pasarla al retriever (langdetect + deep-translator). La pregunta original se mantiene para el prompt.
2. **Prompt mejorado**: Se añadió la regla explícita de que el LLM responda siempre en el mismo idioma en que el usuario formuló la pregunta.

### Evolución: Ollama → OpenAI

El proyecto comenzó usando **Ollama** (LLM y embeddings locales) para desarrollo sin coste de API. Debido al alto consumo de RAM que requería, se migró a **OpenAI** para el entorno de producción. El software funciona con ambos proveedores; la elección se hace por configuración (`PROMTIOR_OPENAI_API_KEY` y `use_openai`).

---

### Flujo resumido (pregunta → respuesta)

1. **Usuario/API** envía la pregunta a FastAPI (LangServe).
2. **PromtiorRAG** recibe la pregunta.
3. **Translation** detecta el idioma y traduce la query al español si es necesario (para el retriever).
4. **Retriever** (Chroma + embeddings del Provider) recupera los chunks más relevantes.
5. **Prompt** combina contexto recuperado + pregunta original.
6. **LLM** (OpenAI u Ollama) genera la respuesta en el idioma del usuario.
7. La **respuesta** se devuelve al usuario.
