---
category: infrastructure
criticality: medium
scope: all
---
# /crcv_cross_repo_convergence
<!-- COMMAND_ID: 005 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: cr_cross_repo_convergence -->

Cross-repository convergence workflow for fixing inconsistencies across all Dadosfera repositories. Use this when you identify a pattern that varies between repos and needs standardization.

**Local Reference**: `commands/crcv_cross_repo_convergence.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/crcv_cross_repo_convergence.md`

Backlinks:
- mini_prompt/lv1/cross_repo_convergence_mini_prompt.md
- standards/run_sh_resource_monitoring_compliance.md (example standard)
- scripts-fera/repo-management/check_console_log_compliance.sh (example check script)

## When to Use

- You notice the same thing is done differently in multiple repos
- A standard exists but repos don't follow it consistently
- You want to roll out a new standard across all repos
- You need to verify compliance across the organization

## Context

This plan was created by the cross-repo convergence workflow from docs-fera.

## Tasks

(Use standard status indicators: `[ ]`, `[~]`, `[x]`, etc. See `standards/project/task_status_standard.md`)

## Standard Reference

See: `docs-fera/standards/{topic}_standard.md`
