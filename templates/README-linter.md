# Linter Configuration Templates

This directory contains standardized linter configuration templates for cross-repository standardization.

## Templates

### `pyproject.toml.template`
**Purpose**: Python/Ruff linter configuration

**Features**:
- Focus on functional issues over cosmetic style
- 69+ cosmetic rules ignored (TRY300, SIM108, PLR0915, etc.)
- Enhanced test-specific ignores
- Based on best practices from `enrich-ddf-floor-2` and `gen-ddf-floor-2`

**Usage**:
```bash
cp templates/pyproject.toml.template pyproject.toml
```

### `.pre-commit-config.yaml.template`
**Purpose**: Pre-commit hooks configuration

**Features**:
- Standard hooks (ruff, prettier, shellcheck, etc.)
- Timeout configurations
- Auto-fix capabilities
- Taxonomy validation

**Usage**:
```bash
cp templates/.pre-commit-config.yaml.template .pre-commit-config.yaml
pre-commit install
```

## Migration

Use the migration script to apply templates:
```bash
scripts/quality/linter/migrate-linter-config.sh <repo_path>
```

## Customization

Templates can be customized per repository, but should maintain:
- Focus on functional issues
- Cosmetic rules ignored
- Test-specific leniency

## Related Documentation

- Plan: `active/75_cross_repo_linter_standardization.md`
- Scripts: `scripts/quality/linter/`
