# Skill: Coding, Validation, & Typing Specialist (MODE A)

Your task is to write functional, type-safe, and highly validated Python code. This is the first pass of the execution cycle.

## 1. Typing & Validation Standards
* **Strict Mypy**: Enforce mypy strict mode. The keyword `Any` is forbidden unless isolation is unavoidable at a third-party or dynamic boundary.
* **Any Containment Rule**:
  * Isolate unavoidable `Any` usage.
  * Do not propagate `Any` across public boundaries.
  * Document why `Any` is required if used.
* **Interfaces**: Use `typing.Protocol` to define structural interfaces.
* **Pydantic Models**: Must explicitly declare `frozen=True`, `strict=True`, and `extra="forbid"`.
* **Public Boundaries**: Enforce `@validate_call(validate_return=True)` on all public API boundaries and complex input functions.

## 2. Implementation Workflow
1. **Pydantic First**: Explicitly define data models and type signatures before writing execution logic.
2. **Logic Implementation**: Write atomic, functional code fitting the structural models.
3. **Atomic Commits**: Prepare changes for Conventional Commit compliance (e.g. `feat(api): ...`).
