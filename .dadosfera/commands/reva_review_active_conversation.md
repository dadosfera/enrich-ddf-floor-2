# /reva_review_active_conversation
<!-- COMMAND_ID: 041 -->
<!-- COMMAND_VERSION: 1.2.0 -->
<!-- COMMAND_TYPE: re_review -->

**Analysis only - no files modified.** Extract and classify ALL tasks from the conversation into logical sections. **Checks for unpushed commits and hook-related push blockers** before classification.

The command MUST suggest tasks for `/active` and `/backlog` plans – complete classification is the goal. The user decides what to act on afterward.

Keep scope strictly to the current conversation. Do not branch into unrelated topics.

Backlinks:

- mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md
- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- mini_prompt/lv1/post_discovery_codebase_improvement_mini_prompt.md

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

**Report unpushed commits status** in the output:
- ✅ **No unpushed commits**: All commits are pushed
- ⚠️ **Unpushed commits (N)**: N commits ahead of origin (not blocked by hooks)
- ⚠️ **Unpushed commits (N) - blocked by hook errors**: N commits ahead of origin, and pre-commit/pre-push hooks are failing

2. Conversation synthesis (no code changes yet)

- Summarize the explicit objective(s) and constraints.
- List key decisions and fixes/improvements attempted or completed.
- Note any blockers, risks, or assumptions that affect scope.

3. Task extraction and classification

- **Relevance Filter (CRITICAL)**:

  - **Strict Scope**: Only include tasks that were explicitly discussed, requested, or worked on in the **current conversation window**.
  - **Git Status Handling**: Items in `git status` that were _not_ part of the current conversation's goals should be categorized as **Other Context (Unrelated)** or ignored if noisy.
  - **Latest Status Wins**: When a task appears multiple times with different statuses (for example, earlier as active and later as finished), treat the latest status as authoritative. Finished items must be listed only under **Finished Tasks**, never under **Active Tasks**.

- **Routing and Classification** (see `glossaries/project_management.md` for canonical statuses):

  - **Finished Tasks**: Items that are clearly done (success criteria met) either in this conversation or in existing `finished` plans. Summarize them under **Finished Tasks** so they are not mistaken for active work. **MUST audit test results, hooks, and test tagging** (verify tests passed, hooks created/updated when needed, and tests properly tagged) for all finished items.
  - **Active Tasks**: Items the conversation clearly committed to, started, or are currently in progress. Recommended for the current active plan.
  - **Prioritized Tasks**: Out-of-scope items that are high-impact, fully defined, and ready to start next. Recommended for `{PLANS_BASE}/prioritized/`.
  - **Blocked Tasks**: Items that cannot proceed due to dependencies, missing info, or external factors.
  - **Backlog Tasks**: Useful ideas or tasks out-of-scope for the current active plan, not yet refined. Recommended for `{PLANS_BASE}/backlog/`.

- **Routing Path Detection**:

  - For Active/Blocked: Detect the **absolute path** of the target active plan (under `${PLANS_BASE}/active/` only; never treat `${PLANS_BASE}/finished/` plans as active. If a finished plan is referenced, its tasks should appear under **Finished Tasks**, not **Active Tasks**).
  - **Do NOT use meta plans as targets**: Meta plans (filenames containing `_meta_plan`) only coordinate other plans; they must never be selected as `Target Active Plan`. When the conversation centers on a meta plan, route each concrete task into specific QW*/CB*/SEC\_/… plans under `active/`, or into `prioritized/` / `backlog` as appropriate.
  - For Prioritized: Detect the **absolute path** of the target prioritized plan.
  - For Backlog: Detect the **absolute path** of the target backlog plan.

4. Output format (produce this in your message)

- **Git Push Status** (start with this):

  - **Unpushed Commits**: N
  - **Status**: ✅ All pushed | ⚠️ N commits ahead (not blocked) | ⚠️ N commits ahead - blocked by hook errors

- **Conversation Context**:

  - **Main Objective**: One sentence summary of what the user originally wanted to achieve.
  - **Goals**: 1–3 bullet points listing the key goals of this specific conversation.

