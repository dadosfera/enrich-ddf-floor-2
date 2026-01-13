# Cursor Commands

This directory contains the **canonical source** for all Cursor IDE commands. Commands are distributed to platform-specific directories (`.cursor/commands/` and `.dadosfera/commands/`) and then to other repositories.

## ⚠️ CRITICAL: Distribution Workflow Required

**AI agents must NEVER directly edit files in:**

- `.cursor/commands/`
- `.dadosfera/commands/`

**These are read-only generated directories. Always edit the source files in `commands/` and run the distribution script.**

See: `guides/distribution_workflow_unified.md` for complete workflow.

**Command authoring best practices**: `guides/commands/command_authoring_best_practices.md`

## Adding a New Command

**⚠️ MANDATORY WORKFLOW** - Follow all steps or your commit will be blocked by the pre-commit hook.

### Quick Checklist

When adding a new command file to this directory, you **must**:

1. ✅ Create command file in `commands/` (this directory) with a unique 4-letter abbreviation prefix (e.g., `arch_archive.md`)
2. ✅ Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
3. ✅ Update command count in `guides/cursor_commands_sync.md`
4. ✅ Add command to list in "Current Commands" section
5. ✅ Update "Last Updated" date in sync guide
6. ✅ Run: `bash _dev/scripts/distribution/distribute_platform_commands.sh`
7. ✅ Verify files exist in `.cursor/commands/` and `.dadosfera/commands/`
8. ✅ Update `README.md` (if command should be discoverable)
9. ✅ Commit all changes together

### Full Documentation

See the complete workflow with detailed instructions:

- **[Adding a New Command Guide](../guides/cursor_commands_sync.md#adding-a-new-command)**

### Pre-Commit Validation

A pre-commit hook automatically validates that new commands follow this workflow. The hook will **block your commit** if:

- Command is not listed in the canonical index
- Distribution script wasn't run
- Command count doesn't match actual files

### Command File Format

Commands should follow this structure:

````markdown
# /abc_command_name

Brief description of what the command does.

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
| `/moda_cursor_ask_mode` | Ask | Read/search/explain only (no edits, no shell) |
| `/modp_cursor_plan_mode` | Plan | Planning only (no edits, no shell) |
| `/modc_cursor_act_mode` | Act | Full execution (edits + shell/tests) |
| `/modb_cursor_debug_mode` | Debug | Diagnosis (diagnostic shell ok; avoid permanent edits) |

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

**Why CLI?** Faster iteration, scriptable, avoids creating real artifacts in IDE.

See `tests/commands/README.md` for detailed CLI testing examples and best practices.

### Testing Resources

- `tests/commands/README.md` - Centralized testing guidelines (including CLI testing)
- `tests/commands/llm_testing_framework.md` - LLM-as-judge pattern documentation
- `tests/commands/evaluation_criteria/` - Scoring rubrics per command
- `recurrent_errors/2025-11-27_ai_agent_command_testing_generates_real_artifacts.md` - Common testing pitfalls

### Running Tests

```bash
# Full test (requires cursor-agent)
bash tests/commands/test_xect_execute_plan.sh

# Structure tests only (fast, no cursor-agent needed)
bash tests/commands/test_xect_execute_plan.sh --structure-only
````

For details on the three-tier testing strategy (structure validation, behavior sampling, LLM-as-judge), see `tests/commands/README.md`.
