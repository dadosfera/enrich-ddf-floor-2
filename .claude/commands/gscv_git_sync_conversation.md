---
category: git
criticality: medium
scope: all
---
# /gscv_git_sync_conversation
<!-- COMMAND_ID: 093 -->
<!-- COMMAND_VERSION: 1.1.1 -->
<!-- COMMAND_TYPE: gs_git_sync_conversation -->

Sync **only the files that were created or modified within the current conversation**, leaving every other dirty file in the working tree untouched. Unlike `/gsyn_git_sync` (which syncs ALL changes), this command is conversation-scoped: the resulting commit reflects exactly the work done in this session and nothing else.

**Critical rule**: Files outside the conversation scope MUST NOT be staged or committed. If they are dirty, they are stashed before the commit and restored after; under no circumstance should they leak into the conversation's commit.

**Critical rule**: The agent MUST NOT report success while files in the conversation scope are still uncommitted/unpushed. Files outside the scope are allowed to remain dirty (or stashed) at the end - that is the intended behavior of this command.

**Critical rule**: This command displays guidance only. The AI must execute each step individually using terminal commands.

**Critical rule**: The command body is self-contained. Do NOT depend on fetching the GitHub URL footer at runtime; it can return 404 for private repos or non-default branches.

**Local Reference**: `commands/gscv_git_sync_conversation.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gscv_git_sync_conversation.md`

Backlinks:
- commands/gsyn_git_sync.md
- commands/gful_git_full_sync.md
- commands/gsta_git_stash.md

## When to Use

- The working tree mixes work from this conversation with unrelated WIP from other tasks, and you want to publish only this conversation's work.
- You explicitly want a commit whose diff matches the conversation's intent (no incidental files).
- You're handing off the conversation and want a focused, traceable commit/PR scope.

## When NOT to Use

- You want to publish EVERYTHING that's dirty -> use `/gsyn_git_sync`.
- The repo has submodules that also need syncing -> use `/gful_git_full_sync` (after deciding what scope makes sense).
- Pushing to a protected branch and bypass is required -> use `/gadm_git_admin_push`.

## Command sequence (run in order)

### 1. Inspect working directory and capture full status

```bash
gtimeout 5 git status
gtimeout 5 git status --porcelain
gtimeout 5 git branch --show-current
```

> Capture the full porcelain output - this is the baseline used to decide which files are in-scope vs out-of-scope, and to verify nothing out-of-scope is accidentally committed.

### 2. Build the conversation-scope file list

The agent (not the user) writes out the explicit list of paths in scope. Show this list to the user inline (in chat) before continuing, so they can correct it if any path is wrong.

```bash
# Example - replace with actual scope from this conversation:
SCOPE_FILES=(
  "path/to/file_a"
  "path/to/file_b"
  "path/to/dir/file_c"
)
printf '%s\n' "${SCOPE_FILES[@]}"
```

### 3. Identify out-of-scope dirty files

```bash
gtimeout 5 git status --porcelain | awk '{print $2}' > /tmp/_gscv_dirty_paths.txt
printf '%s\n' "${SCOPE_FILES[@]}" | sort -u > /tmp/_gscv_scope_paths.txt
sort -u /tmp/_gscv_dirty_paths.txt > /tmp/_gscv_dirty_sorted.txt
comm -23 /tmp/_gscv_dirty_sorted.txt /tmp/_gscv_scope_paths.txt > /tmp/_gscv_out_of_scope.txt
cat /tmp/_gscv_out_of_scope.txt
```

> The contents of `/tmp/_gscv_out_of_scope.txt` are the files that must NOT enter this commit.

### 4. Stash out-of-scope dirty files (only if any exist)

If `/tmp/_gscv_out_of_scope.txt` is non-empty, stash those paths so the working tree contains only the conversation scope before staging.

```bash
if [ -s /tmp/_gscv_out_of_scope.txt ]; then
  # `git stash push -- <paths>` stashes only the listed paths.
  # Use xargs to expand the file list safely.
  xargs -a /tmp/_gscv_out_of_scope.txt -d '\n' \
    gtimeout 15 git stash push -m "gscv: park out-of-scope WIP $(date +%Y%m%d_%H%M%S) --"
  gtimeout 5 git stash list
fi
```

> After this step, `git status` should show only the conversation-scope paths as modified/untracked.
> `git stash push -- <paths>` does NOT stash untracked files unless `-u` is added. If any out-of-scope path is untracked, re-run with `-u` (see Failure modes section).

### 5. Verify only scope files remain dirty

```bash
gtimeout 5 git status --porcelain
```

> Every line of output should correspond to an entry in `${SCOPE_FILES[@]}`. If anything else still appears dirty (e.g., a path that was untracked but not stashed), STOP and reconcile manually before continuing - do NOT proceed to staging.

### 6. Stage only the scope files

```bash
gtimeout 5 git add -- "${SCOPE_FILES[@]}"
gtimeout 5 git status --short
```

