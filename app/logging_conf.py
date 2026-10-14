"""Structured logging configuration module.

Provides a unified JSON logging formatter for production observability,
structured diagnostics, and log aggregation systems.
"""

from __future__ import annotations

import logging
import sys

from pythonjsonlogger import jsonlogger


class StructuredJsonFormatter(logging.Formatter):
    """Custom JSON formatter ensuring standard schema for all log records."""

    def __init__(self, fmt: str | None = None, datefmt: str | None = None) -> None:
        """Initialize the JSON formatter with baseline field format string.

        Args:
            fmt: Optional log format template.
            datefmt: Optional timestamp formatting string.
        """
        super().__init__(fmt=fmt, datefmt=datefmt)
        self._impl = jsonlogger.JsonFormatter(  # type: ignore[attr-defined]
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format log record into structured JSON representation.

        Args:
            record: The logging LogRecord to serialize.

        Returns:
            str: JSON-encoded log line.
        """
        return self._impl.format(record)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logger to output structured JSON formatted logs.

    Args:
        level: Minimum logging level (defaults to INFO).
    """
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredJsonFormatter())
    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Retrieve or initialize a logger instance with structured JSON configuration.

    Args:
        name: Logger name namespace.

    Returns:
        logging.Logger: Configured logger.
    """
    configure_logging()
    return logging.getLogger(name)
