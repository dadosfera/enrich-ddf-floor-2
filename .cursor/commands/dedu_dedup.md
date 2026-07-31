---
category: infrastructure
criticality: medium
scope: all
---
# /dedu_dedup
<!-- COMMAND_ID: 008 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: de_dedup -->

Run a safe, dry-run deduplication sweep over repository files or commands using the canonical deduplication workflows from `dadosfera/workflows-fera`.

**Local Reference**: `commands/dedu_dedup.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/dedu_dedup.md`

Backlinks:
- mini_prompt/lv1/deduplication_check_mini_prompt.md
- mini_prompt/lv1/duplicate_tests_checker_mini_prompt.md
- mini_prompt/lv1/safe_file_organization_and_movement_mini_prompt.md
- mini_prompt/lv1/plans_consolidation_merging_deduplication_mini_prompt.md
- guides/project_taxonomy.md
- guides/project_structure_ontology.md
- templates/run_main_entry_point.md
- templates/plans/meta_plan_template.md

## Relationship to Massive Scope Commands

When deduplication involves massive scope (100+ files), this command integrates with the batch execution workflow:

- `/crpl_create_central_plan_massive_scope` creates sector-scoped batch plans that reference `/dedu_dedup`
- `/btex_batch_execute_massive_scope` executes deduplication within assigned directory sectors
- Each batch agent runs `/dedu_dedup` scoped to its assigned directories only
