"""
Configuración Ollama (LLM y embeddings locales).
Variables de entorno: PROMTIOR_OLLAMA_*
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class OllamaConfig(BaseConfig):
    """
    Configuración para Ollama: modelo de chat y de embeddings, URL base.
    Prefijo: PROMTIOR_OLLAMA_
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_OLLAMA_")

    model: str = Field(default="llama2", description="Modelo de chat")
    temperature: float = Field(default=0.4, ge=0.0, le=2.0, description="Temperatura")
    base_url: Optional[str] = Field(default=None, description="URL base de Ollama (ej: http://localhost:11434)")
    embedding_model: str = Field(
        default="nomic-embed-text",
        description="Modelo de embeddings para RAG (ej: ollama pull nomic-embed-text)"
    )
