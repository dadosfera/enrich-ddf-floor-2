# /gis-git-sync

**CRITICAL: This command displays guidance only. The AI must manually execute each step individually using terminal commands.**

- **Why files remain changed**: This command shows documentation - it does NOT execute git operations automatically. The AI agent must run each git command separately using `run_terminal_cmd`.
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results.
- **Safety first**: No automated scripts, no chaining, no force-push, no `--no-verify`. Each command must be reviewed individually.
- **Manual execution required**: The AI cannot create or run bash scripts for git operations.

## Required AI execution flow (AI must run these commands individually):

**AI must execute each of these commands individually using `run_terminal_cmd`:**

1. **AI executes**: Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. **AI executes**: Sync remotes (and prune deleted refs)

```bash
gtimeout 10 git fetch --all --prune
```

2.1) **AI executes**: Review current stashes (MANDATORY)

```bash
gtimeout 10 git stash list
```

**Guidance**: If stash count > 10 or old stashes exist, run `/gst-git-stash` first to triage.

2.2) **AI executes**: Create a temporary stash before risky operations (MANDATORY)

```bash
gtimeout 10 git stash push -m "WIP before git-sync"
```

2.3) **AI executes**: Inspect or restore a stash (choose one) (MANDATORY if stashes exist)

```bash
gtimeout 10 git stash show -p stash@{0}
```

```bash
gtimeout 30 git restore -p --source=stash@{0} -- .
```

2.4) **AI executes**: Drop the stash when done (MANDATORY if stash applied/empty)

```bash
gtimeout 5 git stash drop stash@{0}
```

2.5) **AI executes**: Check for untracked files before staging

```bash
gtimeout 5 git status --short
```

3. **AI executes**: Stage changes (including untracked files)

```bash
gtimeout 10 git add -A
```

**Note**: `git add -A` stages ALL changes including:

- Modified files (M)
- Deleted files (D)
- **Untracked files (??)** - This catches all new files
- Files already tracked that were modified

  3.1) **AI executes**: Verify what was staged (including untracked files)

```bash
gtimeout 5 git status --short
```

**Note**: If any files shown should NOT be committed (e.g., build artifacts, secrets), unstage them:

```bash
gtimeout 5 git reset HEAD <file>
# Then update .gitignore if needed
```

4. **AI executes**: Run hooks (if configured)

```bash
gtimeout 60 pre-commit run --all-files
```

4.1) **AI executes**: Re-stage files if hooks modified them

```bash
gtimeout 10 git add -A
```

4.2) **AI executes**: If taxonomy violations are reported, move files as instructed, then re-run hooks

```bash
# Follow hook output to move files (e.g., .cline/rules -> .clinerules, keep .dadosfera/rules)
gtimeout 10 git add -A
gtimeout 60 pre-commit run --all-files
```

5. **AI executes**: Commit (single-line, no emojis; describe what changed and why)

```bash
gtimeout 10 git commit -m "<meaningful commit message describing changes>"
```

5.1) **AI executes**: Verify current branch before pushing (CRITICAL SAFETY CHECK)

```bash
gtimeout 5 git branch --show-current
```

**Note**: Review the branch name displayed. Ensure you're pushing to the intended branch (e.g., not accidentally pushing to `main` when working on a feature branch).

6. **AI executes**: Push (set upstream on first push if needed)

```bash
gtimeout 15 git push
# If push fails with "no upstream branch", then:
gtimeout 15 git push --set-upstream origin $(git branch --show-current)
```

**AI execution notes:**

- Execute each command separately using `run_terminal_cmd`
- Stop immediately if any command fails and report the error
- **IMPORTANT**: `git add -A` in step 3 will add ALL untracked files (??). Always check `git status --short` before and after staging to see what will be committed.
- If untracked files should not be committed, unstage them with `git reset HEAD <file>` and add appropriate patterns to `.gitignore`
- Re-stage after hooks that modify files; resolve taxonomy per hook guidance (.cline -> .clinerules; .dadosfera/rules stays)
- Verify output of each command before proceeding
- **CRITICAL**: In step 5.1, verify the branch name before pushing. Report the branch name to the user and confirm it's the intended branch (especially important to avoid pushing to `main`/`master` accidentally)
- For commit message, use a meaningful description of what actually changed

---

## Troubleshooting: IDE shows pending changes, CLI looks clean

When the IDE reports changes but `git status` seems clean, do the following:

1) Get concise status with symbols
```bash
gtimeout 5 git status --short
```

2) Inspect actual diffs for specific files the IDE lists
```bash
gtimeout 5 git diff <path/to/file>
```

3) List modified tracked files explicitly
```bash
gtimeout 5 git ls-files -m
```

4) Check untracked files and whether they should be added or ignored
```bash
gtimeout 5 git status --short
gtimeout 5 git check-ignore -v <path>  # see which ignore rule matches
```

5) If hooks auto-fixed whitespace/EOLs, re-stage and re-run hooks
```bash
gtimeout 10 git add -A
gtimeout 60 pre-commit run --all-files
```

6) Common causes to consider
- Trailing newline/whitespace fixes by hooks or editor
- Files under `.tmp/` or other ignored paths (intentionally not tracked)
- IDE cache; refresh the Git view and ensure files are saved

---

**Last updated**: 2025-11-21
