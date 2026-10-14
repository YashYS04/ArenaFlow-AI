# Contributing to ArenaFlow AI

Thank you for your interest in contributing to **ArenaFlow AI**! We welcome contributions to our smart stadium operations and wayfinding assistant for the FIFA World Cup 2026.

This document outlines the workflow, development environment setup, coding standards, and pull request procedures.

---

## 1. Branch Naming Conventions

When creating branches, please follow these standardized prefixes:

* `feat/<feature-name>`: New feature implementations or enhancements.
* `fix/<bug-name>`: Bug fixes and issue patches.
* `docs/<topic>`: Documentation improvements, diagrams, or updates.
* `refactor/<target>`: Code restructuring without functional behavior changes.
* `test/<component>`: Test coverage additions or test harness updates.
* `chore/<task>`: Maintenance, CI/CD pipeline, or dependency updates.

*Example:* `feat/sensory-room-wayfinding` or `fix/sse-stream-buffer`

---

## 2. Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```text
<type>(<scope>): <short description in present tense>

[optional body explaining motivation and context]

[optional footer(s) referencing issue IDs]
```

**Allowed Types:**
* `feat`: A new feature (paired with unit tests).
* `fix`: A bug fix (paired with regression tests).
* `docs`: Documentation changes only.
* `test`: Adding missing tests or correcting existing tests.
* `refactor`: A code change that neither fixes a bug nor adds a feature.
* `build` / `ci`: Changes that affect the build system or CI pipeline.

*Important:* In ArenaFlow AI, new features and bug fixes must always be committed **together with their corresponding tests** in the same focused commit.

---

## 3. Local Development Setup

### Prerequisites
* Python 3.11 or higher
* Git

### Step-by-Step Installation
1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YashYS04/ArenaFlow-AI.git
   cd ArenaFlow-AI
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install pinned dependencies:
   ```bash
   pip install -r requirements.lock.txt
   ```

4. Configure local environment variables:
   ```bash
   cp .env.example .env
   ```
   *(ArenaFlow operates out-of-the-box with `MockLLM` if `GEMINI_API_KEY` is not provided).*

---

## 4. Quality Assurance & Verification

Before submitting a Pull Request, all automated quality gates must pass locally:

### 1. Code Style and Linting
```bash
ruff check .
```

### 2. Static Type Checking (Strict Mypy)
```bash
mypy app
```

### 3. Test Suite & Coverage Threshold
```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=70
```
*(The core codebase maintains high test coverage across all routing, schema, and API modules).*

### 4. Dependency Security Audit
```bash
pip-audit -r requirements.txt
```

---

## 5. Pull Request Process

1. Ensure all new code paths include corresponding unit and integration tests.
2. Verify that local linting (`ruff`), typechecking (`mypy`), and test suites (`pytest`) are 100% green.
3. Submit a Pull Request against the `main` branch with a clear title and description of the changes.
4. The automated GitHub Actions CI pipeline will validate:
   * Code formatting and lint rules.
   * Strict type compliance.
   * Pytest suite execution and test coverage thresholds.
   * Dependency vulnerability audits via `pip-audit`.
5. Once all CI checks are green and code review is approved, your PR will be merged.
