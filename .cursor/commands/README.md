# Cursor Commands

This directory contains the **canonical source** for all Cursor IDE commands. Commands are distributed to platform-specific directories (`.cursor/commands/` and `.dadosfera/commands/`) and then to other repositories.

## Adding a New Command

**⚠️ MANDATORY WORKFLOW** - Follow all steps or your commit will be blocked by the pre-commit hook.

### Quick Checklist

When adding a new command file to this directory, you **must**:

1. ✅ Create command file in `commands/` (this directory) with a unique 3-letter abbreviation prefix (e.g., `arc_archive.md`)
2. ✅ Run collision check: `python3 _dev/scripts/commands/check_command_collisions.py`
3. ✅ Update command count in `guides/cursor_commands_sync.md`
3. ✅ Add command to list in "Current Commands" section
4. ✅ Update "Last Updated" date in sync guide
5. ✅ Run: `bash scripts/distribution/distribute_platform_commands.sh`
6. ✅ Verify files exist in `.cursor/commands/` and `.dadosfera/commands/`
7. ✅ Update `README.md` (if command should be discoverable)
8. ✅ Commit all changes together

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

## Current Commands

See `guides/cursor_commands_sync.md` for the complete list of canonical commands.

## Command Naming Convention

All commands use unique 3-letter abbreviation prefixes (e.g., `arc_archive`, `rev_review`, `ded_dedup`).

**Collision Avoidance**: Ensure your abbreviation doesn't appear as a substring in other command names (unless they share the same prefix). Use `_dev/scripts/commands/check_command_collisions.py` to verify.

For information about the migration from `gis-*` prefixes, see the [Command Migration Guide](../guides/command_migration_guide.md).
```
