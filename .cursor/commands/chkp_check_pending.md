---
# Dadosfera Metadata
category: quality
criticality: high
scope: all
commandId: "044"
version: "2.5.0"
type: "ch_check_pending"
canonical: "docs-fera@/commands/chkp_check_pending.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/chkp_check_pending.md"
backlinks:
  - "commands/reva_review_active_conversation.md"
  - "commands/arch_archive.md"
  - "commands/gswp_git_sweep.md"
  - "guides/collaboration/pending_to_merge_worktree.md"
  - "mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md"

# Claude Code Metadata
name: "Check Pending"
description: "Check for pending tasks, uncommitted changes, and incomplete work items"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 044 -->
<!-- COMMAND_VERSION: 2.5.0 -->
<!-- COMMAND_TYPE: ch_check_pending -->
<!-- UPDATED: 2026-07-08 - Pending-to-merge worktree (Step 1.10): map other-agent work into a durable shared plan instead of leaving it in the disposable report; "Other Agents' Work" + "What Happens Next" hard-fork sections replace the loose Notes ending -->
# /chkp_check_pending

**Command**: `/chkp_check_pending`

**Read-only validation.** Extract and list explicitly pending tasks and proposed actions (that were ignored or not seen) from the current conversation, **check for uncommitted changes, unpushed commits, and hook-related push blockers** (separated by conversation source), and **audit regression-prevention evidence for completed tasks** — without analysis, classification, or scope suggestions.

**Concurrent-agent safety**: If another agent may be live in this repo, do your work in **your own git worktree** (one worktree per agent) before any `checkout`/`reset`/`stash`/`merge`/`clean` — in a shared checkout those operations silently destroy another agent's uncommitted work, at any change size. SSoT: `guides/collaboration/multi_agent_worktree_workflow.md`.

**Critical rule — no action on other-agent work**: Items classified "From Other Conversations/Agents" (Step 1.3/1.5) are **display-only** in this conversation. Never propose committing them, never editorialize about whether they're "in scope," never take any action regarding them — they are mapped into the shared pending-to-merge plan (Step 1.10) for `/gswp_git_sweep` to handle later. See `guides/collaboration/pending_to_merge_worktree.md`.

**Critical rule — no self-initiated git writes**: This command never runs `git add`, `git commit`, or `git push`, and never stages anything in the primary checkout. Its only side-effect write is appending one entry to the pending-to-merge plan file inside the dedicated worktree (Step 1.10) — that worktree is never the tree this conversation is working in.

**Strict "No Lazy Done" Policy**:
- Do **not** accept a task as "Done" just because the user said so.
- If a task is claimed as "Done" but lacks **Evidence** (tests/hooks/lint), explicit `⚠️` flags MUST be prominent.
- Trust artifacts (files, test outputs), not promises.

For completed tasks, audit and flag missing/failed evidence across:
- **Tests** (unit/integration/regression/mutation/etc., as applicable) + **test tagging**
- **Git hooks** (pre-commit / pre-push) and whether they're installed/configured
- **Linting/static checks** (often via pre-commit: ruff, shellcheck, YAML/JSON checks)
- **Runtime / OS-level validation** (running the thing, smoke checks, CLI exit codes, health checks)
- **Documentation + inline comments** (README/AGENTS/guides updates; docstrings/in-line comments for non-obvious logic)

Flags incomplete/failed evidence as `⚠️` warnings.
Uses `⚪` for missing evidence that is likely not necessary (benign missing).

This command is strictly informational—use it to get a quick, unadorned view of what remains to be done in the conversation. No routing, no recommendations, no out-of-scope ideas.

## Command sequence (run in order)

0. Count command invocations in this conversation

Scan the conversation history (see Step 0.5 for how to access it) to count how many times `/chkp_check_pending` (or `/chkp`) has been invoked in the current conversation. Include all variations:
- `/chkp_check_pending`
- `/chkp`
- Explicit mentions like "run chkp_check_pending" or "execute chkp"

**Report**: "**Command Run Count**: N (this is the Nth time this command has been run in this conversation)"

0.5. Access conversation history (authoritative source for the initial goal)

This command depends on the **first user message**, which is often **not fully present** in the current context window. You MUST attempt to access the full conversation transcript before extracting the initial goal or conversation-scoped files.

**Primary method (preferred)**: Use Cursor conversation transcripts

- **Look for an explicit transcript path** in the current session context, previous summaries, or prior notes.
- If no path is provided, check for Cursor transcripts under:
  - `$HOME/.cursor/projects/*/agent-transcripts/*.txt`

If multiple transcript files exist, select the **most recently modified** transcript in the matching project directory (or the one whose filename is referenced in prior summaries).

Example (read-only) discovery commands:

```bash
# List candidate transcript files (newest first)
ls -t "$HOME/.cursor/projects"/*/agent-transcripts/*.txt 2>/dev/null | head -25
```

Example (read-only) transcript read commands:

```bash
# Read the top of the transcript to capture the first user message (authoritative initial goal source)
TRANSCRIPT_PATH="/absolute/path/to/transcript.txt"
sed -n '1,200p' "$TRANSCRIPT_PATH"
```

**Fallback method**: Use available conversation context only

If no transcript file is accessible, proceed using only the current conversation context, but you MUST add a limitation note in the output:
- `⚠️ Transcript not found/readable; initial goal identification may be incomplete (context window limitation).`

1. Confirm repository context and check git status (uncommitted, committed, pushed)

