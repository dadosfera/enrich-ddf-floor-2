---
category: infrastructure
criticality: medium
scope: all
---
# /prop_propagate_fixes
<!-- COMMAND_ID: 038 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pr_propagate_fixes -->

End-of-session command that journals all fixes made during a long debugging/development conversation and propagates them to all deployment targets: local repo, cloud instances, container registries, and Infrastructure-as-Code.

**Local Reference**: `commands/prop_propagate_fixes.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/prop_propagate_fixes.md`

Backlinks:
- mini_prompt/lv2/cloud_vs_local_repo_state_sync_mini_prompt.md
- commands/gsyn_git_sync.md
- commands/docu_document.md
- lessons_learned/

## Quick Checklist (TL;DR)

(Use standard status indicators. See `standards/project/task_status_standard.md`)

## Summary

Brief description of what application/service was being fixed.

## Environment

- Instance: (OCI instance name/IP, AWS EC2, etc.)

### Fix 1: [Short description]

- **Problem**: What was failing

### Fix 2: [Short description]

(repeat for each fix)

## Configuration Changes

- Environment variables added/changed

## Infrastructure Changes Needed

(Use standard status indicators)

## Follow-up Tasks

(Use standard status indicators)

### Previous Working State

- Commit: <previous-commit-hash>

## Post-Deployment Health (5 min after deploy)

- [ ] No new errors in logs

### Repository

- [x] Changes committed: <commit-hash>

### Cloud Instance

- [x] Code synced to: <instance-name>

### Container Registry

- [x] Image pushed: <image:tag>

### Infrastructure as Code

- [x] Updated files: <file-list>

### Verification

- [x] Health check: PASSED
