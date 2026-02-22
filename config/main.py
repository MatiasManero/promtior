from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig
from config.app import AppConfig
from config.openai import OpenAIConfig
from config.ollama import OllamaConfig
from config.web import WebConfig
from config.chroma import ChromaConfig

class Settings(BaseConfig):
    """
    Clase principal: app, proveedores (openai, ollama), web (RAG), chroma y vector_store.
    """

    app: AppConfig = Field(default_factory=AppConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    web: WebConfig = Field(default_factory=WebConfig)
    chroma: ChromaConfig = Field(default_factory=ChromaConfig)

    vector_store: str = Field(
        default="chroma",
        description="Backend del vector store: chroma, pgvector o qdrant",
    )

    use_openai: bool = Field(
        default=True,
        description="Priorizar OpenAI si está disponible (api_key configurada)"
    )

    rag_translate_query: bool = Field(
        default=True,
        description="Traducir pregunta al español para el retriever cuando el usuario pregunta en otro idioma (embeddings en español)",
    )

    def provider(self) -> str:
        """'openai' si use_openai y hay api_key, sino 'ollama'."""
        if self.use_openai and self.openai.api_key:
            return "openai"
        return "ollama"