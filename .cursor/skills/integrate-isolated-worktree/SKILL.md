---
name: integrate-isolated-worktree
description: >-
  Closes an isolated git worktree end-to-end into main: gap-analyze the
  conversation's initial scope, execute remaining in-scope work, update and
  finish the plan (docs/plans or _dev/docs/plans by repo type), park out-of-scope
  items in backlog, open/merge/close a PR, verify, then delete the worktree.
  Use when finishing worktree-isolated feature work, integrating a concurrent
  agent branch into main, or when the user asks to merge/close/cleanup a
  worktree without losing multi-agent context.
---

# Integrate Isolated Worktree

## Overview

Turn a finished (or nearly finished) **isolated worktree** into a clean `main`
integration: scope gap → execute → plan hygiene → PR → merge → verify → delete
worktree.

**Core principle:** Nothing leaves the worktree until it is either (a) committed
on a PR that lands on `main`, (b) parked as a backlog plan, or (c) explicitly
waived by the user. Uncommitted / untracked / other-agent WIP must never be
silently discarded.

**Announce at start:** "I'm using the integrate-isolated-worktree skill to land
this worktree on main."

**Pairs with:** `using-git-worktrees` (create), `finishing-a-development-branch`
(choose path), `verification-before-completion`, `/gscv_git_sync_conversation`,
`/chkp_check_pending`, `/arch_archive`, `/merg_merge` / `/gbyp_git_protection_bypass` (slash invocation authorizes Scenario A writes for the named PR).

**SSoT (concurrency):** `guides/collaboration/multi_agent_worktree_workflow.md`

## When to use

- User asks to integrate / merge / close / cleanup an isolated worktree
- Implementation in a worktree is done (or almost done) and must reach `main`
- Concurrent-agent session needs a deterministic land-and-delete path
- Prefer this over `finishing-a-development-branch` when the decision is already
  "PR → merge → delete worktree" (no option menu)

## Hard stops (do not proceed)

Stop and report if any of these hold:

1. Current directory is **not** the worktree being integrated (or path is ambiguous)
2. Another agent owns this tree (you did not create it) — never `reset`/`stash`/`clean`
3. Unrelated dirty files belong to **other conversations/agents** (route via
   `guides/collaboration/pending_to_merge_worktree.md` + `/chkp_check_pending`)
4. Tests/lints required by the repo fail and cannot be fixed in-scope
5. Merge conflicts with `main` that need human policy decisions
6. User has not authorized push/merge when branch protection or org policy requires it

## Progress checklist

Copy and tick as you go:

```text
Integrate Isolated Worktree
- [ ] 0. Context freeze (identity + inventory)
- [ ] 1. Gap analysis vs initial conversation scope
- [ ] 2. Execute remaining in-scope work
- [ ] 3. Resolve plans root + update plan
- [ ] 4. Park out-of-scope / extras → backlog
- [ ] 5. Move completed plan → finished
- [ ] 6. Commit conversation scope + push branch
- [ ] 7. Open PR → merge (7b bypass pre-check before any `/gbyp`) → MERGED
- [ ] 8. Verify on main (git + local gates only; no redeploy)
- [ ] 9. Delete worktree + prune + final report
```

---

## Step 0 — Context freeze

Run **inside the worktree** being integrated:

```bash
pwd
git rev-parse --show-toplevel
git branch --show-current
git status -sb
git worktree list
git stash list
git log --oneline -5
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
```

Record:

| Field | Value |
|-------|-------|
| Worktree path | |
| Branch | |
| Base (`main`/`master`) | |
| Primary checkout path | |
| Sibling worktrees (other agents) | |
| Dirty files (this conversation) | |
| Dirty files (other / unknown) | |
| Active plan path (if any) | |

**Never** `checkout` / `reset` / `stash -u` / `clean` in a tree you did not create.
If dirty files are not yours → `/chkp_check_pending` Step 1.10 path; do not absorb them.

