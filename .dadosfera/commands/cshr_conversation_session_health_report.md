---
category: maintenance
criticality: medium
scope: all
---
# /cshr_conversation_session_health_report
<!-- COMMAND_ID: 092 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: cshr_conversation_session_health_report -->

Read-only diagnostic command that generates a comprehensive health report for Claude Code conversation sessions. Classifies all JSONL files, validates sessions-index.json integrity, detects orphaned files, and provides actionable fix recommendations.

**Autonomy Level:** 1 (fully autonomous, read-only — no files modified)

**Session Classification Types:**
- `normal` — 3+ real messages, coherent conversation (keep)
- `file-history-only` — Only metadata messages, 0 real messages (safe to delete)
- `deletion-artifact` — 1-2 messages containing "Conversation deleted permanently" (safe to delete)
- `phantom` — < 4 real messages, tool_result-only user messages (review needed)
- `empty` — 0 messages or 0-byte file (safe to delete)

**Critical rule**: This is a READ-ONLY command. It never modifies files — only reports and recommends.

**Critical rule**: Use /delc --clean-phantoms to act on phantom/junk session recommendations.

**Critical rule**: Use /delc --rebuild-index to fix sessions-index.json issues.

**Local Reference**: `commands/cshr_conversation_session_health_report.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/cshr_conversation_session_health_report.md`

Backlinks:
- commands/delc_delete_conversation.md
- commands/reva_review_active_conversation.md
- agents/session-health.md
- guides/claude/session_health_management.md

## When to Use

- Periodically (weekly) to catch session health issues early
- After bulk deletion operations to verify cleanup was complete
- When conversations show 'No prompt' or crash on resume with 'exit code 1'
- When deleted conversations keep reappearing (phantom bug)
- Before running /delc --clean-phantoms to preview what will be removed

## When NOT to Use

- To actually delete or fix sessions (use /delc --clean-phantoms or --rebuild-index)
- To review conversation content (use /reva)
- For non-Claude-Code platforms (Cline/Dadosfera not yet supported)

## Command sequence (run in order)

### 1. Detect Project and Storage Location

Determine the Claude Code project directory by normalizing the git root path.

```bash
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PROJECT_NAME=$(echo "$GIT_ROOT" | sed 's|[/_\\]|-|g')
CONV_DIR="$HOME/.claude/projects/$PROJECT_NAME"
```

> Path normalization: / _ \ all become -
> Example: /Users/foo/bar → -Users-foo-bar

### 2. Scan and Classify All Sessions

Parse each JSONL file and classify it based on message content and types.

```python
# Classification algorithm (pseudocode)
if total_messages == 0 → empty
if real_messages == 0 → file-history-only
if real_messages <= 2 and contains 'Conversation deleted permanently' → deletion-artifact
if real_messages < 4 and all user messages are tool_result → phantom
else → normal
```

> Metadata types (skipped): file-history-snapshot, queue-operation, custom-title, summary
> Sidechain messages (isSidechain: true) are excluded from real message count
> Conservative: when uncertain, classify as normal (never auto-delete a real conversation)

### 3. Validate sessions-index.json

Compare index entries against actual JSONL files on disk to find ghosts, missing entries, and stale metadata.

```python
# Validation checks
ghosts = index_session_ids - disk_session_ids    # In index, no file on disk
missing = disk_session_ids - index_session_ids   # File on disk, not in index
stale = entries where firstPrompt == 'No prompt' but file has real user messages
```

> Ghost entries cause 'exit code 1' crash when trying to resume the session
> Missing entries cause conversations to not appear in the session picker
> Stale entries show 'No prompt' instead of the actual first user message

### 4. Detect Orphaned Files

Find backup files and subagent directories that are no longer associated with any active session.

```python
backups = glob("*.backup") + glob("*.deleted-backup-*")
orphan_dirs = [d for d in subdirectories if d.name not in active_session_ids]
```

> Backup files accumulate from previous rename/delete operations
> Orphaned subagent directories waste disk space

### 5. Validate Settings

Check .claude/settings.json for known issues like legacy hooks matcher format.

```python
# Check each hook matcher
for matcher in settings.hooks:
    if isinstance(matcher, dict):
        report('legacy matcher format — should be regex string')
```

> Claude Code v2.1.27+ requires matcher to be a regex string, not an object
> Legacy format: {"tools": ["Bash"]} → New format: "Bash"

### 6. Generate Report

Output structured report with classification summary, index validation, orphan detection, and actionable recommendations.

```bash
# Default format: summary text
# --detailed: adds per-session breakdown
# --json: machine-readable JSON output
```

> Always include specific /delc commands in recommendations
> Report is consumed by /delc --health for preview before cleanup

## Command Flags

- *(no flags)* — Default: summary report for current project
- `--detailed` — Include per-session breakdown with classification details
- `--json` — Output as JSON (machine-readable)
- `--phantoms-only` — Only report phantom/junk session classification
- `--index-only` — Only validate sessions-index.json
- `--orphans-only` — Only detect orphaned files
- `--project <name>` — Override project name detection

## Session Classification Reference

| Type | Detection | Action |
|------|-----------|--------|
| `normal` | 3+ real messages (user/assistant), coherent conversation | Keep |
| `file-history-only` | Only file-history-snapshot/queue-operation messages, 0 real messages | Safe to delete |
| `deletion-artifact` | 1-2 real messages, content contains "Conversation deleted permanently" | Safe to delete |
| `phantom` | < 4 real messages, all user messages are tool_result (no user text) | Review needed |
| `empty` | 0 messages total or 0-byte file | Safe to delete |

## Version History

- **v1.0.0** (2026-01-31): Initial implementation
  - Session classification: 5 types (normal, file-history-only, deletion-artifact, phantom, empty)
  - sessions-index.json validation (ghost, missing, stale entries)
  - Orphaned file detection (backups, subagent directories)
  - Settings validation (hooks format)
  - Three output modes: summary, detailed, JSON
  - Focus flags: --phantoms-only, --index-only, --orphans-only
  - Actionable recommendations with fix commands

## Related Commands

- `/delc_delete_conversation`
- `/reva_review_active_conversation`
- `/chkp_check_pending`
