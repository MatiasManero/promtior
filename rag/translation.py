"""
Traducción de la pregunta del usuario al español para el retriever.
Cuando los embeddings están en español, traducir la query mejora la recuperación
si el usuario pregunta en otro idioma (ej. inglés). La pregunta original se
mantiene para el prompt para que el LLM responda en el idioma del usuario.
"""

import langdetect

from logger import get_logger

log = get_logger(__name__)

# Idiomas que consideramos "español" (no traducir)
ES_LANG_CODES = {"es", "ca", "eu", "gl"}  # español, catalán, euskera, gallego


def _detect_language(text: str) -> str | None:
    """Detecta el idioma del texto. Devuelve código ISO (ej. 'en', 'es') o None si falla."""
    if not (text and text.strip()):
        return None
    try:
        return langdetect.detect(text.strip())
    except Exception as e:
        log.debug("langdetect falló", text_preview=text[:50] if text else "", error=str(e))
        return None


def _translate_to_spanish(text: str) -> str:
    """Traduce el texto al español usando deep-translator (Google)."""
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="auto", target="es").translate(text.strip())
        return translated if translated else text
    except Exception as e:
        log.warning("Traducción fallida, usando texto original", error=str(e))
        return text


def query_for_retrieval(query: str, translate_enabled: bool = True) -> str:
    """
    Devuelve la query a usar para el retriever.
    Si translate_enabled y la pregunta no está en español, la traduce al español.
    Si no, devuelve la pregunta tal cual.
    """
    if not translate_enabled or not (query and query.strip()):
        return query

    lang = _detect_language(query)
    if lang is None:
        log.debug("Idioma no detectado, intentando traducir", query_preview=query[:80] if query else "")
        return _translate_to_spanish(query)
    if lang.lower() in ES_LANG_CODES:
        return query
    translated = _translate_to_spanish(query)
    log.debug("Query traducida para retriever", lang_origen=lang, query_preview=query[:60], translated_preview=translated[:60])
    return translated
