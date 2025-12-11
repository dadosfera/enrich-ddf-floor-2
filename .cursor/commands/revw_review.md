# /revw_review

**Analysis only - no files modified.** Extract and classify ALL tasks from the conversation into logical sections.

The command MUST suggest tasks for `/active` and `/backlog` plans - complete classification is the goal. The user decides what to act on afterward.

Keep scope strictly to the current conversation. Do not branch into unrelated topics.

Backlinks:

- mini_prompt/lv1/mini_prompt_meta_plan_mini_prompt.md
- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- mini_prompt/lv1/post_discovery_codebase_improvement_mini_prompt.md

## Command sequence (run in order)

1. Confirm repository context (for references only)

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Conversation synthesis (no code changes yet)

- Summarize the explicit objective(s) and constraints.
- List key decisions and fixes/improvements attempted or completed.
- Note any blockers, risks, or assumptions that affect scope.

3. Task extraction and classification

- **Relevance Filter (CRITICAL)**:
  - **Strict Scope**: Only include tasks that were explicitly discussed, requested, or worked on in the **current conversation window**.
  - **Git Status Handling**: Items in `git status` that were _not_ part of the current conversation's goals should be categorized as **Other Context (Unrelated)** or ignored if noisy.

- **Routing and Classification** (see `glossaries/project_management.md` for canonical statuses):
  - **Active Tasks**: Items the conversation clearly committed to, started, or are currently in progress. Recommended for the current active plan.
  - **Prioritized Tasks**: Out-of-scope items that are high-impact, fully defined, and ready to start next. Recommended for `{PLANS_BASE}/prioritized/`.
  - **Blocked Tasks**: Items that cannot proceed due to dependencies, missing info, or external factors.
  - **Backlog Tasks**: Useful ideas or tasks out-of-scope for the current active plan, not yet refined. Recommended for `{PLANS_BASE}/backlog/`.

- **Routing Path Detection**:
  - For Active/Blocked: Detect the **absolute path** of the target active plan (use specific plan, not meta plan).
  - For Prioritized: Detect the **absolute path** of the target prioritized plan.
  - For Backlog: Detect the **absolute path** of the target backlog plan.

4. Output format (produce this in your message)

- **Conversation Context** (Start with this):
  - **Main Objective**: One sentence summary of what the user originally wanted to achieve.
  - **Goals**: 1-3 bullet points listing the key goals of this specific conversation.

- **Use a single global task counter for all tasks**:
  - Start at **1** and increment for every new task.
  - Do **not** restart numbering in later sections.

- **Plan Path Display Logic**:
  - Display **Target Active Plan**: `<absolute_path_to_active_plan>` at the top if it applies to most active sections.
  - Otherwise, display **Plan Path**: `<path>` inside each relevant section.

- **Structure the response with these sections (in this order)**:
  1. **Active Tasks** (Currently being worked on)
  2. **Prioritized Tasks** (Ready to start, waiting for active slot)
  3. **Blocked Tasks** (Cannot proceed due to dependency)
  4. **Backlog Tasks** (Future / Not yet refined)
  5. **Other Context (Unrelated)** (Pending git changes not part of this task)

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
**Main Objective**: Refactor the review command to improve clarity and reduce redundancy.
**Goals**:

- Optimize output format for active plans.
- Add conversation context summary.

**Target Active Plan**: `/Users/me/projects/my-repo/{PLANS_BASE}/active/QW_2h_HIGH_update_reviews.md`

**Active Tasks**

1. Fix linter errors in `commands/revw_review.md` – introduced during command update
2. Update README.md to reference new review command structure – mentioned but not completed

**Prioritized Tasks**
**Plan Path**: `/Users/me/projects/my-repo/{PLANS_BASE}/prioritized/QW_1h_HIGH_git_cleanup.md`

3. Run `git sync` to push changes – ready to execute, no blockers
4. Move `old_plan.md` to `finished/` – fully defined, next in queue

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

**Key points from this example:**

- Global numbering: 1→7 across all sections.
- Logical flow: Active → Prioritized → Blocked → Backlog (canonical status order).
- **Target Active Plan** shown once at top.
- Clear separation by canonical status (see `glossaries/project_management.md`).

## Relationship to other commands

- **`/revw_review`** (this command): **Complete analysis, no side effects.**
  - Classifies ALL tasks from the conversation.
  - Suggests routing for every task.
  - No files are created or modified.

- **`/arch_archive`**: **Persistence and archival.**
  - Saves the conversation to archives.
  - Updates plans with the classified tasks.

- **`/pfac_plan_from_active_tasks_conversation`**: **Mid-conversation plan sync.**
  - Updates a specific active plan only (`_dev/docs/plans/active/` for -fera repos, `docs/plans/active/` for others).

--- End Command ---
