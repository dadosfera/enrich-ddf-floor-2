# /gsyn_git_sync

<!-- COMMAND_ID: 019 -->
<!-- COMMAND_VERSION: 1.2.0 -->
<!-- COMMAND_TYPE: gs_git_sync -->

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

2.1) **AI executes**: Check what will be committed (no stash by default)

```bash
gtimeout 5 git status --short
```

**Guidance**: Identify exactly which files from the current conversation must be included. Do **not** stash unless you truly cannot commit right now.

3. **AI executes**: Stage only the intended files (prefer specific paths)

```bash
gtimeout 10 git add <path1> <path2>  # or git add -A if all are wanted
```

3.1) **AI executes**: Verify staged set

```bash
gtimeout 5 git status --short
```

**Note**: If something should not be committed, unstage it:

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
CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
```

```bash
# Check if branch exists locally or remotely
gtimeout 10 git show-ref --verify --quiet refs/heads/"$CURRENT_BRANCH" && echo "local" || echo "not_local"
```

```bash
gtimeout 10 git show-ref --verify --quiet refs/remotes/origin/"$CURRENT_BRANCH" && echo "remote" || echo "not_remote"
```

```bash
# Check upstream tracking branch
gtimeout 10 git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null && echo "upstream_set" || echo "no_upstream"
```

**Note**: Review the branch name displayed. Ensure you're pushing to the intended branch (e.g., not accidentally pushing to `main` when working on a feature branch).

6. **AI executes**: Push (set upstream on first push if needed)

```bash
# Attempt push with upstream detection
gtimeout 15 git push
```

```bash
# If push fails with "no upstream branch", set upstream and push
if [ $? -ne 0 ]; then
  gtimeout 15 git push --set-upstream origin "$CURRENT_BRANCH"
fi
```

7. **Optional fallback**: If you cannot commit now (rare)

- Use `/gsta_git_stash` to park changes safely without destructive commands.
- Document why a stash was used and drop/restore intentionally later.

**AI execution notes:**

- Execute each command separately using `run_terminal_cmd`
- Stop immediately if any command fails and report the error
- Prefer staging explicit paths; use `git add -A` only when every change is meant to go in.
- If untracked files should not be committed, unstage them with `git reset HEAD <file>` and add appropriate patterns to `.gitignore`
- Re-stage after hooks that modify files; resolve taxonomy per hook guidance (.cline -> .clinerules, keep .dadosfera/rules)
- Verify output of each command before proceeding
- **CRITICAL**: In step 5.1, verify the branch name before pushing. Report the branch name to the user and confirm it's the intended branch (especially important to avoid pushing to `main`/`master` accidentally)
- For commit message, use a meaningful description of what actually changed

---

## Troubleshooting: IDE shows pending changes, CLI looks clean

When the IDE reports changes but `git status` seems clean, do the following:

1. Get concise status with symbols

```bash
gtimeout 5 git status --short
```

2. Inspect actual diffs for specific files the IDE lists

```bash
gtimeout 5 git diff <path/to/file>
```

3. List modified tracked files explicitly

```bash
gtimeout 5 git ls-files -m
```

4. Check untracked files and whether they should be added or ignored

```bash
gtimeout 5 git status --short
gtimeout 5 git check-ignore -v <path>  # see which ignore rule matches
```

5. If hooks auto-fixed whitespace/EOLs, re-stage and re-run hooks

```bash
gtimeout 10 git add -A
gtimeout 60 pre-commit run --all-files
```

6. Common causes to consider

- Trailing newline/whitespace fixes by hooks or editor
- Files under `.tmp/` or other ignored paths (intentionally not tracked)
- IDE cache; refresh the Git view and ensure files are saved

---

**Last updated**: 2025-12-07

**Version History**:

- 1.2.0: Added branch detection and upstream tracking verification before push operations
- 1.1.0: Added troubleshooting section for IDE/CLI status discrepancies
- 1.0.0: Initial version
