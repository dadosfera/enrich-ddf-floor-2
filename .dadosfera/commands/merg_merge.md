---
category: automation
criticality: critical
scope: all
---

# /merg_merge

**Local Reference**: `commands/merg_merge.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/merg_merge.md`

<!-- COMMAND_ID: 033 -->
<!-- COMMAND_VERSION: 1.13.3 -->
<!-- COMMAND_TYPE: me_merge -->
<!-- CANONICAL_SOURCE: markdown-only (no commands/json/core peer). See commands/markdown_only_commands.yaml -->
<!-- UPDATED: 2026-07-10 - Add stale-authorization detection for branch/PR targets so merge attempts distinguish already-merged/already-closed/no-longer-present states with explicit operator messages. -->
<!-- UPDATED: 2026-07-10 - Clarify that pre-merge safety stashes must be triaged to completion: reintegrate unique content, or drop them if superseded by the final merged branch state. -->
<!-- UPDATED: 2026-01-29 - Add cleanup policy + prefer PR merge --delete-branch when PR exists -->
<!-- UPDATED: 2026-07-05 - WIP preservation: prefer backup branch over stash; Step 20c blocking gate + STASH_* audit log -->
<!-- UPDATED: 2026-07-07 - Concurrent-agent safety callout: link multi_agent_worktree_workflow SSoT -->

Safely merge an agent branch into the default branch using zero-trust validation, isolation testing, manual conflict handling, and rollback points. This follows the practices in the referenced mini prompt and the terminal command safety guidelines (timeouts, no chaining, short commands).

**Concurrent-agent safety**: If another agent may be live in this repo, do your work in **your own git worktree** (one worktree per agent) before any `checkout`/`reset`/`stash`/`merge`/`clean` — in a shared checkout those operations silently destroy another agent's uncommitted work, at any change size. SSoT: `guides/collaboration/multi_agent_worktree_workflow.md`.


**Local Reference**: `commands/merg_merge.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/merg_merge.md`

Backlinks:

- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- standards/git/branch_convention.md
- standards/git/pull-request-best-practices.md

## ⚠️ Authorization Requirements

Before merging into `main` or protected branches, this command requires:

1. **Explicit User Authorization**: User must confirm bypass operations when prompted
2. **Environment Variable** (optional): `USER_AUTHORIZATION_BYPASS_BRANCH_PROTECTION=true` in `.env` (skips interactive prompts)
3. **Admin Privileges**: GitHub user must have admin access to repository

**Safety Rules Applied**:
- `4_20_branch_protection_bypass_authorization`: Requires explicit confirmation before bypass operations
- `1_02_autonomy_user_handoff`: Level 4 operations (committing to main) require explicit approval

**If push to protected branch fails**: The command will STOP and request explicit user authorization before proceeding with any PR workflow or branch protection bypass operations.

## Solo-admin merge (when you authored the PR and there is no second reviewer)

GitHub forbids `gh pr review --approve` on your own PR, and `gh pr merge --admin` will still fail with `At least 1 approving review is required` if `enforce_admins: true` and you are not in `bypass_pull_request_allowances`. In that situation, **do not** force-push, do not rename `main`, and do not weaken protection by hand. Instead, hand off the merge step (Step 19+) to `/gbyp_git_protection_bypass` (v2.0.0+), which:

1. Detects whether the branch is governed by classic protection or by Repository/Org Rulesets (the classic API silently no-ops on Rulesets).
2. Adds your user to `bypass_pull_request_allowances` via `PATCH .../required_pull_request_reviews` (smaller blast radius than rewriting full protection).
3. Temporarily disables `enforce_admins` only when needed.
4. Performs `gh pr merge --admin --merge --delete-branch` and audits the action to `logs/git_sync_operations.log`.
5. Phase 7 restores core protections by default (`enforce_admins`, required PR checks, rulesets) and keeps user-scoped allowances; use `REVERT_PROTECTION=1` if you need a full rollback in cleanup.

After `/gbyp_git_protection_bypass` returns, resume `/merg_merge` from Step 20 (cleanup policy) onwards on a clean target branch.

**Recurrent post-merge gotcha (handled in Step 20+):** if `gh pr merge` reported a local git error but the PR is actually merged on GitHub, treat the remote as the source of truth — re-run `gh pr view <PR>` to confirm `state == MERGED`, then stash any blocking local changes, `git checkout main`, and `git pull --ff-only origin main` before deleting the local feature branch.

## 🥞 Stacked-PR awareness (read before merging any PR that has dependents)

**Critical rule**: A PR is a *stack base* if any other open PR uses its head branch as a base. Treat stack bases differently from leaf PRs. The stack-merge footgun fixed by this section caused the [`pr_stack_premature_branch_delete`](../recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md) incident.

**Why this matters**: GitHub auto-closes any PR whose base branch is deleted, and once closed, GitHub **will not let you reopen the PR or change its base**. If `gh pr merge --delete-branch` deletes a stack base before its children are retargeted, every dependent PR is silently destroyed and you must recreate them by hand (with all their description/review history lost).

### Decide leaf vs. stack base BEFORE picking the merge flag

Run this before Step 19 / Step 20b (and again right before any `--delete-branch`):

```bash
# Detect children: open PRs that use this PR's head branch as their base.
# Requires PR_NUMBER (or AGENT_BRANCH) to be set; see step 6a.
HEAD_BRANCH=$(gtimeout 10 gh pr view "${PR_NUMBER:-$AGENT_BRANCH}" --json headRefName --jq .headRefName)
DEPENDENT_PRS=$(gtimeout 10 gh pr list --state open --base "$HEAD_BRANCH" \
                  --json number,headRefName,title --jq '.')
DEPENDENT_COUNT=$(echo "$DEPENDENT_PRS" | jq 'length')

echo "Head branch: $HEAD_BRANCH"
echo "Open PRs that depend on it (i.e. use it as their base): $DEPENDENT_COUNT"
echo "$DEPENDENT_PRS" | jq -r '.[] | "  - #\(.number) \(.headRefName): \(.title)"'

if [ "$DEPENDENT_COUNT" -gt 0 ]; then
  echo "⚠️  This is a STACK BASE. Do NOT pass --delete-branch to gh pr merge yet."
  echo "    Use the 'stack-base merge sequence' below instead."
  export STACK_BASE=1
else
  echo "✅ This is a LEAF PR. The normal --delete-branch flow is safe."
  export STACK_BASE=0
fi
```

### Stack-base merge sequence (do NOT delete the branch yet)

When `STACK_BASE=1`, replace the normal Step 20b `gh pr merge ... --delete-branch` recipe with:

