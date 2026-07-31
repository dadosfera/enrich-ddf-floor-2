---
category: git
criticality: medium
scope: all
---
# /gsta_git_stash
<!-- COMMAND_ID: 021 -->
<!-- COMMAND_VERSION: 1.7.1 -->
<!-- COMMAND_TYPE: gs_git_stash -->

Safe stash workflow: inspect tree, save with descriptive message, list, inspect by hunk, optionally cherry-pick, then pop or drop with overwrite protection.

**Critical rule**: **Default: branch, not stash.** Use stash ONLY when ALL are true: (1) context switch < 30 minutes, (2) pop planned in same session, (3) patch backup saved to `.tmp/stash_backups/`. Otherwise: `git checkout -b wip/<topic>-YYYYMMDD` and commit. Never `git stash -u` for overnight parking.

**Critical rule**: This command displays guidance only. The AI must manually execute each step individually using terminal commands.

**Critical rule**: NEVER `git stash drop` without first running `git stash show -p stash@{N}` and saving the patch. Stash drops are unrecoverable except via `git fsck`.

**Critical rule**: NEVER `git stash pop` onto a tree with conflicting modifications - prefer `git stash apply` so the stash entry survives the conflict resolution.

**Local Reference**: `commands/gsta_git_stash.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gsta_git_stash.md`

## When to Use

- You need to switch branches with uncommitted changes
- You want to keep WIP aside before /gful_git_full_sync or /gsyn_git_sync
- You need to triage a long-lived stash list and recover useful pieces
- You need to cherry-pick part of a stash into a different branch

## When NOT to Use

- If the work is mature enough to commit - just commit it on a branch
- For changes spanning many files where a feature branch is more appropriate
- When you cannot afford even temporary loss - commit to a scratch branch instead

## Command sequence (run in order)

### 1. Inspect current state

```bash
gtimeout 5 git status
gtimeout 10 git diff --stat
gtimeout 5 git stash list
```

### 2. Stash with a descriptive message

Always include a message. Untracked files require -u; ignored files require -a (rare).

```bash
# Tracked files only (default)
gtimeout 10 git stash push -m "WIP: <topic> $(date +%Y%m%d_%H%M%S)"

# Include untracked files
# gtimeout 10 git stash push -u -m "WIP: <topic>"

# Stash a subset only
# gtimeout 10 git stash push -m "WIP: <topic>" -- path/to/file path/to/dir/
```

### 3. List and identify

```bash
gtimeout 5 git stash list
gtimeout 5 git stash show stash@{0} --stat
```

### 4. Inspect by hunk before applying

Read every hunk you intend to apply. Save a patch copy as backup.

```bash
gtimeout 30 git stash show -p stash@{0}

# Save backup patch (overwrite-safe)
mkdir -p .tmp/stash_backups
gtimeout 30 git stash show -p stash@{0} > ".tmp/stash_backups/stash_$(date +%Y%m%d_%H%M%S).patch"
```

### 5. Apply (preferred over pop)

`apply` keeps the stash entry; `pop` removes it on success. Use `apply` while you are still verifying.

```bash
gtimeout 30 git stash apply stash@{0}

# Only after you confirm the working tree is correct:
# gtimeout 5 git stash drop stash@{0}
```

### 6. Cherry-pick a stash to another branch

Useful when the stash belongs on a different branch than where it was created.

```bash
gtimeout 5 git checkout <target-branch>
gtimeout 30 git stash apply stash@{0}
# resolve any conflicts, then commit normally
```

### 7. Pop only when fully verified

Pop = apply + drop. Skip if Step 5 surfaced any conflict.

```bash
gtimeout 5 git stash pop stash@{0}
```

## Default: branch, not stash

Use stash **ONLY** when ALL are true:

- Context switch **< 30 minutes**
- Pop is planned **in the same session**
- Patch backup saved to `.tmp/stash_backups/`

**Otherwise** (preferred for multi-file / overnight WIP):

```bash
git checkout -b wip/<topic>-$(date +%Y%m%d)
git add <scope>
git commit -m "wip(<topic>): <short description>"
# Optional: git push -u origin HEAD
```

For large untracked bundles before merge, prefer `/merg_merge` backup branch (Step 4) over `git stash push -u`.

## Stash audit log (merg / gscv sessions)

When creating or restoring stashes during merge or conversation sync, append to `logs/git_sync_operations.log`:

```text
<UTC-ISO> STASH_CREATED ref=stash@{N} reason=<merg_merge|gscv> step=<N> actor=<email>
<UTC-ISO> STASH_RESTORED ref=stash@{N} method=apply|pop
<UTC-ISO> STASH_KEPT ref=stash@{N} reason=<user-approved>
```

## Overwrite-protection rules

Before any `pop` or `drop`:

1. Confirm Step 4 saved a `.patch` backup.
2. Confirm `git status` shows a tree compatible with the stash (no overlapping modified files).
3. Prefer `git stash apply` over `git stash pop` until the result is verified.
4. NEVER chain `pop` immediately after `push` — list and inspect first.

## Recovery from accidental drop

If a stash was dropped without a backup patch:

```bash
# Find dangling commits (stashes are commits)
gtimeout 30 git fsck --no-reflog | awk '/dangling commit/ {print $3}'

# Inspect each candidate
# gtimeout 10 git show <sha>

# Recreate the stash entry
# gtimeout 5 git stash apply <sha>
```

This only works while git's garbage collector has not yet pruned the dangling commit (default ~14 days).

## Don'ts

- Don't `git stash` without a `-m "..."` message — old stashes become indistinguishable.
- Don't accumulate >5 stash entries — triage them.
- Don't `git stash pop` onto a dirty tree without inspecting hunks first.
- Don't use stash as long-term storage — promote to a branch.

## Private-repo / 404 note

The `**Git URL Reference**:` footer can return 404 in private repos or non-default branches. Treat it as traceability metadata only; the instructions above are self-contained.

## Related Commands

- `/gsyn_git_sync`
- `/gful_git_full_sync`
- `/merg_merge`
