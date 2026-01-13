# /chkp_check_pending

<!-- COMMAND_ID: 044 -->
<!-- COMMAND_VERSION: 1.4.0 -->
<!-- COMMAND_TYPE: ch_check_pending -->

**Read-only validation.** Extract and list ONLY explicitly pending tasks from the current conversation, **check for unpushed commits and hook-related push blockers**, and **audit test results, hooks, and test tagging for completed tasks** (verify tests passed, hooks created/updated when needed, and tests properly tagged) — without analysis, classification, or scope suggestions. Flags incomplete/failed tests, missing hooks, untagged tests, and unpushed commits blocked by hooks as `⚠️` warnings.

This command is strictly informational—use it to get a quick, unadorned view of what remains to be done in the conversation. No routing, no recommendations, no out-of-scope ideas.

Backlinks:

- `commands/reva_review_active_conversation.md` (comprehensive classification; use when scope expansion is desired)
- `commands/arch_archive.md` (persistence; use after /chkp to archive conversation + plan routing)
- `mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md`

## Command sequence (run in order)

1. Confirm repository context and check git push status

```bash
gtimeout 5 git rev-parse --show-toplevel
```

Check for unpushed commits and hook-related push blockers:

```bash
# Check if there are commits ahead of origin
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
UNPUSHED_COUNT=$(git rev-list HEAD...origin/$CURRENT_BRANCH --count 2>/dev/null || echo "0")

# If there are unpushed commits, check if they're blocked by hook errors
if [ "$UNPUSHED_COUNT" -gt 0 ]; then
  # Check if pre-commit hooks would fail (dry-run)
  if command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --all-files --hook-stage pre-push 2>&1 | grep -q "Failed\|error" && HOOK_ERRORS="yes" || HOOK_ERRORS="no"
  else
    HOOK_ERRORS="unknown"
  fi
fi
```

**Report unpushed commits status**:
- ✅ **No unpushed commits**: All commits are pushed
- ⚠️ **Unpushed commits (N)**: N commits ahead of origin (not blocked by hooks)
- ⚠️ **Unpushed commits (N) - blocked by hook errors**: N commits ahead of origin, and pre-commit/pre-push hooks are failing

2. Extract pending items from conversation

Scan the conversation history for:

- ✅ **Explicit "pending" markers** (e.g., `- [ ] Task`, `**Pending:**`, `TODO:`, `FIXME:`)
- ✅ **Unfinished tasks** (e.g., marked as `in_progress`, `blocked`, `waiting`, `open`)
- ✅ **Explicit commitments** that the user or AI committed to _in this conversation_ but did not complete (e.g., “I’ll do X next”)

3. Extract completed items + test/hooks evidence (completed-only audit)

Scan the conversation for:

- ✅ **Completed markers** (e.g., `Done:`, `✅`, “fixed”, “implemented”, “merged”, “shipped”)
- ✅ **Test evidence markers** (explicit only):
  - **Tests run**: `tests/run_tests.sh`, `pytest`, `npm test`, `pnpm test`, `yarn test`, `go test`, `cargo test`, `make test`, etc.
    - **Status check**: Must also verify that tests **passed** (exit code 0 or explicit "✅ all tests passed")
    - **⚠️ Flag**: If tests ran but you see `❌`, `failed`, `error`, or non-zero exit — mark as `⚠️ tests failed / incomplete`
  - **Tests added**: explicit mention of test files/paths, or "added unit/integration tests"
    - **Status check**: Must also confirm tests are **passing** after creation (ran successfully with 100% pass rate)
    - **⚠️ Flag**: If tests were added but not yet run/passing — mark as `⚠️ tests created but not passing`
  - **Test tagging check**: For tests added/run, verify they are tagged with:
    - **Category**: `infrastructure`, `integration`, `ai_testing`, `unit` (or explicit N/A if not applicable)
    - **Criticality**: `critical`, `high`, `medium`, `low` (or explicit N/A if not applicable)
    - **Scope**: `infra`, `integration`, `docs`, `all` (or explicit N/A if not applicable)
    - **Subcategory/Subscope**: If applicable to the test suite
    - **⚠️ Flag**: If tests were added but no tagging evidence found — mark as `⚠️ tests missing tags (category/criticality/scope)`
  - **Explicit N/A**: "no tests needed", "docs-only", "read-only change", or similar _explicitly stated_