```bash
# 1. Merge the base PR WITHOUT deleting the branch.
gtimeout 60 gh pr merge "$PR_NUMBER" --merge        # NO --delete-branch
# (or, with admin override:)
# gtimeout 60 gh pr merge "$PR_NUMBER" --merge --admin

# 2. Retarget every direct child onto main (or the new shared base).
echo "$DEPENDENT_PRS" | jq -r '.[].number' | while read -r CHILD_PR; do
  echo "Retargeting #$CHILD_PR -> main"
  gtimeout 15 gh pr edit "$CHILD_PR" --base main

  # 2a. Verify the base actually updated (GitHub silently keeps the old base if the API rejects).
  NEW_BASE=$(gtimeout 10 gh pr view "$CHILD_PR" --json baseRefName --jq .baseRefName)
  if [ "$NEW_BASE" != "main" ]; then
    echo "❌ #$CHILD_PR did not retarget (still base=$NEW_BASE). STOP and investigate before deleting any branch."
    exit 1
  fi
  echo "   ✅ #$CHILD_PR now targets main"
done

# 3. ONLY NOW is it safe to delete the merged branch.
gtimeout 15 git push origin --delete "$HEAD_BRANCH"
```

### Rebase-before-replace guard (when a child must be rebased onto a new base)

When a child branch is behind `main` on unrelated sibling commits (e.g. parallel fixes landed via PRs `#87`/`#89` in the canonical incident), a naive squash-merge of the rebased child would **revert those sibling commits**. Run this diff-check before merging any rebased child:

```bash
# Variables: CHILD_BRANCH = the child branch you just rebased onto main
#            CHILD_PR     = its PR number
gtimeout 10 git fetch origin main "$CHILD_BRANCH"

# Files the child PR claims to change (per its diff vs. main):
gtimeout 15 gh pr diff "$CHILD_PR" --name-only | sort -u > .tmp/child_pr_files.txt

# Files that main has but the rebased branch would "lose" if squash-merged:
gtimeout 10 git diff --name-only "$CHILD_BRANCH"..origin/main | sort -u > .tmp/files_on_main_only.txt

# Any overlap means the squash-merge would silently roll back commits that
# already landed on main via OTHER PRs. STOP if so.
OVERLAP=$(comm -12 .tmp/child_pr_files.txt .tmp/files_on_main_only.txt)
if [ -n "$OVERLAP" ]; then
  echo "❌ STOP. The rebased child would revert commits already on main in these files:"
  echo "$OVERLAP" | sed 's/^/   - /'
  echo "Re-rebase the child onto current origin/main, resolve, and re-run this guard."
  exit 1
fi
echo "✅ No overlap. Safe to merge the rebased child."
```

### When a child PR is auto-closed (recovery procedure)

If `--delete-branch` was already used prematurely and a child PR is now CLOSED with its base branch gone, the **only** path forward is a replacement PR. GitHub will not let you reopen a closed PR or change its base:

```bash
# 1. Rebase the orphaned head branch onto current main, resolve, and force-push as a NEW branch
#    (do NOT reuse the orphan branch name if you can avoid it).
git fetch origin main
git checkout "<orphan-head-branch>"
git rebase origin/main
# Resolve any conflicts, then RUN THE rebase-before-replace guard above
# against this branch + main, BEFORE creating the replacement PR.

# 2. Open a replacement PR carrying the original PR description plus a "Replaces #<orig>" link.
ORIG_BODY=$(gtimeout 10 gh pr view <orig> --json body --jq .body)
gh pr create --base main --head "<orphan-head-branch>" \
  --title "<orig title>" \
  --body "$(printf 'Replaces #<orig> (auto-closed when its base branch was deleted with #<base-orig>).\n\n---\n\n%s' "$ORIG_BODY")"
```

## Usage

- Set `AGENT_BRANCH` to the source branch to merge.
- Optionally set `TARGET_BRANCH` to override the default branch (defaults to origin/HEAD).
- Follow steps in order; stop on any error and resolve before proceeding.

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Set variables (edit `AGENT_BRANCH` as needed)

```bash
AGENT_BRANCH="agent-branch-name"
DEFAULT_BRANCH=$(gtimeout 5 git symbolic-ref --short refs/remotes/origin/HEAD | sed 's@^origin/@@' || echo main)
TARGET_BRANCH="${DEFAULT_BRANCH}"  # override if merging into a non-default branch
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || echo "")

# Cleanup policy (prevents “merge complete but cleanup pending” surprises)
# - conservative: keep rollback artifacts for 1–7 days
# - standard (default): delete local rollback branch; remote cleanup remains gated by explicit authorization
# - aggressive: require remote cleanup; otherwise do not mark merge “complete”
CLEANUP_MODE="${CLEANUP_MODE:-standard}"  # conservative|standard|aggressive
```

2a. Check for authorization environment variable (for protected branches)

```bash
# Check if target branch is protected (main/master) and if authorization is pre-configured
if [ "$TARGET_BRANCH" = "main" ] || [ "$TARGET_BRANCH" = "master" ]; then
  # Check specifically for uncommented line at start of string or following newline
  if [ -f .env ] && grep -q "^USER_AUTHORIZATION_BYPASS_BRANCH_PROTECTION=true" .env; then
    echo "✅ Found USER_AUTHORIZATION_BYPASS_BRANCH_PROTECTION=true in .env"
    export USER_AUTHORIZED_BYPASS=true
  else
    echo "⚠️  WARNING: USER_AUTHORIZATION_BYPASS_BRANCH_PROTECTION not set in .env"
    echo "Explicit authorization will be required for bypass operations."
    export USER_AUTHORIZED_BYPASS=false
  fi
else
  export USER_AUTHORIZED_BYPASS=false
fi
```

3. Verify GitHub CLI auth and identify GitHub CLI user (for PR/bypass operations)

```bash
gtimeout 10 gh auth status
```

```bash
gtimeout 10 gh auth status --json user --jq '.user.login'
```

3a. Optional (Admin-only): Check branch protection bypass for the GitHub CLI user

```bash
gtimeout 10 gh auth status --json user --jq '.user.login'
```

```bash
gtimeout 10 gh api "repos/$REPO/collaborators/$(gh auth status --json user --jq '.user.login')/permission" --jq '.permission'
```

```bash
# View current bypass user list for the target branch (read-only)
gtimeout 10 gh api "repos/$REPO/branches/$TARGET_BRANCH/protection/required_pull_request_reviews" --jq '.bypass_pull_request_allowances.users[].login'
```

Note: To configure bypass (admin-only), follow the procedure in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md` (“GitHub CLI User Configuration Guide”).

4. Create safety backup — **prefer backup branch over stash for untracked WIP**

**Default (preferred)**: Park untracked/multi-file WIP on a dedicated branch instead of stashing.

```bash
gtimeout 5 git branch --show-current
```

```bash
mkdir -p .tmp
BACKUP_BRANCH="backup-pre-merge-$(date +%Y%m%d_%H%M%S)"
WIP_BRANCH="wip/pre-merge-$(date +%Y%m%d_%H%M%S)"
echo "$BACKUP_BRANCH" > .tmp/pre_merge_backup_branch.txt

