# /moda_cursor_ask_mode

<!-- COMMAND_ID: 056 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: mode_ask -->

**Operational mode (Ask).** Read-only learning and exploration. The agent may read/search and explain, but must not modify files or run terminal commands.

Backlinks:

- `guides/cursor/MODE_SYSTEM_OVERVIEW.md`
- `guides/cursor/mode_commands_quick_reference.md`

## Activation

```bash
/moda_cursor_ask_mode
```

## Core rules (non-negotiable)

- **Read-only**: Do not create, edit, move, or delete files.
- **No terminal**: Do not run shell commands or start servers.
- **Clarify intent**: Ask focused questions only when necessary; otherwise, infer and explain.
- **Cite evidence**: When explaining repo behavior, cite concrete file paths and relevant excerpts.
- **No planning output**: Do not write plans, task breakdowns, or next-step roadmaps (use Plan Mode for that).

## What you should do

- Read and navigate the codebase/docs to answer questions.
- Summarize how something works and where it is implemented.
- Call out risks, unknowns, and where to look next (as questions, not action items).

## What you must not do

- No edits, patches, PR-style changes, refactors, or “I went ahead and fixed it”.
- No “Recommended Next Steps” lists or scope expansion.

--- End Command ---
