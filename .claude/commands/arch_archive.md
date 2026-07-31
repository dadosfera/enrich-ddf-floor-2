---
category: planning
criticality: medium
scope: all
---
# /arch_archive
<!-- COMMAND_ID: 001 -->
<!-- COMMAND_VERSION: 1.1.1 -->
<!-- COMMAND_TYPE: ar_archive -->

Archive conversation and create backlog plan. **MANDATORY**: run WIP gate (Git evidence) before marking any plan Finished. Never archive with deliverables only in working tree or transcript.

**Critical rule**: This command is an end-of-journey / archival flow. It **must not leave related plans in the active plans directory**.

**Critical rule**: **WIP GATE (P0)**: Before setting status `Finished`, complete the Git evidence checklist below. If `IN_GIT < FILES_CREATED`, status MUST be `Finished (local only — NOT in remote)` — never plain `Finished`.

**Critical rule**: Run `/chkp_check_pending` and `/gscv_git_sync_conversation` (or ask user to commit) **before** archiving code deliverables.

**Critical rule**: See `guides/agent_session_closure.md` for the full session-closure workflow.

**Local Reference**: `commands/arch_archive.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/arch_archive.md`

Backlinks:
- mini_prompt/lv1/archive_conversation_review_and_plan_mini_prompt.md
- guides/agent_session_closure.md
- commands/chkp_check_pending.md
- commands/gscv_git_sync_conversation.md

## Command sequence (run in order)

### 1. WIP gate — Git evidence (MANDATORY before Finished)

Build from tool-call history (Write/StrReplace/EditNotebook/Delete) in this conversation.

```bash
gtimeout 5 git stash list
gtimeout 5 git branch --list 'backup-pre-merge-*' 'wip/*'
# FILES_CREATED from conversation; per path: git log -1 --oneline -- <path>
```

> Checklist: FILES_CREATED, IN_GIT (X/N), STASHES, BACKUP_BRANCHES, RECOMMENDED_ACTION
> If user did not authorize commit: use templates/wip_handoff.md

### 2. Move related plans out of active/

Relocate or finish related active plans per archival policy.

```bash
# Review _dev/docs/plans/active/ for related plans; move to backlog/finished per policy
```

## Git evidence (required in every archived plan)

Every archive plan that delivered code MUST include:

```markdown
## Git evidence

| Path | In git? | Commit hash | Branch | Notes |
|------|---------|-------------|--------|-------|
| path/to/file | yes/no | abc1234 or — | feature/x | |

**FILES_CREATED**: N
**IN_GIT**: X/N
**Stashes**: (output of `git stash list` or "none")
**Backup branches**: (list or "none")
**Status rule**: If X < N → plan status = `Finished (local only — NOT in remote)`
**Recommended action**: commit+push | wip branch | recover stash | user waiver
```

## Commit queue (multi-feature sessions)

When the session touched multiple features, include:

| Feature | Branch | Files | Committed? | Owner | Next action |
|---------|--------|-------|------------|-------|-------------|
| topic-a | wip/topic-a | 3 | no | agent | `/gscv` or user commit |

## Next actions (not-yet-tried / unplanned)

- [ ] Action 1 (clear verb, scope, owner/context if known)

## Context from conversation

- Key decisions, constraints, and notes that justify the next actions

## Links

- Related plans (if any) and references
- `guides/agent_session_closure.md`
- `templates/wip_handoff.md`

## Overview

Brief description and scope.

## Current Status

- Not started; ready to begin
- OR `Finished (local only — NOT in remote)` when Git evidence shows uncommitted deliverables
- OR `Finished` only when IN_GIT = FILES_CREATED (or explicit user waiver documented)

## Pending Tasks

### High Priority

### Medium Priority

- [ ] Task 2

## Next Actions

1. Immediate step 1

## Context from Conversation

- Key decisions and constraints

## Success Criteria

- Expected outcomes and quality bars
- Git evidence section complete before status `Finished`
