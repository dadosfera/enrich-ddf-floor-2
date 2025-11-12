# Troubleshooting Pre-commit Hooks

This guide covers common issues with pre-commit hooks and their solutions.

## Common Issues

### 1. Hook Installation Fails: "Cowardly refusing to install hooks with `core.hooksPath` set"

**Symptoms**:
```
pre-commit install
[ERROR] Cowardly refusing to install hooks with `core.hooksPath` set.
```

**Root Cause**: Git is configured to use a custom hooks path, which conflicts with pre-commit.

**Solution**:
```bash
# Check current Git hooks path
git config --get core.hooksPath

# Unset the custom hooks path
git config --unset-all core.hooksPath

# Now install pre-commit hooks
pre-commit install
```

**Prevention**: Avoid setting `core.hooksPath` when using pre-commit. Pre-commit manages its own hooks.

**Related**: [Pre-commit Documentation](https://pre-commit.com/#conflicting-hooks)

---

### 2. Missing Script Error: "validate_taxonomy.py not found"

**Symptoms**:
```
[ERROR] validate-taxonomy........................................................Failed
- hook id: validate-taxonomy
- exit code: 1
- Could not find script: scripts/validate_taxonomy.py
```

**Root Cause**: The `scripts/validate_taxonomy.py` file is missing or not executable.

**Solution**:
```bash
# Verify the file exists
ls -la scripts/validate_taxonomy.py

# If missing, check if it was deleted or moved
git log --all --full-history -- scripts/validate_taxonomy.py

# Make sure it's executable
chmod +x scripts/validate_taxonomy.py

# Test it manually
python3 scripts/validate_taxonomy.py
```

**Prevention**: Ensure `scripts/validate_taxonomy.py` is committed to the repository and executable.

**Related**: [Scripts Documentation](../../scripts/README.md)

---

### 3. JSON Validation Fails: "check-json" Hook Errors

**Symptoms**:
```
[ERROR] check-json..............................................................Failed
- hook id: check-json
- exit code: 1
- Files were modified by this hook
```

**Root Cause**: The `check-json` hook is trying to validate JSON files in `node_modules/` or `.vscode/` that may contain non-standard JSON.

**Solution**:
1. **Update `.pre-commit-config.yaml`** to exclude problematic directories:
```yaml
- id: check-json
  exclude: (venv/|__pycache__/|\.git/|\.mypy_cache/|\.ruff_cache/|node_modules/|\.vscode/)
```

2. **Verify global exclude pattern**:
```yaml
exclude: ^(venv/|__pycache__/|\.git/|\.mypy_cache/|\.ruff_cache/|\.pytest_cache/|htmlcov/|node_modules/|\.vscode/)
```

**Prevention**: Always exclude `node_modules/` and `.vscode/` from JSON validation hooks.

**Related**: [Pre-commit Configuration](../../.pre-commit-config.yaml)

---

### 4. Import Sorting Conflicts: isort vs Ruff

**Symptoms**:
- Pre-commit hooks loop infinitely
- isort removes blank lines, ruff adds them back
- Error: "Files were modified by this hook" repeatedly

**Root Cause**: Using both `isort` and Ruff's `I` rule for import sorting causes conflicts.

**Solution**:
1. **Migrate to Ruff-only** (recommended):
   - Remove isort hook from `.pre-commit-config.yaml`
   - Remove `--ignore=I001` from ruff hook
   - Let Ruff handle all import sorting

2. **Or disable Ruff's import sorting** (not recommended):
   - Add `--ignore=I001` to ruff hook
   - Keep isort for import sorting

**Prevention**: Use Ruff-only setup. Don't combine isort with Ruff.

**Related**:
- [Ruff Migration Guide](../lessons_learned/2025-01-27_ruff-migration.md)
- [Ruff Configuration Guide](../guides/cursor/isort-ruff-configuration-guide.md)

---

### 5. Commit Message Validation Fails: "commitlint" Errors

**Symptoms**:
```
[ERROR] commitlint................................................................Failed
- hook id: commitlint
- exit code: 1
- ⧗   input: your commit message
- ✖   header must not be longer than 72 characters
```

**Root Cause**: Commit message doesn't follow conventional commit format or exceeds length limits.

**Solution**:
1. **Follow conventional commit format**:
   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```

2. **Keep header under 72 characters**

3. **Valid types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Example**:
```bash
# Good
git commit -m "fix: resolve pre-commit hook conflicts"

# Bad (too long)
git commit -m "fix: resolve pre-commit hook conflicts between isort and ruff that were causing infinite loops"
```

**Prevention**: Use conventional commit format. Keep messages concise.

**Related**: [Conventional Commits](https://www.conventionalcommits.org/)

---

### 6. Ruff Formatting Conflicts

**Symptoms**:
- Ruff format makes changes, but they conflict with other formatters
- Files keep getting reformatted on each commit

**Root Cause**: Multiple formatters configured (e.g., Black + ruff-format).

**Solution**:
1. **Use Ruff-only** (recommended):
   - Remove Black from `.pre-commit-config.yaml`
   - Use only `ruff-format` hook

2. **Or disable Ruff formatting**:
   - Remove `ruff-format` hook
   - Use only Black

**Prevention**: Use a single formatter. Don't combine Black with ruff-format.

**Related**: [Ruff Migration Guide](../lessons_learned/2025-01-27_ruff-migration.md)

---

## General Troubleshooting Steps

### 1. Verify Pre-commit Installation

```bash
# Check if pre-commit is installed
pre-commit --version

# Check if hooks are installed
ls -la .git/hooks/pre-commit

# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### 2. Run Hooks Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Run hooks with verbose output
pre-commit run --all-files --verbose
```

### 3. Clear Pre-commit Cache

```bash
# Clear cache if hooks are behaving unexpectedly
pre-commit clean

# Reinstall after clearing
pre-commit install
```

### 4. Check Hook Configuration

```bash
# Validate .pre-commit-config.yaml
pre-commit validate-config

# List all configured hooks
pre-commit run --all-files --hook-stage pre-commit
```

### 5. Update Hook Versions

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Test after update
pre-commit run --all-files
```

## Getting Help

If issues persist:

1. **Check logs**: Run hooks with `--verbose` flag
2. **Review configuration**: Verify `.pre-commit-config.yaml` syntax
3. **Check documentation**: See related guides and lessons learned
4. **Test manually**: Run individual tools (ruff, shellcheck, etc.) manually

## Related Documentation

- [Pre-commit Configuration](../../.pre-commit-config.yaml)
- [Ruff Migration Guide](../lessons_learned/2025-01-27_ruff-migration.md)
- [Ruff Configuration Guide](../guides/cursor/isort-ruff-configuration-guide.md)
- [Scripts Documentation](../../scripts/README.md)
- [Main README](../../README.md#pre-commit-hooks)

---

**Last Updated**: 2025-01-27
