---
category: automation
criticality: medium
scope: all
---
# /modc_act_mode
<!-- COMMAND_ID: 058 -->
<!-- COMMAND_VERSION: 2.1.0 -->
<!-- COMMAND_TYPE: mode_act -->

**Operational mode (Act).** Full execution mode: implement changes, run commands and tests, and complete the task end-to-end.

**Critical rule**: Act mode does NOT mean 'skip planning'. For non-trivial tasks, plan first (/modp_plan_mode) and only then act.

**Critical rule**: Act mode does NOT bypass safety rules. Always-applied workspace rules (preserve all functionality, restricted folder usage, ignored-file restrictions, absolute path handling) still apply.

**Local Reference**: `commands/modc_act_mode.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/modc_act_mode.md`

Backlinks:
- guides/cursor/MODE_SYSTEM_OVERVIEW.md
- guides/cursor/mode_commands_quick_reference.md
- standards/agents/autonomous_execution.md

## When to Use

- The plan or scope is clear and you are ready to implement
- Single-file or small, well-scoped edits with no architectural decisions
- Bug fixes where the root cause is already understood
- Running tests, linters, or other verification commands as part of the task

## When NOT to Use

- When you do not yet understand the code - use /moda_ask_mode first
- When the approach has significant trade-offs - use /modp_plan_mode first
- When chasing a runtime failure - use /modb_debug_mode first

## Allowed actions

- All reading actions (Read, Grep, Glob, semantic search)
- File edits (Write, StrReplace, Delete, EditNotebook)
- Shell commands (Shell, with appropriate timeouts)
- MCP tool calls (after reading their schema)
- Running tests, linters, build scripts
- Committing locally (NEVER pushing without /gsyn_git_sync, /gful_git_full_sync, or /gadm_git_admin_push)

## Still forbidden in Act mode

- Editing files in `.gitignore`, `.cursorignore`, `.dadosferaignore` without `XPTO AUTHORIZATION:` from the user
- Editing files in restricted/ without the proposal workflow
- Editing command instances in `.cursor/commands/` or `.dadosfera/commands/` (edit canonical sources in `commands/json/core/` instead)
- `git push --force` to main/master
- Removing existing functionality without an explicit deprecation request

## Verification expectations

After substantive edits in Act mode:

- Run linters/typechecks for the language touched
- Run targeted tests for the modules changed
- Read back the diff and confirm it matches intent
- If tests fail, fix forward; do NOT commit broken state

## Transition guidance

- Discovered the design is wrong -> /modp_plan_mode
- Discovered an unrelated runtime bug -> /modb_debug_mode
- Need to verify a behavior before changing more code -> /moda_ask_mode

## Reference

- [guides/cursor/MODE_SYSTEM_OVERVIEW.md](../../guides/cursor/MODE_SYSTEM_OVERVIEW.md)
- [guides/cursor/mode_commands_quick_reference.md](../../guides/cursor/mode_commands_quick_reference.md)
- [standards/agents/autonomous_execution.md](../../standards/agents/autonomous_execution.md)

## Related Commands

- `/moda_ask_mode`
- `/modp_plan_mode`
- `/modb_debug_mode`
- `/gsyn_git_sync`
