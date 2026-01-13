# /modp_cursor_plan_mode

<!-- COMMAND_ID: 057 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: mode_plan -->

**Operational mode (Plan).** Strategic planning and design without implementation. The agent may read/search and discuss trade-offs, but must not modify files or run terminal commands.

Backlinks:

- `guides/cursor/MODE_SYSTEM_OVERVIEW.md`
- `guides/cursor/mode_commands_quick_reference.md`

## Activation

```bash
/modp_cursor_plan_mode
```

## Core rules (non-negotiable)

- **No execution**: Do not run shell commands.
- **No edits**: Do not create, edit, move, or delete files.
- **Produce a plan**: Provide a clear plan with phases, risks, and validation steps.
- **Decision clarity**: If multiple approaches exist, present options with pros/cons and pick a recommendation.
- **Assumptions explicit**: List assumptions and what would change the plan.

## Outputs that are allowed (examples)

- Implementation plan with milestones, dependencies, and acceptance criteria
- Migration strategy with rollback and verification steps
- Debugging hypotheses and experiment plan (without executing)

## Outputs that are not allowed

- Code changes, patches, or “I updated X file”
- Running tests/builds or “I executed commands”

--- End Command ---
