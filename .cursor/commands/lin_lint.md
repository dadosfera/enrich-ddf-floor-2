# /lin_lint

Run repository-wide linting, auto-fix, and config scanning using the existing pre-commit hooks and linting standards (Ruff, shellcheck, YAML/JSON checks). Use this after code changes and before `/git-sync` to keep the repo clean and consistent.

Backlinks:

- .pre-commit-config.yaml
- config/lint/ruff-shared.toml
- docs/guides/cursor-ide-linting-guide.md
- docs/guides/cursor/isort-ruff-configuration-guide.md
- mini_prompt/lv1/automated_linting_mini_prompt.md
- mini_prompt/lv5/automated_linting_mini_prompt.md
- mini_prompt/lv1/git_hooks_optimization_mini_prompt.md

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Quick status snapshot (scope what you are linting)

```bash
gtimeout 5 git status --short | head -40
```

3. Ensure pre-commit is available (linting entry point)

```bash
gtimeout 10 pre-commit --version
```

If this fails, install `pre-commit` in your Python environment (for example with `pip install pre-commit`) before continuing.

4. Run fast, focused Python lint + auto-fix (Ruff only)

```bash
gtimeout 120 pre-commit run ruff --all-files
```

```bash
gtimeout 120 pre-commit run ruff-format --all-files
```

- These use the shared configuration from `pyproject.toml` and `config/lint/ruff-shared.toml`.
- Re-run as needed until errors are fixed or explicitly ignored in config.

5. Run full lint and config scan via pre-commit (all hooks)

```bash
gtimeout 300 pre-commit run --all-files
```

- This will run:
  - Ruff (lint + auto-fix) and Ruff formatter for Python
  - YAML/JSON structure checks
  - Trailing whitespace and end-of-file fixes
  - Shellcheck for `.sh` scripts
- Review the output carefully; fix or adjust configuration instead of blindly ignoring rules.

6. Optional: cosmetic-only linting (style/format passes)

- For large, cosmetic-only cleanups (formatting, style-only rules), follow:
  - `mini_prompt/lv5/automated_linting_mini_prompt.md`
- Keep cosmetic runs separate from functional fixes (dedicated commit).

7. Optional: run central tests to sanity-check after linting

```bash
gtimeout 240 bash tests/run_tests.sh --all
```

- Use `tests/run_tests.sh` scopes (`--category`, `--safe-rm`, etc.) if you want a narrower run first.

8. Final verification before `/git-sync`

```bash
gtimeout 5 git status --short | head -40
```

- Confirm only intentional changes are present (lint fixes, config updates, and related edits).
- When satisfied, use `/git-sync` to stage, commit, and push following the repository's sync policy.
