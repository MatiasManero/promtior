"""
Punto de entrada para ejecutar la aplicación.
Uso: python app.py
En Railway (y entornos cloud) se usa la variable de entorno PORT.
"""

import os

import uvicorn

from config import settings
from logger import configure_logging, get_logger

if __name__ == "__main__":
    configure_logging()
    log = get_logger(__name__)
    config = settings()
    log.info("Iniciando servidor uvicorn", host=config.app.host, port=config.app.port)
    uvicorn.run(
        "app.main:app",
        host=config.app.host,
        port=config.app.port,
        reload=config.app.reload,
    )
