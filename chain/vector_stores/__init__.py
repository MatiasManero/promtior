"""
Vector stores para RAG: Chroma (y futuros pgvector, Qdrant).
Cada implementación en su módulo; la base registra vía __init_subclass__.
"""

from chain.vector_stores.base import BaseVectorStore
from chain.vector_stores.chroma import ChromaVectorStore

__all__ = ["BaseVectorStore", "ChromaVectorStore"]
