# isort/Ruff Configuration Guide for Cursor IDE

**Last Updated**: 2025-01-27
**Applies to**: All repositories using Ruff for import sorting
**Migration Status**: ✅ Migrated from Black + isort to Ruff-only (2025-01-27)

## Overview

This guide explains how to properly configure Cursor IDE to work with Ruff-based import sorting and prevent isort extension conflicts.

**Recent Migration**: This repository has been migrated from a Black + isort setup to a Ruff-only configuration. This eliminates tool conflicts, improves performance, and simplifies maintenance. See [Migration Details](#migration-from-black--isort) below.

## Problem

When using **Ruff** for import sorting (via the `I` rule in `pyproject.toml`), the standalone isort extension in Cursor IDE can cause conflicts:

- **Server crashes**: "The isort server crashed 5 times in the last 3 minutes"
- **Connection errors**: "Pending response rejected since connection got disposed"
- **Extension conflicts**: isort extension tries to start even when isort isn't installed

## Solution

Disable the isort extension in workspace settings and configure Ruff as the formatter.

## Configuration Steps

### Step 1: Verify Ruff Configuration

Ensure your `pyproject.toml` has Ruff configured with the `I` rule for import sorting:

```toml
[tool.ruff]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort (import sorting)
    # ... other rules
]

[tool.isort]
# This config is used by Ruff's isort plugin, not standalone isort
profile = "black"
line_length = 88
```

### Step 2: Configure Cursor Settings

Add the following to `.cursor/settings.json` (or `.vscode/settings.json`):

```json
{
  "isort.server.enabled": false,
  "isort.check": false,
  "isort.enabled": false,
  "isort.args": [],
  "python.sortImports.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  }
}
```

### Step 3: Reload Cursor Window

**Critical**: After updating settings, you must reload the Cursor window:

1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Developer: Reload Window"
3. Press Enter

### Step 4: Verify Configuration

After reloading, verify:

- ✅ No "isort server crashed" errors
- ✅ No "Pending response rejected" errors
- ✅ Import sorting works on save (via Ruff)

## Settings Explanation

### `isort.server.enabled: false`

Disables the isort language server completely, preventing crashes.

### `isort.check: false`

Disables isort checking on save.

### `isort.enabled: false`

Completely disables the isort extension.

### `python.sortImports.provider: "none"`

Tells Cursor not to use any provider for import sorting (Ruff handles it via formatter).

### Ruff Configuration

- `editor.defaultFormatter: "charliermarsh.ruff"` - Uses Ruff for formatting
- `source.organizeImports: "explicit"` - Ruff organizes imports on save

## Troubleshooting

### Errors Persist After Reload

If you still see isort errors after reloading:

1. **Manually disable extension**:

   - Press `Cmd+Shift+X` to open Extensions
   - Search for "isort"
   - Click gear icon → "Disable (Workspace)"

2. **Clear extension cache** (if needed):

   ```bash
   rm -rf ~/Library/Application\ Support/Cursor/CachedExtensions
   ```

3. **Uninstall extension** (last resort):
   - Extensions view → isort → Uninstall
   - Reload window

### Import Sorting Not Working

If imports aren't being sorted on save:

1. Verify Ruff extension is installed and enabled
2. Check `pyproject.toml` has `"I"` in Ruff's `select` list
3. Verify `editor.formatOnSave: true` in settings
4. Check Ruff extension logs: `Cmd+Shift+P` → "Ruff: Show Output"

### Standalone isort Projects

If your project uses standalone isort (not Ruff):

1. Install isort in your virtual environment:

   ```bash
   pip install isort
   ```

2. Keep isort extension enabled (or install it)

3. Configure `python.sortImports.provider: "isort"` in settings

## Cross-Repository Setup

When setting up a new repository:

1. Copy `.cursor/settings.json` from a correctly configured repo
2. Ensure `pyproject.toml` has Ruff configured with `"I"` rule
3. Reload Cursor window after opening workspace

## Verification Checklist

- [ ] `pyproject.toml` has Ruff with `"I"` rule
- [ ] `.cursor/settings.json` has `isort.server.enabled: false`
- [ ] `.cursor/settings.json` has `python.sortImports.provider: "none"`
- [ ] `.cursor/settings.json` has Ruff as default formatter
- [ ] Cursor window has been reloaded
- [ ] No isort server crash errors
- [ ] Import sorting works on save

## Migration from Black + isort

**Date**: 2025-01-27
**Status**: ✅ Complete

### What Changed

1. **Removed tools**:

   - `black` - Replaced by `ruff format`
   - `isort` - Replaced by Ruff's `I` rule

2. **Updated pre-commit hooks**:

   - Removed `black` hook
   - Removed `isort` hook
   - Added `ruff-format` hook
   - Removed `--ignore=I001` from ruff (Ruff now handles imports)

3. **Updated configuration**:
   - Removed `[tool.black]` from `pyproject.toml`
   - Removed `[tool.isort]` from `pyproject.toml`
   - Added `[tool.ruff.format]` section
   - Updated comments to reflect Ruff-only setup

### Benefits

- ✅ **No conflicts**: Single tool eliminates isort/ruff/black conflicts
- ✅ **Faster**: Ruff is 10-100x faster than Black + isort
- ✅ **Simpler**: One tool, one configuration
- ✅ **Modern**: Ruff is the recommended modern Python tooling

### Migration Steps (for other repos)

1. Remove Black and isort from `.pre-commit-config.yaml`
2. Add `ruff-format` hook
3. Remove `--ignore=I001` from ruff hook
4. Update `pyproject.toml` to remove Black/isort configs
5. Add `[tool.ruff.format]` section
6. Test pre-commit hooks

See [Lessons Learned: Ruff Migration](../../lessons_learned/2025-01-27_ruff-migration.md) for detailed migration guide.

## Related Documentation

- [Lessons Learned: Ruff Migration](../../lessons_learned/2025-01-27_ruff-migration.md) - Detailed migration guide
- [Troubleshooting: Pre-commit Hooks](../../troubleshooting/pre-commit-hooks.md) - Common pre-commit issues
- [Main README](../../../README.md#code-quality--standards) - Project code quality standards
- [Pre-commit Configuration](../../../.pre-commit-config.yaml) - Current hook configuration

## Quick Reference

**Settings to add:**

```json
{
  "isort.server.enabled": false,
  "isort.check": false,
  "isort.enabled": false,
  "python.sortImports.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  }
}
```

**After updating settings:**

1. Reload window: `Cmd+Shift+P` → "Developer: Reload Window"
2. Verify no errors
3. Test import sorting on save

---

**Questions?** Check the troubleshooting section or related documentation links above.
