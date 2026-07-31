---
category: quality
criticality: medium
scope: all
---
# /lint_lint
<!-- COMMAND_ID: 030 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: li_lint -->

Run repository-wide linting and auto-fix using the pre-commit hooks already configured in `.pre-commit-config.yaml`. Use this after code changes and before /gsyn_git_sync to keep the repo clean and consistent.

**Critical rule**: This command displays guidance only. The AI must manually execute each step individually using terminal commands.

**Critical rule**: Lint configuration is per-repo. Always check `.pre-commit-config.yaml`, `pyproject.toml`, and `config/lint/` first; do NOT assume a fixed tool set.

**Local Reference**: `commands/lint_lint.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/lint_lint.md`

Backlinks:
- .pre-commit-config.yaml
- config/lint/ruff-shared.toml
- docs/guides/cursor-ide-linting-guide.md
- docs/guides/cursor/isort-ruff-configuration-guide.md
- mini_prompt/lv1/automated_linting_mini_prompt.md
- mini_prompt/lv5/automated_linting_mini_prompt.md
- mini_prompt/lv1/git_hooks_optimization_mini_prompt.md

## When to Use

- After substantive code changes, before committing
- When preparing to run /gsyn_git_sync or /gful_git_full_sync
- When a CI pre-commit job has failed and you need to reproduce + fix locally
- When merging or rebasing introduced formatting drift

## When NOT to Use

- On a brand-new clone before installing hooks - run /hook_hooks_setup first
- When the lint failure is in a generated file - fix the generator instead
- When you only need to validate one file - call the relevant linter directly (faster)

## Command sequence (run in order)

### 1. Discover the active lint stack

Each repo configures lint differently. Read the config before running anything.

```bash
gtimeout 5 ls -la .pre-commit-config.yaml pyproject.toml ruff.toml .ruff.toml 2>/dev/null
gtimeout 5 ls config/lint/ 2>/dev/null
```

### 2. Ensure pre-commit is installed and hooks are wired

```bash
gtimeout 10 pre-commit --version
gtimeout 30 pre-commit install --install-hooks
```

### 3. Run pre-commit on changed files (fast)

Default mode used by the pre-commit hook itself.

```bash
gtimeout 120 pre-commit run --files $(git diff --name-only --cached)
# Or, for unstaged changes too:
# gtimeout 120 pre-commit run --files $(git diff --name-only HEAD)
```

### 4. Run pre-commit on the whole repo (slow, before a major sync)

```bash
gtimeout 600 pre-commit run --all-files
```

### 5. Run targeted linters when pre-commit reports failures

Match the failing hook to its underlying tool and run it directly with --fix where supported.

```bash
# Python (Ruff)
gtimeout 60 ruff check --fix .
gtimeout 60 ruff format .

# Shell
gtimeout 60 shellcheck $(git ls-files '*.sh')

# YAML
gtimeout 30 yamllint .

# JSON
gtimeout 30 python -m json.tool path/to/file.json > /dev/null
```

### 6. Re-stage auto-fixed files and re-run

```bash
gtimeout 5 git status
gtimeout 5 git add -A
gtimeout 120 pre-commit run --files $(git diff --name-only --cached)
```

## Failure triage

- **Hook says 'files were modified'**: pre-commit auto-fixed them. Re-stage (Step 6) and run again.
- **Hook says 'something we can't fix automatically'**: read the error, edit the file, re-run.
- **Hook is misconfigured / wrong tool version**: use `/fixh_fix_precommit_errors` and DO NOT just disable the hook.
- **Hook is too slow on large repos**: scope to changed files (Step 3) instead of `--all-files` (Step 4).

## Don'ts

- Don't use `--no-verify` past failing hooks unless remediation was attempted and user authorization was explicitly requested (after checking for concurrent AI sessions).
- Don't blanket-add `# noqa` / `# type: ignore` to silence lint - fix the cause or document the exception.
- Don't edit `.pre-commit-config.yaml` directly to skip a hook (that's a `restricted/` proposal flow).

## Related Commands

- `/fixh_fix_precommit_errors`
- `/hook_hooks_setup`
- `/gsyn_git_sync`
- `/gful_git_full_sync`
