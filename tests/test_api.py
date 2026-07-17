from __future__ import annotations

import pytest


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_stadium_metadata_endpoint(client):
    res = client.get("/api/stadium")
    assert res.status_code == 200
    data = res.json()
    assert data["stadium"]["name"] == "MetLife Stadium"
    assert len(data["zones"]) > 0
    assert len(data["facilities"]) > 0
    assert "restroom" in data["intents"]
    assert "en" in data["languages"]


def test_assist_endpoint_happy_path(client, base_payload):
    res = client.post("/api/assist", json=base_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["used_llm"] is False
    assert "route_steps" in data
    assert len(data["route_steps"]) > 0
    assert "facility" in data
    assert data["language"] == "en"


def test_assist_endpoint_validation_error(client, base_payload):
    # Invalid zone code
    payload = dict(base_payload, current_location="invalid;zone")
    res = client.post("/api/assist", json=payload)
    assert res.status_code == 422


def test_assist_stream_endpoint_no_question(client, base_payload):
    res = client.post("/api/assist/stream", json=base_payload)
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]
    
    # Read response text
    body = res.text
    assert "event: result" in body
    assert "data: " in body


def test_assist_stream_endpoint_with_question(client, base_payload):
    payload = dict(base_payload, question="Which direction?")
    res = client.post("/api/assist/stream", json=payload)
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]

    body = res.text
    # Should yield metadata event first, then token, then result
    assert "event: metadata" in body
    assert "event: token" in body
    assert "event: result" in body


def test_incidents_api_endpoints(client):
    # Fetch initial incidents (empty)
    res_list1 = client.get("/api/incidents")
    assert res_list1.status_code == 200
    assert res_list1.json() == []

    # Report an incident via assist endpoint using staff persona
    staff_payload = {
        "persona": "staff",
        "language": "en",
        "current_location": "concourse_lower_sw",
        "destination_intent": "first_aid",
        "accessibility_needs": [],
        "ticket_section": None,
        "minutes_to_kickoff": 20,
        "question": None,
        "incident_report": "Heavy crowd congestion",
        "reported_issue_type": "congestion"
    }
    
    res_report = client.post("/api/assist", json=staff_payload)
    assert res_report.status_code == 200
    inc_id = res_report.json()["incident_action_logged"]
    assert inc_id is not None

    # Fetch active incidents (should have 1 item)
    res_list2 = client.get("/api/incidents")
    assert res_list2.status_code == 200
    data = res_list2.json()
    assert len(data) == 1
    assert data[0]["id"] == inc_id
    assert data[0]["resolved"] is False

    # Resolve incident
    res_resolve = client.post(f"/api/incidents/{inc_id}/resolve")
    assert res_resolve.status_code == 200
    assert res_resolve.json() == {"status": "resolved"}

    # Fetch incidents again (resolved should be True)
    res_list3 = client.get("/api/incidents")
    assert res_list3.json()[0]["resolved"] is True


def test_resolve_incident_not_found(client):
    res = client.post("/api/incidents/inc_nonexistent/resolve")
    assert res.status_code == 404


def test_index_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]


def test_assist_endpoint_route_not_found(client):
    # Log an incident of type spill at concourse_lower_sw, which blocks it
    from app.services.incidents import get_incident_manager
    get_incident_manager().report_incident("concourse_lower_sw", "spill", "Spill incident")

    payload = {
        "persona": "fan",
        "language": "en",
        "current_location": "concourse_lower_sw",
        "destination_intent": "restroom",
        "accessibility_needs": [],
        "ticket_section": None,
        "minutes_to_kickoff": 20,
        "question": None
    }
    res = client.post("/api/assist", json=payload)
    assert res.status_code == 404
