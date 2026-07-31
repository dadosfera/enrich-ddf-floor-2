---
category: git
criticality: high
scope: all
---
# /gswp_git_sweep
<!-- COMMAND_ID: 095 -->
<!-- COMMAND_VERSION: 1.5.0 -->
<!-- COMMAND_TYPE: gs_git_sweep -->
<!-- CANONICAL_SOURCE: markdown-only (no commands/json/core peer). See commands/markdown_only_commands.yaml -->
<!-- UPDATED: 2026-07-15 - Add mandatory sweep ledger/state machine, admin-merge local-error reconciliation, post-merge remote branch cleanup guard, baseline-debt classification, and ignored-artifact vs git-clean distinction from live cleanup learnings. -->
<!-- UPDATED: 2026-07-10 - Add stale-authorization detection so the sweep re-checks PR/branch/worktree/stash targets before deletion/merge and emits explicit "already resolved" messages instead of reusing a consumed authorization. -->
<!-- UPDATED: 2026-07-10 - Clarify final pre-merge stash triage: if stash was created by this sweep/merg flow, analyze it and either recover unique content or drop it when superseded, without stopping for a redundant second authorization prompt. -->
<!-- UPDATED: 2026-07-09 - Phase 2.5 now flushes and removes the pending-to-merge worktree after merge so the final clean state has no transient worktrees. -->
<!-- UPDATED: 2026-07-07 - Live-sweep learnings: concurrent-session detection, shared-stash-stack safety (SHA tracking, sequential stash@{0} extraction, stray-autostash guard), squash-merge branch-delete fix, release/{stage} lifecycle-branch guard (Phase 3/4), dirty-default-branch handoff (Phase 0c), shared index-file conflict handling, byproduct-PR authorization -->

Full-repository git hygiene sweep. Orchestrates `/chkp_check_pending`, `/gsta_git_stash`, `/gsyn_git_sync`, `/gful_git_full_sync`, `/merg_merge`, `/gbyp_git_protection_bypass`, `/gadm_git_admin_push`, and the `using-git-worktrees` skill to drive a repo to a **clean-slate** state: default branch synced with origin, no pending local or remote branches, no open PRs, no stash entries (any content worth keeping has already landed in a PR/commit), and no leftover worktrees.

**Critical rule**: This command never deletes or closes anything itself without going through the delegated command that owns that resource — stash → `/gsta_git_stash`, branch merge/delete → `/merg_merge`, protected-branch bypass → `/gbyp_git_protection_bypass`, admin push → `/gadm_git_admin_push`. It is a checklist and router, not a replacement for their safety gates.

**Critical rule**: Every deletion (branch, stash, worktree) or PR close requires the same explicit per-item user authorization the delegated command already requires. Never batch-delete with wildcards; list first, act one at a time.

**Critical rule**: Before executing any previously authorized destructive step, re-check that the target still exists and is still unresolved. If the fresh read-only check shows the PR/branch/worktree/stash was already merged, closed, deleted, removed, or dropped, treat the old authorization as **stale/consumed** and stop that action with an explicit message such as `Authorization stale: PR #108 is already merged; nothing remains to merge.` or `Authorization stale: worktree <path> is already gone; nothing remains to remove.` Do not spend the old authorization on a different target.

**Critical rule**: "No stashes without analysis" means each stash must be either (a) confirmed already fully represented in a merged/open PR and safe to drop, or (b) promoted to a branch + PR (Phase 2) before it is dropped — never dropped solely because it is old.

**Critical rule**: If the only stash left near the end of the sweep is a safety stash created by this same sweep or by `/merg_merge` inside this same cleanup flow (for example `Pre-merge safety backup`), do not stop merely because "a stash exists". Finish the triage: inspect the patch, decide whether any unique content still needs recovery, and then either recover it or drop it. A user authorization to execute the sweep/merge cleanup already covers that final per-stash decision, as long as the specific stash was inspected and a backup patch was saved first.

**Critical rule**: "Everything is saved in git" is not automatically true. Untracked files and `.gitignore`d files (heavy local-only images/media/model weights, `.env`/credentials) are never captured by a commit, a branch, or a plain `git stash push`, and are **permanently and unrecoverably deleted** the moment their containing worktree/checkout is removed. Phase 0b is mandatory before any worktree removal or branch deletion; do not skip it because "the branch/worktree looks clean" — verify with `git status --ignored`.

