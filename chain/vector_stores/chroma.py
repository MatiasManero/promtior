"""
Implementación del vector store con Chroma (persistencia en disco).
"""

from collections.abc import Callable
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from chain.vector_stores.base import BaseVectorStore
from config.main import Settings
from logger import get_logger

log = get_logger(__name__)


class ChromaVectorStore(BaseVectorStore, store_name="chroma"):
    """
    Vector store con Chroma: persist_directory por proveedor de embeddings.
    Usa settings.chroma (ChromaConfig) para vector_store_path y rag_top_k.
    """

    def _persist_dir(self) -> Path:
        base_path = Path(self._settings.chroma.vector_store_path)
        persist_dir = base_path / self._embedding_provider_name
        persist_dir.mkdir(parents=True, exist_ok=True)
        return persist_dir

    def _exists(self) -> bool:
        return (self._persist_dir() / "chroma.sqlite3").exists()

    def get_retriever(
        self,
        load_documents: Callable[[], list[Document]],
    ) -> BaseRetriever:
        persist_str = str(self._persist_dir())

        if self._exists():
            log.info("Cargando vector store Chroma desde disco", persist_dir=persist_str)
            vectorstore = Chroma(
                persist_directory=persist_str,
                embedding_function=self._embeddings,
            )
        else:
            log.info("Indexando documentos en Chroma (primera vez)", persist_dir=persist_str)
            docs = load_documents()
            if not docs:
                log.error("No se pudieron cargar documentos para el vector store")
                raise RuntimeError(
                    "No se pudieron cargar documentos del sitio de Promtior."
                )
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=self._embeddings,
                persist_directory=persist_str,
            )
            vectorstore.persist()
            log.info("Vector store Chroma indexado y persistido", num_docs=len(docs))

        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": self._settings.chroma.rag_top_k},
        )
