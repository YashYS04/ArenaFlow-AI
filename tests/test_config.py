from __future__ import annotations

import json
from app.config import Settings


def test_config_allowed_origins_parsing():
    # 1. Parsing from JSON string list
    s1 = Settings(allowed_origins='["http://localhost:3000", "http://example.com"]')
    assert s1.allowed_origins == ["http://localhost:3000", "http://example.com"]

    # 2. Parsing from standard Python list
    s2 = Settings(allowed_origins=["http://site.com"])
    assert s2.allowed_origins == ["http://site.com"]

    # 3. Parsing from comma-separated string
    s3 = Settings(allowed_origins="http://local:80, http://local:81")
    assert s3.allowed_origins == ["http://local:80", "http://local:81"]

    # 4. Fallback for invalid types
    s4 = Settings(allowed_origins=None)
    assert s4.allowed_origins == ["*"]


def test_config_gemini_enabled():
    s_enabled = Settings(gemini_api_key="test_key")
    assert s_enabled.gemini_enabled is True

    s_disabled = Settings(gemini_api_key=None)
    assert s_disabled.gemini_enabled is False
