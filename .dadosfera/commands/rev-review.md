# /rev-review

Review the entire conversation to extract and classify tasks, then route them toward the right planning docs: (1) **pending tasks** that were committed/started but not finished, and (2) **proposed-but-not-initiated tasks**, each split by whether they belong in the current active plan or in a backlog plan. Keep scope strictly to the current problem; do not branch into new topics or edit plans directly from this command.

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

- **Status dimension** (mutually exclusive):
  - **Pending**: Items the conversation clearly committed to and/or started but did not finish.
  - **Proposed (not initiated)**: Suggestions or ideas that were raised but never started.
- **Routing dimension** (mutually exclusive per task for this review):
  - **Recommended to current active plan**: Tasks that advance the current objective and should live in the closest `docs/plans/active/` plan (often via `/plan_from_active_tasks_conversation`).
  - **Recommended to backlog plan**: Tasks that are useful but out-of-scope for the current active plan, better tracked under `docs/plans/backlog/`.
- Every task must get **exactly one Status** (Pending vs Proposed) and **one Routing** (Active vs Backlog); do **not** duplicate the same task across sections.

4. Output format (produce this in your message)

- **Use a single global task counter for all tasks**:
  - Start at **1** and increment for every new task.
  - Do **not** restart numbering in later sections.
- Structure the response with these sections (in this order):
  - **Pending Tasks – recommended to current `/active` plan (or TBD `/active` plan)**
  - **Proposed Tasks – recommended to current `/active` plan (or TBD `/active` plan)**
  - **Pending Tasks – recommended to a `/backlog` plan**
  - **Proposed Tasks – recommended to a `/backlog` plan**
- Under each section, list tasks as `N. <task>` with a short rationale tying each task back to the conversation (why it matters, where it came from).
- Do **not** create a separate “Next tasks” section; prioritization is implied by whether a task is routed to the current active plan vs backlog.

5. Optional local references (for validation; do not create or move plans here)

```bash
gtimeout 5 git status --short
```

```bash
gtimeout 5 ls -1 docs/plans 2>/dev/null | head -50
```

## Notes

- This command is **read-only with respect to planning docs**: it must not create, move, or edit files under `docs/plans/`.
- Keep scope tight to the current conversation’s problem; avoid unrelated initiatives even if they look attractive.
- Be concise and actionable; prefer fewer, clearer tasks over an exhaustive but noisy list.

## Example Output

```markdown
**Pending Tasks – recommended to current `/active` plan**

1. Fix linter errors in `commands/gis-review.md` – introduced during command update
2. Update README.md to reference new review command structure – mentioned but not completed

**Proposed Tasks – recommended to current `/active` plan** 3. Add pre-commit hook to validate command format – suggested as quality improvement

**Pending Tasks – recommended to `/backlog` plan** 4. Create visual diagram of command relationships – started research but out of scope

**Proposed Tasks – recommended to `/backlog` plan** 5. Automate command sync across all repos – nice-to-have for future 6. Add command versioning system – discussed as potential enhancement
```

**Key points from this example:**

- Global numbering: 1→6 across all sections (no restarts)
- Each task appears exactly once (no duplicates)
- Rationale ties each task back to conversation context
- Routing is clear: tasks 1-3 go to active plan, tasks 4-6 go to backlog

## Relationship to other commands

- **`/review`**: Analyzes the conversation and **classifies tasks** (Pending vs Proposed, Active-plan vs Backlog-plan) with a single global numbering sequence. It only produces a structured task list; it does **not** edit any plan files.
- **`/plan_from_active_tasks_conversation`**: Primary **consumer** of `/review` tasks that are "recommended to current `/active` plan". It takes those tasks and folds them into a specific `docs/plans/active/` plan, organizing them into Completed / In Progress / Pending / Blocked for that objective.
- **`/archive`**: Typical **consumer** of `/review` tasks that are "recommended to a `/backlog` plan`". It materializes those items into backlog/prioritized plan files and (optionally) conversation archives when you are closing out a journey.
- The behavior and structure defined in this file are **only for `/review`**. Other commands operate on the resulting plan files, using `/review`'s output as input rather than redefining task semantics.
