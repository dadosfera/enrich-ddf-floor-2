---
category: documentation
criticality: high
scope: all
---
# /depc_deprecation_sweep
<!-- COMMAND_ID: 081 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: de_deprecation_sweep -->

Run a repo-wide, read-only deprecation sweep to (1) detect deprecated files and (2) find references to deprecated commands/files from non-deprecated sources. This prevents deprecated docs and scripts from silently spreading misinformation.

**Critical rule**: This command is READ-ONLY. Do not delete or move files as part of this sweep.

**Critical rule**: The sweep must scan the entire repository tree, excluding only explicitly allowed heavy/generated directories (e.g. node_modules/, exports/, .git/).

**Local Reference**: `commands/depc_deprecation_sweep.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/depc_deprecation_sweep.md`

Backlinks:
- guides/cursor_commands_sync.md
- guides/technical/deprecate_files_usage.md
- _dev/scripts/quality_governance/deprecation_sweep.py

## When to Use

- You suspect deprecated docs/scripts are still being referenced
- You renamed/migrated commands, workflows, scripts, guides, or standards
- Before/after large documentation refactors to ensure no stale references remain

## When NOT to Use

- As a replacement for actual removals (this produces evidence and a report; removals still need targeted, safe edits)

## Usage

`/depc_deprecation_sweep`

## Command sequence (run in order)

1. Run the sweep script (repo-wide, read-only) and write a JSON report.

```bash
python3 _dev/scripts/quality_governance/deprecation_sweep.py \
  --root . \
  --output analysis/deprecation_sweep_report.json
```

2. Inspect the report and prioritize fixes:
- Fix **non-historical** references first (guides, active scripts, workflows, templates)
- Treat references inside historical areas (e.g. `_dev/docs/plans/finished/`) as informational unless they are causing real confusion

3. Apply targeted updates:
- Update references to replacements (paths/commands)
- If the content should remain: ensure deprecation headers include `REMOVAL_DATE`/`DELETE_AFTER` and `REPLACED_BY` where appropriate
- If the content should be removed: remove only after verifying repo-wide references (use the sweep report as evidence)
