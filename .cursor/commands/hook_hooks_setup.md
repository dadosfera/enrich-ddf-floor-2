# /hook_hooks_setup
<!-- COMMAND_ID: 034 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ho_hooks_setup -->

Set up and standardize git hooks (pre-commit + optional pre-push) and, when applicable, npm/yarn/pnpm lifecycle scripts that keep hooks installed automatically.

**Local Reference**: `commands/hook_hooks_setup.md`
**Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/commands/hook_hooks_setup.md

Backlinks:

- **Local Reference**: `standards/git/git_hooks_standard.md`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/standards/git/git_hooks_standard.md
- **Local Reference**: `standards/maturity/pre_commit_maturity.md`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/standards/maturity/pre_commit_maturity.md
- **Local Reference**: `templates/pre-commit-config.yaml.template`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/templates/pre-commit-config.yaml.template
- **Local Reference**: `mini_prompt/lv1/git_hooks_optimization_mini_prompt.md`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/git_hooks_optimization_mini_prompt.md
- **Local Reference**: `mini_prompt/ignore_files_hooks_linters_check.md`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/ignore_files_hooks_linters_check.md
- **Local Reference**: `commands/lint_lint.md`
  **Git URL Reference**: https://github.com/dadosfera/docs-fera/blob/main/commands/lint_lint.md

## Purpose

- **Bootstrap hooks**: Ensure `.pre-commit-config.yaml` exists and pre-commit is installed and wired to the repo.
- **Standardize behavior**: Align with Dadosfera git hook standards and pre-commit maturity model.
- **Keep hooks installed**: Optionally wire npm/yarn/pnpm lifecycle scripts so hooks stay active after installs.

## When to Use

- New or existing repos that should use **pre-commit** for linting, formatting, and structural checks.
- Repos where developers sometimes commit without hooks installed.
- When introducing npm/yarn/pnpm workflows and you want them to keep hooks installed automatically.

## When NOT to Use

- Repos that intentionally do **not** use git hooks (rare; usually not recommended).
- CI-only enforcement scenarios where local hooks are explicitly out of scope (use CI config instead).

## Pattern Selection

### When to Use Pattern A (Direct Pre-commit)

- Python-first projects
- Simple projects without Node.js tooling
- No custom pre-push infrastructure checks needed
- Minimal setup requirements

### When to Use Pattern B (Husky Hybrid)

- Node.js projects with lint-staged
- Need NVM/Node environment setup
- Require custom pre-push checks (infrastructure, IP validation, etc.)
- Want automatic hook installation via npm lifecycle

## Command sequence (run in order)

**All commands must be run individually with `run_terminal_cmd` using `gtimeout`, no chaining with `&&`, and no `--no-verify` flags.**

1. Verify repository context and pre-commit availability

   ```bash
   gtimeout 5 git rev-parse --show-toplevel
   ```

   ```bash
   gtimeout 10 pre-commit --version
   ```

   - If `pre-commit` is missing, install it first (for example with `pip install pre-commit` in your Python environment).

2. Ensure `.pre-commit-config.yaml` exists (copy from template if needed)

   ```bash
   gtimeout 5 ls .pre-commit-config.yaml
   ```

   - If this fails, create the config from the shared template:

   ```bash
   gtimeout 5 cp templates/pre-commit-config.yaml.template .pre-commit-config.yaml
   ```

   - After copying, review and adjust hooks to match the repository’s languages and standards.

3. Install the core `pre-commit` hook

   ```bash
   gtimeout 15 pre-commit install
   ```

   - This writes `.git/hooks/pre-commit` and ensures local commits are gated by the configured hooks.

4. (Optional but recommended) Install a `pre-push` hook

   ```bash
   gtimeout 15 pre-commit install --hook-type pre-push
   ```

   - Use this when you want stronger guarantees before code leaves the workstation (tests, heavier checks).

5. Configure npm/yarn/pnpm lifecycle scripts (only if `package.json` exists)

   **For Pattern A (Direct Pre-commit):**

   - If the repository uses Node tooling, open `package.json` and ensure there is a lifecycle script that keeps hooks installed, for example:

   ```jsonc
   {
     "scripts": {
       // ...other scripts...
       "postinstall": "pre-commit install --install-hooks || true"
     }
   }
   ```

   - Keep this idempotent and tolerant (`|| true`) so installs don't fail on environments without Python/pre-commit available.
   - For **Python-first projects**, reuse your existing install/bootstrapping flow (`pip install`, `pip install -e .`, `poetry install`, `requirements*.txt`-driven setup, `make hooks-install`, etc.) and consider adding a small wrapper that runs `pre-commit install --install-hooks` as part of that flow.
   - For **other ecosystems** (Ruby, Go, Java, etc.), explicitly web-search for the appropriate lifecycle hook (for example: `"&lt;language&gt; run script after dependency install"`) and then call `pre-commit install --install-hooks` from that hook so behavior matches the Node/Python patterns.

   **For Pattern B (Husky Hybrid):**

   - Install Husky:

   ```bash
   gtimeout 30 npm install --save-dev husky
   gtimeout 10 npx husky install
   ```

   - Configure `package.json`:

   ```jsonc
   {
     "scripts": {
       "prepare": "husky"
     },
     "lint-staged": {
       "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"]
     }
   }
   ```

   - Create `.husky/pre-commit` (see Pattern B example in `standards/git/git_hooks_standard.md`)
   - Create `.husky/pre-push` (see Pattern B example in `standards/git/git_hooks_standard.md`)
   - Make hooks executable:

   ```bash
   chmod +x .husky/pre-commit .husky/pre-push
   ```

   - Install pre-commit hooks:

   ```bash
   gtimeout 15 pre-commit install --hook-type pre-commit
   gtimeout 15 pre-commit install --hook-type pre-push
   ```

6. Run hooks once on the full repo to validate setup

   ```bash
   gtimeout 300 pre-commit run --all-files
   ```

   - Fix any reported issues or adjust `.pre-commit-config.yaml` rather than disabling or skipping hooks.

7. Final verification and commit

   ```bash
   gtimeout 5 git status --short | head -40
   ```

   - Confirm only intentional changes are present (new `.pre-commit-config.yaml`, hook tweaks, and any auto-fixes).
   - Commit with a clear message (for example, `chore: setup git hooks with pre-commit`) and **never** bypass hooks with `--no-verify`.