# Option A (PREFERRED when untracked files exist or >5 files changed):
# git checkout -b "$WIP_BRANCH"
# git add -A && git commit -m "wip: pre-merge safety $(date +%Y%m%d_%H%M%S)"
# git checkout -   # return to merge branch with clean tree

# Option B (fallback — short context switch only):
gtimeout 10 git branch "$BACKUP_BRANCH"
echo "Created backup branch: $BACKUP_BRANCH"
```

Use **stash only** when ALL are true: context switch < 30 min, restore planned same session, patch saved to `.tmp/stash_backups/`. Otherwise use Option A above.

```bash
# Stash fallback (include untracked) — log STASH_CREATED after push:
gtimeout 15 git stash push --include-untracked -m "Pre-merge safety backup (including untracked)"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) STASH_CREATED ref=$(git stash list | head -1 | sed 's/:.*//') reason=merg_merge step=4 actor=$(git config user.email 2>/dev/null || echo unknown)" >> logs/git_sync_operations.log 2>/dev/null || true
```

4.0) Record the exact pre-merge stash reference (MANDATORY)

**Why**: This prevents “forgotten stash” data loss. Do not proceed until you have captured the stash ref (or confirmed no stash was created).

```bash
# Capture newest stash line (if any) and persist it for later restore/reintegration
gtimeout 10 git stash list | head -n 1 > .tmp/pre_merge_stash.txt
cat .tmp/pre_merge_stash.txt
```

```bash
# Extract stash ref like "stash@{0}" (empty if no stash exists)
PRE_MERGE_STASH_REF=$(sed 's/:.*//' .tmp/pre_merge_stash.txt 2>/dev/null || echo "")
echo "Pre-merge stash ref: ${PRE_MERGE_STASH_REF:-<none>}"
```

4a. Verify working directory is clean

```bash
gtimeout 5 git status --porcelain | grep . && { echo "Working directory not clean after stash. Aborting to prevent data loss."; exit 1; } || echo "Working directory clean."
```

5. Fetch all remote branches to ensure up-to-date branch information

```bash
gtimeout 30 git fetch --all --prune
```

6. Discover branches (local and remote) for context

```bash
gtimeout 15 git branch --list
```

```bash
gtimeout 15 git branch -r
```

```bash
gtimeout 15 git branch -a
```

```bash
gtimeout 15 git branch -a | grep "agent-" || true  # optional: highlight agent branches
```

```bash
gtimeout 30 gh pr list --state open --json number,title,headRefName,author,labels --limit 50
```

6a. Optional: Handle open PR for the agent branch (merge | close | update)

```bash
gtimeout 10 gh pr list --state open --head "$AGENT_BRANCH" --json number --jq '.[0].number' > .tmp/${AGENT_BRANCH}_pr_number.txt
```

```bash
PR_NUMBER=$(cat .tmp/${AGENT_BRANCH}_pr_number.txt 2>/dev/null || echo "")
```

```bash
[ -n "$PR_NUMBER" ] && gtimeout 10 gh pr view "$PR_NUMBER" --json mergeable,mergeStateStatus,title
```

If `PR_NUMBER` is empty, do **not** assume "just create/merge something". First detect whether the authorization target is stale:

```bash
if [ -z "$PR_NUMBER" ]; then
  LAST_BRANCH_PR=$(gtimeout 10 gh pr list --state all --head "$AGENT_BRANCH" \
    --json number,state,title --jq '.[0] // empty' 2>/dev/null || true)

  if [ -n "$LAST_BRANCH_PR" ]; then
    LAST_PR_NUMBER=$(echo "$LAST_BRANCH_PR" | jq -r '.number')
    LAST_PR_STATE=$(echo "$LAST_BRANCH_PR" | jq -r '.state')
    if [ "$LAST_PR_STATE" = "MERGED" ]; then
      echo "Authorization stale: branch $AGENT_BRANCH was already merged via PR #$LAST_PR_NUMBER; nothing remains to merge."
      exit 0
    fi
    if [ "$LAST_PR_STATE" = "CLOSED" ]; then
      echo "Authorization stale: latest PR for $AGENT_BRANCH is already closed (#$LAST_PR_NUMBER); confirm whether a replacement PR is needed."
      exit 1
    fi
  fi

  echo "No open PR currently exists for $AGENT_BRANCH."
fi
```

Reference: See Step 5.6 in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md` for actions to merge, close, or update the PR.

6b. Verify remote CI status for the agent branch (if PR exists)

```bash
[ -n "$PR_NUMBER" ] && gtimeout 15 gh pr checks "$PR_NUMBER" || echo "No PR or checks passed/skipped"
```

6c. Check if agent branch exists locally or remotely and select newest

```bash
# First: check if local branch exists
gtimeout 10 git show-ref --verify --quiet refs/heads/"$AGENT_BRANCH" && echo "local branch found" || echo "local branch not found"
```

```bash
# Second: discover remote branch reference (if any)
gtimeout 15 git for-each-ref --format='%(refname:short)' "refs/remotes/*/$AGENT_BRANCH" || true
```

```bash
# Third: capture the first matching remote branch ref
REMOTE_BRANCH_REF=$(gtimeout 15 git for-each-ref --format='%(refname:short)' "refs/remotes/*/$AGENT_BRANCH" | head -n 1)
echo "Remote branch ref: ${REMOTE_BRANCH_REF:-<none>}"
```

```bash
# Fourth: determine which branch to use (prefer the most recently updated)
# This reduces merge conflicts by using the branch with the latest changes
LOCAL_EXISTS=$(gtimeout 10 git show-ref --verify --quiet refs/heads/"$AGENT_BRANCH" 2>/dev/null && echo "yes" || echo "no")
REMOTE_EXISTS=$([ -n "$REMOTE_BRANCH_REF" ] && echo "yes" || echo "no")

if [ "$LOCAL_EXISTS" = "yes" ] && [ "$REMOTE_EXISTS" = "yes" ]; then
  # Both exist: compare last commit dates and use the newer one
  LOCAL_DATE=$(gtimeout 10 git log -1 --format=%ct "refs/heads/$AGENT_BRANCH" 2>/dev/null || echo "0")
  REMOTE_DATE=$(gtimeout 10 git log -1 --format=%ct "$REMOTE_BRANCH_REF" 2>/dev/null || echo "0")

  if [ "$LOCAL_DATE" -gt "$REMOTE_DATE" ]; then
    AGENT_BRANCH_REF="$AGENT_BRANCH"
    LOCAL_STR=$(date -r "$LOCAL_DATE" +%Y-%m-%d\ %H:%M:%S 2>/dev/null || echo "unknown")
    REMOTE_STR=$(date -r "$REMOTE_DATE" +%Y-%m-%d\ %H:%M:%S 2>/dev/null || echo "unknown")
    echo "Using local branch (newer: $LOCAL_STR vs remote: $REMOTE_STR)"
  elif [ "$REMOTE_DATE" -gt "$LOCAL_DATE" ]; then
    AGENT_BRANCH_REF="$REMOTE_BRANCH_REF"
    REMOTE_STR=$(date -r "$REMOTE_DATE" +%Y-%m-%d\ %H:%M:%S 2>/dev/null || echo "unknown")
    LOCAL_STR=$(date -r "$LOCAL_DATE" +%Y-%m-%d\ %H:%M:%S 2>/dev/null || echo "unknown")
    echo "Using remote branch (newer: $REMOTE_STR vs local: $LOCAL_STR)"
  else
    # Same date or error: prefer local (safer for testing)
    AGENT_BRANCH_REF="$AGENT_BRANCH"
    echo "Using local branch (same commit date or unable to compare)"
  fi
elif [ "$LOCAL_EXISTS" = "yes" ]; then
  AGENT_BRANCH_REF="$AGENT_BRANCH"
  echo "Using local branch (remote not found)"
elif [ "$REMOTE_EXISTS" = "yes" ]; then
  AGENT_BRANCH_REF="$REMOTE_BRANCH_REF"
  echo "Using remote branch (local not found)"
else
  echo "Branch $AGENT_BRANCH not found locally or remotely"; exit 1
fi
echo "Selected branch reference: $AGENT_BRANCH_REF"
```

