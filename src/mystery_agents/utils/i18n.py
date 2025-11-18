"""Internationalization (i18n) labels and translations for the mystery game generator.

This module centralizes all user-facing text translations to ensure consistent
multilingual support across the application.
"""

from mystery_agents.utils.constants import LANG_CODE_ENGLISH, LANG_CODE_SPANISH

# Document template labels for all markdown files
DOCUMENT_LABELS = {
    LANG_CODE_ENGLISH: {
        # Host Guide
        "host_guide_title": "Mystery Party Host Guide",
        "game_information": "Game Information",
        "game_id": "Game ID",
        "created": "Created",
        "players": "Players",
        "duration": "Duration",
        "minutes": "minutes",
        "language": "Language",
        "era": "Era",
        "location": "Location",
        "gathering_reason": "Gathering Reason",
        "introduction": "Introduction (Read to Guests)",
        "setup_instructions": "Setup Instructions",
        "your_role_act1": "Your Role in Act 1: The Victim",
        "see_victim_sheet": "📄 See your dedicated Victim Character Sheet (victim_character_sheet.pdf) for complete details.",
        "victim_sheet_includes": "The victim character sheet includes:",
        "full_background": "Full character background and personality traits",
        "public_persona": "Public persona and secrets",
        "costume_suggestions": "Costume suggestions",
        "character_portrait": "Character portrait (if images enabled)",
        "quick_summary": "Quick summary:",
        "no_description": "No victim role description provided.",
        "runtime_tips": "Runtime Tips",
        "murder_event": "The Murder Event (Transition to Act 2)",
        "no_murder_guide": "No murder event guide provided.",
        "act2_detective": "Act 2: You Are Now the Detective",
        "intro_script": "Introduction Script (Read to Players)",
        "no_act2_intro": "No Act 2 intro script provided.",
        "detective_role": "Your Detective Role",
        "see_detective_sheet": "📄 See your dedicated Detective Character Sheet (detective_character_sheet.pdf) for complete details.",
        "detective_sheet_includes": "The detective character sheet includes:",
        "character_description": "Full character description and personality traits",
        "clues_list": "Complete list of clues to reveal with interpretations",
        "guiding_questions": "Guiding questions to ask players",
        "solution_script": "Final solution script for the big reveal",
        "quick_tip": "Quick Tip",
        "keep_sheet_handy": "Keep the detective character sheet handy during Act 2 for quick reference!",
        # Solution
        "solution_title": "Complete Solution",
        "the_killer": "The Killer",
        "unknown": "Unknown",
        "rationale": "Rationale",
        "no_rationale": "No rationale provided.",
        "truth_narrative": "Truth Narrative",
        "no_truth_narrative": "No truth narrative provided.",
        "timeline_events": "Timeline of Events",
        "no_timeline": "No timeline provided.",
        "murder_event_title": "MURDER EVENT",
        "time": "Time",
        "what_happened": "What Happened",
        "characters_involved": "Characters Involved",
        # Epochs
        "epoch_modern": "Modern",
        "epoch_1920s": "1920s",
        "epoch_victorian": "Victorian",
        "epoch_custom": "Custom",
        # Invitation
        "invitation_title": "Mystery Party Invitation",
        "you_are_invited": "You Are Invited!",
        "role": "Role",
        "event_details": "Event Details",
        "date_time": "Date & Time",
        "tbd_host": "[To be determined by host]",
        "see_you_there": "See you there!",
        "what_you_receive": "What You'll Receive",
        "invitation": "This invitation",
        "character_sheet_full": "A character sheet with your full background and secrets",
        "portrait_if_enabled": "Your character portrait (if images enabled)",
        # Character Sheet
        "character_sheet_title": "Character Sheet",
        "your_character": "Your Character",
        "personality_traits": "Personality Traits",
        "backstory": "Backstory",
        "public_description": "Public Description",
        "personal_secrets": "Personal Secrets (Keep These Secret!)",
        "personal_goals": "Personal Goals",
        "motive": "Motive for Crime (If Guilty)",
        "no_motive": "No specific motive.",
        "costume": "Costume Suggestion",
        "no_costume": "No specific costume suggestion.",
        "act1_objectives": "Your Act 1 Objectives",
        "no_objectives": "No objectives defined.",
        "relation_to_victim": "Your Relationship to the Victim",
        "relationships": "Relationships with Other Characters",
        "remember_secrets": "Remember: use your secrets strategically during the investigation!",
        # Victim Sheet
        "victim_sheet_title": "Victim Character Sheet",
        "host_act1_role": "Your Role in Act 1",
        "important_note": "Important Note",
        "died_before_act2": "This character died before the investigation. You will NOT play this role during Act 2.",
        "embody_character": "Embody this character's personality and secrets",
        "create_tension": "Create tension and intrigue with the suspects",
        "follow_timing": "Follow the host guide for timing the murder event",
        # Detective Sheet
        "detective_sheet_title": "Detective Character Sheet",
        "host_act2_role": "Your Role in Act 2: The Detective",
        "clues_to_reveal": "Clues to Reveal During Investigation",
        "how_to_interpret": "How to Interpret",
        "final_solution": "Final Solution (The Big Reveal)",
        "solution_timing": "When players are ready for the solution (or time runs out):",
        "see_host_guide": "📄 See the host guide for complete clue reference and detailed investigation strategy.",
        # Clue Reference
        "clue_reference_title": "Clue Reference (Host Only)",
        "clue_overview": "Overview",
        "total_clues": "Total clues",
        "host_only_warning": "This document contains spoiler information about which clues incriminate/exonerate suspects. Do NOT share with players.",
        "players_get_clean": "Players will receive clean versions of the clues without the metadata.",
        # General
        "no_image": "No character image available.",
    },
    LANG_CODE_SPANISH: {
        # Host Guide
        "host_guide_title": "Guía del Anfitrión - Fiesta Misterio",
        "game_information": "Información del Juego",
        "game_id": "ID del Juego",
        "created": "Creado",
        "players": "Jugadores",
        "duration": "Duración",
        "minutes": "minutos",
        "language": "Idioma",
        "era": "Época",
        "location": "Ubicación",
        "gathering_reason": "Motivo de la Reunión",
        "introduction": "Introducción (Leer a los Invitados)",
        "setup_instructions": "Instrucciones de Preparación",
        "your_role_act1": "Tu Rol en el Acto 1: La Víctima",
        "see_victim_sheet": "📄 Ver tu Hoja de Personaje de la Víctima dedicada (victim_character_sheet.pdf) para detalles completos.",
        "victim_sheet_includes": "La hoja del personaje de la víctima incluye:",
        "full_background": "Trasfondo completo del personaje y rasgos de personalidad",
        "public_persona": "Personalidad pública y secretos",
        "costume_suggestions": "Sugerencias de vestuario",
        "character_portrait": "Retrato del personaje (si las imágenes están habilitadas)",
        "quick_summary": "Resumen rápido:",
        "no_description": "No se proporcionó descripción del rol de la víctima.",
        "runtime_tips": "Consejos Durante el Juego",
        "murder_event": "El Evento del Asesinato (Transición al Acto 2)",
        "no_murder_guide": "No se proporcionó guía del evento del asesinato.",
        "act2_detective": "Acto 2: Ahora Eres el Detective",
        "intro_script": "Guión de Introducción (Leer a los Jugadores)",
        "no_act2_intro": "No se proporcionó guión de introducción del Acto 2.",
        "detective_role": "Tu Rol como Detective",
        "see_detective_sheet": "📄 Ver tu Hoja de Personaje del Detective dedicada (detective_character_sheet.pdf) para detalles completos.",
        "detective_sheet_includes": "La hoja del personaje del detective incluye:",
        "character_description": "Descripción completa del personaje y rasgos de personalidad",
        "clues_list": "Lista completa de pistas para revelar con interpretaciones",
        "guiding_questions": "Preguntas guía para hacer a los jugadores",
        "solution_script": "Guión de la solución final para la gran revelación",
        "quick_tip": "Consejo Rápido",
        "keep_sheet_handy": "¡Mantén la hoja del personaje del detective a mano durante el Acto 2 para consulta rápida!",
        # Solution
        "solution_title": "Solución Completa",
        "the_killer": "El Asesino",
        "unknown": "Desconocido",
        "rationale": "Justificación",
        "no_rationale": "No se proporcionó justificación.",
        "truth_narrative": "Narrativa de la Verdad",
        "no_truth_narrative": "No se proporcionó narrativa de la verdad.",
        "timeline_events": "Cronología de Eventos",
        "no_timeline": "No se proporcionó cronología.",
        "murder_event_title": "EVENTO DEL ASESINATO",
        "time": "Hora",
        "what_happened": "Qué Sucedió",
        "characters_involved": "Personajes Involucrados",
        # Epochs
        "epoch_modern": "Moderna",
        "epoch_1920s": "Años 20",
        "epoch_victorian": "Victoriana",
        "epoch_custom": "Personalizada",
        # Invitation
        "invitation_title": "Invitación a Fiesta Misterio",
        "you_are_invited": "¡Estás Invitado!",
        "role": "Rol",
        "event_details": "Detalles del Evento",
        "date_time": "Fecha y Hora",
        "tbd_host": "[A determinar por el anfitrión]",
        "see_you_there": "¡Nos vemos allí!",
        "what_you_receive": "Lo Que Recibirás",
        "invitation": "Esta invitación",
        "character_sheet_full": "Una hoja de personaje con tu trasfondo completo y secretos",
        "portrait_if_enabled": "Tu retrato de personaje (si las imágenes están habilitadas)",
        # Character Sheet
        "character_sheet_title": "Hoja de Personaje",
        "your_character": "Tu Personaje",
        "personality_traits": "Rasgos de Personalidad",
        "backstory": "Historia",
        "public_description": "Descripción Pública",
        "personal_secrets": "Secretos Personales (¡Mantén Estos en Secreto!)",
        "personal_goals": "Objetivos Personales",
        "motive": "Motivo para el Crimen (Si Es Culpable)",
        "no_motive": "Sin motivo específico.",
        "costume": "Sugerencia de Vestuario",
        "no_costume": "Sin sugerencia específica de vestuario.",
        "act1_objectives": "Tus Objetivos del Acto 1",
        "no_objectives": "No se definieron objetivos.",
        "relation_to_victim": "Tu Relación con la Víctima",
        "relationships": "Relaciones con Otros Personajes",
        "remember_secrets": "¡Recuerda: usa tus secretos estratégicamente durante la investigación!",
        # Victim Sheet
        "victim_sheet_title": "Hoja de Personaje de la Víctima",
        "host_act1_role": "Tu Rol en el Acto 1",
        "important_note": "Nota Importante",
        "died_before_act2": "Este personaje murió antes de la investigación. NO jugarás este rol durante el Acto 2.",
        "embody_character": "Encarna la personalidad y secretos de este personaje",
        "create_tension": "Crea tensión e intriga con los sospechosos",
        "follow_timing": "Sigue la guía del anfitrión para el momento del asesinato",
        # Detective Sheet
        "detective_sheet_title": "Hoja de Personaje del Detective",
        "host_act2_role": "Tu Rol en el Acto 2: El Detective",
        "clues_to_reveal": "Pistas para Revelar Durante la Investigación",
        "how_to_interpret": "Cómo Interpretar",
        "final_solution": "Solución Final (La Gran Revelación)",
        "solution_timing": "Cuando los jugadores estén listos para la solución (o se acabe el tiempo):",
        "see_host_guide": "📄 Ver la guía del anfitrión para la referencia completa de pistas y estrategia de investigación detallada.",
        # Clue Reference
        "clue_reference_title": "Referencia de Pistas (Solo Anfitrión)",
        "clue_overview": "Resumen",
        "total_clues": "Total de pistas",
        "host_only_warning": "Este documento contiene información de spoilers sobre qué pistas incriminan/exoneran a los sospechosos. NO compartir con los jugadores.",
        "players_get_clean": "Los jugadores recibirán versiones limpias de las pistas sin los metadatos.",
        # General
        "no_image": "No hay imagen del personaje disponible.",
    },
}

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


