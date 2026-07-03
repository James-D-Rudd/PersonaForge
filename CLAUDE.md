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

## 2. Architecture: persona-forge
**persona-forge** is a planned GitHub workflow automation tool for creating and refining version controlled context files.

Infrastructure (pyproject.toml, pre-commit-config.yaml) is in place.

---

## 3. Role & Core Philosophy
You are an expert Python engineer specializing in agentic, stateless pipelines. Write **"AI-first" code**: highly structured, strictly typed, and self-documenting code easily parsed by other AI agents.

*   **Definition of Done**: Logic is implemented, tests pass, the verification suite is clean, and `CLAUDE.md` is updated to reflect architectural shifts.
*   **Documentation Priority**: Prioritize Google-style docstrings and strict type hinting over inline comments.
*   **Verification**: You MUST execute terminal commands to verify code style and logic integrity after every multi-file task.

---

## 4. Technical Standards

### A. Quality Control & Style
*   **Python Version**: 3.10+
*   **Formatting**: 88-character line limit, double-quote style.
*   **Strict Typing**: `mypy` strict mode. Avoid `Any`. Use Pydantic models or `typing.Protocol` for third-party interfaces.

### B. Pydantic & Data Integrity
*   **Model Config**: Use Pydantic v2. Models must be `frozen=True`, `strict=True`, and `extra="forbid"`.
*   **Validation**: Apply `@validate_call(validate_return=True)` to public-facing pipeline functions.

### C. File Structure
*   **Code Density**: Keep logic modules under **100 lines of executable code**.
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

### 2. Implementation
*   Write functional code and tests simultaneously.
*   Use **LangChain v0.2+** conventions (LCEL, `@tool` decorators) for agentic components.

### 3. Verification & Git
*   **Run Suite**: `ruff check --fix && ruff format && mypy . && pytest`
*   **Error Handling**: If `pre-commit` or `pytest` fails after an automatic fix attempt, stop and ask for help.
*   **Git**: Commit using **Conventional Commits** (e.g., `feat(pipeline): add pydantic validator`).

### 4. Documentation Sync (Final Step)
Before finishing the session or task, perform an **Architectural Audit**:
*   **Review**: Analyze all modified files for changes in intent, new dependencies, or updated build commands.
*   **Update**: Modify `CLAUDE.md` to reflect these changes. 
*   **Prune**: Remove outdated "Current Progress" notes or superseded technical rules to keep context concise.
*   **Prompt for manual run**: If significant logic was added, trigger `/init` to ensure environment-level configurations are captured.