7. Establish baseline test results (allows longer timeout)

```bash
gtimeout 600 _dev/tests/run_tests.sh --all --baseline > .tmp/baseline_tests.log
```

8. Create isolated test branch and merge agent branch without committing

```bash
gtimeout 10 git checkout -b test-agent-merge-$(date +%Y%m%d_%H%M%S)
```

```bash
# Fetch specific branch if using remote reference (already fetched in step 5, but ensure latest)
if [[ "$AGENT_BRANCH_REF" != "$AGENT_BRANCH" ]]; then
  REMOTE_NAME="${AGENT_BRANCH_REF%%/*}"
  REMOTE_BRANCH="${AGENT_BRANCH_REF#*/}"
  gtimeout 30 git fetch "$REMOTE_NAME" "$REMOTE_BRANCH"
fi
```

```bash
gtimeout 30 git merge "$AGENT_BRANCH_REF" --no-commit --no-ff
```

9. If conflicts occur: STOP and resolve manually per the mini prompt (Enhanced Conflict Resolution). After manual resolution, continue. To inspect:

```bash
gtimeout 10 git status
```

10. Run full isolated tests on merged state (allows longer timeout)

```bash
gtimeout 600 _dev/tests/run_tests.sh --all --isolated > .tmp/agent_tests.log
```

11. Compare results and check for degradations

```bash
gtimeout 60 diff .tmp/baseline_tests.log .tmp/agent_tests.log > .tmp/test_diff.log
```

```bash
gtimeout 30 grep -c "FAILED" .tmp/agent_tests.log || true
```

```bash
gtimeout 30 grep -c "REGRESSION" .tmp/test_diff.log || true
```

12. Return to target branch and verify synchronization

```bash
gtimeout 10 git checkout "$TARGET_BRANCH"
```

```bash
# Zero-Trust Sync: Ensure local target branch matches remote exactly before merging
gtimeout 15 git fetch origin "$TARGET_BRANCH"
```

```bash
gtimeout 15 git pull origin "$TARGET_BRANCH" --ff-only || {
  echo "⚠️  Cannot fast-forward $TARGET_BRANCH. Local branch diverged."
  echo ""
  echo "MANDATORY: Resolve divergence BEFORE continuing the merge workflow."
  echo "Do NOT proceed to steps 13+ until local and remote are reconciled."
  echo ""
  echo "IMPORTANT: Any baseline/isolated test results collected earlier may no longer be trustworthy,"
  echo "because the target branch has changed on the remote. After reconciliation, re-run this command."
  echo ""
  echo "Recommended (merge-based) divergence resolution workflow:"
  echo "  12b. Create an integration branch from origin/$TARGET_BRANCH"
  echo "  12c. Merge local $TARGET_BRANCH into it and resolve conflicts"
  echo "  12d. Run hooks/tests on the integrated state"
  echo "  12e. Merge integrated state back to $TARGET_BRANCH via PR (preferred)"
  exit 1
}
```

```bash
gtimeout 10 git status --porcelain
```

12b. Divergence resolution (MANDATORY when Step 12 ff-only pull fails)

**Goal**: Produce a clean, tested branch that contains **both**:
- the current remote target branch (`origin/$TARGET_BRANCH`), and
- your local commits on `$TARGET_BRANCH`,
so you can safely continue the merge workflow.

**Why this is mandatory**: If `origin/$TARGET_BRANCH` has new commits, the agent-branch merge validation is no longer trustworthy until the target branch divergence is resolved.

```bash
# Create a temporary integration branch from the remote target
INTEGRATION_BRANCH="tmp-target-origin-${TARGET_BRANCH}-$(date +%Y%m%d_%H%M%S)"
gtimeout 10 git checkout -b "$INTEGRATION_BRANCH" "origin/$TARGET_BRANCH"
echo "Integration branch: $INTEGRATION_BRANCH"
```

12c. Merge local target branch into the integration branch (conflicts may occur)

```bash
# Merge local target history into the integration branch
# If conflicts happen: STOP and resolve manually per the mini prompt.
gtimeout 30 git merge "$TARGET_BRANCH" --no-ff
```

```bash
# Inspect conflict state / working tree
gtimeout 10 git status
```

12d. Validate the integrated state (hooks + tests)

```bash
gtimeout 60 pre-commit run --all-files
```

```bash
# Note: --post-merge flag reused here for integrated state validation (target_integration log clarifies context)
gtimeout 600 _dev/tests/run_tests.sh --all --post-merge > .tmp/target_integration_tests.log
```

12e. Complete divergence resolution (preferred: PR into protected branch)

**Preferred** (safer on protected branches): push the integration branch and open a PR targeting `$TARGET_BRANCH`.

```bash
gtimeout 15 git push -u origin "$INTEGRATION_BRANCH"
```

```bash
# Create PR to reconcile divergence (merge via the repo's normal required-review process; do not auto-merge)
gtimeout 30 gh pr create --base "$TARGET_BRANCH" --head "$INTEGRATION_BRANCH" --title "chore: reconcile ${TARGET_BRANCH} divergence" --body "Reconciles local and remote ${TARGET_BRANCH} so merge validation can proceed safely."
```

After the PR is merged into `$TARGET_BRANCH`, re-run this command from a clean `$TARGET_BRANCH` that matches `origin/$TARGET_BRANCH` (Step 12 should succeed with `--ff-only`).

13. Pre-merge hooks

```bash
gtimeout 60 pre-commit run --all-files
```

14. Create rollback checkpoints (tags)

```bash
gtimeout 10 git tag pre-merge-checkpoint-$(date +%Y%m%d_%H%M%S)
```

```bash
gtimeout 15 git tag -a build-$(date +%Y%m%d-%H%M)-g$(git rev-parse --short HEAD) -m "Automated build tag"
```

