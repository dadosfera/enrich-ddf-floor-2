---
category: planning
criticality: medium
scope: all
---
# /xqpa_xqt_plan_all
<!-- COMMAND_ID: 016 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_xqt_plan_all -->

Execute ALL active plans in priority order without complex validation overhead.

**Local Reference**: `commands/xqpa_xqt_plan_all.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/xqpa_xqt_plan_all.md`

Backlinks:
- mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md
- commands/xect_execute_plan.md
- commands/plca_complete_all_active.md
- commands/next_next_plan_cycle.md

## When to Use

- When you need to execute multiple active plans in one session
- When you want simple sequential execution without overlap detection
- When working with standard models (not just high-register)
- When you want to batch-process plans quickly

## When NOT to Use

- When you need completion verification and overlap detection → use `/plca_complete_all_active`
- When you want to execute only the conversation-related plan → use `/xect_execute_plan`
- When you need to review plans before execution → use `/exal_xpand_all_active_plans`

## Command sequence (run in order)

### 1. Phase 1: Context Discovery

```bash
# Discover all active plans in priority order
# (placeholder for discovery logic)
```

### 2. Phase 2: Priority Sorting

```bash
# Build dependency-aware execution queue
# (placeholder for sorting logic)
```

### 3. Phase 3: Sequential Execution

```bash
# Execute each plan via xect_execute_plan
# (placeholder for execution loop)
```

## Purpose

Execute ALL active plans in priority order using a lightweight, sequential approach without complex validation overhead. Designed for batch-processing plans quickly through three phases: Context Discovery, Priority Sorting, and Sequential Execution.

## Command Sequence

### 1. Phase 1: Context Discovery

### 2. Phase 2: Priority Sorting

### 3. Sequential Execution