def get_document_labels(language: str) -> dict[str, str]:
    """
    Get translated labels for document templates.

    Args:
        language: Language code (e.g., "en", "es")

    Returns:
        Dictionary mapping label keys to translated strings
    """
    return DOCUMENT_LABELS.get(language, DOCUMENT_LABELS[LANG_CODE_ENGLISH])


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


def translate_epoch(epoch: str, language: str) -> str:
    """
    Translate standard epoch names to target language.

    Args:
        epoch: Epoch identifier (e.g., "modern", "1920s", "Victorian", "custom")
        language: Target language code

    Returns:
        Translated epoch name
    """
    labels = get_document_labels(language)
    epoch_lower = epoch.lower()

    # Map epoch values to label keys
    epoch_mapping = {
        "modern": "epoch_modern",
        "1920s": "epoch_1920s",
        "victorian": "epoch_victorian",
        "custom": "epoch_custom",
    }

    label_key = epoch_mapping.get(epoch_lower)
    if label_key and label_key in labels:
        return labels[label_key]

    # Return original if no translation found
    return epoch


# Common room name translations (Spanish only for now)
ROOM_TRANSLATIONS_ES = {
    "study": "Estudio",
    "library": "Biblioteca",
    "dining_room": "Comedor",
    "drawing_room": "Sala de estar",
    "lounge": "Salón",
    "bedroom": "Dormitorio",
    "master_bedroom": "Dormitorio principal",
    "kitchen": "Cocina",
    "parlor": "Sala",
    "ballroom": "Salón de baile",
    "conservatory": "Invernadero",
    "billiard_room": "Sala de billar",
    "wine_cellar": "Bodega",
    "gallery": "Galería",
    "terrace": "Terraza",
    "garden": "Jardín",
    "veranda": "Veranda",
    "office": "Oficina",
    "deck": "Cubierta",
    "cabin": "Camarote",
    "suite": "Suite",
    "captains_quarters": "Camarote del capitán",
    "main_deck": "Cubierta principal",
    "observation_deck": "Cubierta de observación",
    "bar": "Bar",
    "restaurant": "Restaurante",
    "spa": "Spa",
    "pool": "Piscina",
    "gym": "Gimnasio",
}


def translate_room_name(room_id: str | None, language: str) -> str:
    """
    Translate room identifier to human-readable name in target language.

    Args:
        room_id: Room identifier (e.g., "study", "dining_room")
        language: Target language code

    Returns:
        Translated room name or formatted original
    """
    if not room_id:
        return get_document_labels(language)["unknown"]

    # For Spanish, use translation dictionary
    if language == LANG_CODE_SPANISH and room_id in ROOM_TRANSLATIONS_ES:
        return ROOM_TRANSLATIONS_ES[room_id]

    # For English or unknown rooms, format nicely: "captains_quarters" -> "Captains Quarters"
    return room_id.replace("_", " ").title()
