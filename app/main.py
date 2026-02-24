"""
Aplicación FastAPI del chatbot de Promtior.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from langserve import add_routes

from rag import chain as chat_chain
from app.endpoints import router
from config import settings
from logger import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)
config = settings()
chain = chat_chain()
log.info("Aplicación iniciada", title=config.app.app_title, chat_path=config.app.chat_path)

app = FastAPI(
    title=config.app.app_title,
    version=config.app.app_version,
    description=config.app.app_description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.cors_allow_origins,
    allow_credentials=config.app.cors_allow_credentials,
    allow_methods=config.app.cors_allow_methods,
    allow_headers=config.app.cors_allow_headers,
)

app.include_router(router)

# Demo web: una sola página estática en /demo
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.is_dir():
    app.mount("/demo", StaticFiles(directory=str(static_dir), html=True), name="demo")

# LangServe registra bajo /chat las rutas automáticas: /chat/invoke, /chat/stream, etc.
add_routes(
    app,
    chain,
    path=config.app.chat_path
)