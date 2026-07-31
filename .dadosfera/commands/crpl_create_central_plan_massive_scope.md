---
category: planning
criticality: medium
scope: all
---
# /crpl_create_central_plan_massive_scope
<!-- COMMAND_ID: 065 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: cr_create_plan -->

Create a central plan and batch structure for massive scope work (thousands of linting errors, test failures, duplications). This command sets up the structure; agents use `/btex_batch_execute_massive_scope` to work on batches.

**Local Reference**: `commands/crpl_create_central_plan_massive_scope.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/crpl_create_central_plan_massive_scope.md`

Backlinks:
- commands/btex_batch_execute_massive_scope.md (execution command)
- mini_prompt/lv2/batch_execution_massive_scope_mini_prompt.md
- glossaries/project_management_glossary.md (Entity definitions: Central Plan, Batch Plan)

## When to Use

- When facing 100+ linting errors that need systematic fixing
- When dealing with 50+ test failures that need categorization
- When consolidating 100+ duplicate files
- When refactoring affects hundreds of files
- **Before agents start working** - this sets up the batch structure

## When NOT to Use

- For small scope work (< 20 items) - use regular plan creation instead
- When central plan already exists - use `/btex_batch_execute_massive_scope` instead
- For agent execution - use `/btex_batch_execute_massive_scope` instead

## Sector Scoping for Duplicate Files

When the problem type involves duplicate files, use directory-based sector scoping to limit each batch to specific directories:

```bash
# Conditional logic for duplicate files
if [[ "$PROBLEM_TYPE" == "duplicate_files" ]]; then
    # Discover directories containing duplicates
    find . -maxdepth 2 -not -path '*/\.*' -type d > duplicate_files_directories.txt

    # Assign directories to batches
    BATCH_DIRS="$(cat "batch_${BATCH_NUM}_dirs.txt")"
fi
```

## 📂 Sector Scope

- Do **NOT** scan the entire repository — work only within assigned directories
- Reference `/dedu_dedup` for the deduplication logic within each sector
- Track which directories have been processed in the central plan

## Relationship to Massive Scope Deduplication

- Central plans for duplicates should reference `/dedu_dedup` for deduplication execution.
- Batch scripts must keep scope constrained to assigned directories and include explicit sector references.

## 🔒 Locking Instructions

(Standard locking instructions apply - see Central Plan)
