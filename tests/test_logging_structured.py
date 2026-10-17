from __future__ import annotations

import json
import logging

from app.logging_conf import StructuredJsonFormatter


def test_structured_log_record_contains_expected_json_keys():
    """Assert that structured JSON logs contain all telemetry and request tracking keys."""
    formatter = StructuredJsonFormatter()
    record = logging.LogRecord(
        name="arenaflow.test",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Sample structured event",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-test-uuid-42"  # type: ignore[attr-defined]
    record.status_code = 200  # type: ignore[attr-defined]
    record.path = "/api/assist"  # type: ignore[attr-defined]
    record.duration_ms = 4.25  # type: ignore[attr-defined]

    formatted_line = formatter.format(record)
    parsed = json.loads(formatted_line)

    expected_keys = {
        "asctime",
        "levelname",
        "name",
        "message",
        "request_id",
        "status_code",
        "path",
        "duration_ms",
    }
    for key in expected_keys:
        assert key in parsed, f"Missing expected structured log key: {key}"

    assert parsed["request_id"] == "req-test-uuid-42"
    assert parsed["status_code"] == 200
    assert parsed["path"] == "/api/assist"


def test_unhandled_exception_handler_returns_structured_500():
    """Assert that unhandled exceptions are caught by the error tracking hook."""
    from fastapi.testclient import TestClient

    from app.config import Settings
    from app.main import create_app

    settings = Settings(
        gemini_api_key=None,
        rate_limit_capacity=1000,
        rate_limit_refill_per_sec=1000.0,
        allowed_origins=["http://testserver"],
    )
    app = create_app(settings)

    # Add a route that triggers an unhandled error to verify error-tracking hook
    @app.get("/test-error")
    async def _error_route():
        raise RuntimeError("Simulated crash for error tracking verification")

    client = TestClient(app, raise_server_exceptions=False)
    res = client.get("/test-error", headers={"X-Request-ID": "err-trace-123"})
    assert res.status_code == 500
    data = res.json()
    assert data["detail"] == "Internal Server Error"
    assert data["request_id"] == "err-trace-123"
    assert res.headers["x-request-id"] == "err-trace-123"
