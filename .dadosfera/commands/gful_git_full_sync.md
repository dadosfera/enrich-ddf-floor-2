# /gful_git_full_sync

<!-- COMMAND_ID: 020 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: gf_git_full_sync -->

**CRITICAL: This command displays guidance only. The AI must manually execute each step individually using terminal commands.**

- **Why files remain changed**: This command shows documentation - it does NOT execute git operations automatically. The AI agent must run each git command separately using `run_terminal_cmd`.
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results.
- **Safety first**: No automated scripts, no chaining, no force-push, no `--no-verify`. Each command must be reviewed individually.
- **Manual execution required**: The AI cannot create or run bash scripts for git operations.

## Required AI execution flow (AI must run these commands individually):

**AI must execute each of these commands individually using `run_terminal_cmd`:**

### Phase 1: Sync Submodules

1. **AI executes**: Identify submodules (recursive)

```bash
gtimeout 10 git submodule status --recursive
```

2. **AI executes**: For **EACH** submodule listed above, starting with the **innermost (deepest nested)** submodules first:

   2.1) **AI executes**: Enter submodule directory

   ```bash
   cd <submodule_path>
   ```

   2.2) **AI executes**: Check status and branch

   ```bash
   gtimeout 5 git status --short
   SUBMODULE_BRANCH=$(gtimeout 5 git branch --show-current)
   echo "Submodule branch: $SUBMODULE_BRANCH"
   ```

   2.2a) **AI executes**: Discover available branches in submodule (local and remote)

   ```bash
   gtimeout 10 git fetch --all --prune
   ```

   ```bash
   gtimeout 10 git branch -a | head -20
   ```

   ```bash
   # Check if current branch exists locally or remotely
   if [ -n "$SUBMODULE_BRANCH" ] && [ "$SUBMODULE_BRANCH" != "HEAD" ]; then
     gtimeout 10 git show-ref --verify --quiet refs/heads/"$SUBMODULE_BRANCH" && echo "local" || echo "not_local"
     gtimeout 10 git show-ref --verify --quiet refs/remotes/origin/"$SUBMODULE_BRANCH" && echo "remote" || echo "not_remote"
   else
     echo "detached_head"
   fi
   ```

   **Note**: If detached HEAD, checkout a branch before committing if you intend to push updates. Use branch discovery to identify available branches.

   2.3) **AI executes**: Stage changes (if any)

   ```bash
   gtimeout 10 git add -A
   ```

   2.4) **AI executes**: Commit changes (if any staged)

   ```bash
   gtimeout 10 git commit -m "chore: sync submodule changes"
   ```

   2.5) **AI executes**: Push changes (if committed)

   ```bash
   # Check upstream tracking before push
   gtimeout 10 git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null && echo "upstream_set" || echo "no_upstream"
   ```

   ```bash
   # Push with upstream detection
   gtimeout 15 git push
   ```

   ```bash
   # If push fails with "no upstream branch", set upstream and push
   if [ $? -ne 0 ] && [ -n "$SUBMODULE_BRANCH" ] && [ "$SUBMODULE_BRANCH" != "HEAD" ]; then
     gtimeout 15 git push --set-upstream origin "$SUBMODULE_BRANCH"
   fi
   ```

   2.6) **AI executes**: Return to root

   ```bash
   cd .. # Or cd /absolute/path/to/root if nested
   ```

### Phase 2: Sync Main Repository

3. **AI executes**: Verify repository context (root)

```bash
gtimeout 5 git rev-parse --show-toplevel
```

4. **AI executes**: Sync remotes (and prune deleted refs)

```bash
gtimeout 10 git fetch --all --prune
```

5. **AI executes**: Stage changes (including submodule pointer updates)

```bash
gtimeout 10 git add -A
```

6. **AI executes**: Verify what was staged

```bash
gtimeout 5 git status --short
```

7. **AI executes**: Run hooks

```bash
gtimeout 60 pre-commit run --all-files
```

8. **AI executes**: Commit (referencing submodule updates if applicable)

```bash
gtimeout 10 git commit -m "chore: sync repo and submodules"
```

9. **AI executes**: Verify current branch before pushing (CRITICAL SAFETY CHECK)

```bash
MAIN_BRANCH=$(gtimeout 5 git branch --show-current)
echo "Main repository branch: $MAIN_BRANCH"
```

```bash
# Check if branch exists locally or remotely
gtimeout 10 git show-ref --verify --quiet refs/heads/"$MAIN_BRANCH" && echo "local" || echo "not_local"
```

```bash
gtimeout 10 git show-ref --verify --quiet refs/remotes/origin/"$MAIN_BRANCH" && echo "remote" || echo "not_remote"
```

```bash
# Check upstream tracking branch
gtimeout 10 git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null && echo "upstream_set" || echo "no_upstream"
```

**Note**: Review the branch name displayed. Ensure you're pushing to the intended branch.

10. **AI executes**: Push (set upstream on first push if needed)

```bash
# Attempt push with upstream detection
gtimeout 15 git push
```

```bash
# If push fails with "no upstream branch", set upstream and push
if [ $? -ne 0 ]; then
  gtimeout 15 git push --set-upstream origin "$MAIN_BRANCH"
fi
```

**AI execution notes:**

- Execute each command separately using `run_terminal_cmd`
- Stop immediately if any command fails and report the error
- Ensure you return to the root directory after handling each submodule
- Verify branch names before pushing in submodules and main repo
- Use branch discovery to identify available branches in submodules before operations

**Version History**:

- 1.1.0: Added branch discovery and upstream tracking verification for submodules and main repository
- 1.0.0: Initial version