**Critical rule**: **Concurrent-agent safety** — if Phase 0a's concurrent-session check (below) shows another agent is actively committing into the SAME working directory this sweep is running in, stop touching that working tree's branch immediately and for the rest of the sweep; route every remaining operation (other branches, PRs, merges) through an isolated `git worktree add` checkout instead — it shares the same `.git` object database but has an independent working tree. SSoT: `guides/collaboration/multi_agent_worktree_workflow.md`.

**Critical rule**: Any worktree this sweep creates (for the isolation above, or for Phase 1 review) must be a true filesystem sibling of the main checkout (e.g. `../docs-fera-wt-<name>`), never a path under a scratch/tmp directory — some repos' hooks assume sibling-repo relative paths (e.g. a companion `../scripts-fera` checkout) and fail with misleading errors otherwise. See `.cursor/skills/using-git-worktrees/SKILL.md`.

**Critical rule**: Never gate success/failure on a piped command's exit code inside an `if` (e.g. `if git commit -m "..." | tail -20; then`) — the `if` sees the exit code of the last command in the pipe, not `git commit`'s, so a blocked commit silently reports as success. Capture output and exit code separately: `OUT=$(git commit -m "..." 2>&1); RC=$?`.

**Critical rule**: Maintain a sweep ledger from Phase 0a through Phase 7. Every PR, branch, remote branch, stash, worktree, and unresolved local artifact must have an owner phase, a live-state recheck, a disposition, and final evidence. Do not rely on memory or conversation context after `origin/main` changes, a PR is created by the sweep, or a bypass merge returns mixed local/GitHub results.

**Critical rule**: `pre-commit run --all-files` is a repository-wide audit, not the default merge gate for a sweep. Prefer impacted tests, command-specific structure tests, generator checks, and the normal commit hooks for the branch under review. If an all-files audit is explicitly run and fixers modify files outside the branch scope, classify the failures as baseline debt, restore unrelated fixer changes, and do not pollute the PR merely to satisfy unrelated repository-wide drift.

**Critical rule**: A clean git tree is not the same as an empty filesystem. Ignored reproducible artifacts such as `node_modules/`, `.tmp/`, `__pycache__/`, and local logs may remain after a successful sweep if they are classified as disposable/reproducible and not slated for deletion. Empty untracked directories may be removed after inspection; secret-shaped, heavy, or content-bearing untracked/ignored paths remain blockers until classified.

**Local Reference**: `commands/gswp_git_sweep.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gswp_git_sweep.md`

Backlinks:
- commands/chkp_check_pending.md
- commands/gsta_git_stash.md
- commands/gsyn_git_sync.md
- commands/gful_git_full_sync.md
- commands/merg_merge.md
- commands/gbyp_git_protection_bypass.md
- commands/gadm_git_admin_push.md
- .cursor/skills/using-git-worktrees/SKILL.md
- guides/collaboration/pending_to_merge_worktree.md
- rules/dadosfera/4_24_destructive_command_authorization.md
- standards/deployment/deployment_standard.md

## When to Use

- Periodic repo hygiene: before a release cut, after a sprint, or when `git branch -a` / `gh pr list` / `git stash list` / `git worktree list` show accumulated clutter
- You want a single "are we clean?" pass instead of running each git command separately
- Preparing a repo for handoff or archival where a clean git state is a prerequisite

## When NOT to Use

- Merging one specific branch — use `/merg_merge` directly
- Triaging one stash — use `/gsta_git_stash` directly
- Routine day-to-day commit+push — use `/gsyn_git_sync`
- If you are not prepared to review each pending branch/PR/stash individually — this command has no "delete everything" shortcut, and there is no safe way to skip that review

## Authorization Requirements

Same authorization model as the commands it delegates to, plus the repo's runtime git guard:

1. Read-only phases (Phase 0a/0b discovery) run without confirmation.
2. Every destructive action (branch delete, stash drop, PR close, worktree remove) requires explicit per-item user confirmation.
   Exception: when a stash was created by this same authorized sweep/merge cleanup flow as a temporary safety artifact, the sweep may complete its final inspect-and-drop decision without stopping for a second redundant prompt, provided the stash was inspected, backed up to `.tmp/stash_backups/`, and explicitly classified as either superseded or still-needed.
3. Deleting or pushing to protected branches inherits `/gbyp_git_protection_bypass` / `/gadm_git_admin_push` authorization requirements — this command does not weaken them.
4. `git branch -d/-D/--delete` is additionally gated at the shell level by `GIT_AUTHORIZE_BRANCH_DELETE=true` (see `rules/dadosfera/4_24_destructive_command_authorization.md`) — do not set this variable autonomously; the user must export it.
5. **`git worktree remove --force`, `git push origin --delete <branch>`, and `git stash drop` are NOT covered by the runtime guard.** There is no automated backstop for these three — Phase 0b's per-file disposition record is the only safety net, so it cannot be skipped.
6. **A PR this sweep opens itself (stash-promotion, docs-recovery, code-review nits-followup) requires its own separate merge authorization** — a prior "merge PR #x and #y" from the user does not automatically extend to a PR the sweep creates afterward, even while executing that same authorization. See Phase 5.
7. When a previously authorized target no longer exists by the time the sweep reaches it, report that explicitly as a stale authorization and continue with the remaining unresolved targets only.

