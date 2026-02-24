"""
Proveedor Ollama: LLM y embeddings locales (sin API key).
"""

from rag.providers.base import BaseProvider
from langchain_community.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings

from logger import get_logger

log = get_logger(__name__)


class OllamaProvider(BaseProvider, provider_name="ollama"):
    """Proveedor Ollama: LLM y embeddings locales (sin API key)."""

    def llm(self):
        config = self._config.ollama
        log.info("Usando Ollama", model=config.model)
        try:
            kwargs = {
                "model": config.model,
                "temperature": config.temperature,
            }
            if config.base_url:
                kwargs["base_url"] = config.base_url
            return ChatOllama(**kwargs)
        except Exception as e:
            log.error(
                "Error al conectar con Ollama",
                error=str(e),
                hint="Asegúrate de que Ollama esté instalado y corriendo.",
            )
            raise

    def embedding_model(self):
        config = self._config.ollama
        return OllamaEmbeddings(
            model=config.embedding_model,
            base_url=config.base_url,
        )
