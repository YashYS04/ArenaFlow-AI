from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Persona(str, Enum):
    fan = "fan"
    staff = "staff"


class Language(str, Enum):
    en = "en"
    es = "es"
    fr = "fr"


class AccessibilityNeed(str, Enum):
    wheelchair = "wheelchair"
    visual = "visual"
    hearing = "hearing"


class AccessibilityMode(str, Enum):
    standard = "standard"
    screen_reader = "screen_reader"
    captioned = "captioned"


class DestinationIntent(str, Enum):
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
    low = "low"
    medium = "medium"
    high = "high"


class UserContext(BaseModel):
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
        if not isinstance(v, list):
            return v
        return list(dict.fromkeys(v))


class FacilityInfo(BaseModel):
    id: str
    name: str
    type: str
    zone: str
    accessible: bool
    landmark: str | None


class RouteStep(BaseModel):
    order: int
    from_zone: str
    to_zone: str
    means: str
    step_free: bool
    distance: int
    landmark: str | None
    instruction: str


class AssistResponse(BaseModel):
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
    status: str