15. Merge agent branch with clear history (no fast-forward)

```bash
gtimeout 30 git merge "$AGENT_BRANCH_REF" --no-ff -m "Merge agent changes after validation"
```

16. Post-merge validation (allows longer timeout)

```bash
gtimeout 600 _dev/tests/run_tests.sh --all --post-merge > .tmp/post_merge_tests.log
```

```bash
gtimeout 60 diff .tmp/baseline_tests.log .tmp/post_merge_tests.log > .tmp/post_merge_diff.log
```

17. Advance environment tags (optional, if you use env/dev tags)

```bash
gtimeout 15 git tag -f env/dev-prev $(git rev-parse env/dev 2>/dev/null || echo HEAD)
```

```bash
gtimeout 15 git tag -f env/dev $(git rev-parse HEAD)
```

```bash
gtimeout 15 git push origin env/dev env/dev-prev
```

18. Clean up isolated test branches (only if merge succeeded)

```bash
# Safer approach: list first, then delete explicitly (avoid command-substitution bulk deletes)
gtimeout 10 git branch --list "test-agent-merge-*"
# Then delete ONE at a time (only if you're sure):
# gtimeout 15 git branch -d test-agent-merge-YYYYMMDD_HHMMSS
```

18a. Authorization check before pushing to protected branches

```bash
# Check if target branch is protected and requires authorization
if [ "$TARGET_BRANCH" = "main" ] || [ "$TARGET_BRANCH" = "master" ]; then
  # Check if authorization was pre-configured via environment variable
  if [ "${USER_AUTHORIZED_BYPASS:-false}" != "true" ]; then
    echo ""
    echo "⚠️  AUTHORIZATION REQUIRED: About to push directly to $TARGET_BRANCH"
    echo "This requires explicit user authorization per rule 4_20_branch_protection_bypass_authorization"
    echo ""
    echo "To authorize this operation, you MUST:"
    echo "  1. Verify the changes are safe."
    echo "  2. Run export USER_AUTHORIZED_BYPASS=true after explicit authorization from the user 'I AUTHORIZE YOU AGENT ID TO PERFORME THE  {bypass}' and re-run this command."
    echo ""
    echo "❌ Execution paused. Waiting for authorization."
    exit 1
  else
    echo "✅ Pre-authorized via USER_AUTHORIZED_BYPASS environment variable"
  fi
fi
```

19. Push target branch and tags

```bash
gtimeout 15 git push origin "$TARGET_BRANCH" || {
  PUSH_ERROR=$?
  if [ "$PUSH_ERROR" -ne 0 ]; then
    # Check if error is due to branch protection
    if git push origin "$TARGET_BRANCH" 2>&1 | grep -q "protected branch\|GH006\|branch protection"; then
      echo ""
      echo "⚠️  BRANCH PROTECTION BLOCKED: Direct push to $TARGET_BRANCH was blocked"
      echo ""
      echo "To proceed with a PR workflow, explicit authorization is required to:"
      echo "  1. Create a PR from $AGENT_BRANCH to $TARGET_BRANCH"
      echo "  2. Merge the PR using admin privileges (--admin flag)"
      echo "  3. Temporarily disable 'enforce_admins' branch protection setting (if needed)"
      echo ""
      echo "⚠️  CRITICAL: Per rule 4_20_branch_protection_bypass_authorization, you MUST explicitly authorize:"
      echo "  - Which specific rules are being bypassed"
      echo "  - Admin merge via PR"
      echo ""
      if [ "${USER_AUTHORIZED_BYPASS:-false}" != "true" ]; then
        echo "❌ Authorization not provided. Stopping merge process."
        echo ""
        echo "To authorize the PR Admin Merge workflow:"
        echo "  Run export USER_AUTHORIZED_BYPASS=true after explicit authorization from the user 'I AUTHORIZE YOU AGENT ID TO PERFORME THE  {bypass}' and re-run this command."
        exit 1
      else
        echo "✅ Pre-authorized via USER_AUTHORIZED_BYPASS environment variable"
      fi

      echo ""
      echo "⚠️  NOTE: The agent should now STOP and request explicit user guidance on:"
      echo "  - Creating the PR (or use existing PR if one exists)"
      echo "  - Merging with admin privileges"
      echo ""
      echo "Preferred PR path (when a PR exists):"
      echo "  - Merge and delete the remote branch automatically:"
      echo "      gtimeout 60 gh pr merge <PR_NUMBER> --merge --delete-branch"
      echo "  - If admin bypass is required AND authorized:"
      echo "      gtimeout 60 gh pr merge <PR_NUMBER> --merge --admin --delete-branch"
      echo ""
      echo "Do NOT proceed autonomously. Follow the authorization protocol in"
      echo "4_20_branch_protection_bypass_authorization.mdc: PAUSE, CLARIFY, IDENTIFY, CONFIRM"
      exit 1
    else
      # Other push error - re-raise it
      exit $PUSH_ERROR
    fi
  fi
}
```

```bash
gtimeout 15 git push origin --tags
```

20. 🧹 Cleanup policy & safe defaults (avoid “pending cleanup”)

Historically this command left cleanup “pending” because:
- **Safety**: local backup branches are immediate rollback points if CI/deployments regress.
- **Permissions**: remote branch deletion can fail due to branch protection / missing rights.
- **Policy**: destructive remote mutations require explicit authorization.

To improve this, `/merg_merge` uses `CLEANUP_MODE`:
- `standard` (default): delete the **local** backup branch once validation + push succeeded.
- `conservative`: keep backup/deprecated branches for 1–7 days.
- `aggressive`: require remote cleanup; otherwise do not mark the merge “complete”.

### 20a. Default local cleanup (automatic in `standard` + `aggressive`)

```bash
echo "=== Cleanup policy ==="
echo "CLEANUP_MODE=$CLEANUP_MODE"

if [ -z "${BACKUP_BRANCH:-}" ] && [ -f .tmp/pre_merge_backup_branch.txt ]; then
  BACKUP_BRANCH=$(cat .tmp/pre_merge_backup_branch.txt 2>/dev/null || echo "")
fi
echo "Backup branch: ${BACKUP_BRANCH:-<not set>}"

if [ "$CLEANUP_MODE" != "conservative" ]; then
  if [ -n "${BACKUP_BRANCH:-}" ] && gtimeout 5 git show-ref --verify --quiet "refs/heads/$BACKUP_BRANCH"; then
    echo "Deleting local backup branch: $BACKUP_BRANCH"
    gtimeout 10 git branch -D "$BACKUP_BRANCH"
  else
    echo "No local backup branch to delete (or already deleted)."
  fi
else
  echo "Conservative mode: keeping local backup branches for 1–7 days."
  gtimeout 10 git branch --list "backup-pre-merge-*"
fi
```

### 20b. Remote branch cleanup (prefer PR merge --delete-branch when PR exists)

**Authorization reminder (repeat here to prevent “agent forgot” errors)**:

Remote branch mutation/deletion is destructive.

