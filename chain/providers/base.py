"""
Proveedor abstracto: registro de subclases vía __init_subclass__.
Recibe AppSettings (openai, ollama, web).
"""

from abc import ABC, abstractmethod
from typing import Any

from config import settings
from config import Settings

class BaseProvider(ABC):
    """
    Proveedor abstracto: expone llm() y embeddings().
    Las subclases se registran en _registry con provider_name.
    """

    _registry: dict[str, type["BaseProvider"]] = {}

    def __init_subclass__(cls, provider_name: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if provider_name is not None:
            cls._provider_name = provider_name
            BaseProvider._registry[provider_name] = cls

    def __init__(self) -> None:
        self._config = settings()

    @property
    def provider_name(self) -> str:
        return self.__class__._provider_name

    @abstractmethod
    def llm(self):
        """Devuelve el LLM (chat) de este proveedor."""
        ...

    @abstractmethod
    def embeddings(self):
        """Devuelve el modelo de embeddings de este proveedor."""
        ...

    @classmethod
    def from_config(cls, app: Settings) -> "BaseProvider":
        """
        Factory: devuelve la instancia del proveedor indicado en la configuración.
        """
        name = app.provider()
        if name not in cls._registry:
            raise ValueError(f"Proveedor desconocido: {name}. Registrados: {list(cls._registry)}")
        return cls._registry[name]()
