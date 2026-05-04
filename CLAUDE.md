# CLAUDE.md

## 1. Development Commands

```bash
# Lint and format (apply fixes)
ruff check . --fix && ruff format .

# Type checking (strict mode)
mypy .

# Run test suite
pytest

# Full verification (Style + Types + Tests)
ruff check . && ruff format --check . && mypy . && pytest
```

---

## 2. Architecture: PersonaForge
**PersonaForge** is a GitHub workflow automation tool that orchestrates issue creation and PR management using the GitHub CLI (`gh`).

*   **master_driver.py**: Entry point that coordinates the full workflow sequence.
*   **genesis.py**: Creates a test branch, adds a file, and opens a PR.
*   **create_issues.py**: Creates GitHub issues for the current branch.
*   **loop_issues.py**: Processes and closes issues.
*   **placeholder.py**: Closes individual issues via `gh` CLI.
*   **utils.py**: Shared `run_command()` utility wrapping `subprocess`.

---

## 3. Role & Core Philosophy
You are an expert Python engineer specializing in agentic, stateless pipelines. Write **"AI-first" code**: highly structured, strictly typed, and self-documenting code easily parsed by other AI agents.

*   **Definition of Done**: Logic is implemented, tests are created/updated, and the verification suite passes with zero errors.
*   **Documentation Priority**: Prioritize Google-style docstrings and strict type hinting over inline comments.
*   **Verification**: You MUST execute terminal commands to verify code style and logic integrity after every multi-file task.

---

## 4. Technical Standards

### A. Quality Control & Style
*   **Python Version**: 3.10+
*   **Formatting**: 88-character line limit, double-quote style (per `pyproject.toml`).
*   **Strict Typing**: `mypy` strict mode. Avoid `Any`. Use Pydantic models or `typing.Protocol` for third-party interfaces.

### B. Pydantic & Data Integrity
*   **Model Config**: Use Pydantic v2. Models must be `frozen=True`, `strict=True`, and `extra="forbid"`.
*   **Validation**: Apply `@validate_call` to public-facing pipeline functions.

### C. File Structure
*   **Code Density**: Keep logic modules under **200 lines of executable code**.
*   **Testing**: All tests in `/tests` using `test_*.py`. Use `/tests/data` for mocks with `pytest` teardown fixtures.

---

## 5. Documentation & Logging

### AI-First Docstrings
Every function (including private `_methods`) must have an exhaustive **Google-style docstring**:
*   **Sections**: `Args`, `Returns`, `Raises`, and a "Usage" `Example`.
*   **Inline Comments**: Only use "Why" comments for non-obvious architectural decisions.

### Observability
*   **Logging**: Use standard Python `logging` with `RotatingFileHandler` and `sys.stderr`.
*   **Schema**: JSON format including `timestamp`, `level`, `module`, `message`, and `exc_info`.

---

## 6. Operational Workflow

### 1. Plan Mode
Generate a Markdown plan before writing code:
*   Files to be modified/created.
*   Pydantic model changes and type signatures.
*   Proposed `pytest` coverage.
*   Required `pyproject.toml` changes (requires user permission).

### 2. Implementation
*   Write functional code and tests simultaneously.
*   Use **LangChain v0.2+** conventions (LCEL, `@tool` decorators) for agentic components.

### 3. Verification & Git
*   **Run Suite**: `ruff check --fix && ruff format && mypy . && pytest`
*   **Error Handling**: If `pre-commit` or `pytest` fails after an automatic fix attempt, stop and ask for help.
*   **Git**: Commit using **Conventional Commits** (e.g., `feat(pipeline): add pydantic validator for openrouter`).