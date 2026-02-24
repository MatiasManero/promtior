"""
RAG: carga del sitio de Promtior, embeddings, retriever y cadena LangChain.
Arquitectura: recuperación sobre el sitio Promtior + generación con LLM.
Soporta embeddings con OpenAI (con API key) u Ollama (local, sin key).
Vector store configurable (Chroma por defecto; futuros: pgvector, Qdrant).
"""

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from config import settings
from rag.context import RAG_SYSTEM, RAG_HUMAN
from rag.providers import get_provider
from rag.translation import query_for_retrieval
from rag.vector_stores import BaseVectorStore
from logger import get_logger

log = get_logger(__name__)


def _format_docs(docs: list[Document]) -> str:
    return "\n\n".join(d.page_content.strip() for d in docs if d.page_content.strip())


class PromtiorRAG:
    """
    Encapsula la cadena RAG de LangChain: retriever (sitio Promtior) + prompt + LLM.
    Singleton: usar PromtiorRAG.instance() donde se necesite la cadena.
    """

    _instance: "PromtiorRAG | None" = None

    def __new__(cls) -> "PromtiorRAG":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_runnable"):
            return
        self._settings = settings()
        self._provider = get_provider(self._settings)
        self._llm = self._provider.llm()
        self._retriever = self._load_retriever()
        self._prompt = self._build_rag_prompt()
        self._runnable = self._build_rag_chain()

    @classmethod
    def instance(cls) -> "PromtiorRAG":
        """Devuelve la instancia única del singleton."""
        return cls()

    def _get_promtior_urls(self) -> list[str]:
        web = self._settings.web
        base = web.base_url.rstrip("/")
        paths = [f"{base}{p}" if p else base for p in web.paths]
        return [base] + paths + web.extra_paths

    def _load_documents(self) -> list:
        """Carga y fragmenta el contenido del sitio de Promtior."""
        urls = self._get_promtior_urls()
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

    def _load_retriever(self):
        """
        Retriever sobre el contenido del sitio de Promtior.
        Usa el vector store configurado (settings.vector_store: chroma, pgvector, qdrant).
        Construye el store si no existe; si existe, lo carga.
        """
        provider_name = self._provider.provider_name
        log.info(
            "Construyendo retriever",
            provider=provider_name,
            vector_store=self._settings.vector_store,
        )
        embedding_model = self._provider.embedding_model()

        store = BaseVectorStore.from_config(
            settings=self._settings,
            embedding_model=embedding_model,
            embedding_provider_name=provider_name,
        )
        return store.get_retriever(load_documents=self._load_documents)

    def _build_rag_prompt(self) -> ChatPromptTemplate:
        """Prompt para RAG: contexto recuperado + pregunta."""
        return ChatPromptTemplate.from_messages([
            ("system", RAG_SYSTEM),
            ("human", RAG_HUMAN),
        ])

    def _build_rag_chain(self):
        """Cadena RAG: recuperar fragmentos → formatear contexto → prompt → LLM."""
        def _assign_context(x):
            retrieval_query = query_for_retrieval(
                x["input"],
                translate_enabled=self._settings.rag_translate_query,
            )
            return _format_docs(self._retriever.invoke(retrieval_query))
        return (
            RunnablePassthrough.assign(context=_assign_context)
            | self._prompt
            | self._llm
            | StrOutputParser()
        )

    @property
    def runnable(self):
        """Runnable para LangServe y para invocar (chain.invoke)."""
        return self._runnable


def chain():
    """Devuelve el runnable de la cadena (usa el singleton)."""
    return PromtiorRAG.instance().runnable