Anti-loss extras for this step: see [reference.md](reference.md#anti-loss-gates).

---

## Step 1 — Gap analysis (initial scope)

Rebuild the **initial conversation scope** from evidence, not memory:

1. User's first request + any explicit acceptance criteria
2. Active plan checkboxes / success criteria (if a plan exists)
3. Files created/edited in this conversation (tool-call history)
4. Commits already on the branch (`git log main..HEAD`)

Produce a short gap table:

| Item | Status | Action |
|------|--------|--------|
| … | done / missing / out-of-scope | execute / skip / backlog |

Rules:

- **In-scope + missing** → Step 2
- **Done** → keep as evidence
- **Out-of-scope / nice-to-have / discovered debt** → Step 4 (backlog), do **not** block merge
- If the initial scope is unclear, stop and ask **one** clarifying question — do not invent scope

---

## Step 2 — Execute remaining in-scope work

Execute only gap-table rows marked **execute**. Stay inside this worktree.

After each meaningful chunk:

```bash
# conversation-scoped commit preferred
# invoke /gscv_git_sync_conversation OR commit with an explicit path list
git status --porcelain
```

Do not claim "feature complete" without git evidence
(`verification-before-completion`).

---

## Step 3 — Resolve plans root + update plan

```bash
REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
# Strip worktree suffix if present (e.g. astral-ddf-wt-foo → astral-ddf)
REPO_BASE="${REPO_NAME%%-wt-*}"
if [[ "$REPO_BASE" =~ -fera$ ]] || [[ "$REPO_NAME" =~ -fera$ ]]; then
  PLANS_DIR="_dev/docs/plans"
else
  PLANS_DIR="docs/plans"
fi
# Prefer existing tree if only one is present
[[ -d "$PLANS_DIR" ]] || { [[ -d "_dev/docs/plans" ]] && PLANS_DIR="_dev/docs/plans"; }
[[ -d "$PLANS_DIR" ]] || { [[ -d "docs/plans" ]] && PLANS_DIR="docs/plans"; }
echo "PLANS_DIR=$PLANS_DIR"
```

Update the active plan for this work:

- Mark completed tasks `[x]`
- Add a **Git evidence** section: branch, commit hashes, PR URL (fill after Step 7)
- Record residual risks / follow-ups that stay in-scope notes (not backlog)

If no plan exists but the session was plan-driven or multi-hour, create a minimal
plan under `$PLANS_DIR/active/` **before** finishing so the archive trail exists.
Skip plan creation for trivial single-commit chores when the user did not use plans.

---

## Step 4 — Park out-of-scope → backlog

For every gap-table row marked **backlog** (and any discovered extras):

1. Create or append `$PLANS_DIR/backlog/<slug>_YYYY-MM-DD.md`
2. Include: origin conversation/worktree/branch, why deferred, acceptance sketch
3. Link that backlog file from the finishing plan ("Deferred")

Template:

```markdown
# Backlog: <title>

**Origin:** worktree `<path>` / branch `<branch>` / conversation `<id or unknown>`
**Deferred on:** <UTC date>
**Why out of scope:** <one line>

## Items
- [ ] …

## Notes
…
```

Do **not** leave out-of-scope work only in chat history.

---

## Step 5 — Move plan → finished

When in-scope work is done and evidenced in git (local commits at minimum):

```bash
mkdir -p "$PLANS_DIR/finished"
git mv "$PLANS_DIR/active/<plan>.md" "$PLANS_DIR/finished/<plan>.md"
```

Status vocabulary (from `guides/agent_session_closure.md`):

| Condition | Plan status label |
|-----------|-------------------|
| All deliverables in git (pushed) | `Finished` |
| In git locally only | `Finished (local only — NOT in remote)` |
| User waived commit | `Finished (local only — user waiver)` + WIP handoff |

Prefer `/arch_archive` when the repo already uses that command for plan moves.

---

## Step 6 — Commit + push

1. Prefer `/gscv_git_sync_conversation` (conversation-scoped; leaves other dirty files alone)
2. Else commit with an **explicit path list** of this conversation's files
3. Push the feature branch:

```bash
git push -u origin HEAD
```

Refuse to include secrets, credential files, or other-agent paths.

---

## Step 7 — PR → merge → closed

```bash
# Create PR if none exists for this branch
gh pr view --json url,state,number 2>/dev/null || \
  gh pr create --base main --title "<concise why>" --body "$(cat <<'EOF'
## Summary
- <what landed from this worktree>
- Plan: `<finished plan path>` (backlog: `<backlog path or n/a>`)

## Test plan
- [ ] <verification commands run>

## Worktree
- Path: `<worktree path>`
- Branch: `<branch>`
EOF
)"
```

### 7a. Try a normal merge first

```bash
gh pr merge --merge --delete-branch
```

If that succeeds → skip 7b/7c and go to terminal-state check below.

### 7b. If merge is blocked — pre-check review-bypass rights (read-only)

**Do not** suggest or run `/gbyp` until this pre-check finishes. Admin role is
**not** the same as review-bypass rights (especially when `enforce_admins: true`).

Run the read-only posture check (same fields as `/gbyp` phases 1–3):

```bash
REPO_INFO=$(gh repo view --json owner,name,defaultBranchRef)
OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
REPO=$(echo "$REPO_INFO" | jq -r '.name')
BRANCH=$(echo "$REPO_INFO" | jq -r '.defaultBranchRef.name')
GITHUB_USERNAME=$(gh api user --jq .login)
mkdir -p .tmp
gh api "repos/$OWNER/$REPO/branches/$BRANCH/protection" > .tmp/current_protection.json

ENFORCE_ADMINS=$(jq -r '.enforce_admins.enabled // false' .tmp/current_protection.json)
REQUIRED_APPROVALS=$(jq -r '.required_pull_request_reviews.required_approving_review_count // 0' .tmp/current_protection.json)
REQUIRE_CODEOWNERS=$(jq -r '.required_pull_request_reviews.require_code_owner_reviews // false' .tmp/current_protection.json)
BYPASS_USERS_JSON=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.users[]? | (.login // .) ]' .tmp/current_protection.json)
USER_HAS_BYPASS=$(echo "$BYPASS_USERS_JSON" | jq -r --arg u "$GITHUB_USERNAME" 'if (index($u)) then "yes" else "no" end')

# Org rulesets cannot be bypassed by repo admins
gh api "repos/$OWNER/$REPO/rulesets" > .tmp/repo_rulesets.json 2>/dev/null || echo '[]' > .tmp/repo_rulesets.json
gh api "orgs/$OWNER/rulesets" > .tmp/org_rulesets.json 2>/dev/null || echo '[]' > .tmp/org_rulesets.json

echo "actor=$GITHUB_USERNAME enforce_admins=$ENFORCE_ADMINS approvals=$REQUIRED_APPROVALS codeowners=$REQUIRE_CODEOWNERS has_bypass=$USER_HAS_BYPASS"
echo "bypass_users=$BYPASS_USERS_JSON"
```

Decision table (report evidence to the user):

| Pre-check result | Next action |
|------------------|-------------|
| Required CI/status checks failing | Fix in this worktree; push; wait — **not** `/gbyp` for green CI |
| Org-level active rulesets block merge | Escalate to org owner; **do not** claim `/gbyp` can fix it |
| `USER_HAS_BYPASS=yes` and user authorizes admin merge | Suggest `/gbyp_git_protection_bypass` Scenario A for **this PR number** |
| `USER_HAS_BYPASS=no` but actor can be added to allowances and user authorizes | Suggest `/gbyp` Scenario A (phase 4 add-user + merge) for **this PR** |
| `USER_HAS_BYPASS=no` and no path to add allowances | Request human review / CODEOWNER — **do not** suggest `/gbyp` |
| CODEOWNERS required and actor is not a code owner / not on bypass list | Request CODEOWNER review — bypass cannot substitute unless listed |

### 7c. Suggest `/gbyp` only after 7b (slash invocation authorizes writes)

When the table says `/gbyp` is viable:

1. Name the **exact PR number** and say you will follow `/gbyp_git_protection_bypass` Scenario A.
2. Have the user invoke `/gbyp` / `/gbyp_git_protection_bypass` for that PR (or treat their slash attach in this turn as authorization). Do **not** invent a second `AUTHORIZE gbyp…` ritual after invocation when the PR target is unambiguous.
3. Run `/gbyp` Scenario A — announce then execute phases 4–7 in the same turn; restore `enforce_admins` per that command’s Phase 7. Force-merge / clearing required status checks still needs separate confirmation.
4. Do **not** invent a parallel bypass; do not skip the command’s restore/verify read-back.

Also prefer `_dev/docs/plans/template/agent_branch_merge_workflow_template.md` when the repo uses that enterprise merge/rollback template.

Ensure terminal state:

```bash
gh pr view --json state,mergedAt,url
# state must be MERGED (merged PRs are closed)
```

Update the finished plan with the PR URL + merge commit SHA.

---

## Step 8 — Verify

**Verify is git + local quality gates only.** It proves the work is on `main`
and the repo’s documented checks pass. It is **not** a deploy step.

**Forbidden in Step 8** (hard stop — do not run these as part of verify):

- Redeploy / deploy / rollout scripts (e.g. `infra/oci/scripts/redeploy.sh`)
- SSH to cloud VMs to pull/restart “to verify”
- Production / staging / pre-alpha / alpha environment mutations
- Any “smoke on the live URL” that changes remote state

If the user wants deploy after land, that is a **separate** authorized request
outside this skill (after Step 8 evidence is already green).

From the **primary checkout** (not the doomed worktree):

```bash
cd <primary-checkout>
git fetch origin
git checkout main
git pull --ff-only origin main
git log -1 --oneline
git merge-base --is-ancestor <feature-tip-or-merge-commit> HEAD && echo "OK: work on main"
```

Repo-specific gates (run what the repo documents):

```bash
# examples — pick the project's real commands
make test   # or npm test / pytest / …
make lint   # if applicable
```

Apply `verification-before-completion`: no success claim without fresh command output
+ git evidence.

Also confirm:

- Finished plan exists under `$PLANS_DIR/finished/`
- Backlog file exists if anything was deferred
- No stash created by this flow that still holds deliverables (`git stash list`)

---

## Step 9 — Mark `reap`, then delete worktree

Only after Step 8 passes. Third parties (and future agents) must be able to see
from the **directory name** that cleanup is safe. SSoT:
`standards/git/worktree_naming.md`.

```bash
cd <primary-checkout>
MERGED_SHA="$(git rev-parse origin/main)"   # or the merge commit from Step 7
WT_PATH="<worktree-path>"                  # often …-wt-live-<slug>

# 1) Rename live/park → reap + stamp status (enables third-party double-check)
WT_LC=""
for cand in _dev/scripts/git/worktree_lifecycle.sh scripts/git/worktree_lifecycle.sh; do
  [[ -x "$cand" ]] && WT_LC="$cand" && break
done
if [[ -n "$WT_LC" ]]; then
  # `mark` prints "OK: <new-path> → reap" and renames the directory when needed
  MARK_OUT=$(bash "$WT_LC" mark "$WT_PATH" reap \
    --merged-sha "$MERGED_SHA" --pr-url "<pr-url>")
  echo "$MARK_OUT"
  WT_PATH=$(echo "$MARK_OUT" | sed -n 's/^OK: \(.*\) → reap$/\1/p')
  [[ -n "$WT_PATH" ]] || { echo "ERROR: could not parse reap path from mark output"; exit 1; }
  bash "$WT_LC" check-reapable "$WT_PATH"
else
  echo "WARN: worktree_lifecycle.sh missing; apply standards/git/worktree_naming.md manually before remove"
fi

# 2) Remove only the reap path
git worktree list
git worktree remove "$WT_PATH"
# if remove fails because of leftover dirty files:
#   1) classify: yours vs other-agent
#   2) commit/park yours OR route others via pending-to-merge
#   3) never git clean -fd as first resort
#   4) never mark reap while dirty
git worktree prune
git worktree list
git branch -d <branch> 2>/dev/null || true   # local branch if still present
```

Final report to the user:

```text
Integrated worktree → main
- Branch: …
- PR: … (MERGED)
- Merge commit: …
- Plan finished: …
- Backlog: … | none
- Worktree marked reap then removed: …
- Verification: <commands + exit evidence>
```

---

## Anti-loss minimum (multi-agent)

Before any destructive step (`reset`, `clean`, `worktree remove`, `branch -D`):

1. `git status --porcelain` + classify every path (this conversation / other / ignore)
2. `git stash list` — recover or backup patches to `.tmp/stash_backups/` before drop
3. `git worktree list` — never remove a sibling agent's tree
4. Push or park: deliverables must be on `origin` or in `$PLANS_DIR/backlog/`
5. Other-agent WIP → pending-to-merge worktree, never your PR

Full gate list + recovery: [reference.md](reference.md)

## Integration

- Create: `using-git-worktrees`
- Choose path (options menu): `finishing-a-development-branch`
- Concurrency SSoT: `guides/collaboration/multi_agent_worktree_workflow.md`
- Naming / reap double-check: `standards/git/worktree_naming.md`
- Pending others: `guides/collaboration/pending_to_merge_worktree.md`
- Closure gates: `guides/agent_session_closure.md`
- Merge template: `_dev/docs/plans/template/agent_branch_merge_workflow_template.md`
- Blocked PR merge: `/gbyp_git_protection_bypass` after Step 7b pre-check (slash invocation authorizes Scenario A writes for the named PR)
