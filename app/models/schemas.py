from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Persona(str, Enum):
    """User profile persona categorizing target query intentions.

    Attributes:
        fan: General public guest seeking navigation help.
        staff: Stadium crew/volunteer reporting incidents and dispatch tasks.
    """
    fan = "fan"
    staff = "staff"


class Language(str, Enum):
    """Supported translation locales.

    Attributes:
        en: English.
        es: Spanish.
        fr: French.
    """
    en = "en"
    es = "es"
    fr = "fr"


class AccessibilityNeed(str, Enum):
    """User-declared structural or interface accessibility requirements.

    Attributes:
        wheelchair: Requires step-free routes (ramps/elevators, no stairs).
        visual: Optimized for screen readers, enabling landmark directions.
        hearing: Optimized with captioned visual alerts.
    """
    wheelchair = "wheelchair"
    visual = "visual"
    hearing = "hearing"


class AccessibilityMode(str, Enum):
    """Resolved interface adjustment options.

    Attributes:
        standard: Regular GUI routing details.
        screen_reader: Voice-compatible navigation descriptions.
        captioned: Enhanced visual cues and quiet areas lookup.
    """
    standard = "standard"
    screen_reader = "screen_reader"
    captioned = "captioned"


class DestinationIntent(str, Enum):
    """Identified category of target destination.

    Attributes:
        restroom: Restrooms and washrooms.
        first_aid: Medical and safety assistance zones.
        concession: Food, beverage, and dining stalls.
        guest_services: Help and volunteer services desks.
        water: Drinking fountain and refill points.
        sensory_room: Quiet sensory chambers.
        exit: Arena exit gate or concourse exit.
        gate: Metro and exterior entry gate.
        seat: Resolved seat block.
    """
    restroom = "restroom"
    first_aid = "first_aid"
    concession = "concession"
    guest_services = "guest_services"
    water = "water"
    sensory_room = "sensory_room"
    exit = "exit"
    gate = "gate"
    seat = "seat"


class CrowdLevel(str, Enum):
    """Estimated crowd concentration index.

    Attributes:
        low: Low congestion.
        medium: Moderate wait times (1.5x routing cost).
        high: Overcrowded (3.0x routing cost, triggers swaps).
    """
    low = "low"
    medium = "medium"
    high = "high"


class UserContext(BaseModel):
    """Incoming user metadata payload for the wayfinding engine.

    Attributes:
        persona: Active role persona.
        language: Output translation language.
        current_location: The active starting zone ID.
        destination_intent: Category of target amenity/zone.
        accessibility_needs: Declared structural requirements.
        ticket_section: Optional seat section string for fan seat routing.
        minutes_to_kickoff: Remaining pre-match minutes.
        question: Optional free-text LLM query.
        incident_report: Optional staff description of reported issues.
        reported_issue_type: Optional staff incident category type.
    """
    persona: Persona = Persona.fan
    language: Language = Language.en
    current_location: Annotated[str, Field(min_length=1, max_length=20, pattern=r"^[a-zA-Z0-9_\-]+$")]
    destination_intent: DestinationIntent
    accessibility_needs: list[AccessibilityNeed] = Field(default_factory=list)
    ticket_section: Annotated[str | None, Field(default=None, max_length=10, pattern=r"^[a-zA-Z0-9_\-]+$")] = None
    minutes_to_kickoff: Annotated[int, Field(ge=-120, le=1440)] = 20
    question: Annotated[str | None, Field(default=None, max_length=280)] = None
    incident_report: Annotated[str | None, Field(default=None, max_length=280)] = None
    reported_issue_type: Annotated[str | None, Field(default=None, max_length=50)] = None

    class Config:
        extra = "forbid"

    @field_validator("accessibility_needs", mode="before")
    @classmethod
    def unique_needs(cls, v: list[str]) -> list[str]:
        """Deduplicate accessibility items to prevent redundant rules application.

        Args:
            v: Raw user array.

        Returns:
            list[str]: Unique string elements.
        """
        if not isinstance(v, list):
            return v
        return list(dict.fromkeys(v))


class FacilityInfo(BaseModel):
    """Detailed target amenity descriptor returned to the client.

    Attributes:
        id: Facility identifier.
        name: Localized facility name.
        type: Category type.
        zone: Zone container ID.
        accessible: Accessible status.
        landmark: Optional descriptive landmark guidance note.
    """
    id: str
    name: str
    type: str
    zone: str
    accessible: bool
    landmark: str | None


class RouteStep(BaseModel):
    """Individual edge transition step for navigation displays.

    Attributes:
        order: Progression order index (1-based).
        from_zone: Origin zone ID.
        to_zone: Target destination zone ID.
        means: Way of movement (walk, ramp, elevator, stairs).
        step_free: True if step-free accessible.
        distance: Distance in meters.
        landmark: Optional localization landmark guidance hint.
        instruction: Natural language instruction text.
    """
    order: int
    from_zone: str
    to_zone: str
    means: str
    step_free: bool
    distance: int
    landmark: str | None
    instruction: str


class AssistResponse(BaseModel):
    """Aggregated response containing route steps and localized answers.

    Attributes:
        answer: Friendly, grounded response.
        route_steps: Ordered transition steps.
        facility: Chosen facility metadata.
        crowd_level: Target zone crowd index.
        language: Active language enum.
        accessibility_mode: Configured accessibility output mode.
        alternatives_note: Alert note if swapped due to congestion.
        urgency: Urgency warning if kickoff is close.
        used_llm: True if generative rephrasing was invoked.
        incident_action_logged: Alphanumeric tracking ID if an incident was logged.
    """
    answer: str
    route_steps: list[RouteStep]
    facility: FacilityInfo
    crowd_level: CrowdLevel
    language: Language
    accessibility_mode: AccessibilityMode
    alternatives_note: str | None
    urgency: str | None
    used_llm: bool
    incident_action_logged: str | None = None


class HealthResponse(BaseModel):
    """Basic service aliveness status response.

    Attributes:
        status: The server status string (e.g. 'ok').
    """
    status: str
