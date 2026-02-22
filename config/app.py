"""
Configuraciones de la aplicación FastAPI.
Incluye OpenAI, Ollama y Web (RAG) como submodelos.
Variables de entorno: PROMTIOR_APP_*, PROMTIOR_OPENAI_*, PROMTIOR_OLLAMA_*, PROMTIOR_WEB_*
"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class AppConfig(BaseConfig):
    """
    Configuraciones de la aplicación FastAPI.
    Prefijo: PROMTIOR_APP_. Incluye openai, ollama y web.
    """

    model_config = SettingsConfigDict(env_prefix="PROMTIOR_APP_")

    # Configuración del servidor
    host: str = Field(default="0.0.0.0", description="Host del servidor")
    port: int = Field(default=8000, description="Puerto del servidor")
    reload: bool = Field(default=False, description="Activar reload en desarrollo")

    # Configuración de la aplicación
    app_title: str = Field(default="Chatbot de Promtior", description="Título de la aplicación")
    app_version: str = Field(default="1.0.0", description="Versión de la aplicación")
    app_description: str = Field(
        default="API del chatbot de Promtior usando LangChain y LangServe",
        description="Descripción de la aplicación"
    )

    # Configuración de CORS
    cors_allow_origins: list[str] = Field(
        default=["*"],
        description="Orígenes permitidos para CORS"
    )
    cors_allow_credentials: bool = Field(
        default=True,
        description="Permitir credenciales en CORS"
    )
    cors_allow_methods: list[str] = Field(
        default=["*"],
        description="Métodos HTTP permitidos en CORS"
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
        description="Headers permitidos en CORS"
    )

    # Configuración de rutas
    chat_path: str = Field(default="/chat", description="Ruta para el endpoint de chat")
