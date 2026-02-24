"""
Proveedor OpenAI: LLM y embeddings con API key.
"""

from rag.providers.base import BaseProvider
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from logger import get_logger

log = get_logger(__name__)


class OpenAIProvider(BaseProvider, provider_name="openai"):
    """Proveedor OpenAI: LLM y embeddings con API key."""

    def llm(self):
        config = self._config.openai
        log.info("Usando OpenAI API", model=config.model)
        return ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            api_key=config.api_key,
        )

    def embedding_model(self):
        config = self._config.openai
        return OpenAIEmbeddings(
            model=config.embedding_model,
            api_key=config.api_key,
        )
