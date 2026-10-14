# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Continuous Integration workflow via GitHub Actions (`.github/workflows/ci.yml`) enforcing linting, strict static typing, test coverage thresholds, and security auditing (`pip-audit`).
- Structured JSON logging formatter (`StructuredJsonFormatter`) via `python-json-logger` in `app/logging_conf.py`.
- Application telemetry metrics and observability endpoints (`/metrics` and `/readyz`) tracking request throughput, status codes, active connections, and system uptime.
- Structured access logging middleware appending `X-Request-ID` and measuring request latency in milliseconds.
- Pinned dependency lockfile (`requirements.lock.txt`) for fully reproducible fresh clone installations.
- Comprehensive `CONTRIBUTING.md` guide and `docker-compose.yml` local container orchestration.

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
