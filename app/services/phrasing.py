from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

_DEFAULT_LANG = "en"

_MEANS: dict[str, dict[str, str]] = {
    "en": {"walk": "walk", "ramp": "take the ramp", "elevator": "take the elevator",
           "stairs": "take the stairs"},
    "es": {"walk": "camine", "ramp": "tome la rampa", "elevator": "tome el ascensor",
           "stairs": "suba por las escaleras"},
    "fr": {"walk": "marchez", "ramp": "empruntez la rampe", "elevator": "prenez l'ascenseur",
           "stairs": "prenez les escaliers"},
}

_CROWD_WORD: dict[str, dict[str, str]] = {
    "en": {"low": "low", "medium": "moderate", "high": "high"},
    "es": {"low": "baja", "medium": "moderada", "high": "alta"},
    "fr": {"low": "faible", "medium": "modérée", "high": "élevée"},
}

_TYPE_LABEL: dict[str, dict[str, str]] = {
    "en": {"restroom": "restroom", "accessible_restroom": "accessible restroom",
           "first_aid": "first aid station", "concession": "concession",
           "guest_services": "guest services desk", "water": "water refill point",
           "sensory_room": "sensory room", "exit": "exit", "gate": "gate",
           "seat": "seat", "elevator": "elevator"},
    "es": {"restroom": "aseo", "accessible_restroom": "aseo accesible",
           "first_aid": "puesto de primeros auxilios", "concession": "puesto de comida",
           "guest_services": "punto de atención", "water": "fuente de agua",
           "sensory_room": "sala sensorial", "exit": "salida", "gate": "puerta",
           "seat": "asiento", "elevator": "ascensor"},
    "fr": {"restroom": "toilettes", "accessible_restroom": "toilettes accessibles",
           "first_aid": "poste de premiers secours", "concession": "point de restauration",
           "guest_services": "comptoir d'accueil", "water": "point d'eau",
           "sensory_room": "salle sensorielle", "exit": "sortie", "gate": "porte",
           "seat": "place", "elevator": "ascenseur"},
}

_STEP: dict[str, dict[str, str]] = {
    "en": {"final": "{verb} to {to}, where you'll find {name}{lm}.", "mid": "{verb} to {to}."},
    "es": {"final": "{verb} hasta {to}, donde encontrará {name}{lm}.", "mid": "{verb} hasta {to}."},
    "fr": {"final": "{verb} jusqu'à {to}, où se trouve {name}{lm}.", "mid": "{verb} jusqu'à {to}."},
}

_ALT_NOTE: dict[str, str] = {
    "en": "A closer {label} was crowded, so a quieter one is suggested.",
    "es": "Un {label} más cercano estaba muy concurrido; se sugiere una opción más tranquila.",
    "fr": "Un(e) {label} plus proche était bondé(e) : une option plus calme est proposée.",
}

_URGENCY: dict[str, str] = {
    "en": "Kickoff in under 15 minutes — please hurry.",
    "es": "El partido comienza en menos de 15 minutos: dese prisa.",
    "fr": "Coup d'envoi dans moins de 15 minutes — dépêchez-vous.",
}

_ANSWER: dict[str, dict[str, str]] = {
    "en": {
        "dest": "Your destination is {name}{lm}.",
        "here": "You're already at this location.",
        "route": "Follow the {n}-step route below (about {d} m).",
        "crowd": "Crowd level there is currently {c}.",
        "landmark": "These directions use landmarks and are optimized for screen readers.",
        "captioned": "Look for visual signage on the way; a quiet Sensory Room is available if you need it.",
        "hurry": "Kickoff is very soon — please head there quickly.",
    },
    "es": {
        "dest": "Su destino es {name}{lm}.",
        "here": "Ya se encuentra en este lugar.",
        "route": "Siga la ruta de abajo en {n} paso(s) (unos {d} m).",
        "crowd": "La afluencia allí es actualmente {c}.",
        "landmark": "Estas indicaciones se basan en puntos de referencia y están optimizadas para lectores de pantalla.",
        "captioned": "Busque la señalización visual por el camino; hay una sala sensorial tranquila disponible si la necesita.",
        "hurry": "El partido está a punto de comenzar: diríjase allí rápidamente.",
    },
    "fr": {
        "dest": "Votre destination est {name}{lm}.",
        "here": "Vous y êtes déjà.",
        "route": "Suivez l'itinéraire ci-dessous en {n} étape(s) (environ {d} m).",
        "crowd": "L'affluence sur place est actuellement {c}.",
        "landmark": "Ces indications s'appuient sur des points de repère et sont optimisées pour les lecteurs d'écran.",
        "captioned": "Repérez la signalétique visuelle en chemin ; une salle sensorielle calme est disponible au besoin.",
        "hurry": "Le coup d'envoi est imminent — rendez-vous-y rapidement.",
    },
}

_STAFF_ANSWER: dict[str, dict[str, str]] = {
    "en": {
        "report_ok": "Incident logged successfully (ID: {id}).",
        "dispatch": "Action Plan: Dispatch {team} to {zone}. Description: {desc}.",
        "spill": "Clean-up Crew",
        "congestion": "Crowd Control Team",
        "maintenance": "Facilities Maintenance",
        "medical": "First Aid Responders",
    },
    "es": {
        "report_ok": "Incidente registrado con éxito (ID: {id}).",
        "dispatch": "Plan de acción: Enviar a {team} a {zone}. Descripción: {desc}.",
        "spill": "Equipo de Limpieza",
        "congestion": "Equipo de Control de Afluencia",
        "maintenance": "Mantenimiento de Instalaciones",
        "medical": "Socorristas de Primeros Auxilios",
    },
    "fr": {
        "report_ok": "Incident enregistré avec succès (ID: {id}).",
        "dispatch": "Plan d'action : Dépêcher {team} à {zone}. Description : {desc}.",
        "spill": "Équipe de Nettoyage",
        "congestion": "Équipe de Régulation des Foules",
        "maintenance": "Service de Maintenance",
        "medical": "Secouristes Médicaux",
    }
}


