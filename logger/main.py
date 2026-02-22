"""
Punto central de configuración de logging con structlog.
Lee el formato desde env (LogConfig) y delega a console o twelve_fa.
Integra uvicorn y langchain para que usen el mismo formato.
"""

import logging
import sys

import structlog

from .config import LogConfig
from . import console as console_backend
from . import twelve_fa as twelve_fa_backend

# Loggers de terceros que redirigimos al mismo formato (uvicorn, langchain)
THIRD_PARTY_LOGGERS = (
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "langchain",
    "langchain_core",
    "langchain_community",
)


def _build_processor_formatter(log_config: LogConfig):
    """Construye el ProcessorFormatter para loggers de la stdlib (uvicorn, langchain)."""
    level = getattr(logging, log_config.level.upper(), logging.INFO)
    if log_config.format == "console":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()
    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
        ],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.UnicodeDecoder(),
            renderer,
        ],
    )


def configure_logging() -> None:
    """
    Configura structlog según PROMTIOR_LOG_FORMAT (console o 12fa).
    Redirige uvicorn y langchain al mismo formato.
    Debe llamarse al arranque de la aplicación.
    """
    log_config = LogConfig()
    level = getattr(logging, log_config.level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    if log_config.format == "console":
        processors = console_backend.get_processors()
    else:
        processors = twelve_fa_backend.get_processors()

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Unificar salida de uvicorn y langchain con nuestro formato
    root = logging.getLogger()
    root.setLevel(level)
    # Reemplazar el handler por defecto por uno con ProcessorFormatter
    for h in root.handlers[:]:
        root.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_build_processor_formatter(log_config))
    root.addHandler(handler)
    for name in THIRD_PARTY_LOGGERS:
        logging.getLogger(name).setLevel(level)


def get_logger(*args, **kwargs):
    """Devuelve un logger de structlog (structlog.get_logger)."""
    return structlog.get_logger(*args, **kwargs)
