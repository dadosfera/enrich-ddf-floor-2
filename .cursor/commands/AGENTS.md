# AGENTS.md

## Purpose
Documents the expected agents (AI/human) for the `commands/` folder, which contains canonical Cursor IDE commands.

## Agents

- **AI Command Agents**
  - **Role:** Create, maintain, and distribute Cursor IDE commands following the canonical workflow.
  - **Entrypoints:**
    - `commands/`: Command definition files
    - `commands/index_commands.yaml`: Command index
  - **Special Instructions:**
    - Follow the mandatory workflow when adding new commands (see `commands/README.md`).
    - Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
    - Update `commands/index_commands.yaml` when adding new commands.
    - Run distribution script: `bash scripts/distribution/distribute_platform_commands.sh`
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
