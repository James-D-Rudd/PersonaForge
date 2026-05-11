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

## 3. Tooling Commands
* **Verify All**: `ruff check . --fix && ruff format . && mypy . && pytest`
* **Test Only**: `pytest`
* **Lint Only**: `ruff check . --fix`

## 4. Documentation Strategy (AI-First)
* **Docstrings**: Google-style for all functions/methods. Include `Args`, `Returns`, `Raises`, and `Example`.
* **Logging**: Standard `logging` + `RotatingFileHandler`. Output: JSON (timestamp, level, module, message).
* **Internal Why**: Use comments only to explain "why" for non-obvious architecture.

## 5. Implementation Workflow
1. **Pydantic First**: Define data models and type signatures before logic.
2. **Atomic Commits**: Use Conventional Commits (e.g., `feat(api): add validation`).
3. **Verify**: Run the "Verify All" command after every task. Stop and report if `pytest` fails.
4. **Context Sync**: Update this file (`CONVENTIONS.md`) every time architecture or standards shift, but only if your certain architecture or standards have shifted.
