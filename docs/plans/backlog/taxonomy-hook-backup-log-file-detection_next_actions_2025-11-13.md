# taxonomy-hook-backup-log-file-detection – next actions

**Status**: backlog
**Created from**: Conversation review on 2025-11-13
**Objective**: Improve taxonomy hook to catch .bak files and log files at root level, determine best locations
**Priority**: Medium
**Estimated effort**: 1 AI hour / 0.5 Human hours

---

## Next actions (not-yet-tried / unplanned)

- [x] **Migrate scripts/ directory under workflows/**
  - **Rationale**: Resolve taxonomy violation blocking commits
  - **Scope**: Move all files from `scripts/` to appropriate locations under `workflows/` (for example, `workflows/scripts/`, `workflows/cost/`, `workflows/quality/`, `workflows/hooks/`)
  - **Owner**: AI Agent + Human Review
  - **Estimated Time**: 30-60 minutes

- [x] **Update all references to scripts/ path**
  - **Rationale**: Update paths in scripts, Makefiles, documentation after migration
  - **Scope**: Replace `scripts/` references with the new `workflows/` locations used in this repository (for example, `workflows/scripts/`, `workflows/cost/`, `workflows/quality/`, `workflows/hooks/`)
  - **Owner**: AI Agent
  - **Estimated Time**: 30-60 minutes

- [ ] **Test repository after scripts/ migration**
  - **Rationale**: Ensure all scripts still work after move
  - **Scope**: Run tests, verify Makefile targets, check documentation links
  - **Owner**: AI Agent + Human Review
  - **Estimated Time**: 15-30 minutes

- [ ] **Commit taxonomy hook improvements**
  - **Rationale**: Save completed work (hook improvements, file cleanup, documentation)
  - **Scope**: Single commit with all improvements
  - **Owner**: AI Agent
  - **Estimated Time**: 5 minutes

- [ ] **Create cleanup script for old backup/log files**
  - **Rationale**: Automate cleanup of old `.bak` and `.log` files from `.tmp/` and `logs/`
  - **Scope**: Utility script for maintenance
  - **Owner**: AI Agent
  - **Estimated Time**: 30 minutes

- [ ] **Set up log rotation for logs/ directory**
  - **Rationale**: Implement log rotation as mentioned in documentation
  - **Scope**: Configure log rotation for application logs
  - **Owner**: AI Agent
  - **Estimated Time**: 30-60 minutes

---

## Context from conversation

### Completed Actions ✅

1. **Taxonomy Hook Improvements**:
   - Added detection for root-level `.bak` and `.backup` files
   - Added detection for root-level `.log` files and `*_log.txt` patterns
   - Updated hook documentation (`workflows/scripts/validate_taxonomy.py`)

2. **File Cleanup**:
   - Moved `.bak` files to `.tmp/` (advanced_auto_fix.py.bak, main.py.bak)
   - Moved `.log` files to `logs/` (ruff_post_fix.log, ruff_advanced_fix.log)

3. **Documentation**:
   - Created `docs/guides/file_location_standards.md` with best practices
   - Documented best locations for backup and log files

4. **.gitignore Updates**:
   - Added `.bak` and `.backup` patterns
   - Added `backup/` directory
   - `.log` patterns already present

### Current Blocker ⚠️

**Issue**: Cannot commit changes because taxonomy hook detects `scripts/` directory violation

**Root Cause**: The `scripts/` directory exists at root level, violating "Nothing new goes in root" rule

**Impact**: All improvements complete and tested, but commit blocked until `scripts/` directory is migrated

### Key Decisions

- **Backup Files Location**: `.tmp/` for temporary, `backup/` for long-term
- **Log Files Location**: `logs/` for application logs, `.tmp/` for temporary logs
- **Hook Location**: Moved to `workflows/scripts/validate_taxonomy.py` (correct location)
- **Validation Order**: Check directory violations first, then file violations

### Constraints

- Hook must run from `workflows/scripts/` to avoid bootstrap issue
- Root-level violations should fail pre-commit hook
- Backup files should be cleaned up after verification
- Log files should be rotated regularly

---

## Links

- **Related Plans**:
  - [taxonomy_hook_improvements_status.md](../active/taxonomy_hook_improvements_status.md) - Execution status
- **Documentation**:
  - [file_location_standards.md](../../guides/file_location_standards.md) - File location best practices
  - [validate_taxonomy.py](../../../workflows/scripts/validate_taxonomy.py) - Taxonomy hook implementation
- **Related Rules**:
  - Folder structure discipline rules
  - File lifecycle discipline rules

---

**Last Updated**: 2025-11-13
