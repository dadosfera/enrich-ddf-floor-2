---
category: automation
criticality: medium
scope: all
---
# /moda_ask_mode
<!-- COMMAND_ID: 056 -->
<!-- COMMAND_VERSION: 2.1.0 -->
<!-- COMMAND_TYPE: mode_ask -->

**Operational mode (Ask).** Read-only learning and exploration. The agent may read, search, and explain, but must NOT modify files or run terminal commands.

**Critical rule**: Switching modes is a behavioral contract, not a tool toggle. The agent MUST refuse write/exec actions for the rest of the turn unless the user explicitly switches to Act or Debug mode.

**Local Reference**: `commands/moda_ask_mode.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/moda_ask_mode.md`

Backlinks:
- guides/cursor/MODE_SYSTEM_OVERVIEW.md
- guides/cursor/mode_commands_quick_reference.md

## When to Use

- Learning a new module or codebase
- Researching implementation patterns
- Understanding existing code before changes
- Asking 'how does this work?' questions
- Analyzing code quality or architecture
- Exploring without commitment

## When NOT to Use

- When the user wants something built or modified - use /modc_act_mode
- When the user wants a written design before implementation - use /modp_plan_mode
- When debugging a runtime failure that needs diagnostic commands - use /modb_debug_mode

## Allowed actions

- Read files (any path the user has access to)
- Search the codebase (Grep, Glob, semantic search)
- Explain code, architecture, and trade-offs
- Cite specific file paths and line numbers
- Ask clarifying questions

## Forbidden actions

- Editing any file (no Write, StrReplace, Delete, EditNotebook)
- Running shell commands (no Shell, no terminal)
- Modifying environment, config, or credentials
- Calling MCP tools that mutate state
- Pretending to do work the mode forbids - if the user asks for an edit, suggest switching to /modc_act_mode

## Transition guidance

- After learning enough to design: /modp_plan_mode
- After learning enough to implement: /modc_act_mode
- If the question turned into a runtime bug: /modb_debug_mode

## Reference

- [guides/cursor/MODE_SYSTEM_OVERVIEW.md](../../guides/cursor/MODE_SYSTEM_OVERVIEW.md)
- [guides/cursor/mode_commands_quick_reference.md](../../guides/cursor/mode_commands_quick_reference.md)

## Related Commands

- `/modp_plan_mode`
- `/modc_act_mode`
- `/modb_debug_mode`
