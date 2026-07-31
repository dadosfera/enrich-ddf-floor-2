---
category: git
criticality: medium
scope: all
---
# /hook_hooks_setup
<!-- COMMAND_ID: 034 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ho_hooks_setup -->

Set up and standardize git hooks (pre-commit + optional pre-push) and, when applicable, npm/yarn/pnpm lifecycle scripts that keep hooks installed automatically.

**Local Reference**: `commands/hook_hooks_setup.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/hook_hooks_setup.md`

Backlinks:
- **Local Reference**:
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/standards/git/git_hooks_standard.md
- **Local Reference**:
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/pre_commit_maturity.md
- **Local Reference**:
- commit-config.yaml.template
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/templates/pre-commit-config.yaml.template
- **Local Reference**:
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/git_hooks_optimization_lv1_mini_prompt.md
- **Local Reference**:
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/ignore_files_hooks_linters_check.md
- **Local Reference**:
- *Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/commands/lint_lint.md

## When to Use

- New or existing repos that should use **pre-commit** for linting, formatting, and structural checks.
- Repos where developers sometimes commit without hooks installed.
- When introducing npm/yarn/pnpm workflows and you want them to keep hooks installed automatically.

## When NOT to Use

- Repos that intentionally do **not** use git hooks (rare; usually not recommended).
- CI-only enforcement scenarios where local hooks are explicitly out of scope (use CI config instead).
