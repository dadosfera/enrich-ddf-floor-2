# /expa_execute_plan_all

Execute ALL active plans in priority order without complex validation overhead.

**Local Reference**: `commands/expa_execute_plan_all.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/expa_execute_plan_all.md`

**Note**: This command is repo-aware. For `-fera` repositories (docs-fera, scripts-fera, etc.), plans are stored in `_dev/docs/plans/`. For all other repositories, plans are stored in `docs/plans/`.

**Canonical Name**: `/expa_execute_plan_all` replaced the deprecated `/exba_execute_batch_all` and `/exba_run_all_plans` duplicates. Update any scripts, prompts, or plans that still mention the old names.

Backlinks:

- mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md
- commands/exec_execute_plan.md
- commands/plca_complete_all_active.md
- commands/next_next_plan_cycle.md

## Purpose

Simple batch execution of ALL active plans in priority order. Unlike `/plca_complete_all_active` (which requires high-register models for complex verification), this command provides straightforward sequential execution suitable for any model.

## When to Use

- When you need to execute multiple active plans in one session
- When you want simple sequential execution without overlap detection
- When working with standard models (not just high-register)
- When you want to batch-process plans quickly

## When NOT to Use

- When you need completion verification and overlap detection → use `/plca_complete_all_active`
- When you want to execute only the conversation-related plan → use `/exec_execute_plan`
- When you need to review plans before execution → use `/exal_expand_all_active_plans`

## Command Sequence

### Phase 1: Context Discovery

```bash
# Confirm repository context
REPO_ROOT=$(gtimeout 5 git rev-parse --show-toplevel)

# Detect repository type for correct plan paths
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
  PLANS_BASE="_dev/docs/plans"
else
  PLANS_BASE="docs/plans"
fi

# List all active plans (excluding meta plans, AGENTS.md, README.md)
gtimeout 5 find "$REPO_ROOT/$PLANS_BASE/active" -type f -name "*.md" \
  ! -name "AGENTS.md" \
  ! -name "README.md" \
  ! -name "*meta*" \
  2>/dev/null | sort
```

### Phase 2: Priority Sorting

Sort plans by priority prefix (highest first):

1. **`QW_`** - Quick Win (execute first)
2. **`CB_`** - Critical Blocker (execute first)
3. **`SEC_`** - Security Issue (execute first)
4. **`HI_ME_`** - High Impact, Medium Effort
5. **`MI_LE_`** - Medium Impact, Low Effort
6. **`HI_HE_`** - High Impact, High Effort
7. **`LI_`** - Low Impact
8. **`RES_`** - Research/Exploration
9. No prefix - Default priority

### Phase 3: Sequential Execution

For each plan in priority order:

1. **Check lock status**: Skip if `.lock` file exists
2. **Create lock**: `touch "$PLAN_PATH.lock"`
3. **Execute plan**: Work through all tasks/checkboxes
4. **Mark completion**: When all `[ ]` become `[x]`:
   - Rename to `.completed` extension
   - Remove `.lock` file
5. **Proceed to next plan**

### Phase 4: Final Sync

```bash
# Perform git sync after all plans executed
git add "$PLANS_BASE/active/"
git commit -m "Execute all active plans batch"
git push origin main
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│                 /expa_execute_plan_all                  │
├─────────────────────────────────────────────────────────┤
│ 1. Discover all active plans                            │
│ 2. Sort by priority (QW > CB > SEC > HI_ME > ...)      │
│ 3. For each plan:                                       │
│    ├── Skip if locked                                   │
│    ├── Create lock                                      │
│    ├── Execute all tasks                                │
│    ├── Mark .completed when done                        │
│    └── Remove lock                                      │
│ 4. Git sync                                             │
└─────────────────────────────────────────────────────────┘
```

## Usage

```bash
# Execute all active plans
/expa_execute_plan_all

# Execute with verbose output
/expa_execute_plan_all --verbose

# Execute only unlocked plans (default behavior)
/expa_execute_plan_all --skip-locked
```

## Output Format

```
🚀 Starting execution of ALL active plans
📁 Plans base: _dev/docs/plans/active/

📋 Found 5 active plans (sorted by priority):
  1. QW_2h_HIGH_fix_critical_bug.md
  2. QW_1h_HIGH_update_docs.md
  3. HI_ME_1d_HIGH_refactor_api.md
  4. MI_LE_4h_MEDIUM_cleanup.md
  5. LI_2h_LOW_nice_to_have.md

🔄 Executing plan 1/5: QW_2h_HIGH_fix_critical_bug.md
   🔒 Lock created
   ⏳ Working on tasks...
   ✅ All tasks completed
   📝 Renamed to .completed
   🔓 Lock removed

🔄 Executing plan 2/5: QW_1h_HIGH_update_docs.md
   ...

✅ Batch execution complete
   Executed: 5 plans
   Skipped (locked): 0 plans
   Failed: 0 plans

📍 Plans directory: /absolute/path/to/_dev/docs/plans/active/
```

## Differences from Similar Commands

| Command | Purpose | Model Requirement | Validation |
|---------|---------|-------------------|------------|
| `/expa_execute_plan_all` | Execute ALL plans simply | Any | Minimal |
| `/exec_execute_plan` | Execute conversation-related plan | Any | Minimal |
| `/plca_complete_all_active` | Verify + detect overlaps + execute | High-register | Comprehensive |
| `/exal_expand_all_active_plans` | Expand/show plans (no execution) | Any | None |

## Error Handling

- **Locked plan**: Skip with warning, continue to next
- **Missing plan file**: Log error, continue to next
- **Git sync failure**: Retry once, then report error
- **Task execution error**: Mark in plan, continue if possible

## Related Commands

- **`/exec_execute_plan`**: Execute single conversation-related plan
- **`/plca_complete_all_active`**: Complex verification and execution (high-register)
- **`/exal_expand_all_active_plans`**: Expand and review all plans
- **`/next_next_plan_cycle`**: PDCA cycle management
- **`/pfac_plan_from_active_tasks_conversation`**: Create plan from conversation
