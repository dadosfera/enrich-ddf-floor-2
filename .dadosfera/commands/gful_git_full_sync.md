---
category: git
criticality: medium
scope: all
---
# /gful_git_full_sync
<!-- COMMAND_ID: 020 -->
<!-- COMMAND_VERSION: 1.3.1 -->
<!-- COMMAND_TYPE: gf_git_full_sync -->

Full git synchronization including remote fetch, integration, and push to ensure local and remote are fully synchronized.

**Critical rule**: This command displays guidance only. The AI must manually execute each step individually using terminal commands.

**Critical rule**: The command body is self-contained. Do NOT depend on fetching the GitHub URL footer at runtime; it can return 404 for private repos or non-default branches.

**Local Reference**: `commands/gful_git_full_sync.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gful_git_full_sync.md`

Backlinks:
- recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md

## When to Use

- Before starting significant work to ensure you have the latest changes
- After being away from a project for a while
- When you want to ensure local and remote are completely in sync
- Before creating a PR to ensure clean history

## When NOT to Use

- During an active merge conflict (resolve first)
- When working on a detached HEAD
- When you intentionally want a divergent local branch

## Command sequence (run in order)

### 1. Verify working directory state

```bash
gtimeout 5 git status
gtimeout 5 git branch --show-current
```

> If the tree is dirty, do NOT skip Step 2. Use either --autostash (Step 3 alternative) or stash explicitly via /gsta_git_stash.

### 2. Stash dirty changes (only if needed)

Skip this step if `git status` reports a clean tree.

```bash
gtimeout 10 git stash push -m "WIP: before full sync $(date +%Y%m%d_%H%M%S)"
gtimeout 5 git stash list
```

### 3. Fetch latest from all remotes

```bash
gtimeout 30 git fetch --all --prune
gtimeout 10 git log HEAD..origin/$(git branch --show-current) --oneline
```

### 4. Integrate remote into current branch

Default: rebase. If the tree is dirty and you skipped Step 2, use the --autostash variant.

```bash
# Default (clean tree)
gtimeout 60 git rebase origin/$(git branch --show-current)

# Dirty-tree alternative (auto-stash + auto-pop)
# gtimeout 60 git pull --rebase --autostash origin $(git branch --show-current)

# If conflicts occur:
# resolve files, then: gtimeout 5 git add <files> && gtimeout 60 git rebase --continue
```

### 5. Push to remote

```bash
gtimeout 30 git push origin $(git branch --show-current)

# If remote diverged and force is authorized (see /gbyp_git_protection_bypass):
# gtimeout 30 git push --force-with-lease origin $(git branch --show-current)
```

### 6. Restore stash if Step 2 ran

Only run if Step 2 created a stash entry.

```bash
gtimeout 5 git stash list
# Inspect stash@{0} then:
# gtimeout 10 git stash pop
```

### 7. Verify synchronization

```bash
gtimeout 5 git status
gtimeout 10 git log origin/$(git branch --show-current)..HEAD --oneline
gtimeout 10 git log HEAD..origin/$(git branch --show-current) --oneline
```

## Handling Conflicts

If conflicts occur during rebase:

```bash
# View conflict files
gtimeout 5 git status

# Resolve conflicts in each file (edit manually)

# Mark as resolved
gtimeout 5 git add {resolved_files}

# Continue rebase
gtimeout 60 git rebase --continue
```

If the rebase is unsalvageable: `gtimeout 5 git rebase --abort` returns to the pre-rebase state.

## Alternative: Merge Instead of Rebase

For shared branches where rebase is not appropriate:

```bash
# Merge instead of rebase
gtimeout 60 git merge origin/$(git branch --show-current)

# Push merge commit
gtimeout 30 git push origin $(git branch --show-current)
```

## Private-repo / 404 note

The `**Git URL Reference**:` footer at the top of this command can return 404 in three common cases: the repository is private, the default branch is not `main`, or the network/auth is restricted. Treat the footer as traceability metadata only. The instructions above are intentionally self-contained and must execute without fetching that URL.

## Post-Sync Checklist

- [ ] Working directory is clean
- [ ] Local and remote branches are in sync
- [ ] No conflicts remain
- [ ] Stash from Step 2 (if any) was popped or intentionally retained
- [ ] All tests pass (run `/tall_tests_all` if appropriate)

## Do NOT use this command to merge stacked PRs

For PR stacks, use `/merg_merge` instead — its 'Stacked-PR awareness' section detects dependents and refuses `--delete-branch` until every child is retargeted. See `recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md`.

## Related Commands

- `/gsyn_git_sync`
- `/gsta_git_stash`
- `/gadm_git_admin_push`
- `/merg_merge`
