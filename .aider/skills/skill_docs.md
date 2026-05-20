# Skill: Technical Writer & Docstring Enforcer (MODE B)
Your task is to analyze existing code and implement Google-style docstrings. This is the second pass of the execution cycle. Do not alter executable logic or code execution paths.

## 1. Structural Format
* Use triple double quotes """ for all docstrings.
* Use a concise one-line summary sentence at the very top, ending with a period.
* Leave a blank line between the summary and the detailed description block (if a description is needed).

## 2. Conditional Section Rules
Evaluate every function, class, and module against these exact conditional criteria. Do not include empty or unneeded sections:

### Args:
* Condition: REQUIRED if the function/method accepts one or more arguments. FORBIDDEN if the function takes no arguments.
* Format:
  Args:
      arg_name: Description of the argument, starting with a capital letter.
  (Note: Omit types from the docstring text block to avoid duplicating inline static type hints).

### Returns:
* Condition: REQUIRED if the function returns a value other than None. FORBIDDEN if the function returns None explicitly or implicitly.
* Format:
  Returns:
      Description of the return value, specifying what data shape or object is passed back.

### Yields:
* Condition: REQUIRED if the function is a generator (uses the yield keyword). FORBIDDEN in standard return functions.
* Format:
  Yields:
      Description of the individual items emitted by the generator.

### Raises:
* Condition: REQUIRED if the function intentionally allows an exception to propagate, or throws an error during execution.
* Format:
  Raises:
      ValueError: State the exact condition or input anomaly that causes this error.

### Examples:
* Condition: OPTIONAL by default. REQUIRED only for public-facing module roots, highly abstract utility helpers, or non-obvious mathematical algorithms.
* Format: Use standard interactive Python prompt style (>>>):
  Examples:
      >>> calculate_area(5.0)
      78.53975

## 3. Object Type Requirements Reference

| Object | Required Elements | Scope Notes |
| --- | --- | --- |
| Modules | Purpose, Usage, Examples | Placed at the absolute top of the .py file. |
| Classes | Summary, Attributes | Document public attributes under an Attributes: section if present. |
| Functions | Summary, [Args], [Returns], [Yields], [Raises] | Describe what it accomplishes conceptually, never how it does it. |
