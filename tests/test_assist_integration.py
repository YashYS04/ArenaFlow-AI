from __future__ import annotations

import json


def test_assist_e2e_offline_mock_llm(client, base_payload):
    """End-to-end integration test asserting offline deterministic assist works with zero API keys."""
    payload = dict(
        base_payload,
        current_location="gate_a",
        destination_intent="seat",
        ticket_section="101",
        minutes_to_kickoff=30,
        question="How do I navigate to my seat?",
    )
    res = client.post("/api/assist", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["used_llm"] is False
    assert data["language"] == "en"
    assert data["facility"]["type"] == "seat"
    assert len(data["route_steps"]) >= 2
    for step in data["route_steps"]:
        assert step["from_zone"]
        assert step["to_zone"]
        assert step["instruction"]
    assert "Your destination is" in data["answer"]


def test_assist_stream_e2e_offline_tokens(client, base_payload):
    """End-to-end SSE integration test asserting offline MockLLM streams tokens properly."""
    payload = dict(
        base_payload,
        current_location="concourse_lower_sw",
        destination_intent="first_aid",
        question="Where is the nearest first aid station?",
    )
    res = client.post("/api/assist/stream", json=payload)
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]

    body = res.text
    assert "event: metadata\ndata: " in body
    assert "event: token\ndata: " in body
    assert "event: result\ndata: " in body

    # Parse metadata and result json
    events = body.split("\n\n")
    result_event = next(e for e in events if e.startswith("event: result"))
    result_json_str = result_event.replace("event: result\ndata: ", "").strip()
    result_data = json.loads(result_json_str)

    assert result_data["facility"]["type"] == "first_aid"
    assert len(result_data["route_steps"]) > 0


def test_assist_stream_step_free_wheelchair_e2e(client, base_payload):
    """End-to-end integration test ensuring wheelchair constraints enforce 100% step-free routing."""
    payload = dict(
        base_payload,
        current_location="gate_a",
        destination_intent="restroom",
        accessibility_needs=["wheelchair"],
        question="Accessible path to restroom please",
    )
    res = client.post("/api/assist/stream", json=payload)
    assert res.status_code == 200

    body = res.text
    events = body.split("\n\n")
    result_event = next(e for e in events if e.startswith("event: result"))
    result_json_str = result_event.replace("event: result\ndata: ", "").strip()
    result_data = json.loads(result_json_str)

    assert all(step["step_free"] is True for step in result_data["route_steps"])