## Definition of "clean slate" (exit criteria)

All of the following must hold when this command completes successfully:

| Check | Command | Expected result |
|---|---|---|
| Default branch synced | `git status` on default branch | "up to date with origin", no ahead/behind |
| No local branches beside default | `git branch` | only `* <default>` |
| No stale/unmerged remote branches | `git branch -r` (after `git fetch --prune`) | only `origin/HEAD`, `origin/<default>` |
| No open PRs | `gh pr list --state open` | empty |
| No stashes | `git stash list` | empty |
| No extra worktrees | `git worktree list` | only the main working copy |
| No unresolved data-loss flags | Phase 0b disposition table | every secret-shaped/heavy/untracked file has a recorded disposition |
| Pending-to-merge worktree cleaned | Phase 2.5 | plan file empty/template, no open PR dependency, and staging worktree removed |

## Sweep ledger and state machine

Create or update `.tmp/git_sweep_ledger.json` during the sweep. The file is a
local audit artifact unless the user explicitly asks to commit a sweep report.
It must be safe to delete after the final report, but while the sweep runs it is
the source of truth for what was inspected and why an item was merged, kept, or
removed.

Minimum schema:

```json
{
  "repo": "owner/name",
  "default_branch": "main",
  "started_at": "ISO-8601",
  "operator": "github-login-or-local-user",
  "items": [
    {
      "kind": "pr|local_branch|remote_branch|stash|worktree|ignored_artifact",
      "id": "PR #123 or branch/path/ref",
      "initial_state": "open|merged|clean|dirty|unmerged|ignored",
      "phase_owner": "0a|0b|1|2|2.5|3|4|5|6|7",
      "risk": "none|data_loss|review_required|baseline_debt",
      "disposition": "merge|keep|drop|remove|classify_only|already_resolved",
      "authorization": "not_required|explicit|stale|new_pr_requires_new_auth",
      "fresh_recheck": "command/output summary",
      "final_evidence": "command/output summary"
    }
  ],
  "baseline_debt": [
    {
      "gate": "pre-commit --all-files",
      "reason": "existing repo-wide failure outside sweep branch",
      "evidence": "short failing hook summary"
    }
  ],
  "exit_criteria": {
    "default_branch_synced": false,
    "no_extra_local_branches": false,
    "no_extra_remote_branches": false,
    "no_open_prs": false,
    "no_stashes": false,
    "single_worktree": false
  }
}
```

State transitions:

| State | Meaning | Allowed next states |
|---|---|---|
| `observed` | Item exists in Phase 0a/0b inventory | `classified`, `already_resolved` |
| `classified` | Disposition and owner phase recorded | `in_progress`, `blocked`, `already_resolved` |
| `in_progress` | Merge/rebase/drop/remove is underway | `merged`, `removed`, `blocked`, `already_resolved` |
| `blocked` | Needs user action, dependency, or baseline-debt decision | `classified`, `in_progress` |
| `merged` | PR/branch content landed in default branch | `cleanup_pending`, `done` |
| `cleanup_pending` | Remote/local branch or worktree cleanup remains | `removed`, `blocked` |
| `removed` | Stash/branch/worktree/artifact removed after recheck | `done` |
| `already_resolved` | Fresh recheck shows prior target no longer exists/open | `done` |
| `done` | Final evidence captured | terminal |

If the sweep creates a new PR while resolving a branch or stash, add it to the
ledger as `authorization: new_pr_requires_new_auth` and do not merge it until
the user explicitly authorizes that PR by number/title.

## Command sequence (run in order)

### Phase 0a: Baseline discovery (read-only)

Reuses the classification logic from `/chkp_check_pending` Step 1.4b/1.6, run repo-wide:

```bash
gtimeout 15 git fetch --prune origin
DEFAULT_BRANCH=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || echo main)

echo "=== Local branches ==="
gtimeout 10 git branch -vv

echo "=== Remote branches ==="
gtimeout 15 git branch -r

echo "=== Stashes ==="
gtimeout 5 git stash list

echo "=== Worktrees ==="
gtimeout 5 git worktree list

echo "=== Open PRs ==="
gtimeout 20 gh pr list --state open --json number,title,headRefName,author,isDraft
```

