---
category: quality
criticality: medium
scope: all
---
# /cprs_commits_prs_rules_analysis
<!-- COMMAND_ID: 061 -->
<!-- COMMAND_VERSION: 1.2.0 -->
<!-- COMMAND_TYPE: qr_rules_review -->

Analyze the last 1000 commits (in 10 chunks of 100) and the last 100 PRs, then identify recurring mistakes and propose improvements to `.cursor/rules/` (or the repo’s rules source-of-truth, if `.cursor/rules/` is generated). Also includes a churn/stability sweep (“frequent flyer” files) to propose systemic stability fixes.

**Local Reference**: `commands/cprs_commits_prs_rules_analysis.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/cprs_commits_prs_rules_analysis.md`

Backlinks:
- **Local Reference**:
- *Git URL Reference**:
- fera/blob/main/mini_prompt/lv2/git_history_commits_prs_rules_improvement_lv2_mini_prompt.md
- **Local Reference**:
- *Git URL Reference**:
- fera/blob/main/rules/cursor/4_23_rule_distribution_discipline.mdc
- **Local Reference**:
- *Git URL Reference**:
- fera/blob/main/guides/rule_distribution_workflow.md
- **Local Reference**:
- *Git URL Reference**:
- fera/blob/main/guides/distribution/distribution_workflow_unified.md
- **Local Reference**:
- *Git URL Reference**:
- fera/blob/main/commands/lint_lint.md

### Summary

- Scanned: last 1000 commits (10×100) + last 100 PRs + churn scan (fix/fail + frequent flyers)

### Top recurring patterns (ranked)

1. <pattern> (rule/process or stability/churn)

### Proposed changes (rules source-of-truth)

- <rule file / JSON source>:

### Proposed stability fixes (systemic)

- <target file / component>:

### Follow-ups

- <optional: plan to implement rule updates and run distribution>

### Built-in detector: PR stack auto-close signature

When scanning the last 100 PRs, flag pairs that look like: a PR closed within minutes of a merge to main, plus a new PR opened against the same head branch with `Replaces #<orig>` in the body. See `recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md`. When found, recommend verifying `/merg_merge` stack-aware sections and `/gbyp_git_protection_bypass` stack-mode timing.