- **Use a single global task counter for all tasks**:

  - Start at **1** and increment for every new task.
  - Do **not** restart numbering in later sections.

- **Plan Path Display Logic**:

  - Display **Target Active Plan**: `<absolute_path_to_active_plan>` at the top if it applies to most active sections.
  - Otherwise, display **Plan Path**: `<path>` inside each relevant section.

- **Structure the response with these sections (in this order)**:

  1. **Finished Tasks** (Completed in this or previous sessions; should not be repeated under Active. **Include explicit test/hooks/tagging evidence** similar to `/chkp_check_pending` output: ✅ evidence | ⚠️ issue | N/A)
  2. **Active Tasks** (Currently being worked on)
  3. **Prioritized Tasks** (Ready to start, waiting for active slot)
  4. **Blocked Tasks** (Cannot proceed due to dependency)
  5. **Backlog Tasks** (Future / Not yet refined)
  6. **Other Context (Unrelated)** (Pending git changes not part of this task)

- Under each section, list tasks as `N. <task>` with a short rationale tying each task back to the conversation.

5. Optional local references (for validation; do not create or move plans here)

```bash
gtimeout 5 git status --short
```

```bash
# Detect plans base for repo type
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
[[ "$REPO_NAME" == *-fera ]] && PLANS_BASE="_dev/docs/plans" || PLANS_BASE="docs/plans"
gtimeout 5 ls -1 "$PLANS_BASE" 2>/dev/null | head -50
```

## Notes

- This command is **read-only with respect to planning docs**: it must not create, move, or edit files under the plans directory (`_dev/docs/plans/` for -fera repos, `docs/plans/` for others).
- Keep scope tight to the current conversation’s problem; avoid unrelated initiatives even if they look attractive.
- Be concise and actionable; prefer fewer, clearer tasks over an exhaustive but noisy list.

## Example Output

```markdown
**Git Push Status**

**Unpushed Commits**: 2
- Status: ⚠️ 2 commits ahead - blocked by hook errors (pre-commit validation failing)

**Main Objective**: Refactor the review command to improve clarity and reduce redundancy.
**Goals**:

- Optimize output format for active plans.
- Add conversation context summary.

**Target Active Plan**: `/Users/me/projects/my-repo/{PLANS_BASE}/active/QW_2h_HIGH_update_reviews.md`

**Finished Tasks**

1. Move `old_plan.md` to `finished/` – already completed in a previous session
   - Tests: N/A (explicit: docs-only change)
   - Hooks: N/A (explicit: docs-only change)

**Active Tasks**

2. Fix linter errors in `commands/reva_review_active_conversation.md` – introduced during command update
3. Update README.md to reference new review command structure – mentioned but not completed

**Prioritized Tasks**
**Plan Path**: `/Users/me/projects/my-repo/{PLANS_BASE}/prioritized/QW_1h_HIGH_git_cleanup.md`

4. Run `git sync` to push changes – ready to execute, no blockers

**Blocked Tasks**

5. Verify output with user – waiting for user feedback

**Backlog Tasks**
**Plan Path**: `/Users/me/projects/my-repo/{PLANS_BASE}/backlog/LI_1d_LOW_future_automation.md`

6. Automate command sync across all repos – nice-to-have for future
7. Add command versioning system – discussed as potential enhancement

**Other Context (Unrelated)**

- Modified `rules/some_rule.md` (pending commit from previous task)
- Untracked file `temp_script.sh`
```

## Relationship to other commands

- **`/reva_review_active_conversation`** (this command): **Complete analysis, no side effects.**
  - Classifies ALL tasks from the conversation.
  - Suggests routing for every task.
  - No files are created or modified.
- **`/arch_archive`**: Persistence and archival.
  - Saves the conversation to archives.
  - Updates plans with the classified tasks.
- **`/pfac_plan_from_active_tasks_conversation`**: Mid-conversation plan sync.
  - Updates a specific active plan only (`_dev/docs/plans/active/` for -fera repos, `docs/plans/active/` for others).

--- End Command ---
