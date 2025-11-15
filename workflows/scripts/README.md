# Scripts Directory

This directory contains utility scripts for development, quality assurance, and project maintenance.

## Overview

Domain-specific workflows live under `workflows/cost/`, `workflows/quality/`, and `workflows/hooks/`.
This directory (`workflows/scripts/`) contains shared utility scripts and cross-repo tools that those workflows can call.

Scripts in this directory are used for:
- **Pre-commit hooks**: Quality checks before commits
- **Project validation**: Ensuring project structure compliance
- **Development utilities**: Helper scripts for common tasks

## Scripts

### `validate_taxonomy.py`

**Purpose**: Validates project directory structure and naming conventions.

**Usage**:
```bash
# Run manually
python3 workflows/scripts/validate_taxonomy.py

# Runs automatically via pre-commit hooks
```

**What it checks**:
1. **Required directories**: Verifies presence of standard project directories:
   - `config/` - Configuration files
   - `docs/` - Documentation
   - `tests/` - Test files
   - `workflows/` - Workflow scripts (including `workflows/scripts/` for utility scripts)

2. **Invalid directory names**: Prevents directories with problematic patterns:
   - `-copy` - Indicates duplicate/clone directories
   - `-backup` - Backup directories
   - `-partial` - Incomplete/partial directories

**Exit codes**:
- `0` - All checks passed
- `1` - Invalid directory name detected (fails pre-commit)

**Configuration**:
- Required directories are defined in `REQUIRED_DIRS` list
- Invalid patterns are defined in `invalid_patterns` list
- Currently set to warn (not fail) on missing directories

**Integration**:
- Configured as a local pre-commit hook in `.pre-commit-config.yaml`
- Runs automatically on every commit attempt
- Can be run manually for validation

**Related Documentation**:
- [Pre-commit Configuration](../.pre-commit-config.yaml)
- [Project Structure Rules](../.cursor/rules/4_01_folder_structure_discipline.mdc)
- [Main README](../README.md#project-structure-validation)

### `quality_governance/pre_commit/canonical_taxonomy_protection.sh`

**Purpose**: Shell script version of taxonomy validation (if needed).

**Note**: The Python version (`validate_taxonomy.py`) is preferred and actively used.

### Other Scripts

- `access_ignored_file.sh` - Access files in `.cursorignore`
- `cursor_ignore_override.sh` - Temporarily override cursor ignore patterns
- `cursor_ignore_restore.sh` - Restore cursor ignore patterns
- `test_dynamic_ports.sh` - Test dynamic port allocation
- `update_documentation_ports.sh` - Update port documentation
- `bulk-update-repo.sh` - Cross-repo standardization helper (expects this repo to use `workflows/` layout)

## Adding New Scripts

When adding new scripts:

1. **Add documentation** to this README
2. **Make executable**: `chmod +x workflows/scripts/your_script.sh`
3. **Add to pre-commit** if it should run automatically
4. **Follow naming conventions**: Use lowercase with underscores
5. **Include usage examples** in script comments

## Pre-commit Integration

Scripts can be integrated as pre-commit hooks by adding to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: your-script-id
      name: Your Script Description
      entry: python3 workflows/scripts/your_script.py
      language: system
      pass_filenames: false
```

## Related Documentation

- [Pre-commit Hooks Documentation](../README.md#pre-commit-hooks)
- [Troubleshooting Pre-commit Issues](../docs/troubleshooting/pre-commit-hooks.md)
- [Project Structure Rules](../.cursor/rules/4_01_folder_structure_discipline.mdc)
