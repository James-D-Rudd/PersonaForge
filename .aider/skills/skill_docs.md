# Skill: Technical Writer & Docstring Enforcer (MODE B)

Your task is to analyze existing code and implement Google-style docstrings. This is the second pass of the execution cycle. Do not alter executable logic or code execution paths.

---

## 1. Structural Format

* Use triple double quotes `"""` for all docstrings.
* Use a concise one-line summary sentence at the top, ending with a period.
* Leave a blank line between the summary and the detailed section block (if needed).
* Docstrings must describe **what the code does, not how it does it**.

---

## 2. Conditional Section Rules

Evaluate every function, class, and module. Include ONLY sections that are semantically required.

---

### Args:
* Condition: REQUIRED if the function/method accepts one or more arguments. FORBIDDEN if no arguments exist.
* Format:
  ```text
  Args:
      arg_name: Description of the argument.
  ```

---

### Returns:
* Condition: REQUIRED if return value is not `None`. FORBIDDEN otherwise.
* Format:
  ```text
  Returns:
      Description of the return value.
  ```

---

### Yields:
* Condition: REQUIRED only for generator functions.
* Format:
  ```text
  Yields:
      Description of yielded values.
  ```

---

### Raises:
* Condition: REQUIRED only for domain-significant or contractually relevant exceptions that are intentionally raised or propagated.
* FORBIDDEN for incidental runtime/interpreter exceptions.
* Format:
  ```text
  Raises:
      ValueError: Condition that triggers the exception.
  ```

---

### Attributes:
* Condition: REQUIRED for classes exposing meaningful public attributes.
* FORBIDDEN if no public attributes exist.
* Format:
  ```text
  Attributes:
      name: Description of attribute.
  ```

---

### Examples:
* Condition: OPTIONAL. Include an EXAMPLES section ONLY if the function meets at least one of the following criteria:
  - Takes complex nested structures (e.g., dict of dicts, mixed lists) as an argument.
  - Requires a specific string format/regex pattern (e.g., ISO dates, custom IDs).
  - Employs tricky mathematical algorithms or edge-case handling (e.g., syncopated timing logic).
  - Returns a composite or custom object structure that isn't immediately clear from the type signature.
  Otherwise, omit the EXAMPLES section.
* Must use `Examples:` (plural always).
* Format:
  ```python
  Examples:
      >>> function_call()
      expected_output
  ```

---

### Notes:
* Condition: OPTIONAL.
* Used for invariants, side effects, behavioral caveats, or performance considerations that affect usage.
* Format:
  ```text
  Notes:
      Additional behavioral context.
  ```

---

### Warnings:
* Condition: OPTIONAL. REQUIRED only when misuse can cause destructive behavior, security risk, or major unintended side effects.
* Format:
  ```text
  Warnings:
      Important caution about usage.
  ```

---

## 3. Object Type Requirements Reference

| Object | Required Elements | Scope Notes |
|--------|------------------|-------------|
| Modules | Purpose, Usage | Placed at top of file |
| Classes | Summary, Attributes (if applicable) | Document public state only |
| Functions | Summary + conditional sections | Never describe implementation details |

---

## 4. Behavioral Constraints

* Never modify executable logic.
* Never change imports, signatures, or control flow.
* Never refactor code.
* Preserve formatting outside docstrings.
* Do not generate placeholder or low-information docstrings.
* Avoid redundancy with type hints.
* Ensure docstrings match actual runtime behavior exactly.
* Keep documentation concise, high-signal, and non-narrative.