```bash
gtimeout 5 git rev-parse --show-toplevel
```

**Step 1.1: Check for uncommitted changes (working directory)**

```bash
# Get all uncommitted changes (staged + unstaged)
gtimeout 5 git status --porcelain=v1

# Get staged files
gtimeout 5 git diff --name-only --cached | sed '/^$/d' || true

# Get unstaged files
gtimeout 5 git diff --name-only | sed '/^$/d' || true
```

**Step 1.2: Identify files from current conversation**

Extract from the conversation history (prefer transcript from Step 0.5):
- Files explicitly mentioned (e.g., "update commands/chkp_check_pending.md", "modify src/utils.ts")
- Files referenced in code blocks, file paths, or edit operations
- Files mentioned in task descriptions or completion markers

Create a set: **CONVERSATION_FILES** = {all files mentioned/modified in this conversation}

**Step 1.3: Classify uncommitted changes by source**

```bash
# For each file in git status output, check if it's in CONVERSATION_FILES
# This will be done by the AI agent comparing the git output against conversation context
```

**Classification logic**:
- **From current conversation**: Files that appear in both git status AND CONVERSATION_FILES
- **From other conversations/agents**: Files that appear in git status but NOT in CONVERSATION_FILES

**Step 1.4: Check for unpushed commits**

```bash
# Check if there are commits ahead of origin
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
UNPUSHED_COUNT=$(git rev-list HEAD...origin/$CURRENT_BRANCH --count 2>/dev/null || echo "0")

# Get list of unpushed commits
if [ "$UNPUSHED_COUNT" -gt 0 ]; then
  # Get commit hashes and messages
  gtimeout 10 git log origin/$CURRENT_BRANCH..HEAD --oneline --format="%h %s"

  # Get files changed in unpushed commits
  gtimeout 10 git diff --name-only origin/$CURRENT_BRANCH..HEAD

  # Check if pre-commit hooks would fail (dry-run)
  if command -v pre-commit >/dev/null 2>&1; then
    # Prefer ref-diff mode to avoid scanning the whole repo (prevents shellcheck timeouts)
    if git rev-parse --verify "origin/$CURRENT_BRANCH" >/dev/null 2>&1; then
      gtimeout 20 pre-commit run --hook-stage pre-push --from-ref "origin/$CURRENT_BRANCH" --to-ref HEAD 2>&1 | grep -q "Failed\\|error" && HOOK_ERRORS="yes" || HOOK_ERRORS="no"
    else
      gtimeout 20 pre-commit run --hook-stage pre-push 2>&1 | grep -q "Failed\\|error" && HOOK_ERRORS="yes" || HOOK_ERRORS="no"
    fi
  else
    HOOK_ERRORS="unknown"
  fi
fi
```

**Step 1.4b: Distinguish stale remote-tracking branches from genuinely unmerged work**

Local listings such as `git branch -a` often show stale `remotes/origin/chore/...` refs **after** their PRs were merged and the remote head was deleted. These look like "branches pending to merge" but are not. To avoid false alarms in the report:

```bash
# 1) Prune local remote-tracking refs that no longer exist on origin
gtimeout 15 git fetch --prune origin

# 2) For each remaining remote branch (other than the default), check whether
#    its tip is already an ancestor of origin/<DEFAULT_BRANCH>.
DEFAULT_BRANCH=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || echo main)
gtimeout 15 git for-each-ref --format='%(refname:short)' refs/remotes/origin \
  | grep -v "^origin/HEAD$" \
  | grep -v "^origin/$DEFAULT_BRANCH$" \
  | while read -r ref; do
      sha=$(git rev-parse "$ref" 2>/dev/null) || continue
      if git merge-base --is-ancestor "$sha" "origin/$DEFAULT_BRANCH" 2>/dev/null; then
        echo "STALE_MERGED  $ref  (already in origin/$DEFAULT_BRANCH; safe to delete on remote)"
      else
        unique=$(git log --oneline "origin/$DEFAULT_BRANCH..$ref" 2>/dev/null | wc -l | tr -d ' ')
        echo "UNMERGED      $ref  (commits not in origin/$DEFAULT_BRANCH: $unique)"
      fi
    done
```

Report the two classes separately:

- **Stale-but-merged remote branches**: not pending; flag for cleanup with `git push origin --delete <branch>` (admin-only; requires authorization).
- **Genuinely unmerged remote branches**: count toward "Unpushed/Pending" only if they contain commits **not** yet in `origin/$DEFAULT_BRANCH`.

This prevents the recurrent false-positive "we still have N branches pending to merge" report when the underlying refs are merely stale local mirrors of already-merged history.

**Step 1.5: Classify unpushed commits by source**

For each unpushed commit:
- Get files changed in that commit
- Compare against CONVERSATION_FILES
- If any file in the commit matches CONVERSATION_FILES → classify as "from current conversation"
- If no files match → classify as "from other conversations/agents"

**Step 1.6: Stash audit**

```bash
gtimeout 5 git stash list

# For each stash entry, inspect size and age (manual review in report):
# gtimeout 10 git stash show --stat stash@{N}

# Flag ORPHAN_STASH when message matches WIP|gscv|Pre-merge and age > 24h
# (agent estimates age from stash message timestamp or reflog if present)

# Optional: count recoverable unreachable commits
gtimeout 30 git fsck --unreachable 2>/dev/null | grep -c 'unreachable commit' || echo "0"
```

Report in **Stash & orphan WIP** section (see output format). Flag `⚠️ ORPHAN_STASH` for stashes matching WIP/gscv/Pre-merge patterns older than 24 hours.