- ✅ **Hooks evidence markers** (explicit only):
  - **Hooks created/updated**: explicit mention of hook files/paths, `.pre-commit-config.yaml` updates, or "added/updated hooks"
    - **When hooks are needed**: Hooks should be created/updated when:
      - New validation logic is added (file structure, naming conventions, content validation)
      - New file types/patterns are introduced that need validation
      - Standards require hooks for certain types of changes (e.g., index files, command files, rule files)
      - Security checks are needed for new patterns (secrets, API keys, hardcoding)
    - **Status check**: Must confirm hooks are **installed and configured** (in `.pre-commit-config.yaml` or `.husky/pre-commit`, and script exists)
    - **⚠️ Flag**: If changes suggest hooks are needed but no hooks were created — mark as `⚠️ hooks may be needed (validation/security checks)`
    - **⚠️ Flag**: If hooks were created but not installed/configured — mark as `⚠️ hooks created but not installed`
  - **Explicit N/A**: "no hooks needed", "no validation required", or similar _explicitly stated_

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
- **No hooks guessing**: Only report hooks as ✅ when:
  1. The conversation explicitly mentions hooks created/updated/installed (or explicitly marks N/A), OR
  2. Changes made clearly don't require hooks (e.g., pure documentation, read-only operations)
  - If changes suggest hooks might be needed (new validation logic, new file patterns, security checks) but no hooks were mentioned, mark as `⚠️ hooks may be needed`.
- **No tagging guessing**: Only report test tagging as ✅ when:
  1. The conversation explicitly mentions test tags (category, criticality, scope) or shows test commands with `--category`, `--criticality`, `--scope` flags, OR
  2. Tests are explicitly marked as not requiring tags (e.g., "simple smoke test", "docs-only test")
  - If tests were added but no tagging evidence is found, mark as `⚠️ tests missing tags`.

4. Output format (produce this in your message)

Generate a simple, read-only report:

```markdown
## Git Push Status

**Unpushed Commits**: N
- Status: ✅ All pushed | ⚠️ N commits ahead (not blocked) | ⚠️ N commits ahead - blocked by hook errors

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
**Completed Missing Hooks Evidence**: H (total with any issue: may be needed, created-not-installed)
- Hooks may be needed: A
- Hooks created but not installed: B
**Completed Missing Test Tagging**: T (total with any issue: missing tags)
- Tests missing tags: T

1. ✅ Completed task description
   - Tests: ✅ <explicit evidence> | ⚠️ not found | ⚠️ tests created but not passing | ⚠️ tests failed / incomplete | ⚠️ tests missing tags (category/criticality/scope) | N/A (explicit)
   - Hooks: ✅ <explicit evidence> | ⚠️ hooks may be needed | ⚠️ hooks created but not installed | N/A (explicit)
```

**Status indicators**:

- `[ ]` – Not started
- `[~]` – In progress / Partially done
- `[!]` – Blocked (waiting for external input, decision, or dependency)
- `[?]` – Unclear or needs clarification

**Example output**:

```markdown
## Git Push Status

**Unpushed Commits**: 2
- Status: ⚠️ 2 commits ahead - blocked by hook errors (pre-commit validation failing)

## Pending Tasks from Current Conversation

**Total Pending**: 3

1. [ ] Implement user authentication endpoint

   - HTTP POST /auth/login; needs database schema review first

2. [~] Add unit tests for payment processing

   - 60% done; still need to cover edge cases for refunds

3. [!] Deploy to staging environment
   - Blocked: waiting for ops team approval on resource allocation

## Completed in This Conversation

**Total Completed**: 6
**Completed Missing Test Evidence**: 2
- Tests not found: 0
- Tests created but not passing: 1
- Tests failed / incomplete: 1
**Completed Missing Hooks Evidence**: 1
- Hooks may be needed: 1
- Hooks created but not installed: 0
**Completed Missing Test Tagging**: 1
- Tests missing tags: 1

1. ✅ Fixed linter errors in src/utils.ts
   - Tests: ✅ bash tests/run_tests.sh --category infrastructure --criticality high (exit 0, all passed)
   - Hooks: N/A (explicit: no validation logic changes)

2. ✅ Updated README with new endpoint docs
   - Tests: N/A (explicit: docs-only change)
   - Hooks: N/A (explicit: docs-only change)

3. ✅ Added payment validation function
   - Tests: ⚠️ tests created but not passing (test file added, not yet run)
   - Hooks: ⚠️ hooks may be needed (new validation logic added, may need pre-commit checks)

4. ✅ Refactored auth middleware
   - Tests: ⚠️ tests failed / incomplete (ran `npm test` but saw 3 failures)
   - Hooks: N/A (explicit: no new validation needed)

5. ✅ Added new index file validation
   - Tests: ✅ bash tests/run_tests.sh --category infrastructure --scope docs (exit 0, all passed)
   - Hooks: ✅ Created validate_index_content.py and installed in .pre-commit-config.yaml

6. ✅ Added integration tests for API endpoints
   - Tests: ⚠️ tests missing tags (category/criticality/scope) (tests added but no --category/--criticality flags mentioned)
   - Hooks: N/A (explicit: no validation hooks needed)
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
- [ ] For each completed item, report:
  - [ ] Explicit test evidence (✅) or `⚠️ not found` / `⚠️ tests created but not passing` / `⚠️ tests failed / incomplete` / `⚠️ tests missing tags` / `N/A (explicit)`
  - [ ] Test tagging evidence (category, criticality, scope) or `⚠️ tests missing tags`
  - [ ] Explicit hooks evidence (✅) or `⚠️ hooks may be needed` / `⚠️ hooks created but not installed` / `N/A (explicit)`
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
