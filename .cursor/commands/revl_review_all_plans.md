# /revl_review_all_plans
<!-- COMMAND_ID: 035 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: re_review -->
<!-- REVIEW_TYPE: all_plans_meta -->

**Analysis only - no files modified.** Review all plans (including meta plans) across the repository. Provides a comprehensive read-only overview of repository coordination artifacts, plans inventory, and project status.

Backlinks:

- mini_prompt/lv1/meta_plan_refresh_mini_prompt.md
- mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
- mini_prompt/lv1/create_meta_plan_mini_prompt.md
- _dev/docs/plans/active/docs-fera_meta_plan.md

## Command sequence (run in order)

1. Confirm repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Locate and display the repository meta plan

```bash
# Find the repository meta plan (usually in _dev/docs/plans/active/)
gtimeout 5 find _dev/docs/plans -name "*_meta_plan.md" -type f 2>/dev/null | head -5
```

3. Display meta plan summary

Read the repository meta plan and summarize:
- **Strategic Objective**: What is the primary goal?
- **Active Plans**: List P0/P1/P2 plans with their status
- **Backlog**: Key items waiting for capacity
- **Current Cycle Progress**: Which PDCA(+Study) cycle step is active?

4. Locate project meta plans

```bash
# Find all project-level meta plans
gtimeout 5 find docs/projects -name "*_meta_plan.md" -type f 2>/dev/null | head -10
```

5. Projects overview

For each project under `docs/projects/active/`:
- **Project Name**: From folder slug
- **Status**: Active, prioritized, blocked, finished
- **Plan Count**: Number of plans in each status folder
- **Meta Plan**: Whether a project-level meta plan exists

6. Related mini prompts status

Check availability of key coordination mini prompts:

```bash
gtimeout 5 ls -la mini_prompt/lv1/meta_plan_refresh_mini_prompt.md 2>/dev/null
gtimeout 5 ls -la mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md 2>/dev/null
gtimeout 5 ls -la mini_prompt/lv1/create_meta_plan_mini_prompt.md 2>/dev/null
gtimeout 5 ls -la mini_prompt/lv1/create_project_mini_prompt.md 2>/dev/null
```

7. Plans inventory snapshot

```bash
# Count plans by status
echo "=== Plans by Status ==="
for status in active prioritized backlog blocked finished; do
  count=$(find docs/plans/$status _dev/docs/plans/$status -name "*.md" -type f 2>/dev/null | grep -v AGENTS.md | grep -v README.md | wc -l | tr -d ' ')
  echo "$status: $count"
done
```

## Output format

Structure your response with:

### Repository Meta Plan Summary
- **Path**: `<absolute_path>`
- **Last Updated**: `<date>`
- **Strategic Objective**: `<one-line summary>`
- **Active Plans**: `<count>` (P0: X, P1: Y, P2: Z)
- **Backlog Items**: `<count>`
- **Current Cycle**: `<cycle number and step>`

### Projects Overview
| Project | Status | Plans (A/P/B/F) | Has Meta Plan |
|---------|--------|-----------------|---------------|
| ...     | ...    | ...             | Yes/No        |

### Plans Inventory
| Status | Count | Location |
|--------|-------|----------|
| active | X     | {PLANS_BASE}/active (_dev/docs/plans for -fera repos) |
| ...    | ...   | ...      |

### Related Mini Prompts
- ✅/❌ `meta_plan_refresh_mini_prompt.md` — Refresh and validate meta plans
- ✅/❌ `project_and_plans_review_reprioritize_mini_prompt.md` — Comprehensive review and reprioritization
- ✅/❌ `create_meta_plan_mini_prompt.md` — Create new meta plans
- ✅/❌ `create_project_mini_prompt.md` — Create new projects

### Recommendations
List 1-3 actionable recommendations based on the review:
1. ...

## Notes

- This command is **read-only**: it does not create, move, or edit any files.
- For refreshing the meta plan, use the `meta_plan_refresh_mini_prompt.md`.
- For comprehensive reprioritization, use `project_and_plans_review_reprioritize_mini_prompt.md`.
- For creating new projects, use `/proj_project` command.

## Relationship to other commands

- **`/revl_review_all_plans`** (this command): Read-only overview of meta plans, projects, and coordination artifacts.
- **`/proj_project`**: Create and manage projects with their meta plans.
- **`/jour_journey_meta_best_track`**: Journey planning and best track selection.
- **`/next_next_plan_cycle`**: Execute the next plan in the active → prioritized → backlog cycle.
- **`/reva_review_active_conversation`**: Review conversation tasks (focuses on task extraction, not meta plan coordination).
