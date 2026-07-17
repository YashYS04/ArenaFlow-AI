from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.schemas import UserContext, Persona, Language, DestinationIntent


def test_valid_minimal_payload(base_payload):
    ctx = UserContext(**base_payload)
    assert ctx.persona == Persona.fan
    assert ctx.language == Language.en
    assert ctx.current_location == "concourse_lower_sw"
    assert ctx.destination_intent == DestinationIntent.restroom
    assert ctx.accessibility_needs == []
    assert ctx.minutes_to_kickoff == 20


def test_invalid_persona(base_payload):
    payload = dict(base_payload, persona="invalid_persona")
    with pytest.raises(ValidationError):
        UserContext(**payload)


def test_invalid_language(base_payload):
    payload = dict(base_payload, language="invalid_lang")
    with pytest.raises(ValidationError):
        UserContext(**payload)


def test_invalid_current_location(base_payload):
    # Location cannot be empty
    payload1 = dict(base_payload, current_location="")
    with pytest.raises(ValidationError):
        UserContext(**payload1)

    # Location cannot have special characters (except _, -)
    payload2 = dict(base_payload, current_location="gate;a")
    with pytest.raises(ValidationError):
        UserContext(**payload2)


def test_invalid_minutes_to_kickoff(base_payload):
    # Too small
    payload1 = dict(base_payload, minutes_to_kickoff=-200)
    with pytest.raises(ValidationError):
        UserContext(**payload1)

    # Too large
    payload2 = dict(base_payload, minutes_to_kickoff=2000)
    with pytest.raises(ValidationError):
        UserContext(**payload2)


def test_invalid_extra_field(base_payload):
    payload = dict(base_payload, hack_attempt="malicious_payload")
    with pytest.raises(ValidationError):
        UserContext(**payload)


def test_accessibility_needs_uniquification(base_payload):
    payload = dict(base_payload, accessibility_needs=["wheelchair", "wheelchair", "visual"])
    ctx = UserContext(**payload)
    assert ctx.accessibility_needs == ["wheelchair", "visual"]


def test_accessibility_needs_non_list_type(base_payload):
    payload = dict(base_payload, accessibility_needs="not_a_list")
    with pytest.raises(ValidationError):
        UserContext(**payload)
