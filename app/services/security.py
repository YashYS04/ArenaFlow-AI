from __future__ import annotations

import html
import re
import threading
import time

_WHITESPACE_RE = re.compile(r"\s+")


def sanitize_text(text: str, max_length: int = 280) -> str:
    """Neutralize free-text user input before it is logged or passed to the LLM.

    Strips control characters, collapses whitespace, HTML-escapes content to prevent
    XSS, and trims it to a safe length limit.
    """
    if not text:
        return ""
    # Strip control characters (chars below 0x20 and 0x7f DEL)
    cleaned = "".join(ch for ch in text if ord(ch) >= 32 and ord(ch) != 127)
    # Collapse multiple whitespaces/tabs
    cleaned = _WHITESPACE_RE.sub(" ", cleaned).strip()
    # Escape HTML to prevent XSS
    cleaned = html.escape(cleaned)
    # Cap length
    return cleaned[:max_length]


class RateLimiter:
    """Thread-safe in-memory token-bucket rate limiter, keyed per client.

    Each key starts with capacity tokens and refills at refill_per_sec
    tokens/second. Each allowed request consumes one token.
    """

    def __init__(self, capacity: int, refill_per_sec: float, max_entries: int = 10_000) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._capacity = float(capacity)
        self._refill = float(refill_per_sec)
        self._max_entries = max_entries
        self._buckets: dict[str, tuple[float, float]] = {}
        self._lock = threading.Lock()

    def _evict_idle(self) -> None:
        """Bound memory usage by dropping least-recently-seen IP buckets."""
        overflow = len(self._buckets) - self._max_entries
        if overflow <= 0:
            return
        # Sort by last-seen timestamp ascending (oldest first) and drop the overflow
        for key in sorted(self._buckets, key=lambda k: self._buckets[k][1])[:overflow]:
            del self._buckets[key]

    def check(self, key: str) -> tuple[bool, float]:
        """Attempt to consume a token for key.

        Returns (allowed, retry_after_seconds).
        """
        now = time.monotonic()
        with self._lock:
            tokens, last = self._buckets.get(key, (self._capacity, now))
            tokens = min(self._capacity, tokens + (now - last) * self._refill)
            if tokens >= 1.0:
                self._buckets[key] = (tokens - 1.0, now)
                allowed, retry_after = True, 0.0
            else:
                self._buckets[key] = (tokens, now)
                retry_after = (1.0 - tokens) / self._refill if self._refill > 0 else 60.0
                allowed = False
            self._evict_idle()
            return allowed, retry_after

    def reset(self) -> None:
        """Reset all buckets (primarily used in test isolation)."""
        with self._lock:
            self._buckets.clear()
