# Conversation archive – taxonomy-hook-backup-log-file-detection (2025-11-13)

## Summary

This conversation focused on improving the taxonomy hook to catch `.bak` files and log files at root level, and determining the best locations for these file types.

**Key Outcomes**:
- ✅ Taxonomy hook updated to detect root-level `.bak` and `.log` files
- ✅ File location standards documented
- ✅ Existing violations cleaned up (files moved to proper locations)
- ✅ `.gitignore` updated to exclude backup files
- ⚠️ Commit blocked by `scripts/` directory violation (requires separate migration)

**Main Objective**: Enhance taxonomy validation to catch backup and log files at root level, establish file location standards.

---

## Backlog doc

- [taxonomy-hook-backup-log-file-detection_next_actions_2025-11-13.md](../plans/backlog/taxonomy-hook-backup-log-file-detection_next_actions_2025-11-13.md)

---

## Related plans

- **Active**: [taxonomy_hook_improvements_status.md](../plans/active/taxonomy_hook_improvements_status.md) - Execution status document
- **Prioritized**: None
- **Backlog**: taxonomy-hook-backup-log-file-detection_next_actions_2025-11-13.md

---

## Notes

### Technical Decisions

1. **Backup Files**:
   - Temporary backups → `.tmp/` directory
   - Long-term backups → `backup/` directory
   - Best practice: Clean up after verification

2. **Log Files**:
   - Application logs → `logs/` directory
   - Temporary logs → `.tmp/` directory
   - Build/test logs → `logs/build/` or `logs/test/`

3. **Hook Implementation**:
   - Hook moved to `workflows/scripts/validate_taxonomy.py` (correct location)
   - Checks directory violations first, then file violations
   - Provides clear error messages with guidance

### Current Status

- **Code Complete**: All hook improvements implemented and tested
- **File Cleanup**: All violations moved to proper locations
- **Documentation**: File location standards guide created
- **Blocker**: Cannot commit due to `scripts/` directory violation

### Next Steps

1. Migrate `scripts/` directory under `workflows/` (for example, into `workflows/scripts/`, `workflows/cost/`, `workflows/quality/`, `workflows/hooks/`)
2. Update all references to `scripts/` path to point to the new `workflows/` locations
3. Test after migration
4. Commit taxonomy hook improvements

---

**Created**: 2025-11-13
