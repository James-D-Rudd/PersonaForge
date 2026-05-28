_⚠️ Potential issue_ | _🟠 Major_ | _⚡ Quick win_

**Stop logging the full argv.**

This emits every command argument verbatim. Downstream `gh issue create` / `gh pr edit` flows pass generated titles and bodies through this helper, so those values will be persisted to logs. Log only the executable/subcommand or redact sensitive flags before emitting.

<details>
<summary>🧰 Tools</summary>

<details>
<summary>🪛 Ruff (0.15.13)</summary>

[error] 30-30: `subprocess` call: check for execution of untrusted input

(S603)

</details>

</details>

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
Verify each finding against current code. Fix only still-valid issues, skip the
rest with a brief reason, keep changes minimal, and validate.

In `@src/personaforge/utils.py` around lines 29 - 31, The current logging prints
the full command argv via logger.info/debug around the
subprocess.run(command...) which may leak sensitive/generated text; change these
logs to only emit the executable/subcommand (e.g., command[0] or '
'.join(command[:2]) for subcommand), or sanitize/redact sensitive
flags/arguments (detect flags like --body, --title, --description or values
matching large text and replace with "[REDACTED]") before logging; update the
logger.info("Running command: ...") and logger.debug("Command ... executed
successfully.") usages to use the sanitized command representation while leaving
subprocess.run(command, ...) unchanged.
```

</details>

<!-- fingerprinting:phantom:medusa:grasshopper -->

<!-- This is an auto-generated comment by CodeRabbit -->