**Step 1.7: Ghost feature heuristic (optional — repos with i18n/locale)**

When the repo has `i18n/`, `locales/`, or `**/locale*.json`:

```bash
# Example: UX help strings referencing pickers/format without matching component in git ls-files
# Agent compares new/changed i18n keys (*_picker_*, *_format_help*) against git ls-files for .jsx/.py/.tsx
```

If UX copy promises UI behavior but no corresponding component/state handler exists in git → flag `⚠️ GHOST_I18N` with key paths. See `guides/quality/ghost_feature_detection.md`.

**Step 1.8: WIP gate — FILES_CREATED vs IN_GIT**

From conversation tool-call history, build **FILES_CREATED**. For each path, check whether it appears in a commit on the current branch:

```bash
# Per path in FILES_CREATED:
gtimeout 5 git log -1 --oneline -- "<path>" 2>/dev/null || echo "NOT_IN_GIT"
gtimeout 5 git ls-files --error-unmatch "<path>" 2>/dev/null && echo "tracked" || echo "untracked"
```

**Gate rule**: If `IN_GIT < FILES_CREATED`, the report MUST show `⚠️ WIP_NOT_IN_GIT` prominently and recommend `/gscv_git_sync_conversation` or user commit before `/arch_archive`.

**Step 1.9: Determine software lifecycle floor (ADDF) for maturity-gated evidence**

Some evidence expectations (notably **cosmetic linting**) are **floor-gated**. Determine the repository's **Software Lifecycle Floor** using:

```bash
# Preferred: README marker (authoritative), else directory-based detection
python3 _dev/scripts/maturity/detect_lifecycle_floor.py
```

**Step 1.10: Map other-agent pending work into the shared pending-to-merge plan**

SSoT: `guides/collaboration/pending_to_merge_worktree.md`. **Run this step only when Step 1.3/1.5 classified ≥1 file or commit as "From Other Conversations/Agents."** On a clean run (nothing in that bucket), skip this step entirely — do not create or touch the worktree.

```bash
# 1) Repo-type detection (fera vs non-fera) — see guides/documentation/project_taxonomy.md
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
if [[ "$REPO_NAME" =~ -fera$ ]]; then
  PLANS_DIR="_dev/docs/plans"
else
  PLANS_DIR="docs/plans"
fi

# 2) Ensure the staging worktree exists for this run (create only if missing)
WT_PATH="$(dirname "$REPO_ROOT")/${REPO_NAME}-wt-pending-to-merge"
if ! git worktree list | grep -q "$WT_PATH"; then
  git worktree add "$WT_PATH" -b chore/pending-to-merge main 2>/dev/null || \
  git worktree add "$WT_PATH" chore/pending-to-merge
fi

# 3) Append one dated entry to the rolling aggregate plan (create from template if absent)
PLAN_FILE="$WT_PATH/$PLANS_DIR/active/pending_to_merge_aggregate.md"
mkdir -p "$(dirname "$PLAN_FILE")"
```

Append a dated entry listing exactly the files/commits already classified "From Other Conversations/Agents" above (repo name, timestamp, conversation identifier if known) — see the entry template in the SSoT guide. **This is a content-only file write.** Do not run `git add`, `git commit`, or `git push` in `$WT_PATH` — that belongs to `/gswp_git_sweep` Phase 2.5, never to this command.

Report back one summary line: "→ N other-agent item(s) mapped to `$WT_PATH/$PLANS_DIR/active/pending_to_merge_aggregate.md` (pending `/gswp_git_sweep`)."

**Report git status**:

```markdown
## Git Status

### Uncommitted Changes (Working Directory)

**From Current Conversation**: N files
- [List of files with status: M=modified, A=added, D=deleted, R=renamed]
  - `M  path/to/file1.md` (modified)
  - `A  path/to/file2.ts` (added)

**From Other Conversations/Agents**: M files
- [List of files with status]
  - `M  path/to/other_file.py` (modified)

**Total Uncommitted**: N + M files

### Committed but Unpushed

**From Current Conversation**: X commits
- Commit hash: message (files changed: N)
  - `abc1234` Fix issue in commands/chkp_check_pending.md (1 file: commands/chkp_check_pending.md)

**From Other Conversations/Agents**: Y commits
- Commit hash: message (files changed: M)
  - `def5678` Update unrelated feature (3 files: src/other.py, tests/other_test.py, README.md)

**Total Unpushed**: X + Y commits
- Status: ✅ All pushed | ⚠️ X+Y commits ahead (not blocked) | ⚠️ X+Y commits ahead - blocked by hook errors
- Hook status: [✅ Pass | ⚠️ Fail | ⚪ Unknown/Not configured]

### Stash & orphan WIP

- stash@{N}: `<message>` (age) [⚠️ ORPHAN_STASH if applicable]
- Recoverable unreachable commits: N (`git fsck --unreachable`)

### WIP gate (FILES_CREATED vs IN_GIT)

- **FILES_CREATED**: N (from conversation tool calls)
- **IN_GIT**: X/N
- Status: ✅ All deliverables committed | ⚠️ WIP_NOT_IN_GIT — run `/gscv` or ask user to commit before archive

### Ghost features (when i18n present)

- [⚠️ GHOST_I18N key paths or "none detected"]
```

