"""
Configuración de structlog en formato 12-factor: JSON a stdout.
"""

import structlog


def get_processors():
    """
    Processors y renderer para formato 12fa (JSON a stdout).
    Retorna la lista completa para structlog.configure(processors=...).
    """
    return [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
