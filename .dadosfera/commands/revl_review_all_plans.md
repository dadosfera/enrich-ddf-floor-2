---
# Dadosfera Metadata
category: planning
criticality: medium
scope: all
commandId: "035"
version: "2.0.0"
type: "re_review"
canonical: "docs-fera@/commands/revl_review_all_plans.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/revl_review_all_plans.md"
backlinks:
  - "mini_prompt/lv1/meta_plan_refresh_lv1_mini_prompt.md"
  - "mini_prompt/lv1/project_and_plans_review_reprioritize_lv1_mini_prompt.md"
  - "mini_prompt/lv1/create_meta_plan_lv1_mini_prompt.md"
  - "mini_prompt/lv1/plans_consolidation_merging_deduplication_lv1_mini_prompt.md"
  - "_dev/docs/plans/active/docs-fera_meta_plan.md"
  - "commands/plrr_plan_reorder.md"

# Claude Code Metadata
name: "Review All Plans"
description: "Review all plans, detect duplications, reorder priorities, and update meta plan (no execution)"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 035 -->
<!-- COMMAND_VERSION: 2.0.0 -->
<!-- COMMAND_TYPE: re_review -->
# /revl_review_all_plans

**Command**: `/revl_review_all_plans`

**PURPOSE**: Comprehensive plan review and organization command. Reviews all plans, detects duplications between `active/`, `finished/`, and `prioritized/`, reorders priorities, and updates the meta plan — **without executing any plans**.

**Local Reference**: `commands/revl_review_all_plans.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/revl_review_all_plans.md`

## When to Use

- When you want to **organize plans** without executing them
- When you need to **detect duplications** between active, finished, and prioritized folders
- When you want to **reprioritize** work based on current context
- When you need to **update the meta plan** with current state
- For periodic planning reviews and coordination checks

## Backlinks

- `mini_prompt/lv1/meta_plan_refresh_lv1_mini_prompt.md`
- `mini_prompt/lv1/project_and_plans_review_reprioritize_lv1_mini_prompt.md`
- `mini_prompt/lv1/plans_consolidation_merging_deduplication_lv1_mini_prompt.md`
- `commands/plrr_plan_reorder.md`

## Command Sequence

### Phase 1: Repository Context & Plan Inventory

```bash
# Detect repository type and plan base
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
  PLANS_BASE="_dev/docs/plans"
else
  PLANS_BASE="docs/plans"
fi

# Ensure all plan directories exist
gtimeout 5 mkdir -p "$PLANS_BASE/active" "$PLANS_BASE/prioritized" "$PLANS_BASE/backlog" "$PLANS_BASE/blocked" "$PLANS_BASE/canceled" "$PLANS_BASE/finished"

# Count plans by status
for status in active prioritized backlog blocked canceled finished; do
  count=$(find "$PLANS_BASE/$status" -name "*.md" -type f ! -name "README.md" ! -name "AGENTS.md" ! -name "index*.yaml" 2>/dev/null | wc -l | tr -d ' ')
  echo "$status: $count plans"
done
```

**Output**: Plans inventory table with counts per status folder.

### Phase 2: Duplication Detection (Active/Finished/Prioritized)

Detect plans that may exist in multiple status folders or have overlapping objectives:

1. **Filename Duplications**: Same plan filename appearing in multiple folders (e.g., `active/` and `finished/`)
2. **Semantic Overlaps**: Plans with similar titles/objectives across folders
3. **Stale Active Plans**: Plans in `active/` that have a corresponding `.completed` version in `finished/`

```bash
# Check for filename duplications across status folders
echo "=== Checking for duplicate plan filenames ==="
for plan in $(find "$PLANS_BASE/active" -name "*.md" -type f ! -name "README.md" ! -name "AGENTS.md" 2>/dev/null); do
  plan_name=$(basename "$plan")
  # Check if same filename exists in finished or prioritized
  if [[ -f "$PLANS_BASE/finished/$plan_name" ]]; then
    echo "⚠️  DUPLICATE: $plan_name exists in both active/ and finished/"
  fi
  if [[ -f "$PLANS_BASE/prioritized/$plan_name" ]]; then
    echo "⚠️  DUPLICATE: $plan_name exists in both active/ and prioritized/"
  fi
done

# Check prioritized vs finished
for plan in $(find "$PLANS_BASE/prioritized" -name "*.md" -type f ! -name "README.md" ! -name "AGENTS.md" 2>/dev/null); do
  plan_name=$(basename "$plan")
  if [[ -f "$PLANS_BASE/finished/$plan_name" ]]; then
    echo "⚠️  DUPLICATE: $plan_name exists in both prioritized/ and finished/"
  fi
done
```

**AI Analysis Required**: Perform semantic analysis of plan titles and objectives to identify overlapping plans that have different filenames but target the same outcome.

