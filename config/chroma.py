"""
Configuración de Chroma (vector store).
Variables de entorno: PROMTIOR_CHROMA_*
"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class ChromaConfig(BaseConfig):
    """
    Configuración del vector store Chroma: ruta de persistencia y top_k del RAG.
    Prefijo: PROMTIOR_CHROMA_
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_CHROMA_")

    vector_store_path: str = Field(
        default="./data/chroma_promtior",
        description="Ruta base donde persistir el vector store (directorio por proveedor de embeddings)",
    )
    rag_top_k: int = Field(
        default=6,
        ge=1,
        le=20,
        description="Número de fragmentos a recuperar por pregunta",
    )