**Concurrent session check** — before trusting any of the above as a stable snapshot, confirm no other session is actively writing into this same working directory:

```bash
echo "=== Files touched in the last 5 minutes (unexpected = another session is active) ==="
find . -newermt '5 minutes ago' -type f -not -path './.git/*' 2>/dev/null

echo "=== Reflog for current branch (commits you didn't just make) ==="
git reflog show "$(git branch --show-current)" | head -20
```

If either turns up activity you did not just produce yourself (fresh file mtimes you can't account for, reflog entries with timestamps/messages that aren't yours), treat this working directory's current branch as owned by another live session: do not commit, stash, reset, or delete anything in it for the remainder of this sweep. Continue the sweep for everything else via `git worktree add` checkouts — see the concurrent-agent-safety and worktree-sibling-placement critical rules above.

Build one table from this output and mirror it in `.tmp/git_sweep_ledger.json`:
for every local branch, remote branch, stash, worktree, and PR, record its name,
initial state, owner phase, risk, and proposed disposition (keep / merge / close
/ drop / remove / classify_only). Nothing is deleted in this phase. If
`origin/main` advances later in the sweep, refresh the live state and update the
same ledger item rather than relying on the stale Phase 0a snapshot.

### Phase 0b: Data-loss preflight (read-only) — untracked and ignored files

**Why this phase exists**: every other phase only touches what git already tracks — commits, branches, stashes, PR refs — which git can mostly recover (reflog, `git fsck` for ~14 days, PR history). That safety net does **not** cover:

- **Untracked files** (`git status` shows `??`) — never included in a stash unless pushed with `-u`/`-a`, never part of any branch or commit.
- **`.gitignore`d files** (`git status --ignored` shows `!!`) — e.g. `.env`, credentials, local model/media caches. Never captured by git at all, by design.

Both classes are **permanently deleted with no recovery path** the instant their containing directory is removed — exactly what `git worktree remove` and any stray `rm -rf` of a checkout do.

**Runtime guard coverage — read before relying on it**: this repo's shell-level git guard (`rules/dadosfera/4_24_destructive_command_authorization.md`) blocks `git branch -d/-D/--delete`, `--force` pushes, pushes to `main`/`master`, `git clean -f*`, `reset --hard`, and `commit --no-verify` behind `GIT_AUTHORIZE_*` env vars requiring explicit user confirmation after remediation attempts and concurrent-session checks. It does **not** gate `git worktree remove --force`, `git push origin --delete <branch>`, or `git stash drop` — the three operations this sweep performs most. For those, this preflight and the per-item confirmation rule are the only safety net.

For the main working tree and every worktree found in Phase 0a:

```bash
for tree in "$(git rev-parse --show-toplevel)" $(git worktree list --porcelain | awk '/^worktree /{print $2}' | tail -n +2); do
  echo "=== $tree ==="
  gtimeout 10 git -C "$tree" status --porcelain --ignored=matching
  # Dry run only -- never pass -f/-fd/-fdx here, this is inspection, not cleanup
  gtimeout 10 git -C "$tree" clean -ndx
done
```

Classify every `??` (untracked) and `!!` (ignored) line:

- **Secret-shaped** — filename matches `\.env(\..+)?$|\.pem$|\.key$|credentials|secrets?\.(json|ya?ml)$|id_rsa`. **STOP.** Do not remove the worktree/branch until the user confirms one of:
  - it is already in OCI Vault (org standard — `standards/deployment/deployment_standard.md`, "OCI Vault is the secret store") and the local copy is redundant, or
  - the user will migrate it to Vault before this phase proceeds, or
  - it is explicitly confirmed disposable (e.g. copied from a template, no unique content).
- **Heavy/binary-shaped** — untracked or ignored file over ~1 MB, or matching common heavy-asset extensions (`png|jpe?g|gif|mp4|mov|psd|zip|tar(\.gz)?|pdf|pt|onnx|safetensors|bin`). **STOP.** Confirm one of:
  - it is reproducible (build output, cache) — safe to lose, note it in the report, or
  - it needs to be committed (via Git LFS if large) or pushed to durable object storage before the tree is removed, or
  - the user explicitly confirms it is disposable.