def _lang(language: str) -> str:
    """Normalize language code to supported set, defaulting to English.

    Args:
        language: Input language code (e.g. 'es').

    Returns:
        str: Supported language code.
    """
    return language if language in _MEANS else _DEFAULT_LANG


def _cap(text: str) -> str:
    """Capitalize only the first letter of the string (leaving other case as-is).

    Args:
        text: Input string.

    Returns:
        str: Capitalized string.
    """
    return text[:1].upper() + text[1:] if text else text


def type_label(facility_type: str, language: str) -> str:
    """Get the localized label name for a facility category.

    Args:
        facility_type: The type string (e.g., 'restroom').
        language: Target language code.

    Returns:
        str: Localized label name.
    """
    lang = _lang(language)
    return _TYPE_LABEL[lang].get(facility_type, facility_type.replace("_", " "))


def step_instruction(
    means: str,
    to_name: str,
    landmark: str | None,
    *,
    is_final: bool,
    facility_name: str,
    language: str,
) -> str:
    """Build a localized, formatted step instruction for routing directions.

    Args:
        means: The mode of transit (e.g., 'elevator').
        to_name: The destination zone name.
        landmark: The landmark direction hint for the zone, if any.
        is_final: True if this is the final step in the path.
        facility_name: The target facility name.
        language: Target language code.

    Returns:
        str: Formatted instruction sentence.
    """
    lang = _lang(language)
    verb = _cap(_MEANS[lang].get(means, _MEANS[lang]["walk"]))
    lm = f" ({landmark})" if (is_final and landmark) else ""
    template = _STEP[lang]["final" if is_final else "mid"]
    return template.format(verb=verb, to=to_name, name=facility_name, lm=lm)


def alternatives_note(facility_type: str, language: str) -> str:
    """Generate a localized warning explaining that a congested option was bypassed.

    Args:
        facility_type: Bypassed facility category.
        language: Target language code.

    Returns:
        str: Alert sentence.
    """
    lang = _lang(language)
    return _ALT_NOTE[lang].format(label=type_label(facility_type, lang))


def urgency_note(language: str) -> str:
    """Get the localized pre-kickoff urgency warning.

    Args:
        language: Target language code.

    Returns:
        str: Warning message.
    """
    return _URGENCY[_lang(language)]


@dataclass(frozen=True)
class PhrasingContext:
    """Dataclass holding resolved navigation stats and incident states.

    Used by phrasing engines to render localized natural-language sentences.

    Attributes:
        language: Language code ('en'/'es'/'fr').
        facility_name: Name of target facility.
        facility_type: Category type of target facility.
        facility_landmark: Optional landmark hint text.
        crowd_level: Resolved crowd index ('low'/'medium'/'high').
        accessibility_mode: Mode code ('standard'/'screen_reader'/'captioned').
        landmark_based: True if landmark hints are active.
        hurry: True if kickoff is imminent.
        alternative_type: Optional bypassed facility type.
        total_distance: Total distance in meters.
        step_count: Number of edges in computed route.
        persona: User persona ('fan' or 'staff').
        incident_id: Tracking ID of logged incident.
        incident_type: Incident hazard category.
        incident_desc: Staff-logged descriptive text.
    """
    language: str
    facility_name: str
    facility_type: str
    facility_landmark: str | None
    crowd_level: str
    accessibility_mode: str
    landmark_based: bool
    hurry: bool
    alternative_type: str | None
    total_distance: int
    step_count: int
    persona: str = "fan"
    incident_id: str | None = None
    incident_type: str | None = None
    incident_desc: str | None = None


@lru_cache(maxsize=256)
def render_answer(ctx: PhrasingContext) -> str:
    """Grounded offline text generation that matches the PhrasingContext details.

    Used to short-circuit simple wayfinding calls (saving LLM token billing)
    and to serve as the baseline template context for LLM rephrasing prompts.

    Args:
        ctx: Resolved context fields.

    Returns:
        str: Formatted paragraphs of instructions.
    """
    lang = _lang(ctx.language)

    if ctx.persona == "staff" and ctx.incident_id:
        staff_a = _STAFF_ANSWER[lang]
        report_msg = staff_a["report_ok"].format(id=ctx.incident_id)
        team_key = ctx.incident_type or "maintenance"
        team = staff_a.get(team_key, staff_a["maintenance"])
        dispatch_msg = staff_a["dispatch"].format(
            team=team,
            zone=ctx.facility_name,
            desc=ctx.incident_desc or ""
        )
        return f"{report_msg} {dispatch_msg}"

    a = _ANSWER[lang]
    crowd = _CROWD_WORD[lang][ctx.crowd_level]
    dest_lm = f" ({ctx.facility_landmark})" if ctx.facility_landmark else ""

    parts = [a["dest"].format(name=ctx.facility_name, lm=dest_lm)]
    if ctx.step_count == 0:
        parts.append(a["here"])
    else:
        parts.append(a["route"].format(n=ctx.step_count, d=ctx.total_distance))
    parts.append(a["crowd"].format(c=crowd))

    if ctx.alternative_type:
        parts.append(alternatives_note(ctx.alternative_type, lang))
    if ctx.landmark_based:
        parts.append(a["landmark"])
    if ctx.accessibility_mode == "captioned":
        parts.append(a["captioned"])
    if ctx.hurry:
        parts.append(a["hurry"])

    return " ".join(parts)
