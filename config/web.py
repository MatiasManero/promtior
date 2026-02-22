"""
Configuración Web: URL base del sitio Promtior y rutas para RAG.
Variables de entorno: PROMTIOR_WEB_*
"""

from typing import Literal

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig

VectorStoreKind = Literal["chroma", "pgvector", "qdrant"]


class WebConfig(BaseConfig):
    """
    Configuración para el contenido web (RAG): URL base y paths a indexar.
    Prefijo: PROMTIOR_WEB_
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_WEB_")

    base_url: str = Field(
        default="https://www.promtior.ai",
        description="URL base del sitio de Promtior para RAG"
    )
    paths: list[str] = Field(
        default=["", "/about-us", "/service", "/contact-us", "/use-cases"],
        description="Rutas del sitio a indexar (paths, sin base_url)"
    )
    extra_paths: list[str] = Field(
        default=["https://careers.promtior.ai"],
        description="URLs absolutas o rutas relativas a indexar (si es ruta, se antepone base_url)"
    )
