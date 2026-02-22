"""
Endpoints de la API del chatbot de Promtior.
"""

from fastapi import APIRouter

from logger import get_logger

log = get_logger(__name__)
router = APIRouter()


@router.get("/")
def read_root():
    """Endpoint raíz con información sobre la API."""
    log.debug("GET /")
    return {
        "message": "API del Chatbot de Promtior",
        "version": "1.0.0",
        "endpoints": {
            "/demo": "Página web de demostración del chatbot",
            "/chat": "LangServe: /chat/invoke para enviar preguntas",
            "/docs": "Documentación interactiva de la API"
        }
    }


@router.get("/health")
def health_check():
    """Endpoint de salud para verificar que el servicio está funcionando."""
    log.debug("GET /health")
    return {"status": "healthy"}