**The user does NOT need to authorize multiple times.**

The AI must STOP unless it has already received and recorded an official explicit approval from the user for the specific destructive action (check the conversation/log before proceeding):
- `{bypass}=DEPRECATE_REMOTE_AGENT_BRANCH` (for creating `deprecated-$AGENT_BRANCH`)
- `{bypass}=DELETE_REMOTE_AGENT_BRANCH` (for deleting `$AGENT_BRANCH` on origin)

If explicit approval has not yet been received, the AI must request it. After the user provides it, the AI should proceed by following this exact instruction:

> "Run export USER_AUTHORIZED_BYPASS=true after explicit authorization from the user 'I AUTHORIZE YOU AGENT ID TO PERFORME THE  {bypass}' and re-run this command."

**Preferred path (when a PR exists and is open)**: merge via PR and let GitHub delete the branch — **but only after the stack-base check**.

```bash
# Reuse the PR discovery output from step 6a (if present)
PR_NUMBER=$(cat .tmp/${AGENT_BRANCH}_pr_number.txt 2>/dev/null || echo "")
if [ -n "$PR_NUMBER" ]; then
  echo "Found PR #$PR_NUMBER for head=$AGENT_BRANCH"

  PR_STATE=$(gtimeout 10 gh pr view "$PR_NUMBER" --json state --jq .state 2>/dev/null || echo "MISSING")
  if [ "$PR_STATE" = "MERGED" ]; then
    echo "Authorization stale: PR #$PR_NUMBER is already merged; skip merge and continue with cleanup/sync."
    exit 0
  fi
  if [ "$PR_STATE" = "CLOSED" ]; then
    echo "Authorization stale: PR #$PR_NUMBER is already closed; do not reuse the old merge authorization."
    exit 1
  fi
  if [ "$PR_STATE" = "MISSING" ]; then
    echo "Authorization stale: PR #$PR_NUMBER no longer resolves on GitHub; refresh branch/PR state before continuing."
    exit 1
  fi

  # MANDATORY: detect dependent PRs before deciding the merge flag.
  # See the "Stacked-PR awareness" section near the top of this command.
  HEAD_BRANCH=$(gtimeout 10 gh pr view "$PR_NUMBER" --json headRefName --jq .headRefName)
  DEPENDENT_COUNT=$(gtimeout 10 gh pr list --state open --base "$HEAD_BRANCH" --json number --jq 'length')

  if [ "$DEPENDENT_COUNT" -gt 0 ]; then
    echo "⚠️  STACK BASE detected ($DEPENDENT_COUNT dependent PR(s) open against $HEAD_BRANCH)."
    echo "    Refusing to pass --delete-branch. Follow the 'Stack-base merge sequence'"
    echo "    in the Stacked-PR awareness section: merge without --delete-branch,"
    echo "    retarget every child onto main with 'gh pr edit <child> --base main',"
    echo "    VERIFY each child's new base, THEN delete the branch."
    gtimeout 60 gh pr merge "$PR_NUMBER" --merge      # NO --delete-branch
    # If admin bypass is required AND authorized:
    # gtimeout 60 gh pr merge "$PR_NUMBER" --merge --admin
    echo "✅ Base PR merged. Now run the retarget loop, then 'git push origin --delete \"$HEAD_BRANCH\"'."
  else
    echo "Leaf PR: safe to merge and delete the branch in one step."
    gtimeout 60 gh pr merge "$PR_NUMBER" --merge --delete-branch
    # If admin bypass is required AND authorized:
    # gtimeout 60 gh pr merge "$PR_NUMBER" --merge --admin --delete-branch
  fi
fi
```

```bash
gtimeout 15 git push origin "$AGENT_BRANCH:refs/heads/deprecated-$AGENT_BRANCH"
```

```bash
gtimeout 15 git push origin --delete "$AGENT_BRANCH"
```

**Safety guard before remote deletion (required)**:

```bash
# Only delete a remote branch if its tip is already included in origin/$TARGET_BRANCH
REMOTE_AGENT_SHA=$(gtimeout 10 git rev-parse "origin/$AGENT_BRANCH" 2>/dev/null || echo "")
if [ -n "$REMOTE_AGENT_SHA" ]; then
  if gtimeout 10 git merge-base --is-ancestor "$REMOTE_AGENT_SHA" "origin/$TARGET_BRANCH"; then
    echo "✅ Remote $AGENT_BRANCH is merged into origin/$TARGET_BRANCH"
  else
    echo "❌ Refusing remote delete: origin/$AGENT_BRANCH is NOT merged into origin/$TARGET_BRANCH"
    echo "Use DEPRECATE_REMOTE_AGENT_BRANCH instead, or investigate divergence."
    exit 1
  fi
else
  echo "ℹ️  No origin/$AGENT_BRANCH found (already deleted or never pushed)."
fi
```

20c. Restore and reintegrate the pre-merge stash (MANDATORY if a stash was created) — **BLOCKING GATE**

**CRITICAL**: Merge is **NOT complete** while `PRE_MERGE_STASH_REF` exists in `git stash list` unless one of:
- `STASH_RESTORED` logged to `logs/git_sync_operations.log` for that ref, OR
- `STASH_KEPT ref=... reason=<user-approved>` logged with explicit user waiver.

If the stash was only a temporary safety backup and the final post-merge branch state already supersedes it, do not leave it behind indefinitely. Save the patch backup, inspect the hunks, confirm the current branch already contains the intended end state, then drop the stash and log the disposition instead of treating "stash exists" as automatically unresolved.

Do not run Step 21 "MERGE COMPLETE" banner until this gate passes. **Prohibited**: `git stash drop` in the same merge session without Step 20c evidence.

```bash
# Confirm whether the recorded stash ref still exists
if [ -n "$PRE_MERGE_STASH_REF" ] && gtimeout 10 git stash list | grep -F "$PRE_MERGE_STASH_REF" >/dev/null 2>&1; then
  echo "✅ Found pre-merge stash: $PRE_MERGE_STASH_REF"
else
  echo "ℹ️  No recorded pre-merge stash to restore (or it was already handled)."
fi
```

```bash
# If present: inspect, then merge changes back safely (interactive patch restore)
if [ -n "$PRE_MERGE_STASH_REF" ] && gtimeout 10 git stash list | grep -F "$PRE_MERGE_STASH_REF" >/dev/null 2>&1; then
  echo "=== Pre-merge stash contents ==="
  gtimeout 15 git stash show --stat "$PRE_MERGE_STASH_REF"
  echo ""
  echo "=== Interactive reintegration (merge, do NOT overwrite) ==="
  gtimeout 30 git restore -p --source="$PRE_MERGE_STASH_REF" -- .
  echo ""
  echo "=== Verify working tree after reintegration ==="
  gtimeout 10 git status --short
fi
```

