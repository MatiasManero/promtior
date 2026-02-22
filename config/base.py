"""
Clase base para configuraciones usando Pydantic BaseSettings.
Prefijo PROMTIOR_; cada subclase define su env_prefix (ej: PROMTIOR_APP_*, PROMTIOR_OPENAI_*).
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Clase base para todas las configuraciones.
    Define el prefijo PROMTIOR_; las subclases deben definir env_prefix completo
    (ej: PROMTIOR_APP_, PROMTIOR_OPENAI_, PROMTIOR_OLLAMA_, PROMTIOR_WEB_).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="PROMTIOR_",
    )
    