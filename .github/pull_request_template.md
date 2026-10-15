## Description
<!-- Provide a concise summary of the changes and motivation -->

## Type of Change
- [ ] `feat`: New feature (paired with tests)
- [ ] `fix`: Bug fix (paired with regression tests)
- [ ] `docs`: Documentation update
- [ ] `refactor`: Internal code refactoring
- [ ] `ci` / `build`: Build system or CI pipeline changes

## PR Quality Checklist
- [ ] **Test Pairing:** All source changes in `app/` include matching unit/integration tests in `tests/`.
- [ ] **Lint & Format:** `ruff check .` passes with zero warnings.
- [ ] **Type Safety:** `mypy app` passes in strict mode without errors.
- [ ] **Coverage Gate:** `pytest` achieves required coverage threshold.
- [ ] **Security Audit:** `pip-audit -r requirements.txt` passes without vulnerabilities.
- [ ] **Documentation:** `README.md`, `CHANGELOG.md`, or docstrings updated where relevant.
