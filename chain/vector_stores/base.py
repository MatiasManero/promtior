"""
Vector store abstracto: registro de implementaciones (Chroma, pgvector, Qdrant).
Cada backend en su propio módulo; la base registra vía __init_subclass__.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from config.main import Settings


class BaseVectorStore(ABC):
    """
    Proveedor abstracto de vector store: construye o carga el store y devuelve un retriever.
    Las subclases se registran en _registry con store_name.
    """

    _registry: dict[str, type["BaseVectorStore"]] = {}

    def __init_subclass__(cls, store_name: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if store_name is not None:
            cls._store_name = store_name
            BaseVectorStore._registry[store_name] = cls

    def __init__(
        self,
        settings: Settings,
        embeddings: Any,
        embedding_provider_name: str,
    ) -> None:
        self._settings = settings
        self._embeddings = embeddings
        self._embedding_provider_name = embedding_provider_name

    @property
    def store_name(self) -> str:
        return self.__class__._store_name

    @abstractmethod
    def get_retriever(
        self,
        load_documents: Callable[[], list[Document]],
        **kwargs: Any,
    ) -> BaseRetriever:
        """
        Devuelve un retriever sobre el contenido indexado.
        Si el store ya existe, lo carga; si no, usa load_documents() para indexar y persistir.
        """
        ...

    @classmethod
    def from_config(
        cls,
        settings: Settings,
        embeddings: Any,
        embedding_provider_name: str,
    ) -> "BaseVectorStore":
        """
        Factory: devuelve la implementación indicada en settings.vector_store.
        """
        name = settings.vector_store
        if name not in cls._registry:
            raise ValueError(
                f"Vector store desconocido: {name}. "
                f"Registrados: {list(cls._registry)}"
            )
        return cls._registry[name](
            settings=settings,
            embeddings=embeddings,
            embedding_provider_name=embedding_provider_name,
        )
