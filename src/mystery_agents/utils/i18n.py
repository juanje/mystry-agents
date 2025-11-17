"""Internationalization (i18n) labels and translations for the mystery game generator.

This module centralizes all user-facing text translations to ensure consistent
multilingual support across the application.
"""

from mystery_agents.utils.constants import LANG_CODE_ENGLISH, LANG_CODE_SPANISH

# Clue metadata labels
CLUE_LABELS = {
    LANG_CODE_ENGLISH: {
        "clue": "Clue",
        "type": "Type",
        "description": "Description",
        "related_info": "Related Information",
        "incriminates": "Incriminates",
        "exonerates": "Exonerates",
        "red_herring": "Red Herring",
        "metadata": "Metadata",
        "none": "None",
        "yes": "Yes",
        "no": "No",
    },
    LANG_CODE_SPANISH: {
        "clue": "Pista",
        "type": "Tipo",
        "description": "Descripción",
        "related_info": "Información Relacionada",
        "incriminates": "Incrimina",
        "exonerates": "Exonera",
        "red_herring": "Pista Falsa",
        "metadata": "Metadatos",
        "none": "Ninguno",
        "yes": "Sí",
        "no": "No",
    },
}


def get_clue_labels(language: str) -> dict[str, str]:
    """
    Get translated labels for clue metadata.

    Args:
        language: Language code (e.g., "en", "es")

    Returns:
        Dictionary mapping label keys to translated strings
    """
    return CLUE_LABELS.get(language, CLUE_LABELS[LANG_CODE_ENGLISH])


def get_language_name(language_code: str) -> str:
    """
    Get the full name of a language from its code.

    Args:
        language_code: Two-letter language code (e.g., "en", "es")

    Returns:
        Full language name (e.g., "English", "Spanish")
    """
    names = {
        LANG_CODE_ENGLISH: "English",
        LANG_CODE_SPANISH: "Spanish",
    }
    return names.get(language_code, language_code)
