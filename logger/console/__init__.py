"""
Configuración de structlog para salida en consola (legible, con colores).
"""

import structlog


def get_processors():
    """
    Processors y renderer para formato consola.
    Retorna la lista completa para structlog.configure(processors=...).
    """
    return [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer(),
    ]
