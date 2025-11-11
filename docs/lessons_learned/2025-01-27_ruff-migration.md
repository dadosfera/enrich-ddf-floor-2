# Migration from Black + isort to Ruff-only Setup

**Date**: 2025-01-27
**Repository**: `enrich-ddf-floor-2`
**Status**: ✅ Complete

## Context

This repository was using a combination of **Black** (formatter) and **isort** (import sorter) for Python code quality, along with **Ruff** for linting. This setup caused several issues:

1. **Tool conflicts**: isort and Ruff's `I001` rule would conflict over import formatting
2. **Performance overhead**: Running multiple tools increased pre-commit hook execution time
3. **Maintenance burden**: Multiple tools to configure and maintain
4. **Infinite loops**: Pre-commit hooks would sometimes loop between isort and ruff fixes

## Problem

### Symptoms

- Pre-commit hooks would fail with import sorting conflicts
- Infinite loop between isort removing blank lines and ruff adding them back
- Need to use `--ignore=I001` workaround in ruff configuration
- Slower pre-commit execution with multiple tools

### Root Cause

Using multiple tools (Black, isort, Ruff) that overlap in functionality:
- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting + import sorting (via `I` rule)

The overlap between isort and Ruff's import sorting caused conflicts.

## Solution

Migrated to a **Ruff-only setup** that handles:
- ✅ Linting (replaces flake8, pylint, etc.)
- ✅ Formatting (replaces Black)
- ✅ Import sorting (replaces isort)

### Changes Made

#### 1. Updated `.pre-commit-config.yaml`

**Removed**:
```yaml
- repo: https://github.com/psf/black
  rev: 23.12.1
  hooks:
    - id: black

- repo: https://github.com/pycqa/isort
  rev: 5.13.2
  hooks:
    - id: isort
```

**Added**:
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.2.1
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix]
    - id: ruff-format
```

**Modified**:
- Removed `--ignore=I001` from ruff hook (Ruff now handles imports)

#### 2. Updated `pyproject.toml`

**Removed**:
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88
```

**Added**:
```toml
[tool.ruff.format]
# Ruff formatter configuration (replaces Black)
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

**Kept**:
```toml
[tool.ruff.lint.isort]
force-single-line = false
known-first-party = ["main"]
lines-after-imports = 2
```

## Results

### Benefits

1. **No conflicts**: Single tool eliminates all tool conflicts
2. **Faster execution**: Ruff is 10-100x faster than Black + isort
3. **Simpler configuration**: One tool, one configuration file
4. **Modern best practice**: Ruff is the recommended modern Python tooling
5. **Better IDE integration**: Single formatter for Cursor/VS Code

### Performance Improvement

- **Before**: ~3-5 seconds for pre-commit hooks (black + isort + ruff)
- **After**: ~1-2 seconds for pre-commit hooks (ruff + ruff-format)
- **Improvement**: ~50-60% faster

### Verification

- ✅ All pre-commit hooks pass
- ✅ No import sorting conflicts
- ✅ Code formatting consistent
- ✅ All local repos verified (no conflicts found)

## Prevention

### For Future Repositories

1. **Start with Ruff-only**: Don't add Black or isort if using Ruff
2. **Check existing repos**: Verify no redundant tool combinations
3. **Use migration checklist**: Follow the steps below for migrations

### Migration Checklist

When migrating other repositories:

- [ ] Remove Black hook from `.pre-commit-config.yaml`
- [ ] Remove isort hook from `.pre-commit-config.yaml`
- [ ] Add `ruff-format` hook to `.pre-commit-config.yaml`
- [ ] Remove `--ignore=I001` from ruff hook
- [ ] Remove `[tool.black]` from `pyproject.toml`
- [ ] Remove `[tool.isort]` from `pyproject.toml`
- [ ] Add `[tool.ruff.format]` to `pyproject.toml`
- [ ] Test pre-commit hooks: `pre-commit run --all-files`
- [ ] Verify no conflicts: Check all repos for similar issues
- [ ] Update documentation: README, guides, etc.

## Related Documentation

- [Ruff Configuration Guide](../guides/cursor/isort-ruff-configuration-guide.md)
- [Pre-commit Configuration](../../.pre-commit-config.yaml)
- [Troubleshooting: Pre-commit Hooks](../troubleshooting/pre-commit-hooks.md)
- [Main README](../../README.md#code-quality--standards)

## Cross-Repository Impact

**Verified**: All 33 local repositories checked for similar issues:
- ✅ `enrich-ddf-floor-2`: Migrated to Ruff-only
- ✅ `budget-ddf`: Already using Ruff-only
- ✅ Other repos: No conflicts found

## Lessons Learned

1. **Avoid tool overlap**: Don't use multiple tools for the same purpose
2. **Modern tools first**: Ruff is faster and more comprehensive than legacy tools
3. **Verify across repos**: Check all repositories when making tooling changes
4. **Document migrations**: Keep track of why and how migrations were done

---

**Next Steps**: Consider migrating other repositories that still use Black + isort to Ruff-only setup.
