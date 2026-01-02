# /modc_cursor_act_mode

<!-- COMMAND_ID: 058 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: mode_act -->

**Operational mode (Act).** Full execution mode: implement changes, run commands/tests, and complete the task end-to-end.

Backlinks:

- `guides/cursor/MODE_SYSTEM_OVERVIEW.md`
- `guides/cursor/mode_commands_quick_reference.md`
- `standards/agents/autonomous_execution.md`

## Activation

```bash
/modc_cursor_act_mode
```

## Core rules (non-negotiable)

- **Execute safely**: Make changes deliberately; avoid risky operations without explicit user approval.
- **Prefer repo workflows**: Use the repository’s standard scripts and test runners.
- **Confirm outcomes**: After edits, run relevant checks/tests (scoped first), then summarize what changed.
- **Keep scope tight**: Implement only what the user asked; no surprise refactors.

## Typical workflow

1. Understand the request (brief assumptions if needed)
2. Inspect relevant files
3. Implement changes
4. Run scoped checks/tests
5. Summarize + next concrete step

--- End Command ---




