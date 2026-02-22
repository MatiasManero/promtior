"""
Cadena de LangChain para el chatbot de Promtior.
Arquitectura RAG: recuperación sobre el sitio Promtior + generación con LLM.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from config import settings
from chain.context import RAG_SYSTEM, RAG_HUMAN
from chain.providers import get_provider
from chain.translation import query_for_retrieval
from chain.rag import retriever
from logger import get_logger

log = get_logger(__name__)

def _format_docs(docs: list[Document]) -> str:
    return "\n\n".join(d.page_content.strip() for d in docs if d.page_content.strip())


class PromtiorChain:
    """
    Encapsula la cadena RAG de LangChain: retriever (sitio Promtior) + prompt + LLM.
    Singleton: usar PromtiorChain.instance() donde se necesite la cadena.
    """

    _instance: "PromtiorChain | None" = None

    def __new__(cls) -> "PromtiorChain":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_runnable"):
            return
        self._settings = settings()
        self._llm = self._build_llm()
        self._retriever = self._load_retriever()
        self._prompt = self._build_rag_prompt()
        self._runnable = self._build_rag_chain()

    @classmethod
    def instance(cls) -> "PromtiorChain":
        """Devuelve la instancia única del singleton."""
        return cls()

    def _build_llm(self):
        """Construye el LLM usando el proveedor registrado (OpenAI u Ollama)."""
        return get_provider(self._settings).llm()

    def _load_retriever(self):
        """Retriever sobre el contenido del sitio de Promtior (RAG)."""
        return retriever()

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
    return PromtiorChain.instance().runnable
