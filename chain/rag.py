"""
RAG: carga del sitio de Promtior, embeddings y retriever.
Soporta embeddings con OpenAI (con API key) u Ollama (local, sin key).
Vector store configurable (Chroma por defecto; futuros: pgvector, Qdrant).
"""

import hashlib

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_transformers import Html2TextTransformer

from config import settings
from chain.providers import get_provider
from chain.vector_stores import BaseVectorStore
from logger import get_logger

log = get_logger(__name__)


def _promtior_urls() -> list[str]:
    config = settings()
    web = config.web
    base = web.base_url.rstrip("/")
    paths = [f"{base}{p}" if p else base for p in web.paths]
    return [base] + paths + web.extra_paths


def _urls_fingerprint(urls: list[str]) -> str:
    """Hash de la lista de URLs para detectar cambios y forzar reindexación."""
    return hashlib.sha256(" ".join(sorted(urls)).encode()).hexdigest()


def _embeddings():
    """Devuelve el modelo de embeddings del proveedor configurado (OpenAI u Ollama)."""
    return get_provider().embeddings()


def _embedding_provider() -> str:
    """Nombre del proveedor actual (para la ruta del vector store)."""
    return get_provider().provider_name


def _load_documents() -> list:
    """Carga y fragmenta el contenido del sitio de Promtior."""
    urls = _promtior_urls()
    log.info("Cargando documentos RAG", url_count=len(urls), urls=urls[:5])
    loader = WebBaseLoader(urls)
    docs = loader.load()
    if not docs:
        log.warning("No se cargó ningún documento", urls=urls)
        return []

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs_transformed)
    log.info("Documentos cargados y fragmentados", docs=len(docs), chunks=len(chunks))
    return chunks


def retriever():
    """
    Devuelve un retriever sobre el contenido del sitio Promtior.
    Usa el vector store configurado (settings.vector_store: chroma, pgvector, qdrant).
    Construye el store si no existe; si existe, lo carga.
    """
    config = settings()
    provider_name = _embedding_provider()
    log.info("Construyendo retriever", provider=provider_name, vector_store=config.vector_store)
    embeddings = _embeddings()

    urls = _promtior_urls()
    store = BaseVectorStore.from_config(
        settings=config,
        embeddings=embeddings,
        embedding_provider_name=provider_name,
    )
    return store.get_retriever(
        load_documents=_load_documents
    )