**Simplified status indicators**:
- ✅ **All clean**: No uncommitted changes, all commits pushed
- ⚠️ **Uncommitted from this conversation**: N files need to be committed
- ⚠️ **Uncommitted from other sources**: M files from other work (may need separate handling)
- ⚠️ **Unpushed from this conversation**: X commits need to be pushed
- ⚠️ **Unpushed from other sources**: Y commits from other work (may need separate handling)
- ⚠️ **Blocked by hooks**: Pre-commit/pre-push hooks are failing

2. Extract initial goal versus other goals from conversation (and goal status)

Scan the conversation history (prefer transcript from Step 0.5) to identify:

- ✅ **Initial goal**: The primary objective stated in the first user message or the first explicit goal statement in the conversation. This is the main purpose that initiated the conversation.
- ✅ **Other goals introduced later**: Any additional goals, objectives, or scope expansions that were introduced after the initial goal (e.g., "also do X", "while we're at it, let's Y", "I also need Z").

For each identified goal, you MUST also determine:

- ✅ **Goal reached status**:
  - `✅` **Reached**: There is explicit evidence in the conversation that the goal was achieved (e.g., deliverable exists, explicit completion statement, or equivalent concrete outcome).
  - `⚠️` **Not reached (but mapped)**: The goal is not yet achieved, but the tasks required to reach it are clearly mapped into an explicit plan artifact.
  - `❌` **Not reached (not mapped)**: The goal is not achieved AND there is no evidence that the tasks required to reach it are mapped into a plan. This is a red error indicator and MUST be shown prominently for the goal.

- ✅ **Plan mapping (only required when goal is not reached)**:
  - A goal is considered **mapped into a plan** when the conversation includes (and/or the repo contains) an explicit plan artifact that captures the tasks needed to reach the goal, such as:
    - `_dev/docs/plans/active/*.md`
    - `_dev/docs/plans/backlog/*.md`
    - `_dev/docs/plans/finished/*.md`
  - Mapping evidence can be:
    - A plan file path referenced in the conversation, plus a clear statement that the goal's tasks are in that plan
    - A plan file created/edited in this conversation whose title/summary/tasks clearly correspond to achieving the goal
  - If mapping is **unclear**, treat it as **not mapped** and use `❌`.

- ✅ **Strict formatting requirement (when status is `❌`)**:
  - If a goal's status is `❌ Not reached (no plan mapping found)`, then the goal's `**Short summary**:` line MUST include the red emoji **on the same line**, e.g. `**Short summary**: ❌ <one-line goal summary>`.

**Format for extraction**:
- **Initial goal**: Extract as a very short line (one sentence or phrase) followed by a descriptive paragraph explaining the context and scope.
- **Other goals**: List each with a very short line followed by a descriptive paragraph, indicating when/how they were introduced relative to the initial goal.

**Identification criteria**:
- The initial goal is typically found in:
  - The first user message (**authoritative**; use transcript if available per Step 0.5)
  - The first explicit task/request statement
  - The first "I need to..." or "Please help me..." statement
- Other goals are typically introduced with:
  - "Also", "Additionally", "While we're at it", "I also need", "Can we also"
  - Explicit scope expansions or new task introductions after the initial work has started
  - Side conversations or tangents that introduce new objectives

3. Extract pending items from conversation

Scan the conversation history (prefer transcript from Step 0.5) for:

- ✅ **Explicit "pending" markers** (e.g., `- [ ] Task`, `**Pending:**`, `TODO:`, `FIXME:`)
- ✅ **Unfinished tasks** (e.g., marked as `in_progress`, `blocked`, `waiting`, `open`)
- ✅ **Explicit commitments** that the user or AI committed to _in this conversation_ but did not complete (e.g., "I'll do X next")

3.5. Extract proposed actions that were ignored or not seen

**Purpose**: Detect AI proposals/recommendations that include actionable items but were not executed or explicitly acknowledged by the user.

**Detection patterns** (scan for AI messages containing):
- ✅ **Recommendation sections**: Headings like "## Recommendation", "## Recommendations", "**Recommendation:**", "**Recommendations:**"
- ✅ **Proposal questions**: "Should I", "Would you like me to", "Can I", "I can", "I could" followed by specific actionable items
- ✅ **Actionable proposals**: Statements that include:
  - Specific file paths to create/modify (e.g., "Create `path/to/file.md`")
  - Specific commands to run (e.g., "Run `npm install`")
  - Specific changes to make (e.g., "Update the function to...")
  - Specific features to implement (e.g., "Add authentication endpoint")
- ✅ **Multiple proposals for same issue**: When multiple proposals address the same problem/need, detect and consolidate

**Exclusion criteria** (do NOT mark as pending if):
- ✅ **Explicitly rejected**: User said "no", "don't", "skip", "not needed", "ignore", or similar rejection
- ✅ **Explicitly deferred**: User said "later", "not now", "maybe later", "we'll do that later", or similar deferral
- ✅ **Already executed**: Evidence of execution found (files created, commands run, changes made) - check against CONVERSATION_FILES and completion markers
- ✅ **User acknowledged but chose different approach**: User responded with alternative solution or different action
- ✅ **Out of scope**: Proposal was explicitly marked as "out of scope", "future work", or "not in this conversation"

**Deduplication logic** (when multiple proposals address same issue):
- ✅ **Group by issue**: Identify proposals that address the same underlying problem or need
- ✅ **Select best proposal**: For each group, select the proposal that is:
  1. **Most specific and actionable** (includes file paths, exact commands, clear steps)
  2. **Most comprehensive** (covers the full scope of the issue)
  3. **Most recent** (if specificity and comprehensiveness are equal, prefer the latest)
  4. **Most professional** (follows standards, includes proper structure, considers edge cases)
