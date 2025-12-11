# /chkp_check_pending

<!-- COMMAND_ID: 044 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ch_check_pending -->

**Read-only validation.** Extract and list ONLY explicitly pending tasks from the current conversation, without analysis, classification, or scope suggestions.

This command is strictly informational—use it to get a quick, unadorned view of what remains to be done in the conversation. No routing, no recommendations, no out-of-scope ideas.

Backlinks:

- `commands/reva_review_active_conversation.md` (comprehensive classification; use when scope expansion is desired)
- `commands/arch_archive.md` (persistence; use after /chkp to archive conversation + plan routing)
- `mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md`

## Command sequence (run in order)

1. Confirm repository context (for references only)

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Extract pending items from conversation

Scan the conversation history for:

- ✅ **Explicit "pending" markers** (e.g., `- [ ] Task`, `**Pending:**`, `TODO:`, `FIXME:`)
- ✅ **Unfinished tasks** (e.g., marked as `in_progress`, `blocked`, `waiting`, `open`)
- ✅ **Clearly stated next steps** that the user or AI committed to but did not complete

**Strict filters (CRITICAL - do NOT override)**:

- **No suggestions**: Do not propose new tasks, improvements, or out-of-scope ideas.
- **No classification**: Do not categorize (Active/Backlog/Prioritized). Just list them.
- **No routing**: Do not suggest which plan they belong to.
- **Conversation-scoped only**: Only include items mentioned or worked on in the current conversation.
- **Latest status wins**: If a task status changed during the conversation (e.g., started as pending, completed later), report only the final status.

3. Output format (produce this in your message)

Generate a simple, read-only report:

```markdown
## Pending Tasks from Current Conversation

**Total Pending**: N

N. [Status] Task description

- Related context or reason (1–2 lines max)
```

**Status indicators**:

- `[ ]` – Not started
- `[~]` – In progress / Partially done
- `[!]` – Blocked (waiting for external input, decision, or dependency)
- `[?]` – Unclear or needs clarification

**Example output**:

```markdown
## Pending Tasks from Current Conversation

**Total Pending**: 3

1. [ ] Implement user authentication endpoint

   - HTTP POST /auth/login; needs database schema review first

2. [~] Add unit tests for payment processing

   - 60% done; still need to cover edge cases for refunds

3. [!] Deploy to staging environment
   - Blocked: waiting for ops team approval on resource allocation
```

4. Optional: note any completed tasks for reference

If the conversation completed work (e.g., merged changes, archived findings), briefly list them as **Completed in This Conversation** so the user knows they are not pending:

```markdown
## Completed in This Conversation

1. ✅ Fixed linter errors in src/utils.ts
2. ✅ Updated README with new endpoint docs
```

## Notes

- **Read-only**: This command produces no file changes, plan updates, or artifact creation. It only reads and reports.
- **Zero scope creep**: This command is designed to prevent the user from drifting into secondary tasks or new ideas. Use `/reva_review_active_conversation` if you want comprehensive analysis and routing suggestions.
- **Use after active work**: Run `/chkp_check_pending` near the end of a session to verify what still needs to be done before closing the conversation.
- **Minimal effort**: The output should be scannable in 10 seconds or less.
- **No interaction required**: The user does not need to confirm, approve, or authorize anything; this is pure reporting.

## Relationship to other commands

- **`/chkp_check_pending`** (this command): **Minimal read-only snapshot** of pending work. No suggestions.
- **`/reva_review_active_conversation`**: **Full conversation analysis** with classification and routing. Use when you want suggestions for next steps.
- **`/arch_archive`**: **Persistence** of conversation findings into plans. Often used after `/reva_review_active_conversation` to formally route tasks into the planning system.
- **`/pfac_plan_from_active_tasks_conversation`**: **Mid-conversation plan sync** (updates only active plans; not a full review).

## Workflow checklist

### For AI Agent:

- [ ] Scan conversation for explicit pending markers
- [ ] Apply strict filters (no suggestions, no classification, no routing)
- [ ] Report only conversation-scoped pending items
- [ ] Note any completed work separately
- [ ] Keep output concise and scannable
- [ ] Do NOT create or modify any files

### For User:

- [ ] Review the pending list
- [ ] Decide: continue working, archive the conversation, or defer to a plan
- [ ] Use `/reva_review_active_conversation` if you want detailed routing suggestions

## Quick Decision Tree

| **Your Need**                                           | **Use This Command**                                       |
| ------------------------------------------------------- | ---------------------------------------------------------- |
| "What's left to do right now?"                          | `/chkp_check_pending` ✅                                   |
| "Show me pending + suggest routing to plans"            | `/reva_review_active_conversation`                         |
| "I'm closing this conversation; save findings to plans" | `/arch_archive` (after `/reva_review_active_conversation`) |
| "Just refresh what's in the current active plan"        | `/pfac_plan_from_active_tasks_conversation`                |

--- End Command ---
