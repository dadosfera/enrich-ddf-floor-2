---
category: planning
criticality: medium
scope: all
---
# /plca_complete_all_active
<!-- COMMAND_ID: 002 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pl_complete_all_active -->

Complete and verify ALL active plans with pre-execution validation, completion verification, and overlap/duplication detection.

**Local Reference**: `commands/plca_complete_all_active.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/plca_complete_all_active.md`

Backlinks:
- commands/xect_execute_plan.md
- commands/next_next_plan_cycle.md

## ⚠️ HIGH-REGISTER MODEL RESTRICTION

**CRITICAL**: Designed for high-register models (Claude Opus, GPT-4) due to complex reasoning requirements.

## Purpose

Orchestrates the entire active plan lifecycle: verify completion, detect overlaps, execute in priority order, and archive.

### Phase 1: Context & Discovery

- Identify repo type and active plans directory

### Phase 2: Completion Verification

- Check `.completed` markers

### Phase 3: Overlap Detection

- Semantic analysis of plan titles/objectives

### Phase 4: Priority Execution

- Sort by priority: QW > CB > SEC > HI_ME > MI_LE

### Phase 5: Cleanup & Archival

- Perform final git sync

## Reference

For detailed logic, troubleshooting, and lifecycle rules, see:
