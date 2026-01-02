# /chkp_check_pending

<!-- COMMAND_ID: 044 -->
<!-- COMMAND_VERSION: 1.2.0 -->
<!-- COMMAND_TYPE: ch_check_pending -->

**Read-only validation.** Extract and list ONLY explicitly pending tasks from the current conversation, and **audit test results for completed tasks** (verify tests passed, or explicitly marked N/A) — without analysis, classification, or scope suggestions. Flags incomplete/failed tests as `⚠️` warnings.

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
- ✅ **Explicit commitments** that the user or AI committed to _in this conversation_ but did not complete (e.g., “I’ll do X next”)

3. Extract completed items + test evidence (completed-only audit)

Scan the conversation for:

- ✅ **Completed markers** (e.g., `Done:`, `✅`, “fixed”, “implemented”, “merged”, “shipped”)
- ✅ **Test evidence markers** (explicit only):
  - **Tests run**: `tests/run_tests.sh`, `pytest`, `npm test`, `pnpm test`, `yarn test`, `go test`, `cargo test`, `make test`, etc.
    - **Status check**: Must also verify that tests **passed** (exit code 0 or explicit "✅ all tests passed")
    - **⚠️ Flag**: If tests ran but you see `❌`, `failed`, `error`, or non-zero exit — mark as `⚠️ tests failed / incomplete`
  - **Tests added**: explicit mention of test files/paths, or "added unit/integration tests"
    - **Status check**: Must also confirm tests are **passing** after creation (ran successfully with 100% pass rate)
    - **⚠️ Flag**: If tests were added but not yet run/passing — mark as `⚠️ tests created but not passing`
  - **Explicit N/A**: "no tests needed", "docs-only", "read-only change", or similar _explicitly stated_

**Strict filters (CRITICAL - do NOT override)**:

- **No suggestions**: Do not propose new tasks, improvements, or out-of-scope ideas.
- **No classification**: Do not categorize (Active/Backlog/Prioritized). Just list them.
- **No routing**: Do not suggest which plan they belong to.
- **Conversation-scoped only**: Only include items mentioned or worked on in the current conversation.
- **Exclude "future work / not pending" lists**: If the conversation explicitly labels a list or section as _not pending_ (e.g., "These are not pending in this conversation but were identified as future work"), **ignore the entire list** — do not include any of its items.
- **No "Recommended Next Steps" sections**: Do not output headings/sections like "Recommended Next Steps", "Future Work", "Follow-ups", "Nice-to-haves", or similar. `/chkp_check_pending` output is only pending + optional completed.
- **Latest status wins**: If a task status changed during the conversation (e.g., started as pending, completed later), report only the final status.
- **No test guessing**: Only report tests as ✅ when BOTH:
  1. The conversation explicitly mentions tests run/added (or explicitly marks N/A), AND
  2. For tests run: Exit code is 0 or output explicitly states "all tests passed" / "tests passed" / "✅ passed"
  3. For tests added: Tests were actually run and verified passing (not just "I created test file X")
  - Otherwise, mark test evidence as `⚠️ not found` (if no mention), `⚠️ tests created but not passing` (if added but not run/passing), or `⚠️ tests failed / incomplete` (if run but failed).

4. Output format (produce this in your message)

Generate a simple, read-only report:

```markdown
## Pending Tasks from Current Conversation

**Total Pending**: N

N. [Status] Task description

- Related context or reason (1–2 lines max)

## Completed in This Conversation

**Total Completed**: M
**Completed Missing Test Evidence**: K (total with any issue: not found, created-not-passing, or failed)
- Tests not found: X
- Tests created but not passing: Y
- Tests failed / incomplete: Z

1. ✅ Completed task description
   - Tests: ✅ <explicit evidence> | ⚠️ not found | N/A (explicit)
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

## Completed in This Conversation

**Total Completed**: 4
**Completed Missing Test Evidence**: 2
- Tests not found: 0
- Tests created but not passing: 1
- Tests failed / incomplete: 1

1. ✅ Fixed linter errors in src/utils.ts

   - Tests: ✅ bash tests/run_tests.sh --category infrastructure (exit 0, all passed)

2. ✅ Updated README with new endpoint docs
   - Tests: N/A (explicit: docs-only change)

3. ✅ Added payment validation function
   - Tests: ⚠️ tests created but not passing (test file added, not yet run)

4. ✅ Refactored auth middleware
   - Tests: ⚠️ tests failed / incomplete (ran `npm test` but saw 3 failures)
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
- [ ] Note completed work separately
- [ ] For each completed item, report explicit test evidence (✅) or `⚠️ not found` / `N/A (explicit)`
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
