from __future__ import annotations

import json
import logging

from app.logging_conf import StructuredJsonFormatter, configure_logging, get_logger


def test_structured_json_formatter():
    formatter = StructuredJsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Sample log message",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-12345"  # type: ignore[attr-defined]
    record.status_code = 200  # type: ignore[attr-defined]

    output = formatter.format(record)
    parsed = json.loads(output)

    assert parsed["name"] == "test_logger"
    assert parsed["levelname"] == "INFO"
    assert parsed["message"] == "Sample log message"
    assert parsed["request_id"] == "req-12345"
    assert parsed["status_code"] == 200
    assert "asctime" in parsed


def test_configure_logging_when_empty_handlers():
    root = logging.getLogger()
    saved_handlers = list(root.handlers)
    try:
        root.handlers.clear()
        configure_logging(level=logging.DEBUG)
        assert len(root.handlers) == 1
        assert isinstance(root.handlers[0].formatter, StructuredJsonFormatter)
        assert root.level == logging.DEBUG

        # Calling again when handlers exist should return early
        configure_logging(level=logging.INFO)
        assert len(root.handlers) == 1
    finally:
        root.handlers = saved_handlers


def test_get_logger():
    logger = get_logger("custom.service")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "custom.service"
