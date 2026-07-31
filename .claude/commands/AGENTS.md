# AGENTS.md

## Purpose
Documents the expected agents (AI/human) for the `commands/` folder, which contains canonical slash commands (AI agent commands invoked with `/command_name` syntax).

## Agents

- **AI Command Agents**
  - **Role:** Create, maintain, and distribute slash commands following the canonical workflow.
  - **Entrypoints:**
    - `commands/`: Command definition files
    - `commands/index_commands.yaml`: Command index
  - **Special Instructions:**
    - Follow the mandatory workflow when adding new commands (see `commands/README.md`).
    - **JSON-first** (default): edit `commands/json/core/<id>_<name>.json`, then run `bash _dev/workflows/command_distribution/build_commands_from_json.sh`.
    - **Markdown-only** (exceptions): edit `commands/<name>.md` directly for commands listed in `commands/markdown_only_commands.yaml`. Never create a stub JSON for these — distribute with `bash _dev/scripts/distribution/distribute_platform_commands.sh`.
    - Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
    - Update `commands/index_commands.yaml` when adding new commands.
    - Run distribution script: `bash _dev/scripts/distribution/distribute_platform_commands.sh`
    - Treat that script as repo-local platform distribution only. For cross-repo rollout, first classify targets with `guides/distribution/repository_distribution_classes.md`: `docs-fera` is source-only, `*-fera` repos are D&ADDF infrastructure consumers, `*-ddf*`/similar non-fera repos are product consumers, and unrelated non-fera repos require explicit opt-in.
    - Ensure commands are listed in `guides/cursor_commands_sync.md`.
    - Never bypass pre-commit validation for command additions.

- **Human Command Maintainers**
  - **Role:** Review command additions, approve command workflows, and ensure command quality.
  - **Entrypoints:** All files in `commands/`.
  - **Special Instructions:**
    - Review PRs for compliance with command workflow requirements.
    - Ensure commands follow naming conventions (3-letter abbreviation prefixes).
    - Validate that distribution scripts have been run.
    - Verify command count matches actual files.
