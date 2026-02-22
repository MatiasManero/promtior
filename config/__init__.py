"""
Módulo de configuración del chatbot de Promtior.
"""

from functools import lru_cache

from config.main import Settings


@lru_cache(maxsize=1)
def settings() -> Settings:
    """
    Retorna la instancia única de configuración (caché con lru_cache).
    """
    return Settings()


def __getattr__(name: str):
    if name == "translation":
        from chain import translation
        return translation
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Settings",
    "settings",
    "translation",
]
