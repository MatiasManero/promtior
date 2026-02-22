"""
Configuración del logging con structlog.
Variables de entorno: PROMTIOR_LOG_*
"""

from typing import Literal

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class LogConfig(BaseConfig):
    """
    Configuración del logging: formato (consola o 12fa) y nivel.
    Prefijo: PROMTIOR_LOG_
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_LOG_")

    format: Literal["console", "12fa"] = Field(
        default="console",
        description="Formato de salida: console (legible) o 12fa (JSON, 12-factor)",
    )
    level: str = Field(
        default="INFO",
        description="Nivel de log: DEBUG, INFO, WARNING, ERROR",
    )
