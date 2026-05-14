# PersonaForge: Development Conventions

## 1. System Guardrails (Aider-Specific)
* **Tone**: Be concise. No conversational filler. Do not explain code unless requested.
* **Architect Mode**: When in Architect mode, propose changes; in Editor mode, apply them strictly.
* **Local Optimization**: Prioritize minimal output tokens.
* **Token Management**: If context grows large, suggest dropping finished files via `/drop`.

## 2. Technical Stack & Standards
* **Environment**: Python 3.10+.
* **Core Libs**: Pydantic v2 (Strict), LangChain v0.2+ (LCEL/`@tool`), Pytest, Ruff.
* **Typing**: `mypy` strict mode. No `Any`. Use `typing.Protocol` for interfaces.
* **Pydantic**: Models must be `frozen=True`, `strict=True`, `extra="forbid"`.
* **Density**: Keep logic modules <100 lines of executable code.
* **Validation**: Use `@validate_call(validate_return=True)` at public API boundaries and for complex inputs.

## 3. Tooling Commands
* **Verify All**: `ruff check . --fix && ruff format . && mypy . && pytest`
* **Test Only**: `pytest`
* **Lint Only**: `ruff check . --fix`

## 4. Documentation Strategy (AI-First)
* **Docstrings**: Google-style for all functions/methods
* **Format**: Use triple double quotes `"""`.
* **Args**: `name (type): description`.
* **Returns**: `type: description`.
* **Raises**: `ExceptionName: Context for error`.
* **Logging**: Standard `logging` + `RotatingFileHandler`. Output: JSON.
* **Internal Why**: Use comments only to explain "why" for non-obvious architecture.

### Object Type Requirements
| Object | Required Elements | Style Notes |
| --- | --- | --- |
| **Modules** | Purpose, Usage, Examples | Placed at the top of the `.py` file. |
| **Classes** | Summary, Attributes | Document public attributes in `Attributes:`. |
| **Functions** | Summary, Args, Returns, Raises | Describe *what* it does, not *how*. |

### Docstring Example (Few-Shot)
```python
def calculate_area(radius: float) -> float:
    """Calculates the area of a circle.

    Uses the standard formula (pi * r^2).

    Args:
        radius: Distance from center to edge. Must be non-negative.

    Returns:
        The calculated area.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 3.14159 * (radius ** 2)

```

## 5. Implementation Workflow
1. **Pydantic First**: Define data models and type signatures before logic.
2. **Atomic Commits**: Use Conventional Commits (e.g., `feat(api): add validation`).
3. **Verify**: Run `ruff check . --fix && ruff format . && mypy . && pytest` after every task.
4. **Context Sync**: Update this file if architecture or standards shift.

## 6. Zero-Tolerance Exception Policy
* **CRITICAL CONSTRAINT**: The keywords `try`, `except`, and `finally` are **STRICTLY FORBIDDEN** in all library logic, utilities, and internal modules.
* **VIOLATION CRITERIA**: Any code containing local error handling (swallowing exceptions) is considered "Broken Code" and a violation of the system architecture.
* **MANDATE**: Fail Loudly. If an operation (file I/O, network, parsing) can fail, let it raise a standard Python exception. Do not wrap it. Do not "protect" the caller.
* **DELEGATION**: Validation MUST happen at the data-layer via Pydantic or `@validate_call(validate_return=True)`. If the data passes validation but the logic fails, the program must crash.
* **__main__ EXCEPTION**: A single `try/except` block is permitted in `if __name__ == "__main__":` blocks and ONLY to map internal crashes to a JSON log and exit code. This is mandatory when the functions called by that block can Raise. 
* **CLEAR RECOVERY**: The only other exepction to this rule isi if there is a clear recovery path (e.g., attempting a fallback API call after a timeout). 
* **PRIORITY**: If you see a try/except block, that does is not one of the exceptions listed, your first priority is to remove it.

## 7. Import Style
* **Module Imports**: Use `from <package> import <module>` to import modules, then reference items as `<module>.ClassName` or `<module>.function_name`. This applies to all imports including standard library.
* **Example**: 
  ```python
  from mypackage import models
  
  repo_info = models.RepoInfo(owner="testowner", repo="testrepo")
  ```
* **Example (Standard Library)**:
  ```python
  from unittest import mock
  
  with mock.patch("module.function") as mock_func:
      ...
  ```
* **Avoid**: Direct class/function imports like `from mypackage.models import RepoInfo` or `from unittest.mock import patch`
