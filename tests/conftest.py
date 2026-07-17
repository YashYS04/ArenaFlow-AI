from __future__ import annotations

from collections.abc import Callable
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.services.incidents import get_incident_manager


def _settings(**overrides) -> Settings:
    params = {
        "gemini_api_key": None,  # Always fallback to MockLLM in tests
        "rate_limit_capacity": 1000,
        "rate_limit_refill_per_sec": 1000.0,
        "allowed_origins": ["http://testserver"],
    }
    params.update(overrides)
    return Settings(**params)


@pytest.fixture
def settings() -> Settings:
    return _settings()


@pytest.fixture
def client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings))


@pytest.fixture
def make_client() -> Callable[..., TestClient]:
    """Factory to build a TestClient with custom settings (e.g. rate limit bounds)."""
    def _make(**overrides) -> TestClient:
        return TestClient(create_app(_settings(**overrides)))
    return _make


@pytest.fixture
def base_payload() -> dict:
    """A minimal valid UserContext payload for testing."""
    return {
        "persona": "fan",
        "language": "en",
        "current_location": "concourse_lower_sw",
        "destination_intent": "restroom",
        "accessibility_needs": [],
        "ticket_section": None,
        "minutes_to_kickoff": 20,
        "question": None
    }


@pytest.fixture(autouse=True)
def reset_incidents():
    """Autouse fixture to reset the IncidentManager before each test case."""
    get_incident_manager().reset()
