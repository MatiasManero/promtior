"""
Módulo de logging con structlog (consola o 12fa).
"""

from .main import configure_logging, get_logger

__all__ = [
    "configure_logging",
    "get_logger",
]