```bash
# Drop the stash ONLY after you confirm it is fully handled
if [ -n "$PRE_MERGE_STASH_REF" ] && gtimeout 10 git stash list | grep -F "$PRE_MERGE_STASH_REF" >/dev/null 2>&1; then
  echo "If (and only if) you have reintegrated everything needed, drop the pre-merge stash:"
  echo "  gtimeout 5 git stash drop \"$PRE_MERGE_STASH_REF\""
  echo ""
  echo "Authorization reminder:"
  echo "  Run export USER_AUTHORIZED_BYPASS=true after explicit authorization from the user 'I AUTHORIZE YOU AGENT ID TO PERFORME THE  {bypass}' and re-run this command."
  echo "  Use {bypass}=DROP_PRE_MERGE_STASH_${PRE_MERGE_STASH_REF}"
  echo ""
  echo "After reintegration, log:"
  echo "  echo \"\$(date -u +%Y-%m-%dT%H:%M:%SZ) STASH_RESTORED ref=$PRE_MERGE_STASH_REF method=apply|pop\" >> logs/git_sync_operations.log"
fi
```

```bash
# BLOCKING: refuse merge-complete if pre-merge stash still exists without audit log
if [ -n "$PRE_MERGE_STASH_REF" ] && gtimeout 10 git stash list | grep -F "$PRE_MERGE_STASH_REF" >/dev/null 2>&1; then
  if ! grep -q "STASH_RESTORED ref=$PRE_MERGE_STASH_REF\\|STASH_KEPT ref=$PRE_MERGE_STASH_REF" logs/git_sync_operations.log 2>/dev/null; then
    echo "❌ BLOCKED: Pre-merge stash $PRE_MERGE_STASH_REF still exists without STASH_RESTORED or STASH_KEPT log."
    echo "   Complete Step 20c reintegration or obtain user waiver before Step 21."
    exit 1
  fi
fi
```

21. 🧹 MANDATORY: Final Cleanup Verification Checklist

**AI agents MUST complete ALL of the following before considering merge done. No exceptions.**

```bash
# ✅ STEP 1: Verify no test branches left locally
echo "=== Checking for leftover test branches ==="
gtimeout 10 git branch --list "test-agent-merge-*" | grep . && { echo "❌ ERROR: Test branches still exist!"; exit 1; } || echo "✅ No test branches"
```

```bash
# ✅ STEP 2: Verify no backup branches left locally
echo "=== Checking for leftover backup branches ==="
gtimeout 10 git branch --list "backup-pre-merge-*" | grep . && { echo "⚠️  WARNING: Backup branches exist (expected if using conservative cleanup)"; } || echo "✅ No backup branches"
```

```bash
# ✅ STEP 3: Verify agent branch is deleted remotely
echo "=== Checking if agent branch was cleaned remotely ==="
gtimeout 10 git ls-remote origin "$AGENT_BRANCH" | grep . && { echo "⚠️  WARNING: Agent branch still exists on remote (may be intentional)"; } || echo "✅ Agent branch cleaned remotely"
```

```bash
# ✅ STEP 4: Verify working directory is absolutely clean
echo "=== Final working directory check ==="
gtimeout 10 git status --porcelain | grep . && { echo "❌ ERROR: Working directory not clean!"; exit 1; } || echo "✅ Working directory clean"
```

```bash
# ✅ STEP 5: List all merge-related artifacts for audit
echo "=== Merge Artifacts Summary (for audit trail) ==="
echo "Local branches with 'backup' or 'pre-merge':"
gtimeout 10 git branch -l | grep -E "(backup|pre-merge)" || echo "  (none)"
echo ""
echo "Remote branches with 'deprecated':"
gtimeout 10 git branch -r | grep deprecated || echo "  (none)"
echo ""
echo "Recent merge checkpoint tags:"
gtimeout 10 git tag -l 'pre-merge-checkpoint-*' | tail -3 || echo "  (none)"
echo ""
echo "Recent build tags:"
gtimeout 10 git tag -l 'build-*' | tail -3 || echo "  (none)"
```

```bash
# ✅ STEP 6: Verify main branch is properly synced
echo "=== Target branch sync check ==="
LOCAL_HASH=$(git rev-parse "$TARGET_BRANCH")
REMOTE_HASH=$(git rev-parse "origin/$TARGET_BRANCH")
if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
  echo "✅ Local $TARGET_BRANCH matches remote"
else
  echo "❌ ERROR: Local and remote $TARGET_BRANCH differ! This should not happen."
  exit 1
fi
```

```bash
# ✅ STEP 7: Check for uncommitted work one final time
echo "=== Uncommitted work check ==="
STASH_COUNT=$(gtimeout 10 git stash list | wc -l)
if [ "$STASH_COUNT" -gt 0 ]; then
  echo "❌ ERROR: $STASH_COUNT stash(es) remain after Step 20c gate. Review: git stash list"
  exit 1
else
  echo "✅ No stashes"
fi
```

```bash
# ✅ STEP 8: Print merge summary
echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ MERGE COMPLETE & VERIFIED                         ║"
echo "╠════════════════════════════════════════════════════════════════════════╣"
echo "║ Agent Branch: $AGENT_BRANCH"
echo "║ Target Branch: $TARGET_BRANCH ($(git rev-parse --short $TARGET_BRANCH))"
echo "║ Merge Date: $(date)"
echo "║                                                                         ║"
echo "║ Post-Merge Actions Completed:                                          ║"
echo "║   ✅ Test branches cleaned up                                          ║"
echo "║   ✅ Working directory pristine                                        ║"
echo "║   ✅ Target branch synchronized with remote                           ║"
echo "║   ✅ All safety checks passed                                         ║"
echo "║                                                                         ║"
echo "║ Remaining Artifacts (for reference):                                   ║"
echo "║   - Backup branches: Delete after 1-7 days                            ║"
echo "║   - Deprecated remote branch: Delete after 1-7 days                   ║"
echo "║   - Checkpoint tags: Delete after 30 days                             ║"
echo "║   - Environment tags (env/dev*): Keep for deployment tracking         ║"
echo "║                                                                         ║"
echo "║ Next Steps:                                                             ║"
echo "║   1. Verify tests pass in CI/CD                                       ║"
echo "║   2. Monitor deployments                                              ║"
echo "║   3. Schedule cleanup of temporary artifacts (see above)              ║"
echo "║                                                                         ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
```

## ⚠️ IMPORTANT: Understanding Post-Merge Artifacts

### What Gets Left Behind

The merge process creates several **safety artifacts** that are NOT automatically cleaned up. You must actively manage them:

### Local Artifacts (on your machine)

| Artifact            | Pattern              | Purpose                   | Recommendation                        |
| ------------------- | -------------------- | ------------------------- | ------------------------------------- |
| **Backup branches** | `backup-pre-merge-*` | Emergency rollback point  | Delete after confirming merge success |
| **Test branches**   | `test-agent-merge-*` | Isolation testing         | Already deleted in step 18            |
| **Stash entry**     | Referenced in step 4 | Saved uncommitted changes | Restore/delete as needed              |

