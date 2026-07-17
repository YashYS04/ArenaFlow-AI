from __future__ import annotations

from app.services.phrasing import (
    PhrasingContext,
    alternatives_note,
    render_answer,
    step_instruction,
    type_label,
    urgency_note,
)


def test_type_labels():
    assert type_label("restroom", "en") == "restroom"
    assert type_label("restroom", "es") == "aseo"
    assert type_label("restroom", "fr") == "toilettes"
    # Unknown type should fallback gracefully
    assert type_label("unknown_type", "en") == "unknown type"


def test_step_instructions():
    # English
    en_step = step_instruction("walk", "Gate A", "landmark", is_final=True, facility_name="Restroom", language="en")
    assert "Walk to Gate A" in en_step
    assert "landmark" in en_step

    # Spanish
    es_step = step_instruction("elevator", "Piso 1", None, is_final=False, facility_name="Aseo", language="es")
    assert "Tome el ascensor hasta Piso 1" in es_step

    # French
    fr_step = step_instruction("stairs", "Étage 2", None, is_final=False, facility_name="Toilettes", language="fr")
    assert "Prenez les escaliers jusqu'à Étage 2" in fr_step


def test_alternatives_notes():
    assert "crowded" in alternatives_note("restroom", "en")
    assert "concurrido" in alternatives_note("restroom", "es")
    assert "bondé" in alternatives_note("restroom", "fr")


def test_urgency_notes():
    assert "hurry" in urgency_note("en")
    assert "prisa" in urgency_note("es")
    assert "dépêchez-vous" in urgency_note("fr")


def test_render_answer_fan():
    # Simple destination reach, 0 steps
    ctx_here = PhrasingContext(
        language="en",
        facility_name="Restroom",
        facility_type="restroom",
        facility_landmark=None,
        crowd_level="low",
        accessibility_mode="standard",
        landmark_based=False,
        hurry=False,
        alternative_type=None,
        total_distance=0,
        step_count=0,
    )
    ans_here = render_answer(ctx_here)
    assert "Your destination is Restroom" in ans_here
    assert "already at this location" in ans_here
    assert "currently low" in ans_here

    # Full route steps, with alternatives note, screen reader & captioned access modes
    ctx_route = PhrasingContext(
        language="es",
        facility_name="Aseos Accesibles",
        facility_type="accessible_restroom",
        facility_landmark="el ascensor",
        crowd_level="high",
        accessibility_mode="captioned",
        landmark_based=True,
        hurry=True,
        alternative_type="restroom",
        total_distance=120,
        step_count=3,
    )
    ans_route = render_answer(ctx_route)
    assert "Aseos Accesibles" in ans_route
    assert "el ascensor" in ans_route
    assert "Siga la ruta de abajo" in ans_route
    assert "lectores de pantalla" in ans_route
    assert "sala sensorial" in ans_route
    assert "partido está a punto de comenzar" in ans_route
    assert "concurrido" in ans_route


def test_render_answer_staff():
    ctx_staff = PhrasingContext(
        language="en",
        facility_name="Gate A",
        facility_type="gate",
        facility_landmark=None,
        crowd_level="low",
        accessibility_mode="standard",
        landmark_based=False,
        hurry=False,
        alternative_type=None,
        total_distance=0,
        step_count=0,
        persona="staff",
        incident_id="inc_123",
        incident_type="spill",
        incident_desc="Drink spill",
    )
    ans_staff = render_answer(ctx_staff)
    assert "Incident logged successfully (ID: inc_123)" in ans_staff
    assert "Dispatch Clean-up Crew to Gate A" in ans_staff
    assert "Drink spill" in ans_staff
