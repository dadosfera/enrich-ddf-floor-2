# Slash Commands

This directory contains generated Markdown for slash commands (AI agent commands invoked with `/command_name` syntax). JSON-backed commands are authored in `commands/json/core/*.json`; declared markdown-only exceptions are authored directly here. Commands are distributed to platform command directories configured in `_dev/config/command_distribution_platforms.json` and then to other repositories.

## ⚠️ CRITICAL: Distribution Workflow Required

**AI agents must NEVER directly edit files in:**

- generated platform command directories

**These are read-only generated directories. Edit `commands/json/core/*.json` for JSON-backed commands, or `commands/*.md` only for commands listed in `commands/markdown_only_commands.yaml`, then run the distribution script.**

See: `docs-fera@ guides/distribution/distribution_workflow_unified.md` for complete workflow.

**Command authoring best practices**: `guides/commands/command_authoring_best_practices.md`

## Markdown-only commands (exceptions to JSON-first)

Most commands use `commands/json/core/*.json` as canonical source. Some commands are **markdown-only** because their content does not round-trip through the JSON converter yet:

- `merg_merge` (033) — `commands/merg_merge.md`
- `chkp_check_pending` (044) — `commands/chkp_check_pending.md`
- `gswp_git_sweep` (095) — `commands/gswp_git_sweep.md`
- `gsyn_git_sync` (019) — `commands/gsyn_git_sync.md`
- `revl_review_all_plans` (035) — `commands/revl_review_all_plans.md`
- `delc_delete_conversation` (088) — `commands/delc_delete_conversation.md`

Registry: `commands/markdown_only_commands.yaml`.

For these commands:

1. Edit `commands/<name>.md` directly (never create a stub JSON — it will be overwritten on the next JSON build).
2. Bump `<!-- COMMAND_VERSION: ... -->` and update `commands/index_commands.yaml` only while the legacy compatibility index is still enforced.
3. Distribute: `bash _dev/scripts/distribution/distribute_platform_commands.sh`

This distribution step updates only the current repo's configured platform
command directories. Cross-repo rollout must use the repository classes in
`guides/distribution/repository_distribution_classes.md` so `docs-fera`,
`*-fera` infrastructure repos, non-fera D&ADDF product repos, and unrelated
non-fera repos are not treated as the same target type.

Future migration to JSON is tracked in `_dev/docs/plans/backlog/QW_4h_HIGH_migrate_merg_merge_json_canonical_2026-06-09.md`.

## Adding a New Command

**⚠️ MANDATORY WORKFLOW** - Follow all steps or your commit will be blocked by the pre-commit hook.

### Quick Checklist

When adding a new command file to this directory, you **must**:

1. ✅ Create command JSON in `commands/json/core/` with a unique 4-letter abbreviation prefix (e.g., `arch_archive`)
2. ✅ Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
3. ✅ Run JSON build: `bash _dev/workflows/command_distribution/build_commands_from_json.sh`
4. ✅ Update legacy compatibility metadata in `commands/index_commands.yaml` while hooks still enforce it
5. ✅ Run: `bash _dev/scripts/distribution/distribute_platform_commands.sh`
6. ✅ Verify files exist in the configured platform command directories
7. ✅ Update `README.md` (if command should be discoverable)
8. ✅ Commit all changes together

### Full Documentation

See the complete workflow with detailed instructions:

- **[Adding a New Command Guide](../guides/cursor_commands_sync.md#adding-a-new-command)**

## Renaming a Command

**⚠️ MANDATORY WORKFLOW** - Follow all steps to ensure all references are updated correctly.

### Quick Checklist

When renaming a command file in this directory, you **must**:

1. ✅ Rename command file in `commands/` (e.g., `old_name.md` → `new_name.md`)
2. ✅ Update all internal references within the command file (command name, file paths, etc.)
3. ✅ Rename corresponding JSON file in `commands/json/core/` (if exists) and update all references within
4. ✅ Update `commands/index_commands.yaml` while the legacy compatibility index is still enforced:
   - Update `name` field to new command name
   - Update `file` field to new filename
   - Update all `backlinks` that reference the old name
   - Keep the **same** `id` (for tracking renames)
   - Bump `version` (MAJOR for breaking changes, MINOR for backward-compatible)
5. ✅ Update all references in other command files, guides, standards, roles, and templates
6. ✅ Update `_dev/scripts/update_commands_ref.py` with new command name mappings (for automated reference updates)
7. ✅ Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
8. ✅ Run distribution script: `bash _dev/workflows/distribution/commands/installers/install_commands.sh`
9. ✅ Verify files exist in the configured platform command directories with new names
10. ✅ Verify old files are removed from distribution targets
11. ✅ Update "Last Updated" date in `guides/cursor_commands_sync.md`
12. ✅ Commit all changes together

### Important Notes

- **Keep the same COMMAND_ID**: When renaming, maintain the same `id` in JSON, the generated markdown file header, and the compatibility index while it is still enforced
- **Version bumping**: Use semantic versioning - MAJOR for breaking changes (name change), MINOR for backward-compatible improvements
- **Comprehensive reference updates**: Search the entire codebase for old command name references (use `grep` to find all occurrences)
- **Historical files**: Old references in `_dev/docs/plans/finished/` and historical reports may be left as-is for historical accuracy

### Pre-Commit Validation

A pre-commit hook automatically validates that new commands follow this workflow. The hook will **block your commit** if:

- Command is not listed in the canonical index
- Distribution script wasn't run
- Command count doesn't match actual files

### Command File Format

**Template**: Use `templates/slash_command.template.md` (Template Version: 1.0.0) as the starting point for new commands.

Commands should follow this structure:

````markdown
# /abc_command_name

<!-- COMMAND_ID: 000 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: <type> -->
<!-- TEMPLATE_VERSION: 1.0.0 -->

Brief description of what the command does.

**Local Reference**: `commands/abc_command_name.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/abc_command_name.md`

Backlinks:

- Related mini prompts or guides

## Command sequence (run in order)

1. Step description

```bash
command here
```
````

## Notes

- Important notes about the command

```

**Template Location**: `templates/slash_command.template.md`
**Template Version**: 1.0.0

See existing commands in this directory for examples.

## Roles vs Modes (IMPORTANT)

- **Role**: *who* the agent should behave as (architect, project manager, tech lead, senior engineer).
- **Mode**: *how* the agent should operate (ask/learn, plan, act/execute, debug).

You can combine them in a session (example: `Role: Tech Lead` + `Mode: Plan`).

## Role Commands

Role commands activate distinct agent roles:

| Command | Role | Focus | Use When |
|---------|------|-------|----------|
| `/rols_role_senior_autonomous_engineer` | Senior Engineer | Initiative + autonomous execution | You want senior judgment and autonomous delivery |
| `/rolt_role_tech_lead` | Tech Lead | Code quality & team mentoring | Reviewing code, improving standards, mentoring teams |
| `/rola_role_arkhitect` | Architect | System design & long-term evolution | Designing architecture, planning major migrations |
| `/rolp_role_prj_manager` | Project Manager | Portfolio & delivery coordination | Coordinating delivery, managing dependencies, planning roadmaps |

**Role docs**: `guides/role_based_commands_tech_lead_architect_pm.md`

## Operational Mode Commands

Mode commands constrain *how* the agent operates:

| Command | Mode | What it allows |
|---------|------|----------------|
| `/moda_ask_mode` | Ask | Read/search/explain only (no edits, no shell) |
| `/modp_plan_mode` | Plan | Planning only (no edits, no shell) |
| `/modc_act_mode` | Act | Full execution (edits + shell/tests) |
| `/modb_debug_mode` | Debug | Diagnosis (diagnostic shell ok; avoid permanent edits) |

**Mode docs**: `guides/cursor/MODE_SYSTEM_OVERVIEW.md`

## Current Commands

See `guides/cursor_commands_sync.md` for the complete list of canonical commands.

## Usage Examples

### Expanding Plans with `/expp_xpand_plan`

The `/expp_xpand_plan` command enriches existing plans with detailed guidelines, strategy validation, and research findings.

**When to use**:
- After creating a new plan that feels sparse (< 500 lines)
- Before starting execution on complex or unfamiliar tasks
- When tasks lack clear acceptance criteria or implementation steps

**Basic usage**:
```

/expp_xpand_plan plans/active/QW_2h_HIGH_add_authentication.md

```

**With options**:
```

# Without web search (offline mode)

/expp_xpand_plan plans/active/QW_2h_HIGH_add_authentication.md false

# Minimal expansion (faster, less detail)

/expp_xpand_plan plans/active/QW_2h_HIGH_add_authentication.md true minimal

# Comprehensive expansion (maximum detail)

/expp_xpand_plan plans/active/QW_2h_HIGH_add_authentication.md true comprehensive

````

**What it does**:
1. Analyzes existing plan structure and identifies gaps
2. Expands tasks with acceptance criteria, implementation steps, and validation methods
3. Adds or enhances strategy validation section (macro view, alternatives, risks)
4. Performs web searches for key technical decisions (if enabled)
5. Adds edge cases, testing strategies, and deployment checklists
6. Ensures plan meets minimum 500-line standard for comprehensive planning

**Typical workflow**:
1. `/reva_review_active_conversation` → Extract tasks from conversation
2. `/pfac_plan_from_active_tasks_conversation` → Create initial plan
3. **`/expp_xpand_plan`** → Enrich plan with details and research
4. Execute comprehensive plan with confidence

For complete documentation, see `commands/expp_xpand_plan.md`.

## Command Naming Convention

All commands use unique **4-letter abbreviation prefixes** (e.g., `arch_archive`, `reva_review_active_conversation`, `dedu_dedup`).

**MANDATORY**: All command prefixes must be exactly 4 letters. This is enforced by the pre-commit hook.

**Collision Avoidance**: Ensure your abbreviation doesn't appear as a substring in other command names (unless they share the same prefix). Use `_dev/scripts/commands/check_command_collisions.py` to verify before committing.

### Using Commands in the Palette

**Always use the 4-letter prefix for unique matches:**

- Type **`/pfac`** → Gets only `pfac_plan_from_active_tasks_conversation`
- Type **`/expp`** → Gets only `expp_xpand_plan`
- Type **`/reva`** → Gets only `reva_review_active_conversation`

**Why this matters**: Typing `/plan` will match multiple commands (e.g., `expp_xpand_plan` and `pfac_plan_from_active_tasks_conversation`) because "plan" appears in both names. The 4-letter prefix system ensures you get exactly one match and prevents collisions.

For information about the migration from `gis-*` prefixes, see the [Command Migration Guide](../guides/command_migration_guide.md).

**Note**: For a sample repository implementation, refer to `solver-mod-bet` (previously `prompts-fera` was used, but it is now deprecated).

## Testing Commands

Command testing uses a specialized LLM testing framework with probabilistic evaluation. Testing documentation is centralized to avoid distributing test guidelines with each command file (reducing token costs).

### Local Testing with CLI Tools

The fastest way to test AI agent commands locally is to use the **CLI version** of the agent:

| IDE / Extension | CLI Tool |
| :--- | :--- |
| **Cursor IDE** | `cursor` CLI |
| **VS Code + Cline** | `cline` CLI |
| **VS Code + AutoDriveDDF** | `autodriveddf` CLI |

**Note**: These CLI tools support slash commands across different platforms.

**Why CLI?** Faster iteration, scriptable, avoids creating real artifacts in IDE.

See `_dev/tests/commands/README.md` for detailed CLI testing examples and best practices.

### Testing Resources

- `_dev/tests/commands/README.md` - Centralized testing guidelines (including CLI testing)
- `guides/ai/llm_as_judge_testing_framework.md` - LLM-as-judge pattern documentation
- `_dev/tests/commands/evaluation_criteria/` - Scoring rubrics per command
- `recurrent_errors/2025-11-27_ai_agent_command_testing_generates_real_artifacts.md` - Common testing pitfalls

### Running Tests

```bash
# Full test (requires cursor-agent)
bash _dev/tests/commands/test_xect_execute_plan.sh

# Structure tests only (fast, no cursor-agent needed)
bash _dev/tests/commands/test_xect_execute_plan.sh --structure-only
````

For details on the three-tier testing strategy (structure validation, behavior sampling, LLM-as-judge), see `_dev/tests/commands/README.md`.

## Commands vs Mini Prompts

**Critical Distinction**: Commands are **executable actions** that help reach **maturity levels** defined by mini prompts. Mini prompts represent **target states** and can be **iterated in loops** until the maturity level is achieved.

See `guides/commands_and_mini_prompts_distinction.md` for complete explanation of:
- How mini prompts represent maturity stages (not directly executable)
- How commands are executable actions that reference mini prompts
- Where each is defined in the LLM IDE automation context
- The relationship between commands and mini prompts
