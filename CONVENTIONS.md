# persona-forge: Core Development Conventions & Dual-Pass Engine

## 1. System Guardrails (Aider-Specific)
* **Tone**: Be concise. No conversational filler. Do not explain code unless requested.
* **Architect Mode**: In Architect mode, propose changes; in Editor mode, apply them strictly.
* **Local Optimization**: Prioritize minimal output tokens.
* **Token Management**: If context grows large, suggest dropping finished files via `/drop`.

## 2. Technical Stack & Standards
* **Environment**: Python 3.10+.
* **Core Libs**: Pydantic v2 (Strict), LangChain v0.2+ (LCEL/`@tool`), Pytest, Ruff.
* **Density**: Keep modules cohesive and compact. Strongly reconsider modules exceeding ~100 lines of executable logic unless domain cohesion clearly justifies it.

## 3. Import Style
* Use `from <package> import <module>` for all imports (including standard library).
* Reference items as `<module>.ClassName` or `<module>.function_name`.
* *Avoid*: Direct imports like `from package.module import Class`.

## 4. Exception Handling Policy
* Avoid defensive exception handling.
* **Mandate**: Fail loudly. Let operations raise standard exceptions naturally unless explicit recovery or cleanup behavior is required.
* **Allowed Uses**:
  * Explicit recovery paths.
  * Retry logic.
  * Resource cleanup.
  * Boundary translation.
  * Structured logging at application boundaries.
  * Backup/fallback execution paths with clear behavioral intent.
* **Forbidden Uses**:
  * Silent suppression.
  * Broad catch-all handlers.
  * Hidden fallback masking.
  * Meaningless wrapper exceptions.
* **Priority**: If you encounter non-compliant exception handling, simplify or remove it immediately.

## 5. Tooling Verification
* Run after every task:
  ```bash
  ruff check . --fix && ruff format . && mypy . && pytest
  ```

---

## 6. Execution Protocols (CRITICAL)
You operate under a strict separation of concerns. You must dynamically shift modes based on the user's intent or current workflow pass:

### [MODE A]: CODING & VALIDATION (Initial Pass)
* **Activation**: Triggered automatically on any initial request to create a new module, refactor an engine, or modify existing execution logic.
* **Instruction**: Apply the guidelines found in `.aider/skills/skill_coding.md`.
* **Constraint**: Focus completely on code execution, validation layers, and safety patterns. Do not generate heavy docstrings during this pass.

### [MODE B]: DOCUMENTATION ENFORCEMENT (Sequential Pass or Standalone)
* **Activation (Sequential)**: Triggered immediately after the underlying code logic for Mode A is verified and committed.
* **Activation (Standalone)**: Triggered immediately if the user manually updates a file and instructs you to *only* update, fix, or generate documentation.
* **Context Clean-up Command**: If transitioning from Mode A to Mode B within the same chat session, you MUST instruct the user to drop the coding skill file by printing:
  ```text
  Please run /drop .aider/skills/skill_coding.md
  ```
* **Instruction**: Apply the strict structural rules found in `.aider/skills/skill_docs.md`.
* **Constraint**: Overlay perfect, conditionally compliant Google-style docstrings. Do not alter any operational code or execution paths.
