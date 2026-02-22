"""
Proveedores de LLM y embeddings (OpenAI, Ollama).
Cada proveedor en su propio módulo; la base registra vía __init_subclass__.
"""

from typing import TYPE_CHECKING

from chain.providers.base import BaseProvider
from chain.providers.openai import OpenAIProvider
from chain.providers.ollama import OllamaProvider

if TYPE_CHECKING:
    from config import Settings

_provider: BaseProvider | None = None


def get_provider(app: "Settings | None" = None) -> BaseProvider:
    """Devuelve la instancia única del proveedor configurado (OpenAI u Ollama)."""
    global _provider
    if _provider is None:
        from config import settings
        _provider = BaseProvider.from_config(app or settings())
    return _provider


__all__ = ["BaseProvider", "OpenAIProvider", "OllamaProvider", "get_provider"]