- **Everything else untracked** — either `git add` and commit it (folds into Phase 2/3/4's normal flow) or get explicit per-file confirmation that it is disposable.
- **Ignored reproducible artifacts** (`node_modules/`, `.tmp/`, `__pycache__/`, local log files) — classify as `ignored_artifact` with disposition `classify_only` unless the user asked for filesystem cleanup. These are not branch/PR/stash blockers once recorded.
- **Empty untracked directories** — may be removed with `rmdir` after proving they contain no files (`find <dir> -type f` empty, size 0). Record the disposition as `removed_empty_dir`.

Only after every flagged file in a given worktree/branch has a recorded disposition may Phase 1 remove that worktree, or Phase 3/4 delete that branch. Report the full disposition table (path, file, size, classification, disposition) alongside the Phase 0a table — never drop it from the final report.

### Phase 0c: Default branch itself is dirty (protected, with unpushed commits and/or uncommitted changes)

If Phase 0a shows `$DEFAULT_BRANCH` itself is ahead of `origin/$DEFAULT_BRANCH` and/or has uncommitted working-tree changes, and the branch is protected (review required, no direct push), resolve this before proceeding to Phase 1 — none of the later phases assume the default branch itself needs cleanup, and Phase 6's fast-forward pull will fail or silently diverge otherwise:

1. If there is an already-committed local-only commit on `$DEFAULT_BRANCH`, branch it off and open a PR: `git checkout -b wip/local-commit-<date> && git push -u origin HEAD && gh pr create --fill`.
2. If there are also still-uncommitted working-tree changes, branch those separately from the same starting point, commit, push, and open a second PR — this second branch depends on the first (it contains the first's commit until the first merges), so treat the pair as a stack.
3. Land the stack in order via `/gbyp_git_protection_bypass`'s 'Stack-mode operation' section (bypass once, merge both PRs in dependency order, restore protection once) rather than improvising a one-off bypass per PR.
4. Only once `$DEFAULT_BRANCH` is clean and confirmed merged, proceed to Phase 1.

### Phase 1: Worktrees

For each entry in `git worktree list` other than the main working copy, after Phase 0b has a recorded disposition for every flagged file in it:

```bash
gtimeout 10 git -C <worktree-path> status --short
```

- Clean (including no unresolved Phase 0b flags), and its branch is already merged into `origin/$DEFAULT_BRANCH` → remove it:
  ```bash
  gtimeout 10 git worktree remove <worktree-path>
  ```
  If this fails with "contains modified or untracked files", that is the safety net working as intended — go back to Phase 0b for that worktree and record dispositions for what it found. **Never** immediately retry with `--force`; `--force` is not gated by the runtime guard and will silently delete anything still sitting there, including unresolved secrets or heavy files.
- Dirty, or its branch is unmerged → do NOT remove yet. Route the branch through Phase 3/4 first (commit or land the work), then remove the worktree once its branch is merged or deleted.
- After removing worktrees whose branch no longer exists: `gtimeout 5 git worktree prune`

### Phase 2: Stashes — land or drop, never silently discard

`git stash show -p` only reconstructs what the original `git stash push` actually captured. A plain `git stash push` (no `-u`/`-a`) never captured untracked or ignored files in the first place — if content was lost that way before this sweep ran, no step here can recover it; Phase 0b exists to stop it happening again going forward, not to undo the past.

**Shared stash stack — not parallelizable across worktrees.** `stash@{N}` refs are repo-global (stored once per repository's `.git`), not per-worktree. If more than one agent/session may be operating on this repo — including via the isolation worktrees created for the concurrent-session rule above — two of them running `git stash branch` / `git stash drop` at the same time will race on the same ref list and silently grab or drop the wrong entry. Extract stashes to durable branches **one at a time, sequentially, in a single session**, always operating on `stash@{0}` — each successful `git stash branch` auto-drops its target and shifts every remaining entry down by one. Only once a stash's content is safely on its own branch (and therefore no longer in `git stash list`) is it safe to hand its commit/push/PR work to a parallel agent — from that point on it is ordinary branch state with no shared mutable structure left to race on.

Before starting extraction, record a durable position→identity mapping, since a stash's own commit SHA remains recoverable for weeks after being dropped (it is an ordinary commit object, not garbage until `git gc` runs):

```bash
for i in $(seq 0 $(($(git stash list | wc -l) - 1))); do
  echo "stash@{$i} -> $(git rev-parse stash@{$i})"
done
```

**Watch for entries that appear mid-loop.** A stray `autostash` entry (git's own automatic stash from some `--autostash`-flagged operation, possibly created by a concurrent session) can appear at the top of the list between iterations without warning, silently shifting every subsequent `stash@{0}` by one and causing branch names to no longer match their actual content. After the extraction loop finishes, verify each resulting branch's identity against the pre-recorded SHA mapping — diff its file list against `git show --name-only <recorded-SHA>` — rather than trusting loop-iteration order alone. If a mismatch is found, rename the branch to match its real content; the recorded SHA remains the reliable source of truth for re-verification even after the stash entry itself is gone.

Hand off to `/gsta_git_stash` for the full per-hunk triage of every entry in `git stash list`. For each stash:

1. Inspect: `git stash show -p stash@{N}` (per `/gsta_git_stash` Step 4).
2. Decide:
   - **Already superseded** (same change already merged via a PR) — confirm via `git log --grep` / diff against `origin/$DEFAULT_BRANCH`, then drop.
   - **Still needed** — promote to a branch and open a PR:
     ```bash
     git checkout -b wip/<topic>-$(date +%Y%m%d)
     git stash apply stash@{N}
     git add <scope>
     git commit -m "wip(<topic>): recovered from stash@{N}"
     git push -u origin HEAD
     gh pr create --fill
     ```
     Do not drop the stash until the PR is opened — Phase 4/5 lands it before it is dropped.

   - **Temporary safety stash created by this same cleanup flow** (for example `Pre-merge safety backup`) — treat it as a required end-of-flow checkpoint, not as an unrelated new authorization round:
     1. Save a patch backup under `.tmp/stash_backups/`.
     2. Compare the stash against the current branch state.
     3. If applying it in reverse does not cleanly match, or if the hunks clearly revert content that has since been restored, regenerated, merged, or intentionally replaced, classify it as **superseded** and drop it.
     4. If it still contains unique content not present on the current branch, recover that content first (branch or cherry-pick the needed pieces), then drop the stash only after the recovery is safely committed or pushed.

     **`git stash branch <name> stash@{N}`** (a one-step alternative to `checkout` + `stash apply` above) checks out, applies, **and auto-drops the stash the instant the checkout+apply succeeds — before anything is committed.** If the following `git commit` then fails (e.g. blocked by a pre-commit hook), the recovered content is safe and uncommitted in the working tree, but the stash entry is already gone from `git stash list` — you cannot re-run the extraction for that stash. Fix whatever is blocking the commit in place and commit again; do not retry the extraction, and never `git reset --hard` or `git clean` to "start over" — that would destroy the only remaining copy of the content.
3. Only after the stash's content is confirmed superseded or captured in an open/merged PR: `git stash drop stash@{N}` (skip this if it was already auto-dropped by `git stash branch`, per the note above).

Exit when `git stash list` is empty.

### Phase 2.5: Pending-to-merge worktree

SSoT: `guides/collaboration/pending_to_merge_worktree.md`. This is the **only** phase that commits, pushes, resets, and removes this worktree — `/chkp_check_pending` only ever appends content to it, never a git operation.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
WT_PATH="$(dirname "$REPO_ROOT")/${REPO_NAME}-wt-pending-to-merge"

if ! git worktree list | grep -q "$WT_PATH"; then
  echo "No pending-to-merge worktree found — nothing accumulated since last sweep."
else
  gtimeout 10 git -C "$WT_PATH" status --short
fi
```

- **Worktree absent** → nothing to do. Report accordingly and move on.
- **Worktree present and clean** → this means there is no pending content in the staging file; remove it to keep the repo clean.
   1. `git worktree remove "$WT_PATH"`
   2. `git branch -d chore/pending-to-merge || git branch -D chore/pending-to-merge` (if the local branch is still present and safe to remove)
- **Worktree present and dirty** (accumulated entries from one or more `/chkp_check_pending` runs):
  1. Commit the plan file in `$WT_PATH`: `git -C "$WT_PATH" add -A && git -C "$WT_PATH" commit -m "chore(pending-to-merge): accumulate other-agent pending work"`.
  2. Push: `git -C "$WT_PATH" push -u origin chore/pending-to-merge`.
  3. Open a PR if none is open for this branch yet (`gh pr create --fill --base "$DEFAULT_BRANCH"`), or note the existing one. **This PR requires its own separate merge authorization**, same as any other PR this sweep opens (Authorization Requirements item 6) — do not fold it into an earlier "merge everything" instruction.
  4. Only after that PR is confirmed merged (`gh pr view <n> --json state`): truncate the plan file back to its empty template, commit ("chore(pending-to-merge): flush after PR #<n> merged"), and push.
  5. Remove transient artifacts:
     - `git worktree remove "$WT_PATH"`
     - `git branch -d chore/pending-to-merge || git branch -D chore/pending-to-merge` (local branch cleanup if present)

### Phase 3: Local branches

**Before checking merge status, screen for lifecycle-tracking branches.** If a branch name matches `release/{stage}` or `release/v{version}-{stage}` (see `standards/lifecycle/lifecycle_standard.md`), do **not** delete it under any disposition in this phase, regardless of merge status — a `release/{stage}` branch sitting at the same commit as `$DEFAULT_BRANCH` trivially passes an ancestor/merged check exactly like an ordinary finished feature branch. This is not hypothetical: a live sweep followed this table as written and deleted a sanctioned `release/alpha` branch, recoverable only because it happened to be at parity with (not ahead of) `$DEFAULT_BRANCH` at the time. Surface it as a distinct "lifecycle-tracking branch, out of scope for this sweep" row and skip it entirely — syncing it (merge default → release/{stage} + push) is a separate, deploy-affecting decision outside this sweep's scope.

For each remaining local branch other than `$DEFAULT_BRANCH`:

- Already merged into `origin/$DEFAULT_BRANCH` → delete: `git branch -d <branch>`. Only use `-D` after confirming why the "not fully merged" warning is expected — never as a default (per `/gsta_git_stash`'s and `/merg_merge`'s "list first, delete one at a time" rule).
  - **Squash-merged branches**: `git merge-base --is-ancestor <branch> origin/$DEFAULT_BRANCH` reports "not an ancestor" for a squash-merged branch, because the squash commit on `$DEFAULT_BRANCH` is not a descendant of the branch's original commits — this is expected, not a sign the branch is unmerged. Confirm the real status via `gh pr view <n> --json state` (look for `MERGED`); if merged, delete with `git branch -D <branch>` (capital `D`), since `-d`'s ancestor-based safety check will incorrectly refuse it.
- Not merged, has a corresponding remote branch/PR → handled in Phase 4/5, not here.
- Not merged, no remote counterpart, and abandoned (user confirms) → `git branch -D <branch>` after explicit confirmation.

### Phase 4: Remote branches

**Same lifecycle-tracking guard as Phase 3, applied before classification runs**: the `grep -vE "^origin/release/"` line below excludes `release/{stage}` / `release/v{version}-{stage}` branches from the merge-status check entirely, since one sitting at parity with `$DEFAULT_BRANCH` would otherwise classify as `STALE_MERGED`. Surface any excluded `release/{stage}` remote branch as "lifecycle-tracking branch, out of scope for this sweep" and skip it — do not delete it under any disposition in this phase.

Reuse the classification from `/chkp_check_pending` Step 1.4b:

```bash
gtimeout 15 git for-each-ref --format='%(refname:short)' refs/remotes/origin \
  | grep -v "^origin/HEAD$" \
  | grep -v "^origin/$DEFAULT_BRANCH$" \
  | grep -vE "^origin/release/" \
  | while read -r ref; do
      sha=$(git rev-parse "$ref" 2>/dev/null) || continue
      if git merge-base --is-ancestor "$sha" "origin/$DEFAULT_BRANCH" 2>/dev/null; then
        echo "STALE_MERGED  $ref"
      else
        echo "UNMERGED      $ref  ($(git log --oneline "origin/$DEFAULT_BRANCH..$ref" | wc -l | tr -d ' ') commits)"
      fi
    done
```

- **STALE_MERGED**: delete on remote, one at a time, after confirmation:
  ```bash
  gtimeout 10 git push origin --delete <branch>
  ```
  If the push is rejected by branch protection or permissions, hand off to `/gadm_git_admin_push` (or `/gbyp_git_protection_bypass` if the branch itself is protected).
- **UNMERGED**: do not delete. If it has no open PR, Phase 5 turns it into a PR (or the work is confirmed abandoned and explicitly discarded by the user). If it has an open PR, land it via `/merg_merge` — that command owns branch deletion after merge (`--delete-branch`), so do not delete it separately here.

### Phase 5: Open PRs

```bash
gtimeout 20 gh pr list --state open --json number,title,headRefName,isDraft,mergeable
```

For each open PR:

- **Ready and mergeable** → `/merg_merge` (which uses `/gbyp_git_protection_bypass` for solo-admin/self-approval cases per its "Solo-admin merge" section). `/merg_merge` deletes the remote branch as part of its own cleanup (Step 20b) — do not delete it separately here.
- **Draft / blocked / stale** → surface to the user; do not auto-close. Closing an open PR is a judgment call the sweep cannot make on its own — get explicit per-PR confirmation, then `gh pr close <number>`.

Before calling `/merg_merge`, refresh the PR state. If the PR is no longer open, emit an explicit stale-target message instead of trying to merge it:

- `Authorization stale: PR #<n> is already merged; nothing remains to merge.`
- `Authorization stale: PR #<n> is already closed; confirm whether a replacement PR is needed instead of reusing the old authorization.`
- `Authorization stale: no open PR remains for branch <name>; refresh the sweep inventory before taking further destructive action.`

**Shared index/registry files can conflict on every PR in the same sweep session.** A file many PRs touch (a plan registry, a command-registry index) will often conflict on merge even when each PR's actual intent is an independent list-append with no real semantic disagreement — see `/gbyp_git_protection_bypass`'s "Pull Request has merge conflicts" troubleshooting entry for the full pattern. When it happens: fetch `origin/$DEFAULT_BRANCH`, merge it into the PR branch in an isolated worktree, and for hunks where both sides simply added distinct entries to the same list/section, **combine both additions rather than picking one side** — verify by reading both sides first; only combine independent nearby additions, not genuine same-line edits.

**Each new PR the sweep itself produces requires its own separate merge authorization.** A stash-promotion PR (Phase 2), a docs-recovery PR, or a code-review nits-followup PR opened as a byproduct of this sweep's own work is not automatically covered by an earlier "merge PR #x and #y" from the user, even under a broad "finish everything" instruction — state the new PR explicitly and get confirmation before running it through the same bypass-and-merge flow. See `/gbyp_git_protection_bypass`'s "Stack-mode operation" section, and Authorization Requirements item 6 above.

**Admin merge local-error reconciliation.** `gh pr merge --admin --merge --delete-branch`
can merge the PR on GitHub and still return a local git error, especially when
`gh` tries to switch or pull a branch that is already checked out in another
worktree (for example: `fatal: 'main' is already used by worktree at ...`).
When that happens:

1. Re-check the PR live: `gh pr view <n> --json state,mergedAt,mergeCommit,headRefName`.
2. If `state == MERGED`, treat GitHub as the source of truth and record
   `disposition=already_resolved` or `merged` in the ledger. Do **not** retry
   the merge or spend the authorization on another PR.
3. `git fetch --prune origin` in the main checkout and fast-forward the default
   branch from `origin/<default>`.
4. If the remote head branch still exists, delete it only after proving its tip
   is included in the default branch:
   ```bash
   git merge-base --is-ancestor "origin/<head-branch>" "origin/$DEFAULT_BRANCH"
   git push origin --delete "<head-branch>"
   ```
5. Remove the local worktree and local branch only after Phase 0b has no
   unresolved data-loss flags for that worktree.

Exit when `gh pr list --state open` is empty.

### Phase 6: Final sync of the default branch

```bash
git checkout "$DEFAULT_BRANCH"
```

Use `/gful_git_full_sync` if any local work landed during this sweep and history needs rebasing/pruning; otherwise `/gsyn_git_sync`'s plain fast-forward pull is sufficient:

```bash
gtimeout 60 git pull --ff-only origin "$DEFAULT_BRANCH"
```

### Phase 7: Verify exit criteria and report

Re-run every check from the "Definition of clean slate" table above and report actual vs. expected for each row. Do not report success if any row still fails — list the remaining item(s) and the phase that owns fixing them instead.

Also report:

- PRs merged during the sweep, with merge commits and timestamps.
- Branches/worktrees removed, with the fresh `merge-base`/PR-state evidence used.
- Baseline debt discovered but not fixed, especially repository-wide
  `pre-commit run --all-files` failures unrelated to the sweep branch.
- Ignored/reproducible artifacts still present and why they are not blockers.
- Branch protection posture after any `/gbyp_git_protection_bypass` call
  (`enforce_admins`, review-bypass users, and whether full rollback was
  requested).

## Related Commands

- `/chkp_check_pending`
- `/gsta_git_stash`
- `/gsyn_git_sync`
- `/gful_git_full_sync`
- `/merg_merge`
- `/gbyp_git_protection_bypass`
- `/gadm_git_admin_push`

## Related

- Skill: `.cursor/skills/using-git-worktrees/SKILL.md`
- Concurrent-agent worktree isolation (SSoT): `guides/collaboration/multi_agent_worktree_workflow.md`
- Pending-to-merge worktree (SSoT for Phase 2.5): `guides/collaboration/pending_to_merge_worktree.md`
- Branch conventions: `standards/git/branch_convention.md`
- Release/lifecycle branch naming: `standards/lifecycle/lifecycle_standard.md`
- PR practices: `standards/git/pull-request-best-practices.md`
- Runtime git guard / destructive-command authorization: `rules/dadosfera/4_24_destructive_command_authorization.md`
- Secret storage standard (OCI Vault): `standards/deployment/deployment_standard.md`
