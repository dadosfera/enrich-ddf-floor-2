---
category: automation
criticality: medium
scope: all
---
# /btex_batch_execute_massive_scope
<!-- COMMAND_ID: 064 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ba_batch_execute -->

Execute massive scope work on existing central plans with batches. **Detects existing central plans** created by `/crpl_create_central_plan_massive_scope` and starts agent work on available batches. **Agents work on ONE batch only** - do not suggest working on other batches.

**Local Reference**: `commands/btex_batch_execute_massive_scope.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/btex_batch_execute_massive_scope.md`

Backlinks:
- mini_prompt/lv2/batch_execution_massive_scope_mini_prompt.md
- commands/xect_execute_plan.md (similar locking mechanism)

## When to Use

- When facing 100+ linting errors that need systematic fixing
- When dealing with 50+ test failures that need categorization
- When consolidating 100+ duplicate files
- When refactoring affects hundreds of files
- When work scope is too large for a single plan

## When NOT to Use

- For small scope work (< 20 items) - use regular `/xect_execute_plan` instead
- For single-file fixes - use direct execution
- For exploratory work - use `/expp_xpand_plan` instead

## Purpose

Execute massive scope work by detecting existing central plans and assigning ONE batch per agent for systematic execution. Enforces strict locking to prevent conflicts.

## Sector-Based Strategy

For duplicate file batches, this command uses a sector-based approach:

- Identifies target directories as Sectors from the batch plan's Sector Scope
- Scan Directory contents within the assigned sector only
- Use `/dedu_dedup` for deduplication logic within each sector
- Global duplicates spanning multiple sectors are NOT handled in this workflow