> The staged set must be exactly the scope set. If `git add` reports `pathspec did not match any files` for a scope path, that path either was deleted intentionally (use `git add -A -- <path>` to stage the deletion) or was never created - reconcile before continuing.

### 7. Commit

```bash
gtimeout 10 git commit -m "<type>(<scope>): <imperative summary of conversation work>" \
                       -m "<body summarizing decisions made in this conversation>"
```

> If the commit fails because the index is empty, the conversation produced no committable file changes. Skip to Step 10 (restore stash) and report that to the user.

### 8. Push

```bash
gtimeout 30 git push origin $(git branch --show-current)
```

> If push prints `Everything up-to-date`, it only means there were no NEW commits to send. It does NOT confirm scope cleanliness - keep going.
> If push is rejected non-fast-forward, STOP. Do NOT `--force`. Switch to `/gful_git_full_sync` (or fetch+rebase manually), then re-run from Step 8.

### 9. Verify scope sync end-state (MANDATORY)

```bash
gtimeout 5 git status
gtimeout 5 git log -1 --oneline
gtimeout 5 git diff --name-only HEAD~1 HEAD
```

> The command is **only successful** when ALL of the following are true:
> - The new commit exists locally and on the remote (commit parity for the branch tip).
> - `git diff --name-only HEAD~1 HEAD` matches `${SCOPE_FILES[@]}` exactly (no extra files, no missing files).
> - No scope file is still listed as modified/untracked in `git status`.
>
> It is EXPECTED that `git status` may still show out-of-scope dirty files (they will be restored from stash in Step 10). That is not a failure for this command.

### 10. Restore stashed out-of-scope changes (only if Step 4 stashed)

```bash
if gtimeout 5 git stash list | grep -q 'gscv: park out-of-scope WIP'; then
  gtimeout 10 git stash pop
  gtimeout 5 git status
fi
```

> If `git stash pop` reports conflicts (because the conversation-scoped commit touched the same lines), STOP and surface the conflict to the user; resolve interactively rather than auto-resolving. The stash entry remains in `git stash list` so nothing is lost.

### 11. Final report or WIP handoff (MANDATORY)

If commit+push succeeded: report scope, remaining dirty files, outstanding stashes.

If user did **not** authorize commit: emit a **WIP handoff** using `templates/wip_handoff.md` (fill paths, branch, suggested git commands). Log explicit user waiver if they said "keep uncommitted".

```bash
# Success path — report in chat:
# - Committed paths + hash: $(git log -1 --oneline)
# - Remaining dirty (post-pop)
# - Outstanding stash entries

# No-commit path — paste filled template from templates/wip_handoff.md
# Include: FILES_CREATED, branch suggestion (wip/<topic>-YYYYMMDD), git add/commit commands
```

> The agent MUST NOT end the session silently with uncommitted conversation-scope files.
> Tests passing alone is NOT sufficient — either commit hash or documented waiver in handoff.

## Determining "conversation scope"

The agent MUST construct an explicit list of files that belong to this conversation BEFORE staging anything. Acceptable sources, in priority order:

1. **Tool-call history**: every file the agent wrote/edited via Write/StrReplace/EditNotebook/Delete/Move during this conversation.
2. **Files explicitly named by the user** in this conversation (treat as in-scope).
3. **Files generated by commands the agent ran** that the user explicitly asked for (e.g., distribution outputs from a sync script the user requested).

Anything that does not appear in any of (1), (2), (3) is OUT of scope, even if it is currently dirty.

If the agent cannot confidently enumerate the scope, STOP and ask the user to confirm the file list before continuing. Do not guess.

## Failure modes and recovery

| Symptom | Cause | Recovery |
| --- | --- | --- |
| `git stash push -- <paths>` fails on untracked files | `git stash push` does not stash untracked files unless `-u` is added | Re-run with `git stash push -u -- <paths>`; or `git add` the untracked file first if it is in scope |
| Step 6 `git add` matches more than the scope (e.g., directory expansion) | A scope entry was a directory containing out-of-scope files | List individual files, not directories, in `SCOPE_FILES` |
| Step 9 `git diff --name-only HEAD~1 HEAD` includes unexpected files | Out-of-scope files leaked through Step 4 (e.g., not stashed because untracked) | `git reset --soft HEAD~1`, return to Step 3, redo with `-u` for untracked |
| Step 10 `git stash pop` has merge conflict | Conversation-scoped commit overlaps with stashed out-of-scope edits | Resolve conflict interactively; stash entry stays until you `git stash drop` it |

## Private-repo / 404 note

The `**Git URL Reference**:` footer can return 404 in private repos or non-default branches. Treat it as traceability metadata only; the instructions above are self-contained.

## Related Commands

- `/gsyn_git_sync` - Sync ALL local changes; ends with a fully clean tree.
- `/gful_git_full_sync` - Recursive sync across submodules; ends with a fully clean tree everywhere.
- `/gsta_git_stash` - Full per-hunk stash triage workflow.
- `/gadm_git_admin_push` - Authorized direct push to protected branches.
- `/lint_lint` - Run before this command to keep the conversation-scoped commit clean.
