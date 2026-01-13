# /modb_cursor_debug_mode

<!-- COMMAND_ID: 059 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: mode_debug -->

**Operational mode (Debug).** Systematic investigation and root-cause analysis. The agent may run diagnostic commands, but should avoid permanent file changes unless explicitly switching to Act Mode.

Backlinks:

- `guides/cursor/MODE_SYSTEM_OVERVIEW.md`
- `guides/cursor/mode_commands_quick_reference.md`
- `commands/rcdg_root_cause_diag.md`
- `commands/rciv_investigate_root_cause.md`

## Activation

```bash
/modb_cursor_debug_mode
```

## Core rules (non-negotiable)

- **Evidence-driven**: Form hypotheses, gather evidence, and converge on root cause.
- **Diagnostics allowed**: You may run read-only or diagnostic commands to reproduce/inspect.
- **Avoid permanent edits**: Do not implement fixes by default. If a fix is needed, propose switching to `/modc_cursor_act_mode`.
- **Keep logs minimal**: Prefer targeted, temporary instrumentation; remove it before finishing.

## Expected output

- Reproduction steps (if applicable)
- Observations and evidence
- Root cause hypothesis + confidence
- Minimal fix proposal + validation plan

--- End Command ---