- ✅ **Mark others as superseded**: Note that other proposals for the same issue exist but are superseded by the selected one

**Verification steps**:
1. For each detected proposal:
   - Check if files mentioned in proposal exist (if file creation was proposed)
   - Check if commands mentioned were executed (if command execution was proposed)
   - Check if changes mentioned were made (if code changes were proposed)
   - Check for explicit user acknowledgment or rejection
2. If no execution evidence AND no explicit rejection/deferral → mark as pending
3. If multiple proposals for same issue → apply deduplication logic

**Output format for proposed actions**:
- List each pending proposed action with:
  - **Proposal source**: Quote or brief description of where the proposal appeared
  - **Proposed action**: Clear description of what was proposed
  - **Status**: `[?]` (unseen/ignored proposal)
  - **Context**: Why it's pending (e.g., "Proposed but not executed or acknowledged")

4. Extract completed items + test/hooks evidence (completed-only audit)

Scan the conversation history (prefer transcript from Step 0.5) for:

- ✅ **Completed markers** (e.g., `Done:`, `✅`, "fixed", "implemented", "merged", "shipped")
- ✅ **Test evidence markers** (explicit only):
  - **Tests run**: `_dev/tests/run_tests.sh`, `pytest`, `npm test`, `pnpm test`, `yarn test`, `go test`, `cargo test`, `make test`, etc.
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

- ✅ **Linting / static checks evidence markers** (explicit only):
  - **Pre-commit / lint commands run**: `pre-commit run --all-files`, `pre-commit run ruff --all-files`, `ruff`, `ruff format`, `shellcheck`, `yamllint`, etc.
    - **Status check**: Must confirm linting **passed** (exit code 0 or explicit "passed/✅")
    - **⚠️ Flag**: If lint ran but failed/incomplete — mark as `⚠️ lint failed / incomplete`
  - **Explicit N/A**: "no linting needed", or similar _explicitly stated_