### Phase 3: Plan Reorder & Reprioritization

Invoke `/plrr_plan_reorder` logic to reprioritize plans based on effort-impact matrix:

```bash
# Reference: @mini_prompt/lv1/project_and_plans_review_reprioritize_lv1_mini_prompt.md
```

**Actions**:
1. Scan all plan folders: `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, `finished/`
2. Apply enhanced effort-impact matrix:
   - **Immediate priorities**: `QW_` (Quick Wins), `CB_` (Critical Blockers), `SEC_` (Security)
   - **High-value follow-ups**: `HI_` (High Impact), technical debt, dependency resolution
3. Output a **shortlist of next 5-10 plans** to execute
4. Identify **consolidation opportunities** (overlapping plans to merge)

**Output**: Prioritized list and consolidation proposal — does NOT move or edit plan files directly.

### Phase 4: Meta Plan Update

```bash
# Find the repository meta plan
META_PLAN=$(find "$PLANS_BASE" -name "*_meta_plan.md" -type f 2>/dev/null | head -1)

# If meta plan exists, read and analyze
if [[ -n "$META_PLAN" && -f "$META_PLAN" ]]; then
  echo "Meta Plan: $META_PLAN"
  # AI: Analyze meta plan and update with current inventory state
else
  echo "⚠️  No meta plan found. Consider creating one using:"
  echo "   @mini_prompt/lv1/create_meta_plan_lv1_mini_prompt.md"
fi
```

**AI Actions**:
1. Update meta plan with current plan counts per status
2. Update the "Current Focus" section based on Phase 3 priorities
3. Add notes about detected duplications from Phase 2
4. Ensure backlinks are current

### Phase 5: Project Meta Plans (Optional)

```bash
# Find project-level meta plans
find docs/projects -name "*_meta_plan.md" -type f 2>/dev/null | head -10
find _dev/docs/projects -name "*_meta_plan.md" -type f 2>/dev/null | head -10
```

**Output**: List of project meta plans with their status.

## Output Format

### Repository Meta Plan Summary

- **Path**: `<absolute_path_to_meta_plan>`
- **Last Updated**: `<date>`
- **Current Focus**: `<extracted_from_meta_plan>`

### Plans Inventory

| Status | Count | Location |
|--------|-------|----------|
| active | N | `$PLANS_BASE/active/` |
| prioritized | N | `$PLANS_BASE/prioritized/` |
| backlog | N | `$PLANS_BASE/backlog/` |
| blocked | N | `$PLANS_BASE/blocked/` |
| canceled | N | `$PLANS_BASE/canceled/` |
| finished | N | `$PLANS_BASE/finished/` |

### Duplication Detection Results

| Type | Plan | Locations | Action |
|------|------|-----------|--------|
| Filename | `plan_name.md` | active/, finished/ | Merge or remove duplicate |
| Semantic | `QW_fix_X.md` / `QW_X_fix.md` | active/, prioritized/ | Consolidate |

### Prioritized Shortlist (Top 10)

| Rank | Plan | Status | Priority | Effort | Impact | Justification |
|------|------|--------|----------|--------|--------|---------------|
| 1 | `QW_...` | active | QW | 1h | HIGH | Quick win, immediate value |
| 2 | `CB_...` | prioritized | CB | 2h | CRITICAL | Blocker for other work |
| ... | ... | ... | ... | ... | ... | ... |

### Consolidation Opportunities

- **Merge candidates**: List of plans with overlapping objectives
- **Recommended action**: Use `mini_prompt/lv1/plans_consolidation_merging_deduplication_lv1_mini_prompt.md`

### Recommendations

1. **Immediate**: [Action based on findings]
2. **Short-term**: [Action based on findings]
3. **Meta plan update**: [If needed]

## Related Commands

| Command | Purpose | When to use |
|---------|---------|-------------|
| `/revl_review_all_plans` (this) | Review, deduplicate, reorder, update meta plan | Planning/organization without execution |
| `/plrr_plan_reorder` | Reorder priorities only | When you only need reprioritization |
| `/plcy_plan_lifecycle_management` | Manage lifecycle (cancel outdated, verify completed) | When you need to move plans between folders |
| `/plca_complete_all_active` | Execute + complete + archive | When you want to execute plans |
| `/revp_prj_portfolio_review` | Portfolio review with project analysis | When you need project-level detail |

## Notes

- **No execution**: This command does NOT execute any plans. Use `/xect_execute_plan` or `/plca_complete_all_active` for execution.
- **No file modifications** (by default): Outputs proposals and recommendations. To apply changes, use the recommended commands or manually move files.
- **Consolidation workflow**: For acting on detected duplications, use `mini_prompt/lv1/plans_consolidation_merging_deduplication_lv1_mini_prompt.md`
