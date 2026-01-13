# /plca_complete_all_active
<!-- COMMAND_ID: 002 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pl_complete_all_active -->

Complete and verify ALL active plans with pre-execution validation, completion verification, and overlap/duplication detection.

**Local Reference**: `commands/plca_complete_all_active.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/plca_complete_all_active.md

Backlinks:
- commands/xect_execute_plan.md
- commands/next_next_plan_cycle.md

## ⚠️ HIGH-REGISTER MODEL RESTRICTION
**CRITICAL**: Designed for high-register models (Claude Opus, GPT-4) due to complex reasoning requirements.

## Purpose
Orchestrates the entire active plan lifecycle: verify completion, detect overlaps, execute in priority order, and archive.

### When to use in the lifecycle

- Run /plca_complete_all_active **after** execution-focused commands like /xect_execute_plan, `/next_next_plan_cycle`, or `/xqpa_xqt_plan_all` (the canonical “execute all plans” command; older aliases such as `/xpal_execute_plan_all` have been removed).
- Its job is to verify which active plans are truly finished using canonical Status fields (`Status:` / `**Status**:` set to `finished`, `completed`, or `done`) and/or `.completed` markers and then move only those verified plans from `active/` to `finished/` in line with `templates/plan_management_system.md`.
- Together with `/arch_archive` (and the `/next_next_plan_cycle` double-verification flow), it is one of the only commands explicitly allowed to move completed plans into `finished/`.

## Command Sequence

### Phase 1: Context & Discovery
- Identify repo type and active plans directory
- List all valid plan files

### Phase 2: Completion Verification
- Check `.completed` markers
- Verify Status fields ("finished", "completed")
- Count checkboxes (all must be `[x]`)
- Move verified plans to `finished/`

### Phase 3: Overlap Detection
- Semantic analysis of plan titles/objectives
- Identify duplicates or merge candidates

### Phase 4: Priority Execution
- Sort by priority: QW > CB > SEC > HI_ME > MI_LE
- Execute top priority plan first

### Phase 5: Cleanup & Archival
- Perform final git sync
- Update meta-plans

**See**: `guides/commands/plca_complete_all_active_guide.md` for detailed logic.

## Usage

```bash
# Standard execution
/plca_complete_all_active

# Dry run (verify only)
/plca_complete_all_active --dry-run
```

## Reference
For detailed logic, troubleshooting, and lifecycle rules, see:
- `guides/commands/plca_complete_all_active_guide.md`
