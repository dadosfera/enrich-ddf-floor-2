# pre-commit-ruff-migration-docs-organization – next actions

Status: backlog
Created from: Conversation review on 2025-11-12
Objective: pre-commit-ruff-migration-docs-organization
Priority: Medium
Estimated effort: 2-4 AI hours / 1-2 Human hours

## Next actions (not-yet-tried / unplanned)

- [ ] Migrate other repositories to Ruff-only setup
  - **Scope**: Check and migrate 31+ local repositories that may still use Black + isort
  - **Context**: `enrich-ddf-floor-2` and `budget-ddf` already use Ruff-only; verify others and migrate if needed
  - **Impact**: Medium (improves consistency and performance across repos)
  - **Effort**: Medium (requires checking each repo's `.pre-commit-config.yaml` and `pyproject.toml`)
- [ ] Verify taxonomy validation hook passes on next commit
  - **Scope**: Ensure no remaining root-level documentation files are flagged
  - **Context**: Taxonomy validation hook was flagging files during commits; most have been moved
  - **Impact**: Low (verification/cleanup)
  - **Effort**: Low (test commit or dry-run)

## Context from conversation

- **Primary objectives completed**:

  - ✅ Migrated `enrich-ddf-floor-2` from Black + isort to Ruff-only setup
  - ✅ Fixed pre-commit hook errors (created `validate_taxonomy.py`, restored config)
  - ✅ Organized documentation files into proper subdirectories (guides, reports, status, summaries, updates, plans)
  - ✅ Archive command copied and committed
  - ✅ Conversation file moved to `docs/conversations/`
  - ✅ All formatting fixes applied and committed

- **Key decisions**:

  - Ruff replaces Black, isort, flake8, and other linting tools (10-100x faster)
  - Documentation should be organized in `docs/` subdirectories by type
  - Pre-commit hooks should validate project taxonomy

- **Constraints**:

  - Cross-repository migration is outside current conversation scope
  - Only `README.md` and `requirements-minimal.txt` remain at root (appropriate)

- **Notes**:
  - All 33 local repositories were checked for ruff/isort conflicts
  - `budget-ddf` already uses Ruff-only (ideal setup)
  - Migration to Ruff-only provides significant performance improvements

## Links

- Conversation: `docs/conversations/cursor_can_you_run_the_app.md`
- Pre-commit config: `.pre-commit-config.yaml`
- Ruff config: `pyproject.toml`
- Taxonomy validation: `scripts/validate_taxonomy.py`
