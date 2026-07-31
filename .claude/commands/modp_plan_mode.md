---
category: automation
criticality: medium
scope: all
---
# /modp_plan_mode
<!-- COMMAND_ID: 057 -->
<!-- COMMAND_VERSION: 2.1.0 -->
<!-- COMMAND_TYPE: mode_plan -->

**Operational mode (Plan).** Strategic planning and design without implementation. The agent may read, search, and discuss trade-offs, but must NOT modify files or run terminal commands.

**Critical rule**: Plan mode produces a plan artifact (textual or .plan.md) - it does NOT execute the plan. Switch to /modc_act_mode for execution.

**Local Reference**: `commands/modp_plan_mode.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/modp_plan_mode.md`

Backlinks:
- guides/cursor/MODE_SYSTEM_OVERVIEW.md
- guides/cursor/mode_commands_quick_reference.md

## When to Use

- Designing the approach for a non-trivial task before any code changes
- Multiple valid approaches exist with significant trade-offs
- Architectural decisions are needed (e.g., 'add caching' -> Redis vs in-memory vs file)
- The task touches many files or systems (large refactors, migrations)
- Requirements are unclear and need exploration before scoping

## When NOT to Use

- Trivial single-file edits - jump straight to /modc_act_mode
- Pure information lookups - use /moda_ask_mode
- Debugging a live failure - use /modb_debug_mode

## Allowed actions

- Read files and search the codebase
- Discuss trade-offs and alternatives
- Produce a written plan (steps, files affected, risks, success criteria)
- Cite specific file paths and line numbers
- Ask clarifying questions

## Forbidden actions

- Editing source files (no Write, StrReplace, Delete, EditNotebook on production code)
- Running shell commands that mutate state
- Calling MCP tools that mutate state
- Skipping the plan and starting to implement

## Plan structure (recommended)

1. **Goal** - one sentence on the desired end state.
2. **Approach** - chosen approach with brief rationale vs alternatives.
3. **Steps** - ordered, each with affected files and verification.
4. **Risks & mitigations** - what can go wrong and the fallback.
5. **Out of scope** - explicit non-goals.
6. **Success criteria** - how we know we are done.

## Transition guidance

- Plan approved -> /modc_act_mode
- Need more context first -> /moda_ask_mode
- Plan exposes a runtime defect -> /modb_debug_mode

## Reference

- [guides/cursor/MODE_SYSTEM_OVERVIEW.md](../../guides/cursor/MODE_SYSTEM_OVERVIEW.md)
- [guides/cursor/mode_commands_quick_reference.md](../../guides/cursor/mode_commands_quick_reference.md)

## Related Commands

- `/moda_ask_mode`
- `/modc_act_mode`
- `/modb_debug_mode`
