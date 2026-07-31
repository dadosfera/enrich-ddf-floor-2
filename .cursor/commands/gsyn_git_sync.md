---
category: git
criticality: medium
scope: all
---
# /gsyn_git_sync
<!-- COMMAND_ID: 019 -->
<!-- COMMAND_VERSION: 1.3.2 -->
<!-- COMMAND_TYPE: gs_git_sync -->
<!-- UPDATED: 2026-07-07 - Concurrent-agent safety callout: link multi_agent_worktree_workflow SSoT -->

Safe day-to-day git sync: status -> stage -> commit -> push. Lower-touch than /gful_git_full_sync (no rebase, no force-push, no autostash gymnastics).

**Concurrent-agent safety**: If another agent may be live in this repo, do your work in **your own git worktree** (one worktree per agent) before any `checkout`/`reset`/`stash`/`merge`/`clean` — in a shared checkout those operations silently destroy another agent's uncommitted work, at any change size. SSoT: `guides/collaboration/multi_agent_worktree_workflow.md`.

**Critical rule**: This command displays guidance only. The AI must manually execute each step individually using terminal commands.

**Critical rule**: The command body is self-contained. Do NOT depend on fetching the GitHub URL footer at runtime; it can return 404 for private repos or non-default branches.

**Local Reference**: `commands/gsyn_git_sync.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gsyn_git_sync.md`

## When to Use

- Routine end-of-task push after small, well-scoped local changes
- When you trust the local commit message conventions and just want to publish work
- When the remote is known not to have diverged (no incoming changes)

## When NOT to Use

- When the remote may have diverged - use /gful_git_full_sync instead so you fetch + integrate first
- When you need to triage a dirty stash - use /gsta_git_stash
- When pushing to a protected branch - use /gadm_git_admin_push

## Command sequence (run in order)

### 1. Inspect working directory

```bash
gtimeout 5 git status
gtimeout 5 git branch --show-current
```

> `git status` reports two different dimensions at once:
> - Commit parity: messages like `Your branch is up to date with 'origin/main'` mean local and remote commits match (nothing to pull/push).
> - Working tree state: `modified:` / `untracked:` lines mean you still have local WIP not committed yet.
>
> Both can be true at the same time. "Up to date" does **not** imply "clean tree".

### 2. Review pending changes

```bash
gtimeout 10 git diff --stat
gtimeout 30 git diff
```

> Read the diff before staging. If the diff is unexpectedly large, stop and triage with /gsta_git_stash.

### 3. Stage changes

Prefer explicit paths over `git add .` when other unrelated changes may be in the tree.

```bash
# Targeted (preferred)
gtimeout 5 git add path/to/file_a path/to/file_b

# Wholesale (only if the diff in Step 2 is fully intended)
# gtimeout 5 git add -A
```

### 4. Commit

```bash
gtimeout 10 git commit -m "<type>(<scope>): <imperative summary>" -m "<optional body explaining why>"
```

### 5. Push

```bash
gtimeout 30 git push origin $(git branch --show-current)
```

If this push is blocked by hooks and you are considering bypassing with `--no-verify`, first run `/fixh_fix_precommit_errors` and try to resolve the root cause. Only then, and only if another session is not actively mutating this repo/worktree, request explicit user authorization for a one-off bypass.

> If push prints `Everything up-to-date`, it only means there were no local commits to send. It does **not** mean your working tree is clean.

> If push is rejected as non-fast-forward, STOP here and switch to /gful_git_full_sync to integrate remote changes before retrying.

### 6. Verify

```bash
gtimeout 5 git status
gtimeout 5 git log -1 --oneline
```

Interpret Step 6 explicitly:
- If status says `up to date with origin/<branch>`, commit history is synchronized.
- If status still shows `modified:` / `untracked:`, you have uncommitted local changes.

## Dirty-tree handling

If `git status` in Step 1 shows changes you do NOT want to commit right now, do one of the following before continuing:

```bash
# Stash for later
gtimeout 10 git stash push -m "WIP: keep aside for sync $(date +%Y%m%d_%H%M%S)"

# Or use /gsta_git_stash for full per-hunk triage
```

Do not commit unrelated changes just to clear the tree.

## Push rejection -> escalate

`gsyn` is intentionally a one-way push. If the push in Step 5 is rejected because the remote has new commits, do NOT add `--force` here. Instead:

1. Run `/gful_git_full_sync` to fetch + rebase first.
2. Re-run `/gsyn_git_sync` from Step 5 only after `/gful` succeeds.

## Push rejected because branch is protected (GH006)

If Step 5 fails with `GH006: Protected branch update failed` (or your hook prints `BLOCKED: Push to main/master requires GIT_AUTHORIZE_MAIN_PUSH=true`), the remote forbids direct push to that branch. Do **not** retry the push, and do **not** rename `main` to “move the work somewhere else.”

Anti-pattern (do **not** do this):

```bash
# ❌ WRONG: This deletes your local main pointer and reattaches your work
#    to a new branch. You then lose `main` until you recreate it from origin/main.
git branch -m main chore/<your-work>
```

Recovery if you already did the rename above:

```bash
git branch main origin/main
git checkout main
git fetch origin
```

Correct flow when push to `main` is blocked:

```bash
# 1) Move HEAD onto a new feature branch (your commits stay reachable)
git switch -c chore/<short-description>

# 2) Push the feature branch
git push -u origin chore/<short-description>

# 3) Open a PR via gh
gh pr create --base main --head chore/<short-description> \
  --title "<imperative summary>" \
  --body  "$(cat <<'EOF'
## Summary
- <bullet 1>
- <bullet 2>

## Test plan
- [ ] <how to verify>
EOF
)"
```

If you must merge as a sole admin and review is blocking, escalate to `/gbyp_git_protection_bypass` (its phases 4–7 add a temporary bypass, perform the admin merge, and leave changes in place unless `REVERT_PROTECTION=1` is set to run phase 7).

## Private-repo / 404 note

The `**Git URL Reference**:` footer can return 404 in private repos or non-default branches. Treat it as traceability metadata only; the instructions above are self-contained.

## Related Commands

- `/gful_git_full_sync`
- `/gsta_git_stash`
- `/gadm_git_admin_push`
- `/lint_lint`
