from __future__ import annotations


def test_health_check(client):
    """Assert GET /health returns 200 with status ok."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert "x-request-id" in res.headers


def test_readyz_success(client):
    """Assert GET /readyz returns 200 when all dependencies are ready."""
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json() == {"status": "ready", "stadium_ready": True, "llm_ready": True}


def test_readyz_stadium_failure(make_client):
    """Assert GET /readyz returns 503 when stadium data load fails."""
    cli = make_client()
    cli.app.state.stadium = None
    res = cli.get("/readyz")
    assert res.status_code == 503
    assert res.json() == {"status": "not_ready", "stadium_ready": False, "llm_ready": True}


def test_readyz_llm_failure(make_client):
    """Assert GET /readyz returns 503 when LLM service is unavailable."""
    cli = make_client()
    cli.app.state.llm = None
    res = cli.get("/readyz")
    assert res.status_code == 503
    assert res.json() == {"status": "not_ready", "stadium_ready": True, "llm_ready": False}
