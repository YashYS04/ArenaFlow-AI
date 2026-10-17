# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-10-17

### Added
- Structured traceback error-tracking hook in middleware with test coverage in `tests/test_logging_structured.py`.
- End-to-end assist integration tests (`tests/test_assist_integration.py`) exercising offline MockLLM and token SSE streaming.
- Modularized frontend architecture (`app/static/i18n.js`, `app/static/map.js`, `app/static/app.js`) with all files under 350 LOC.
- Configured `.eslintrc.json` for frontend JavaScript static analysis.
- Multi-manifest discovery with `[tool.poetry.dependencies]` in `pyproject.toml`.

---

## [1.1.0] - 2026-10-15

### Added
- Multi-stage parallel CI pipeline (`lint`, `typecheck`, `test`, `audit`) with GitHub Actions pip caching.
- RFC-compliant 503 readiness probe for service unreadiness and dedicated `tests/test_health.py` test suite.
- Pinned deterministic lockfiles (`requirements.lock.txt` and `uv.lock`).
- Dependabot automated weekly dependency update configuration (`.github/dependabot.yml`).
- PR template and contributor code review checklist in `CONTRIBUTING.md`.

---

## [1.0.0] - 2026-07-17

### Added
- Deterministic rules-first context engine (`app/services/context_engine.py`) prioritizing graph pathfinding over LLM hallucinations.
- Step-free Dijkstra routing algorithm (`app/services/routing.py`) with support for stairs, ramps, elevators, and distance calculation.
- Dynamic crowd-congestion penalty multipliers (1.5x for moderate crowd, 3.0x for heavy crowd) with automatic facility reassignment.
- Live incident management (`app/services/incidents.py`) allowing staff to report spills or hazards that dynamically block affected zones.
- Pluggable Generative AI phrasing layer (`app/services/llm.py`) with streaming Server-Sent Events (SSE) and offline `MockLLM` fallback.
- Multilingual assistance supporting English (`en`), Spanish (`es`), and French (`fr`).
- Comprehensive accessibility modes supporting wheelchair step-free paths, low-vision landmark guidance, and screen-reader compatibility.
- Interactive MetLife Stadium SVG vector map with real-time route rendering and incident hazard highlighting.
- High-contrast visual mode (pure black/yellow) and Web Speech API Text-to-Speech (TTS) route narration.
- 100% statement test coverage across all Python modules with 74 baseline unit and integration tests.
- Strict Mypy type annotations and Ruff lint configuration.
