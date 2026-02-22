"""
Configuración OpenAI (LLM y embeddings).
Variables de entorno: PROMTIOR_OPENAI_*
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class OpenAIConfig(BaseConfig):
    """
    Configuración para OpenAI: API key, modelo de chat y de embeddings.
    Prefijo: PROMTIOR_OPENAI_
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_OPENAI_")

    api_key: Optional[str] = Field(default=None, description="API Key de OpenAI")
    model: str = Field(default="gpt-5-mini", description="Modelo de chat")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperatura")
    embedding_model: str = Field(
        default="text-embedding-3-large",
        description="Modelo de embeddings para RAG"
    )
