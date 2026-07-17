from __future__ import annotations

import pytest

from app.models.schemas import (
    AccessibilityMode,
    UserContext,
)
from app.services.context_engine import RouteNotFound, build_decision, run_assist
from app.services.llm import MockLLM
from app.services.stadium_data import get_stadium


def test_build_decision_standard_fan(base_payload):
    stadium = get_stadium()
    ctx = UserContext(**base_payload)
    decision = build_decision(ctx, stadium)

    assert decision.language == "en"
    assert decision.accessibility_mode == AccessibilityMode.standard
    assert decision.landmark_based is False
    assert decision.hurry is False
    assert len(decision.route_steps) > 0


def test_build_decision_wheelchair_user(base_payload):
    stadium = get_stadium()
    payload = dict(base_payload, accessibility_needs=["wheelchair"])
    ctx = UserContext(**payload)
    decision = build_decision(ctx, stadium)

    assert decision.accessibility_mode == AccessibilityMode.standard
    assert all(step.step_free for step in decision.route_steps)


def test_build_decision_visual_user(base_payload):
    stadium = get_stadium()
    payload = dict(base_payload, accessibility_needs=["visual"])
    ctx = UserContext(**payload)
    decision = build_decision(ctx, stadium)

    assert decision.accessibility_mode == AccessibilityMode.screen_reader
    assert decision.landmark_based is True


def test_build_decision_hearing_user(base_payload):
    stadium = get_stadium()
    payload = dict(base_payload, accessibility_needs=["hearing"])
    ctx = UserContext(**payload)
    decision = build_decision(ctx, stadium)

    assert decision.accessibility_mode == AccessibilityMode.captioned


def test_build_decision_imminent_kickoff_urgency(base_payload):
    stadium = get_stadium()
    payload = dict(base_payload, minutes_to_kickoff=5, destination_intent="gate")
    ctx = UserContext(**payload)
    decision = build_decision(ctx, stadium)

    assert decision.hurry is True
    assert decision.urgency is not None


def test_build_decision_seat_resolution(base_payload):
    stadium = get_stadium()

    # Lower bowl seat section
    payload1 = dict(base_payload, destination_intent="seat", ticket_section="134")
    ctx1 = UserContext(**payload1)
    decision1 = build_decision(ctx1, stadium)
    assert decision1.facility.id == "seat_lower"

    # Upper bowl seat section
    payload2 = dict(base_payload, destination_intent="seat", ticket_section="320")
    ctx2 = UserContext(**payload2)
    decision2 = build_decision(ctx2, stadium)
    assert decision2.facility.id == "seat_upper"


def test_build_decision_facility_crowd_swap(base_payload):
    stadium = get_stadium()
    payload = dict(base_payload, destination_intent="concession", current_location="concourse_lower_sw")
    ctx = UserContext(**payload)
    decision = build_decision(ctx, stadium)

    assert decision.facility.id != "concession_sw"
    assert decision.alternatives_note is not None


def test_build_decision_unreachable_gate_due_to_blocks(base_payload):
    stadium = get_stadium()
    from app.services.incidents import get_incident_manager
    manager = get_incident_manager()

    # Block gates and concourses around lower concourse
    manager.report_incident("concourse_lower_sw", "spill", "spill details")
    manager.report_incident("concourse_lower_nw", "maintenance", "blocked stairs")
    manager.report_incident("concourse_lower_se", "spill", "maintenance spill")
    manager.report_incident("concourse_lower_ne", "maintenance", "blocked elevator")

    payload = dict(base_payload, destination_intent="seat", current_location="gate_a")
    ctx = UserContext(**payload)
    with pytest.raises(RouteNotFound):
        build_decision(ctx, stadium)


@pytest.mark.asyncio
async def test_run_assist_without_question(base_payload):
    stadium = get_stadium()
    ctx = UserContext(**base_payload)
    llm = MockLLM()
    response = await run_assist(ctx, stadium, llm)
    assert response.used_llm is False
    assert "Your destination is" in response.answer


@pytest.mark.asyncio
async def test_run_assist_async(base_payload):
    stadium = get_stadium()
    llm = MockLLM()

    # Short circuit (no question)
    ctx1 = UserContext(**base_payload)
    res1 = await run_assist(ctx1, stadium, llm)
    assert res1.used_llm is False
    assert "Your destination is" in res1.answer

    # Engagement (with question)
    payload = dict(base_payload, question="Where is it?")
    ctx2 = UserContext(**payload)
    res2 = await run_assist(ctx2, stadium, llm)
    assert res2.used_llm is False


def test_build_decision_unreachable_restroom_due_to_blocks(base_payload):
    stadium = get_stadium()
    from app.services.incidents import get_incident_manager
    manager = get_incident_manager()

    # Block SW concourse completely
    manager.report_incident("concourse_lower_sw", "spill", "spill details")
    manager.report_incident("concourse_lower_nw", "maintenance", "blocked stairs")
    manager.report_incident("concourse_lower_se", "spill", "maintenance spill")
    manager.report_incident("concourse_lower_ne", "maintenance", "blocked elevator")

    # Trying to route from concourse_lower_sw to restroom (which are in other zones)
    payload = dict(base_payload, destination_intent="restroom", current_location="concourse_lower_sw")
    ctx = UserContext(**payload)
    with pytest.raises(RouteNotFound):
        build_decision(ctx, stadium)