- ✅ **Runtime / OS-level validation evidence markers** (explicit only):
  - **Runtime checks**: `bash _dev/tests/run_tests.sh ...` (when it's a runtime harness), `python -m ...`, `node ...`, `make run`, `docker compose up`, `curl /health`, CLI invocations with expected output, service restart + health check, etc.
    - **Status check**: Must confirm runtime validation **passed** (exit code 0, "healthy", "OK", or explicit "passed")
    - **⚠️ Flag**: If runtime validation ran but failed/incomplete — mark as `⚠️ runtime validation failed / incomplete`
  - **Explicit N/A**: "not runnable locally", "docs-only", or similar _explicitly stated_

- ✅ **Documentation + inline comments evidence markers** (explicit only):
  - **Docs updated**: README/AGENTS/guides/patterns/lessons_learned/troubleshooting updated with the change
  - **Inline comments/docstrings updated**: explicit mention of docstring/comment additions for tricky logic
  - **Explicit N/A**: "no docs needed", "self-explanatory change", or similar _explicitly stated_

**Strict filters (CRITICAL - do NOT override)**:

- **No suggestions**: Do not propose new tasks, improvements, or out-of-scope ideas.
- **No classification**: Do not categorize (Active/Backlog/Prioritized). Just list them.
- **No routing**: Do not suggest which plan they belong to.
- **Conversation-scoped only**: Only include items mentioned or worked on in the current conversation.
- **Exclude "future work / not pending" lists**: If the conversation explicitly labels a list or section as _not pending_ (e.g., "These are not pending in this conversation but were identified as future work"), **ignore the entire list** — do not include any of its items.
- **No "Recommended Next Steps" sections**: Do not output headings/sections like "Recommended Next Steps", "Future Work", "Follow-ups", "Nice-to-haves", or similar. `/chkp_check_pending` output is only pending + optional completed.
- **Latest status wins**: If a task status changed during the conversation (e.g., started as pending, completed later), report only the final status.
- **Emoji Severity Levels**:
  - `✅` = **Found & Passed** (Evidence exists and shows success)
  - `⚠️` = **Missing & Needed** (No evidence found, and the task involves code/logic where tests/lint/hooks are typically required) OR **Found & Failed**
  - `⚪` = **Missing & Not Needed** (No evidence found, but the task involves only documentation, plans, text files, or read-only analysis where tests/lint/hooks are generally not applicable)
  - `N/A` = **Explicitly N/A** (User or context explicitly stated it's not needed)

- **Test Evaluation**:
  - **Code changes** (scripts, source code, logic): If no test evidence -> `⚠️ not found`
  - **Non-code changes** (docs, plans, markdown, config values): If no test evidence -> `⚪ not found`
  - **Exceptions**: If tests are failing or incomplete -> `⚠️` regardless of file type.
- **Hooks Evaluation**:
  - **New patterns/logic**: If no hooks evidence -> `⚠️ hooks may be needed`
  - **Standard edits/docs**: If no hooks evidence -> `⚪ not found`
- **Lint Evaluation**:
  - **Code changes**: If no lint evidence -> `⚠️ not found`
  - **Docs/plans**: If no lint evidence -> `⚪ not found`
    - **Do not escalate docs to ⚠️ by default**: This repo's standard is that **Markdownlint is disabled** (purely cosmetic), so documentation files are **not required** to have "markdown lint" evidence.
    - **Floor-aware constraint**: Do **not** require or "expect" cosmetic/style lint evidence unless the conversation explicitly states the repo is **Floor 4+ / lv5** *and* cosmetic linting is enabled.
    - **When cosmetic linting is enabled**: Markdown files must be included and markdownlint should be activated using `config/lint/markdownlint-cosmetic.json`. In that case, missing markdownlint evidence for documentation changes is `⚠️ not found`.
    - **Reference**: `standards/linting/README.md`, `standards/linting/markdownlint_disabled_standard.md`, `mini_prompt/lv5/automated_linting_lv5_mini_prompt.md`

5. Output format (produce this in your message)

Generate a simple, read-only report:

```markdown
## Command Run Count

**Command Run Count**: N (this is the Nth time this command has been run in this conversation)

## Git Status

### Uncommitted Changes (Working Directory)

**From Current Conversation**: N files
- [List files with status]

**From Other Conversations/Agents**: M files
- [List files with status]

**Total Uncommitted**: N + M files

### Committed but Unpushed

**From Current Conversation**: X commits
- [List commits with files changed]

**From Other Conversations/Agents**: Y commits
- [List commits with files changed]

**Total Unpushed**: X + Y commits
- Status: ✅ All pushed | ⚠️ X+Y commits ahead (not blocked) | ⚠️ X+Y commits ahead - blocked by hook errors
- Hook status: [✅ Pass | ⚠️ Fail | ⚪ Unknown/Not configured]

## Conversation Goals

### Initial Goal

**Goal status**: ✅ Reached | ⚠️ Not reached (plan-mapped) | ❌ Not reached (no plan mapping found)

**Plan mapping**: ✅ Mapped to `<plan_path>` | ⚠️ Not mapped (required when status is not reached)

**Short summary**: One-line description of the primary objective

Descriptive paragraph explaining the context, scope, and purpose of the initial goal that started this conversation.

### Other Goals Introduced

**Goal status**: ✅ Reached | ⚠️ Not reached (plan-mapped) | ❌ Not reached (no plan mapping found)

**Plan mapping**: ✅ Mapped to `<plan_path>` | ⚠️ Not mapped (required when status is not reached)

**Short summary**: One-line description of additional goal

Descriptive paragraph explaining when and how this goal was introduced, and its relationship to the initial goal.

## Pending Tasks from Current Conversation

**Total Pending**: N

N. [Status] Task description

- Related context or reason (1–2 lines max)

## Proposed Actions (Unseen/Ignored)

**Note**: This section only appears if there are proposed actions detected. These are actionable proposals made by the AI that were not executed, explicitly rejected, or deferred. They represent potential work that may have been missed.

**Total Proposed Actions**: P

P. [?] Proposed action description

- **Proposal source**: [Brief quote or description of where proposal appeared]
- **Context**: [Why it's pending - e.g., "Proposed but not executed or acknowledged"]
- **Superseded proposals**: [If this is the selected proposal from multiple options, note: "Selected from N proposals addressing the same issue"]

**Note**: If no proposed actions are detected, this section is omitted entirely.

## Completed in This Conversation

**Total Completed**: M
**Completed Missing Test Evidence**: K (total with ⚠️ issue)
- Tests not found: X (use ⚠️ only if > 0)
- Tests created but not passing: Y (use ⚠️ only if > 0)
- Tests failed / incomplete: Z (use ⚠️ only if > 0)
**Completed Missing Hooks Evidence**: H (total with ⚠️ issue)
- Hooks may be needed: A (use ⚠️ only if > 0)
- Hooks created but not installed: B (use ⚠️ only if > 0)
**Completed Missing Test Tagging**: T (total with ⚠️ issue)
- Tests missing tags: T (use ⚠️ only if > 0)
**Completed Missing Lint Evidence**: L (total with ⚠️ issue)
- Lint not found: L1 (use ⚠️ only if > 0)
- Lint failed / incomplete: L2 (use ⚠️ only if > 0)
**Completed Missing Runtime Validation**: R (total with ⚠️ issue)
- Runtime not found: R1 (use ⚠️ only if > 0)
- Runtime validation failed / incomplete: R2 (use ⚠️ only if > 0)
**Completed Missing Docs/Comments Evidence**: D (total with ⚠️ issue)
- Docs/comments not found: D (use ⚠️ only if > 0)

1. ✅ Completed task description
   - Tests: ✅ <evidence> | ⚠️ not found (missing) | ⚪ not found (not needed) | ⚠️ tests created but not passing | ⚠️ tests failed / incomplete | N/A (explicit)
   - Hooks: ✅ <evidence> | ⚠️ hooks may be needed | ⚪ not found (not needed) | ⚠️ hooks created but not installed | N/A (explicit)
   - Lint: ✅ <evidence> | ⚠️ not found (missing) | ⚪ not found (not needed) | ⚠️ lint failed / incomplete | N/A (explicit)
   - Runtime: ✅ <evidence> | ⚠️ not found (missing) | ⚪ not found (not needed) | ⚠️ runtime validation failed / incomplete | N/A (explicit)
   - Docs/Comments: ✅ <evidence> | ⚠️ not found (missing) | ⚪ not found (not needed) | N/A (explicit)

## Other Agents' Work (Awareness Only)

**Note**: This section only appears if Step 1.3/1.5 classified ≥1 file or commit as "From Other Conversations/Agents." Omit entirely on a clean run.

- **Uncommitted**: M files (see Git Status above for the list)
- **Unpushed**: Y commits (see Git Status above for the list)
- **Mapped to shared plan**: `<worktree-path>/<plans-dir>/active/pending_to_merge_aggregate.md` (Step 1.10; see `guides/collaboration/pending_to_merge_worktree.md`)

**Do not act on this. Not part of this conversation's scope.** No commits, no scope commentary, no recommendations regarding these items in this conversation.

## What Happens Next

**This conversation's pending total**: N pending task(s) + P proposed action(s)

Choose one:

1. **Execute now** — work through the pending tasks and proposed actions listed above.
2. **Archive and stop** — run `/arch_archive` to persist findings and close this conversation.

This command does not commit, push, or resolve anything itself, and takes no position on which option to choose.
```

**Status indicators** (See `standards/project/task_status_standard.md`):

- `[ ]` – Not started
- `[~]` – In progress / Partially done
- `[!]` – Blocked (waiting for external input, decision, or dependency)
- `[?]` – Unclear or needs clarification

## Notes

- **Read-only w.r.t. the primary checkout**: This command produces no file changes, plan updates, or artifact creation in the repo/branch this conversation is working in. Step 1.10's write happens only in the dedicated, separate pending-to-merge worktree, and only when other-agent work was found — never in the primary checkout, and never followed by a commit.
- **Zero scope creep**: This command is designed to prevent the user from drifting into secondary tasks or new ideas. Use `/reva_review_active_conversation` if you want comprehensive analysis and routing suggestions.
- **Use after active work**: Run `/chkp_check_pending` near the end of a session to verify what still needs to be done before closing the conversation.
- **Minimal effort**: The output should be scannable in 10 seconds or less.
- **No interaction required**: The user does not need to confirm, approve, or authorize anything; this is pure reporting.
- **Proposed actions detection**: The command now detects AI proposals/recommendations that were not executed or explicitly acknowledged, helping catch work that may have been missed. When multiple proposals address the same issue, only the best (most specific, comprehensive, recent, and professional) is shown.
- **Hard fork, not a suggestion**: The report always ends with "What Happens Next" — execute now, or `/arch_archive` and stop. This command must never trail off into attempting a commit, or explaining why other-agent items are out of scope; that explanation already lives in "Other Agents' Work" above and does not need repeating.

## Relationship to other commands

- **`/chkp_check_pending`** (this command): **Minimal read-only snapshot** of pending work. No suggestions.
- **`/reva_review_active_conversation`**: **Full conversation analysis** with classification and routing. Use when you want suggestions for next steps.
- **`/arch_archive`**: **Persistence** of conversation findings into plans. Often used after `/reva_review_active_conversation` to formally route tasks into the planning system.
- **`/pfac_plan_from_active_tasks_conversation`**: **Mid-conversation plan sync** (updates only active plans; not a full review).
- **`/gswp_git_sweep`**: **Commits, pushes, and cleans** the shared pending-to-merge plan this command maps other-agent work into (Step 1.10 → its Phase 2.5). This command never commits/pushes it itself.

## Workflow checklist

### For AI Agent:

- [ ] Count how many times `/chkp_check_pending` has been invoked in this conversation
- [ ] Access the full conversation history (prefer transcript files; see Step 0.5)
- [ ] Extract files mentioned/modified in the current conversation (CONVERSATION_FILES)
- [ ] Check git status for uncommitted changes (staged + unstaged)
- [ ] Classify uncommitted changes: from current conversation vs other sources
- [ ] Check for unpushed commits and get files changed in each commit
- [ ] Classify unpushed commits: from current conversation vs other sources
- [ ] Check hook status for unpushed commits
- [ ] If any file/commit classified "from other sources": map it into the pending-to-merge worktree's aggregate plan (Step 1.10) — never comment on its scope or propose committing it
- [ ] Identify initial goal from first user message or first explicit goal statement
- [ ] Identify other goals introduced later in the conversation
- [ ] Format goals with short summary line followed by descriptive paragraph
- [ ] Scan conversation for explicit pending markers
- [ ] Scan conversation for AI proposals/recommendations with actionable items
- [ ] Verify proposals were not executed (check files, commands, changes)
- [ ] Verify proposals were not explicitly rejected or deferred
- [ ] Apply deduplication logic for multiple proposals addressing same issue
- [ ] Select best proposal when duplicates exist (specificity > comprehensiveness > recency > professionalism)
- [ ] Apply strict filters (no suggestions, no classification, no routing)
- [ ] Report only conversation-scoped pending items and proposed actions
- [ ] Note completed work separately
- [ ] For each completed item, report:
  - [ ] Explicit test evidence (✅) or `⚠️ not found` / `⚪ not found` / `⚠️ tests created but not passing` / `⚠️ tests failed / incomplete` / `⚠️ tests missing tags` / `N/A (explicit)`
  - [ ] Test tagging evidence (category, criticality, scope) or `⚠️ tests missing tags`
  - [ ] Explicit hooks evidence (✅) or `⚠️ hooks may be needed` / `⚪ not found` / `⚠️ hooks created but not installed` / `N/A (explicit)`
- [ ] Keep output concise and scannable
- [ ] End the report with "Other Agents' Work" (only if non-empty) then "What Happens Next" — never trail off into a commit attempt or scope commentary
- [ ] Do NOT create, modify, add, or commit any file in the primary checkout — the only allowed write is Step 1.10's append inside the dedicated pending-to-merge worktree, and only content, never a git operation

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

---

**Local Reference**: `commands/chkp_check_pending.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/chkp_check_pending.md`

End Command ---

## Annex: Example Output

```markdown
## Command Run Count

**Command Run Count**: 2 (this is the 2nd time this command has been run in this conversation)

## Git Status

### Uncommitted Changes (Working Directory)

**From Current Conversation**: 2 files
- `M  commands/chkp_check_pending.md` (modified)
- `A  _dev/tests/commands/test_chkp_check_pending_structure.sh` (added)

**From Other Conversations/Agents**: 1 file
- `M  scripts/other_script.sh` (modified)

**Total Uncommitted**: 3 files

### Committed but Unpushed

**From Current Conversation**: 1 commit
- `abc1234` Update chkp command to check uncommitted changes (1 file: commands/chkp_check_pending.md)

**From Other Conversations/Agents**: 1 commit
- `def5678` Fix unrelated bug in utils.py (2 files: src/utils.py, tests/test_utils.py)

**Total Unpushed**: 2 commits
- Status: ⚠️ 2 commits ahead - blocked by hook errors (pre-commit validation failing)
- Hook status: ⚠️ Fail (pre-commit hooks failing on lint checks)

## Conversation Goals

### Initial Goal

**Goal status**: ✅ Reached

**Short summary**: Update the `/chkp_check_pending` command to distinguish initial goals from later-introduced goals

The conversation started with a request to modify the `/chkp_check_pending` command to recover and clearly distinguish the initial goal of the conversation versus other goals that were introduced later. The format should use a very short line followed by a descriptive paragraph to make this distinction clear in the command output.

### Other Goals Introduced

**Goal status**: ⚠️ Not reached (plan-mapped)

**Plan mapping**: ✅ Mapped to `_dev/docs/plans/active/QW_2h_HIGH_add_tests_for_goal_extraction.md`

**Short summary**: Add test coverage for the goal extraction logic

Introduced mid-conversation after the initial command update was completed, this goal focuses on ensuring the new goal extraction feature has proper test coverage to validate it correctly identifies initial versus later-introduced goals.

## Pending Tasks from Current Conversation

**Total Pending**: 3

1. [ ] Implement user authentication endpoint

   - HTTP POST /auth/login; needs database schema review first

2. [~] Add unit tests for payment processing

   - 60% done; still need to cover edge cases for refunds

3. [!] Deploy to staging environment
   - Blocked: waiting for ops team approval on resource allocation

## Proposed Actions (Unseen/Ignored)

**Total Proposed Actions**: 2

1. [?] Create API maturity mini prompt covering Swagger, versioning, rate limits, API key UI management, and scoping
   - **Proposal source**: "## Recommendation - Create: An API maturity mini prompt covering Swagger, versioning, rate limits, API key UI management, and scoping"
   - **Context**: Proposed but not executed or acknowledged
   - **Superseded proposals**: Selected from 1 proposal addressing API maturity documentation gap

2. [?] Create documentation clarifying different types of API keys and their use cases
   - **Proposal source**: "## Recommendation - Create: Documentation clarifying the different types of API keys and their use cases"
   - **Context**: Proposed but not executed or acknowledged
   - **Superseded proposals**: Selected from 1 proposal addressing API key type documentation gap

## Completed in This Conversation

**Total Completed**: 6
**Completed Missing Test Evidence**: 1
- Tests not found: 0
- Tests created but not passing: 0
- Tests failed / incomplete: 1
**Completed Missing Hooks Evidence**: 1
- Hooks may be needed: 1
- Hooks created but not installed: 0
**Completed Missing Test Tagging**: 1
- Tests missing tags: 1

1. ✅ Fixed linter errors in src/utils.ts
   - Tests: ✅ bash _dev/tests/run_tests.sh --category infrastructure --criticality high (exit 0, all passed)
   - Hooks: ⚪ not found (not needed)

2. ✅ Updated README with new endpoint docs
   - Tests: ⚪ not found (not needed)
   - Hooks: ⚪ not found (not needed)

3. ✅ Added payment validation function
   - Tests: ⚠️ tests created but not passing (test file added, not yet run)
   - Hooks: ⚠️ hooks may be needed (new validation logic added, may need pre-commit checks)

4. ✅ Refactored auth middleware
   - Tests: ⚠️ tests failed / incomplete (ran `npm test` but saw 3 failures)
   - Hooks: ⚪ not found (not needed)

5. ✅ Added new index file validation
   - Tests: ✅ bash _dev/tests/run_tests.sh --category infrastructure --scope docs (exit 0, all passed)
   - Hooks: ✅ Created validate_index_content.py and installed in .pre-commit-config.yaml

6. ✅ Created project implementation plan
   - Tests: ⚪ not found (not needed)
   - Hooks: ⚪ not found (not needed)

## Other Agents' Work (Awareness Only)

- **Uncommitted**: 1 file (see Git Status above — `scripts/other_script.sh`)
- **Unpushed**: 1 commit (see Git Status above — `def5678`)
- **Mapped to shared plan**: `../docs-fera-wt-pending-to-merge/_dev/docs/plans/active/pending_to_merge_aggregate.md` (Step 1.10; see `guides/collaboration/pending_to_merge_worktree.md`)

**Do not act on this. Not part of this conversation's scope.**

## What Happens Next

**This conversation's pending total**: 3 pending task(s) + 2 proposed action(s)

Choose one:

1. **Execute now** — work through the pending tasks and proposed actions listed above.
2. **Archive and stop** — run `/arch_archive` to persist findings and close this conversation.

This command does not commit, push, or resolve anything itself, and takes no position on which option to choose.
```
