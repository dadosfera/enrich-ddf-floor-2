# File Location Standards

**Purpose**: Define standard locations for different file types to maintain clean project structure.

---

## 📁 File Type Locations

### Backup Files (`.bak`, `.backup`)

**Best Locations**:
1. **Temporary backups**: `.tmp/` directory
   - Use for backups created during automated operations
   - Should be cleaned up after verification
   - Example: `advanced_auto_fix.py.bak` → `.tmp/advanced_auto_fix.py.bak`

2. **Long-term backups**: `backup/` directory
   - Use for backups that need to be preserved
   - Should be organized by date or purpose
   - Example: `backup/2025-11-12/config.py.bak`

3. **Best Practice**: Clean up `.bak` files after verifying changes
   - `.bak` files are created before destructive operations
   - Once changes are verified, backups can be deleted
   - Use version control (git) for long-term history

**Taxonomy Hook**: Catches `.bak` and `.backup` files at root level

---

### Log Files (`.log`, `*_log.txt`)

**Best Locations**:
1. **Application logs**: `logs/` directory
   - Main application logs
   - Organized by service or component
   - Example: `logs/app.log`, `logs/api.log`

2. **Temporary logs**: `.tmp/` directory
   - Build logs, test logs, temporary output
   - Should be cleaned up regularly
   - Example: `.tmp/build.log`, `.tmp/test.log`

3. **Build/test logs**: `logs/build/` or `logs/test/` subdirectories
   - CI/CD logs
   - Test execution logs
   - Example: `logs/build/deploy.log`, `logs/test/unit.log`

4. **Best Practice**:
   - Rotate logs regularly
   - Use log rotation tools
   - Exclude logs from git (add to `.gitignore`)

**Taxonomy Hook**: Catches `.log` files and `*_log.txt` files at root level

---

### Documentation Files

**Best Locations**:
1. **Reports and summaries**: `docs/reports/` or `docs/summaries/`
2. **Plans and guides**: `docs/plans/` or `docs/guides/`
3. **Status updates**: `docs/status/` or `docs/updates/`
4. **Quick references**: `docs/guides/`

**Taxonomy Hook**: Catches documentation patterns at root level

---

## 🚫 Prohibited Root-Level Files

The following file types should **NOT** be at root level:

- ❌ `.bak` / `.backup` files → Move to `.tmp/` or `backup/`
- ❌ `.log` files → Move to `logs/` or `.tmp/`
- ❌ Documentation files (`*_REPORT.md`, `*_PLAN.md`, etc.) → Move to `docs/`
- ❌ Root-level directories: `active/`, `scripts/` → Move to appropriate locations

---

## ✅ Allowed Root-Level Files

The following files are **allowed** at root level:

- ✅ `README.md` - Project documentation
- ✅ `CHANGELOG.md` - Change history
- ✅ `LICENSE` / `LICENSE.md` - License file
- ✅ `CONTRIBUTING.md` - Contribution guidelines
- ✅ Configuration files: `pyproject.toml`, `package.json`, `Makefile`
- ✅ Essential files: `.gitignore`, `.pre-commit-config.yaml`

---

## 🔧 Migration Guide

### Moving Backup Files

```bash
# Temporary backups → .tmp/
mv *.bak .tmp/

# Long-term backups → backup/
mkdir -p backup/$(date +%Y-%m-%d)
mv *.backup backup/$(date +%Y-%m-%d)/
```

### Moving Log Files

```bash
# Create logs directory if needed
mkdir -p logs

# Move application logs
mv *.log logs/

# Move temporary logs to .tmp/
mv build.log .tmp/
mv test.log .tmp/
```

### Cleanup Script

```bash
# Clean up old backup files
find .tmp -name "*.bak" -mtime +7 -delete

# Clean up old log files
find logs -name "*.log" -mtime +30 -delete
```

---

## 📋 Taxonomy Hook Validation

The taxonomy hook (`workflows/scripts/validate_taxonomy.py`) automatically checks for:

1. ✅ Root-level `.bak` / `.backup` files
2. ✅ Root-level `.log` files
3. ✅ Root-level documentation files
4. ✅ Root-level `active/` directory
5. ✅ Root-level `scripts/` directory

**Pre-commit**: The hook runs automatically on every commit attempt.

**Manual Check**: Run `python3 workflows/scripts/validate_taxonomy.py`

---

## 🎯 Best Practices Summary

1. **Backup Files**:
   - Use `.tmp/` for temporary backups
   - Use `backup/` for long-term backups
   - Clean up after verification

2. **Log Files**:
   - Use `logs/` for application logs
   - Use `.tmp/` for temporary logs
   - Rotate logs regularly

3. **Documentation**:
   - Use `docs/` subdirectories
   - Keep root clean

4. **General Rule**: "Nothing new goes in the project root"

---

**Last Updated**: 2025-11-12
**Related**: `workflows/scripts/validate_taxonomy.py`