### Remote Artifacts (on GitHub)

| Artifact              | Pattern                        | Purpose                        | Cleanup Strategy                                |
| --------------------- | ------------------------------ | ------------------------------ | ----------------------------------------------- |
| **Deprecated branch** | `deprecated-${AGENT_BRANCH}`   | Preserved copy of agent branch | Delete after confirming remote state (1-7 days) |
| **Checkpoint tags**   | `pre-merge-checkpoint-*`       | Emergency rollback points      | Keep for 30 days, then delete                   |
| **Build tags**        | `build-YYYYMMDD-HHMM-gXXXXXXX` | Automated build markers        | Manage per your release cycle                   |
| **Env tags**          | `env/dev`, `env/dev-prev`      | Environment snapshots          | Manage per your deployment policy               |

### Why These Artifacts Exist

These artifacts serve critical safety functions:

- **Backups**: Allows rollback if post-merge issues arise
- **Checkpoints**: Enables recovery from merge failures
- **Deprecated branches**: Preserves branch history for reference/audit
- **Tags**: Track merge points and build history

### Cleanup Strategy Options

**Option A (Conservative - Recommended for First Merges)**

```bash
# Wait 7 days before cleanup
# This allows time to detect any issues
# Run at end of retention period:
gtimeout 10 git branch --list "backup-pre-merge-*"
# Delete ONE at a time (only if you're sure):
# gtimeout 10 git branch -D backup-pre-merge-YYYYMMDD_HHMMSS
gtimeout 10 git push origin --delete deprecated-${AGENT_BRANCH}
gtimeout 10 git tag -l 'pre-merge-checkpoint-*'
# Delete ONE tag at a time (after verifying age/need):
# gtimeout 10 git tag -d pre-merge-checkpoint-YYYYMMDD_HHMMSS
# gtimeout 15 git push origin --delete pre-merge-checkpoint-YYYYMMDD_HHMMSS
```

**Option B (Standard - Recommended for Regular Operations)**

```bash
# Delete local artifacts immediately, keep remote for 30 days
# Delete immediately after tests pass
gtimeout 10 git branch --list "backup-pre-merge-*"
# Delete ONE at a time (only if you're sure):
# gtimeout 10 git branch -D backup-pre-merge-YYYYMMDD_HHMMSS

# Delete deprecated branch after confirming state
gtimeout 10 git push origin --delete deprecated-${AGENT_BRANCH}

# Keep checkpoint tags for 30 days, then delete manually
# Set a calendar reminder to delete these tags
```

**Option C (Aggressive - For Confident Teams)**

```bash
# Clean up everything immediately after step 19 completes
# Only use if you have high confidence and good monitoring

# Delete local backup branch
gtimeout 10 git branch --list "backup-pre-merge-*"
# Delete ONE at a time (only if you're sure):
# gtimeout 10 git branch -D backup-pre-merge-YYYYMMDD_HHMMSS

# Delete remote deprecated branch
gtimeout 10 git push origin --delete deprecated-${AGENT_BRANCH}

# Keep checkpoints - only delete after 30 days
# Do NOT delete env/* tags - these track deployments
```

### Manual Verification Before Cleanup

Always verify before deleting anything:

```bash
# List local artifacts that could be cleaned
echo "=== Local branches to clean ==="
gtimeout 10 git branch | grep -E "(backup-pre-merge|test-agent-merge)" || echo "None found"

# List remote artifacts
echo "=== Remote branches to clean ==="
gtimeout 10 git branch -r | grep -E "(deprecated|backup)" || echo "None found"

# List cleanup-eligible tags
echo "=== Tags created during this merge ==="
gtimeout 10 git tag -l | grep -E "(pre-merge-checkpoint|build)" | head -5

# Calculate tag age (macOS)
echo "=== Tag ages ==="
for tag in $(git tag -l 'pre-merge-checkpoint-*' | tail -5); do
  date_str=$(echo "$tag" | sed 's/pre-merge-checkpoint-//')
  year=${date_str:0:4}
  month=${date_str:4:2}
  day=${date_str:6:2}
  echo "$tag: $year-$month-$day"
done
```

### Common Cleanup Issues

**Issue**: Cannot delete local branch (branch not fully merged)

```bash
# Safer approach: list first, then delete explicitly (avoid wildcard force-deletes)
gtimeout 10 git branch --list "backup-pre-merge-*"
# Then delete ONE at a time (only if you're sure):
# gtimeout 10 git branch -D backup-pre-merge-YYYYMMDD_HHMMSS
```

**Issue**: Remote branch deletion permission denied

```bash
# Solution: Check GitHub permissions, may need admin to delete
# Or ask repo maintainer to delete the deprecated branch
```

**Issue**: Too many tags accumulated

```bash
# Safer approach: list candidates, then delete explicitly (avoid command-substitution mass deletes)
gtimeout 10 git tag -l 'pre-merge-checkpoint-*'
# Delete ONE tag at a time (after verifying age/need):
# gtimeout 10 git tag -d pre-merge-checkpoint-YYYYMMDD_HHMMSS
# gtimeout 15 git push origin --delete pre-merge-checkpoint-YYYYMMDD_HHMMSS
```

### Documentation References

- See `mini_prompt/lv2/agent_branch_merge_mini_prompt.md` for extended cleanup strategy
- See `standards/git/branch_convention.md` for branch naming conventions
- See `guides/cursor_commands_sync.md` for distribution of merge command updates

## Notes

- **Branch Detection**: The command now automatically detects whether a branch exists locally or remotely and uses the appropriate reference.
- **Smart Branch Selection**: When both local and remote versions exist, the command compares their last commit timestamps and automatically uses the branch that was updated most recently. This reduces merge conflicts by prioritizing the branch with the latest changes.
- **Comprehensive Branch Discovery**: All branches (local and remote) are discovered and fetched before merge operations to ensure accurate branch state.
- Conflicts must be resolved manually following the “Enhanced Manual Conflict Resolution Process” in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md`
- Never use destructive commands (`git reset --hard`, `--no-verify`, force-push) unless explicitly authorized by policy, only after attempting to fix hook/verification errors first, and only after confirming no concurrent AI session is actively mutating the repo/worktree.
- Timeouts >20s are used only for tests; keep non-test operations ≤15s
- Execute each command individually; do not chain with `&&`
- Use this guide alongside the mini prompt for full zero-trust validation and rollback strategy

---

**Last updated**: 2026-06-09 (v1.12.0 - Stack-aware merge: detect dependent PRs, defer `--delete-branch` for stack bases, add rebase-before-replace guard, document auto-close recovery)
**Previous**: 2026-01-29 (v1.11.0 - Add cleanup policy + prefer PR merge `--delete-branch` when PR exists)
**Previous**: 2026-01-28 (v1.9.0 - Add explicit divergence resolution workflow 12b-12e before completing merge)
**Previous**: 2026-01-17 (v1.8.0 - Added explicit authorization checks and agent-safe bypass workflow)
