---
category: git
criticality: high
scope: all
---
# /gbyp_git_protection_bypass
<!-- COMMAND_ID: 023 -->
<!-- COMMAND_VERSION: 2.4.2 -->
<!-- COMMAND_TYPE: gb_git_protection_bypass -->

Admin-only command for bypassing branch protection in two scenarios: (A) a PR that is blocked from merging into main, and (B) a direct commit blocked from being pushed straight to main. Distinguishes Classic Branch Protection from GitHub Rulesets. Phases 1–3 are read-only and safe to run autonomously. All write phases require explicit user authorization. Phase 7 always performs a partial rollback by default and applies a full rollback to the original posture only when explicitly requested via `REVERT_PROTECTION=1`; otherwise user-scoped allowances are intentionally kept.

**Critical rule**: This command modifies branch protection settings. Read phases (1–3) are safe; write phases (4–6) require explicit user authorization for each step.

**Critical rule**: "Explicit user authorization" means the user confirms the *exact* command about to run, in the same turn — not a standing grant from earlier in the session, and never a shell variable the user exports in their own terminal. Guarded git operations invoked by this command (e.g. phase 10's direct push to `main`, gated by `GIT_AUTHORIZE_MAIN_PUSH` per `rules/dadosfera/4_24_destructive_command_authorization.md`) are checked inside the same shell process that runs the git command — a user-side `export` never reaches an agent's tool-invoked shell calls, and env vars set in one tool call do not persist into the next. Once authorized, set the variable and run the guarded command together, in the same tool invocation (e.g. `export GIT_AUTHORIZE_MAIN_PUSH=true && git push origin "$LOCAL_REF:$BRANCH"`). Never pre-set these variables speculatively "just in case" before asking, and re-ask per new category of destructive action rather than assuming one grant covers the rest of the session.

**Critical rule**: Admin role is NOT the same as bypass rights. With `enforce_admins: true`, even repository admins must be explicitly listed under `bypass_pull_request_allowances` to merge without approval.

**Critical rule**: GitHub forbids self-approval of PRs (`gh pr review --approve` on your own PR will always fail). Bypass is the only autonomous path when you are the sole admin.

**Critical rule**: If the branch is governed by Repository or Organization Rulesets (not classic protection), the classic `/branches/{branch}/protection` endpoints will silently no-op. Use `/repos/{owner}/{repo}/rulesets` and `/orgs/{org}/rulesets` instead.

**Critical rule**: Organization-level rulesets cannot be bypassed by repo admins. Only org owners (or users explicitly listed in the org ruleset bypass actors) can merge.

**Critical rule**: `require_code_owner_reviews: true` requires a CODEOWNER approval; a generic write-access approval will not satisfy it.

**Critical rule**: By default, Phase 7 performs a **partial** rollback: core protections like `enforce_admins`, `required_pull_request_reviews`, and disabled rulesets are restored, but user/direct-push allowances (`TARGET_USERNAME` / `DIRECT_PUSH_USERS`) remain. Use `REVERT_PROTECTION=1` only if you want a **full rollback** to the exact pre-command posture.

**Critical rule**: Direct push to a protected branch is a stronger violation of normal review hygiene than an admin PR merge. Prefer scenario A (PR + admin merge) whenever a PR is feasible. Scenario B (direct push bypass) is reserved for emergencies, repository bootstrapping, or one-off automation commits where opening a PR is impossible or actively harmful.

**Critical rule**: Removing `required_pull_request_reviews` (scenario B, phase 9) is a much wider relaxation than the bypass-list approach used in scenario A. While the requirement is removed, ANY user with push access can push directly to the branch. Keep the window between phase 9 and optional cleanup as short as possible when rollback is requested.

**Critical rule**: **Stacked-PR mode**: when scenario A is used to merge a PR that has open dependent PRs (i.e. it is the base of a stack), do NOT run Phase 7 between merges. Run Phase 7 ONCE, after the last PR in the stack has been merged. See `recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md` and the 'Stack-mode operation' section of this command.

**Critical rule**: A user's authorization to run this command against an already-enumerated set of PRs does NOT automatically extend to a PR the agent itself opened as a byproduct of that work (e.g. a stash-promotion PR, a docs-recovery PR, a review-nits followup PR) — even under a broad "finish everything" instruction that covers the known PR set. Name the byproduct PR by number/title and get separate, explicit merge authorization for it before running phase 6, rather than assuming the original grant covers it.

**Critical rule**: Before any authorized write phase that targets a specific PR, refresh that PR's live state. If it is already `MERGED`, `CLOSED`, or no longer resolvable, treat the prior authorization as stale/consumed and emit an explicit message; do not change protection or attempt an admin merge against a different or already-resolved target.

**Local Reference**: `commands/gbyp_git_protection_bypass.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/gbyp_git_protection_bypass.md`

Backlinks:
- rules/cursor/4_20_branch_protection_bypass_authorization.mdc
- rules/cursor/4_24_destructive_command_authorization.mdc
- guides/github/branch_protection_bypass_guide.md
- recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md

## When to Use

- When you need to check (read-only) the current bypass posture of a protected branch
- **Scenario A — blocked PR merge**: when you need to merge a PR you authored and you are the only repo admin (no second reviewer available)
- **Scenario A — blocked PR merge**: when `gh pr merge --admin` is failing with 'At least 1 approving review is required'
- **Scenario B — blocked direct push to main**: when `git push origin main` is rejected with `protected branch hook declined`, `Changes must be made through a pull request`, or `Required status check ... is expected`, AND opening a PR is not feasible (emergency hotfix, automated bootstrap commit, single-author repo)
- When you need to add or remove a user from the PR review bypass allowances
- When auditing who can bypass branch protection on a given branch

## When NOT to Use

- For normal development — always prefer getting a real review and a normal merge
- Without repository admin privileges (write phases will fail)
- On branches governed only by an Organization Ruleset where you are not an org owner (cannot be bypassed at the repo level — neither scenario)
- When CODEOWNERS approval is the binding constraint and you are not a CODEOWNER (bypass cannot substitute for code owner review unless you are also added to bypass)
- On repositories without any branch protection or rulesets configured (nothing to bypass)
- For scenario B: when a normal PR + admin merge (scenario A) is feasible. Scenario B widens the protection surface more than scenario A and should be the last resort.

## Command sequence (run in order)

### 1. Verify repository context, current user, and admin permission

```bash
set -e
mkdir -p .tmp logs

REPO_ROOT=$(gtimeout 5 git rev-parse --show-toplevel)
cd "$REPO_ROOT"

GITHUB_USERNAME=$(gtimeout 10 gh api user --jq .login)
REPO_INFO=$(gtimeout 10 gh repo view --json owner,name,defaultBranchRef)
OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
REPO=$(echo "$REPO_INFO" | jq -r '.name')
DEFAULT_BRANCH=$(echo "$REPO_INFO" | jq -r '.defaultBranchRef.name')
BRANCH="${BRANCH:-$DEFAULT_BRANCH}"

PERM=$(gtimeout 10 gh api "repos/$OWNER/$REPO/collaborators/$GITHUB_USERNAME/permission" --jq .permission 2>/dev/null || echo "unknown")

echo "Repo:       $OWNER/$REPO"
echo "User:       $GITHUB_USERNAME"
echo "Branch:     $BRANCH"
echo "Permission: $PERM"

if [ "$PERM" != "admin" ]; then
  echo "❌ User is not an admin on $OWNER/$REPO. Read-only checks may still work but write phases will fail."
fi
```

### 2. Detect protection mode (Classic Branch Protection vs Rulesets)

Critical: rulesets and classic branch protection use different APIs. The classic /branches/{branch}/protection endpoint silently no-ops for rules enforced via Rulesets.

```bash
PROTECTION_PAYLOAD=$(gtimeout 10 gh api "repos/$OWNER/$REPO/branches/$BRANCH/protection" 2>/dev/null || echo '{}')
echo "$PROTECTION_PAYLOAD" > .tmp/current_protection.json

REPO_RULESETS=$(gtimeout 10 gh api "repos/$OWNER/$REPO/rulesets" 2>/dev/null || echo '[]')
echo "$REPO_RULESETS" > .tmp/repo_rulesets.json

ORG_RULESETS=$(gtimeout 10 gh api "orgs/$OWNER/rulesets" 2>/dev/null || echo '[]')
echo "$ORG_RULESETS" > .tmp/org_rulesets.json

HAS_CLASSIC=$(jq -r 'if has("required_pull_request_reviews") then "yes" else "no" end' .tmp/current_protection.json)

# Bug fix (2026-07-07, confirmed independently in two separate live sweeps same day):
# gh api returns a 404 JSON *object* (e.g. {"message":"Not Found",...}) when the
# caller isn't an org owner / the endpoint is inaccessible -- NOT an empty array.
# `jq 'length'` on that object counts its keys (typically 3: message,
# documentation_url, status), producing a misleading "3 org-level rulesets" false
# positive instead of "org rulesets endpoint inaccessible". Check the JSON type
# before counting, for both the repo- and org-level responses.
repo_rulesets_type() { jq -r 'type' .tmp/repo_rulesets.json; }
org_rulesets_type() { jq -r 'type' .tmp/org_rulesets.json; }

if [ "$(repo_rulesets_type)" = "array" ]; then
  REPO_RULESET_COUNT=$(jq 'length' .tmp/repo_rulesets.json)
  REPO_RULESETS_ACCESSIBLE=yes
else
  REPO_RULESET_COUNT=0
  REPO_RULESETS_ACCESSIBLE=no
fi

if [ "$(org_rulesets_type)" = "array" ]; then
  ORG_RULESET_COUNT=$(jq 'length' .tmp/org_rulesets.json)
  ORG_RULESETS_ACCESSIBLE=yes
else
  ORG_RULESET_COUNT=0
  ORG_RULESETS_ACCESSIBLE=no
fi

echo "Classic branch protection on $BRANCH: $HAS_CLASSIC"
if [ "$REPO_RULESETS_ACCESSIBLE" = "yes" ]; then
  echo "Repo-level rulesets:               $REPO_RULESET_COUNT"
else
  echo "Repo-level rulesets:               inaccessible ($(jq -r '.message // "unknown error"' .tmp/repo_rulesets.json))"
fi
if [ "$ORG_RULESETS_ACCESSIBLE" = "yes" ]; then
  echo "Org-level rulesets:                $ORG_RULESET_COUNT"
else
  echo "Org-level rulesets:                inaccessible ($(jq -r '.message // "unknown error"' .tmp/org_rulesets.json)) -- not an org owner, or endpoint unavailable. This does NOT mean zero rulesets exist; it means this check cannot see them. Treat as unknown, not as confirmed-absent."
fi

if [ "$ORG_RULESETS_ACCESSIBLE" = "yes" ] && [ "$ORG_RULESET_COUNT" -gt 0 ]; then
  echo "⚠️  Org-level rulesets present. They CANNOT be bypassed by repo admins. Only org owners (or actors listed in the org ruleset bypass list) can merge."
fi
```

### 3. Read current bypass posture (review bypass vs push restrictions; enforce_admins; CODEOWNERS)

Distinguish bypass_pull_request_allowances (PR review bypass — the one that matters for `gh pr merge --admin`) from restrictions/users (who can push directly).

```bash
ENFORCE_ADMINS=$(jq -r '.enforce_admins.enabled // false' .tmp/current_protection.json)
REQUIRED_APPROVALS=$(jq -r '.required_pull_request_reviews.required_approving_review_count // 0' .tmp/current_protection.json)
REQUIRE_CODEOWNERS=$(jq -r '.required_pull_request_reviews.require_code_owner_reviews // false' .tmp/current_protection.json)

BYPASS_USERS_JSON=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.users[]? | (.login // .) ]' .tmp/current_protection.json)
BYPASS_TEAMS_JSON=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.teams[]? | (.slug // .name // .) ]' .tmp/current_protection.json)
BYPASS_APPS_JSON=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.apps[]? | (.slug // .name // .) ]' .tmp/current_protection.json)

PUSH_RESTRICTION_USERS=$(jq -r '[ .restrictions.users[]? | (.login // .) ]' .tmp/current_protection.json)

USER_HAS_BYPASS=$(echo "$BYPASS_USERS_JSON" | jq -r --arg u "$GITHUB_USERNAME" 'if (index($u)) then "yes" else "no" end')

cat <<EOF
=== Read-only summary ===
enforce_admins:                  $ENFORCE_ADMINS
required_approving_review_count: $REQUIRED_APPROVALS
require_code_owner_reviews:      $REQUIRE_CODEOWNERS
bypass_pull_request_allowances.users: $BYPASS_USERS_JSON
bypass_pull_request_allowances.teams: $BYPASS_TEAMS_JSON
bypass_pull_request_allowances.apps:  $BYPASS_APPS_JSON
restrictions.users (push-only):       $PUSH_RESTRICTION_USERS
Current user '$GITHUB_USERNAME' has bypass: $USER_HAS_BYPASS
EOF

if [ -f CODEOWNERS ] || [ -f .github/CODEOWNERS ] || [ -f docs/CODEOWNERS ]; then
  echo "⚠️  CODEOWNERS file present. With require_code_owner_reviews=$REQUIRE_CODEOWNERS, a generic approval may not be enough."
fi
```

### 4. [REQUIRES AUTHORIZATION] Add user to PR review bypass allowances (correct API)

This is the CORRECT endpoint to bypass the 'requires N approving reviews' rule. Do NOT confuse with `restrictions/users` (which controls push, not review bypass). Run only after the user explicitly authorizes the change.

```bash
TARGET_USERNAME="${TARGET_USERNAME:-$GITHUB_USERNAME}"

NEW_BYPASS_USERS=$(jq -r --arg u "$TARGET_USERNAME" '
  ([ .required_pull_request_reviews.bypass_pull_request_allowances.users[]? | (.login // .) ] + [$u])
  | unique
' .tmp/current_protection.json)

KEEP_TEAMS=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.teams[]? | (.slug // .name // .) ]' .tmp/current_protection.json)
KEEP_APPS=$(jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.apps[]? | (.slug // .name // .) ]' .tmp/current_protection.json)
DISMISS_STALE=$(jq -r '.required_pull_request_reviews.dismiss_stale_reviews // false' .tmp/current_protection.json)
REQUIRE_LAST_PUSH=$(jq -r '.required_pull_request_reviews.require_last_push_approval // false' .tmp/current_protection.json)

jq -n \
  --argjson required_approving_review_count "${REQUIRED_APPROVALS:-1}" \
  --argjson dismiss_stale_reviews "$DISMISS_STALE" \
  --argjson require_code_owner_reviews "$REQUIRE_CODEOWNERS" \
  --argjson require_last_push_approval "$REQUIRE_LAST_PUSH" \
  --argjson users "$NEW_BYPASS_USERS" \
  --argjson teams "$KEEP_TEAMS" \
  --argjson apps  "$KEEP_APPS" \
  '{
    dismiss_stale_reviews: $dismiss_stale_reviews,
    require_code_owner_reviews: $require_code_owner_reviews,
    required_approving_review_count: $required_approving_review_count,
    require_last_push_approval: $require_last_push_approval,
    bypass_pull_request_allowances: {
      users: $users,
      teams: $teams,
      apps: $apps
    }
  }' > .tmp/required_pr_reviews_patch.json

echo "PATCH payload (.tmp/required_pr_reviews_patch.json):"
cat .tmp/required_pr_reviews_patch.json

gtimeout 15 gh api -X PATCH \
  "repos/$OWNER/$REPO/branches/$BRANCH/protection/required_pull_request_reviews" \
  --input .tmp/required_pr_reviews_patch.json > .tmp/patch_response.json

echo "✅ Added '$TARGET_USERNAME' to bypass_pull_request_allowances.users on $OWNER/$REPO@$BRANCH"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp ADD bypass user=$TARGET_USERNAME repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
```

### 5. [REQUIRES AUTHORIZATION] Temporarily disable enforce_admins (only when needed for --admin merge)

When enforce_admins=true, even admins are subject to all rules and `gh pr merge --admin` is rejected. Disable it ONLY for the duration of the merge, and restore in Phase 7.

```bash
ORIGINAL_ENFORCE_ADMINS="$ENFORCE_ADMINS"
echo "$ORIGINAL_ENFORCE_ADMINS" > .tmp/original_enforce_admins.txt

if [ "$ENFORCE_ADMINS" = "true" ]; then
  gtimeout 10 gh api -X DELETE "repos/$OWNER/$REPO/branches/$BRANCH/protection/enforce_admins" >/dev/null
  echo "✅ Temporarily disabled enforce_admins on $OWNER/$REPO@$BRANCH (will restore in Phase 7)"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp DISABLE enforce_admins repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
else
  echo "ℹ️  enforce_admins already disabled — no change needed."
fi
```

### 6. [REQUIRES AUTHORIZATION] Merge the PR with admin override and delete the head branch

Pass PR_NUMBER as an env var, or let this step pick the open PR for the current branch. Before changing protection or merging, refresh the PR state and stop with an explicit stale-authorization message if the target is already merged, already closed, or no longer resolvable. Uses --admin (now permitted because enforce_admins is off and the user is in bypass_pull_request_allowances) and --delete-branch to clean up the remote head.

```bash
if [ -z "${PR_NUMBER:-}" ]; then
  CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)
  PR_NUMBER=$(gtimeout 10 gh pr list --state open --head "$CURRENT_BRANCH" --json number --jq '.[0].number' || echo "")
fi

if [ -z "$PR_NUMBER" ]; then
  CURRENT_BRANCH="${CURRENT_BRANCH:-$(gtimeout 5 git branch --show-current)}"
  LAST_BRANCH_PR=$(gtimeout 10 gh pr list --state all --head "$CURRENT_BRANCH" \
    --json number,state,title --jq '.[0] // empty' 2>/dev/null || true)

  if [ -n "$LAST_BRANCH_PR" ]; then
    LAST_PR_NUMBER=$(echo "$LAST_BRANCH_PR" | jq -r '.number')
    LAST_PR_STATE=$(echo "$LAST_BRANCH_PR" | jq -r '.state')
    case "$LAST_PR_STATE" in
      MERGED)
        echo "Authorization stale: PR #$LAST_PR_NUMBER for $CURRENT_BRANCH is already merged; nothing remains to bypass or merge."
        exit 0
        ;;
      CLOSED)
        echo "Authorization stale: latest PR for $CURRENT_BRANCH is already closed (#$LAST_PR_NUMBER); do not reuse the old bypass authorization."
        exit 1
        ;;
    esac
  fi

  echo "❌ No open PR detected for $CURRENT_BRANCH. Set PR_NUMBER=<n> only if you intend to target a different still-open PR."
  exit 1
fi

PR_STATE=$(gtimeout 10 gh pr view "$PR_NUMBER" --json state,title,headRefName --jq '.state' 2>/dev/null || echo "MISSING")
if [ "$PR_STATE" = "MERGED" ]; then
  echo "Authorization stale: PR #$PR_NUMBER is already merged; nothing remains to bypass or merge."
  exit 0
fi
if [ "$PR_STATE" = "CLOSED" ]; then
  echo "Authorization stale: PR #$PR_NUMBER is already closed; confirm whether a replacement PR is needed."
  exit 1
fi
if [ "$PR_STATE" = "MISSING" ]; then
  echo "Authorization stale: PR #$PR_NUMBER no longer resolves on GitHub; refresh the target before changing protection."
  exit 1
fi

echo "Merging PR #$PR_NUMBER on $OWNER/$REPO ..."
MERGE_STRATEGY="${MERGE_STRATEGY:---merge}"

if gtimeout 30 gh pr merge "$PR_NUMBER" --admin $MERGE_STRATEGY --delete-branch; then
  echo "✅ Merged PR #$PR_NUMBER and deleted head branch."
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp MERGE pr=#$PR_NUMBER repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
else
  echo "❌ Merge failed. Inspect: gh pr view $PR_NUMBER --json reviewDecision,mergeStateStatus,mergeable"
  echo "   Common cause: org-level ruleset (not bypassable from repo) or CODEOWNERS not satisfied."
  exit 1
fi
```

### 7. [OPTIONAL CLEANUP] Restore protection changes

By default, this workflow intentionally keeps user-scoped permissions (for example, temporary bypass-user and direct-push allowances) in place after the bypass sequence.
Use `REVERT_PROTECTION=1` if you want a full rollback to the exact pre-command posture.

`REVERT_PROTECTION=1` will reverse each relaxation (including user-scoped allowances) using the snapshots in `.tmp/`.

```bash
REVERT_PROTECTION="${REVERT_PROTECTION:-0}"

if [ "$REVERT_PROTECTION" != "1" ]; then
  # Default: restore broad protections but keep user-specific allowances.
  echo "ℹ️  REVERT_PROTECTION != 1; performing partial rollback to preserve intended direct-push/bypass-user allowances."

  # 7a. Restore enforce_admins (if it was temporarily disabled)
  if [ -f .tmp/original_enforce_admins.txt ] && [ "$(cat .tmp/original_enforce_admins.txt)" = "true" ]; then
    gtimeout 10 gh api -X POST "repos/$OWNER/$REPO/branches/$BRANCH/protection/enforce_admins" >/dev/null
    echo "✅ Restored enforce_admins=true on $OWNER/$REPO@$BRANCH"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp RESTORE enforce_admins repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
  fi

  # 7c. Scenario B: restore required_pull_request_reviews if phase 9 removed it
  if [ -f .tmp/original_required_pr_reviews.json ]; then
    ORIG_HAD_REQUIREMENT=$(jq -r 'if . == null or . == {} then "no" else "yes" end' .tmp/original_required_pr_reviews.json)
    if [ "$ORIG_HAD_REQUIREMENT" = "yes" ]; then
      # Reconstruct the PATCH payload from the original snapshot
      jq '{
        dismiss_stale_reviews: (.dismiss_stale_reviews // false),
        require_code_owner_reviews: (.require_code_owner_reviews // false),
        required_approving_review_count: (.required_approving_review_count // 1),
        require_last_push_approval: (.require_last_push_approval // false),
        bypass_pull_request_allowances: {
          users: [ .bypass_pull_request_allowances.users[]? | (.login // .) ],
          teams: [ .bypass_pull_request_allowances.teams[]? | (.slug // .name // .) ],
          apps:  [ .bypass_pull_request_allowances.apps[]?  | (.slug // .name // .) ]
        }
      }' .tmp/original_required_pr_reviews.json > .tmp/restore_pr_reviews.json

      gtimeout 15 gh api -X PATCH \
        "repos/$OWNER/$REPO/branches/$BRANCH/protection/required_pull_request_reviews" \
        --input .tmp/restore_pr_reviews.json > /dev/null

      echo "✅ Restored required_pull_request_reviews on $OWNER/$REPO@$BRANCH"
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp RESTORE pr_required repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
    fi
  fi

  # 7d. Scenario B: restore each disabled ruleset (PUT the original snapshot back)
  for snap in .tmp/ruleset_*_original.json; do
    [ -f "$snap" ] || continue
    rid=$(basename "$snap" | sed -E 's/^ruleset_([0-9]+)_original\.json$/\1/')
    scope=$(jq -r '.source_type // "Repository"' "$snap")
    if [ "$scope" = "Organization" ]; then
      endpoint="orgs/$OWNER/rulesets/$rid"
    else
      endpoint="repos/$OWNER/$REPO/rulesets/$rid"
    fi
    gtimeout 15 gh api -X PUT "$endpoint" --input "$snap" > /dev/null && \
      echo "✅ Restored ruleset id=$rid (scope=$scope)" && \
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp RESTORE ruleset=$rid scope=$scope repo=$OWNER/$REPO actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
  done

  echo "✅ Partial cleanup complete. Core protections restored; user-scoped allowances kept."
else
  # 7b. Full rollback: restore required pull-request allowance user list and original restrictions
  # Scenario A: remove the temporary bypass user unless KEEP_BYPASS=1
  HAS_PR_REVIEWS_NOW=$(gtimeout 10 gh api "repos/$OWNER/$REPO/branches/$BRANCH/protection" 2>/dev/null \
                       | jq -r 'if has("required_pull_request_reviews") then "yes" else "no" end' || echo "no")
  if [ "${KEEP_BYPASS:-0}" = "1" ]; then
    echo "ℹ️  KEEP_BYPASS=1 set — leaving '${TARGET_USERNAME:-$GITHUB_USERNAME}' in bypass list."
  elif [ "$HAS_PR_REVIEWS_NOW" = "yes" ]; then
    CURRENT=$(gtimeout 10 gh api "repos/$OWNER/$REPO/branches/$BRANCH/protection")
    REMAINING_USERS=$(echo "$CURRENT" | jq -r --arg u "${TARGET_USERNAME:-$GITHUB_USERNAME}" '
      [ .required_pull_request_reviews.bypass_pull_request_allowances.users[]? | (.login // .) ]
      | map(select(. != $u))
    ')
    KEEP_TEAMS=$(echo "$CURRENT" | jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.teams[]? | (.slug // .name // .) ]')
    KEEP_APPS=$(echo  "$CURRENT" | jq -r '[ .required_pull_request_reviews.bypass_pull_request_allowances.apps[]?  | (.slug // .name // .) ]')
    KEEP_DISMISS=$(echo "$CURRENT" | jq -r '.required_pull_request_reviews.dismiss_stale_reviews // false')
    KEEP_CODEOWNERS=$(echo "$CURRENT" | jq -r '.required_pull_request_reviews.require_code_owner_reviews // false')
    KEEP_REQUIRE_LAST_PUSH=$(echo "$CURRENT" | jq -r '.required_pull_request_reviews.require_last_push_approval // false')
    KEEP_COUNT=$(echo "$CURRENT" | jq -r '.required_pull_request_reviews.required_approving_review_count // 1')

    jq -n \
      --argjson required_approving_review_count "$KEEP_COUNT" \
      --argjson dismiss_stale_reviews "$KEEP_DISMISS" \
      --argjson require_code_owner_reviews "$KEEP_CODEOWNERS" \
      --argjson require_last_push_approval "$KEEP_REQUIRE_LAST_PUSH" \
      --argjson users "$REMAINING_USERS" \
      --argjson teams "$KEEP_TEAMS" \
      --argjson apps  "$KEEP_APPS" \
      '{
        dismiss_stale_reviews: $dismiss_stale_reviews,
        require_code_owner_reviews: $require_code_owner_reviews,
        required_approving_review_count: $required_approving_review_count,
        require_last_push_approval: $require_last_push_approval,
        bypass_pull_request_allowances: {users: $users, teams: $teams, apps: $apps}
      }' > .tmp/required_pr_reviews_cleanup.json

    gtimeout 15 gh api -X PATCH \
      "repos/$OWNER/$REPO/branches/$BRANCH/protection/required_pull_request_reviews" \
      --input .tmp/required_pr_reviews_cleanup.json > /dev/null

    echo "✅ Removed '${TARGET_USERNAME:-$GITHUB_USERNAME}' from bypass_pull_request_allowances on $OWNER/$REPO@$BRANCH"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp REMOVE bypass user=${TARGET_USERNAME:-$GITHUB_USERNAME} repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
  fi

  # 7e. Restore push restrictions users if this was altered in phase 9
  if [ -f .tmp/original_restrictions_users.json ]; then
    ORIG_USERS=$(cat .tmp/original_restrictions_users.json)
    KEEP_TEAMS_R=$(jq -r '[ .restrictions.teams[]? | (.slug // .name // .) ]' .tmp/current_protection.json 2>/dev/null || echo '[]')
    KEEP_APPS_R=$(jq -r  '[ .restrictions.apps[]?  | (.slug // .name // .) ]' .tmp/current_protection.json 2>/dev/null || echo '[]')

    jq -n \
      --argjson users "$ORIG_USERS" \
      --argjson teams "$KEEP_TEAMS_R" \
      --argjson apps  "$KEEP_APPS_R" \
      '{users: $users, teams: $teams, apps: $apps}' > .tmp/restore_restrictions.json

    gtimeout 15 gh api -X PUT \
      "repos/$OWNER/$REPO/branches/$BRANCH/protection/restrictions" \
      --input .tmp/restore_restrictions.json > /dev/null

    echo "✅ Restored push restrictions list on $OWNER/$REPO@$BRANCH"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp RESTORE restrictions repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
  fi

  # 7a-c already handled: enforce_admins, required_pull_request_reviews, rulesets above.
  echo "✅ Cleanup complete. Branch protection fully restored to original posture."
fi

rm -rf .tmp/current_protection.json .tmp/repo_rulesets.json .tmp/org_rulesets.json \
       .tmp/required_pr_reviews_patch.json .tmp/required_pr_reviews_cleanup.json \
       .tmp/original_enforce_admins.txt .tmp/patch_response.json \
       .tmp/original_required_pr_reviews.json .tmp/restore_pr_reviews.json \
       .tmp/original_restrictions_users.json .tmp/restore_restrictions.json \
       .tmp/ruleset_*_original.json .tmp/ruleset_*_disabled.json \
       .tmp/dp_blockers.json 2>/dev/null || true

```

### 8. [Scenario B] Diagnose what blocks direct push to the branch

Read-only, but scoped to the direct-push question: which mechanism is currently rejecting `git push origin <branch>`? Run after phases 1–3.

```bash
HAS_PR_REQUIREMENT=$(jq -r 'if has("required_pull_request_reviews") and (.required_pull_request_reviews != null) then "yes" else "no" end' .tmp/current_protection.json)
HAS_PUSH_RESTRICTIONS=$(jq -r 'if has("restrictions") and (.restrictions != null) then "yes" else "no" end' .tmp/current_protection.json)
USER_IN_RESTRICTIONS="n/a"
if [ "$HAS_PUSH_RESTRICTIONS" = "yes" ]; then
  USER_IN_RESTRICTIONS=$(jq -r --arg u "$GITHUB_USERNAME" '
    [ .restrictions.users[]? | (.login // .) ] | if (index($u)) then "yes" else "no" end
  ' .tmp/current_protection.json)
fi
HAS_REQUIRED_SIGNATURES=$(jq -r '.required_signatures.enabled // false' .tmp/current_protection.json)
HAS_REQUIRED_STATUS=$(jq -r 'if has("required_status_checks") and (.required_status_checks != null) then "yes" else "no" end' .tmp/current_protection.json)

# Rulesets that block direct push to this branch (active + targets branch + has pull_request rule)
REPO_BLOCKING_RULESETS=$(jq -r --arg b "$BRANCH" '
  [ .[] | select(.enforcement == "active")
        | select(any(.conditions.ref_name.include[]?; . == "~DEFAULT_BRANCH" or . == "refs/heads/'"$BRANCH"'" or . == "refs/heads/*"))
        | .id
  ]
' .tmp/repo_rulesets.json 2>/dev/null || echo '[]')
ORG_BLOCKING_RULESETS=$(jq -r '
  [ .[] | select(.enforcement == "active") | .id ]
' .tmp/org_rulesets.json 2>/dev/null || echo '[]')

jq -n \
  --arg branch "$BRANCH" \
  --arg user  "$GITHUB_USERNAME" \
  --arg pr_req "$HAS_PR_REQUIREMENT" \
  --arg push_restr "$HAS_PUSH_RESTRICTIONS" \
  --arg user_in_restr "$USER_IN_RESTRICTIONS" \
  --arg sigs "$HAS_REQUIRED_SIGNATURES" \
  --arg req_status "$HAS_REQUIRED_STATUS" \
  --arg enforce_admins "$ENFORCE_ADMINS" \
  --argjson repo_rs "$REPO_BLOCKING_RULESETS" \
  --argjson org_rs  "$ORG_BLOCKING_RULESETS" \
  '{branch: $branch, user: $user,
    classic: {
      required_pull_request_reviews: $pr_req,
      restrictions: $push_restr,
      user_in_restrictions: $user_in_restr,
      required_signatures: $sigs,
      required_status_checks: $req_status,
      enforce_admins: $enforce_admins
    },
    rulesets: { repo_active_branch_targeted: $repo_rs, org_active: $org_rs }
  }' > .tmp/dp_blockers.json

echo "=== Direct-push blockers for $BRANCH ==="
cat .tmp/dp_blockers.json

if [ "$(jq -r '.org_active | length' .tmp/dp_blockers.json)" -gt 0 ]; then
  echo "⚠️  Org-level rulesets active. Repo admin cannot bypass them. Escalate to an org owner."
fi

if [ "$HAS_PR_REQUIREMENT" = "no" ] && [ "$HAS_PUSH_RESTRICTIONS" = "no" ] && \
   [ "$ENFORCE_ADMINS" != "true" ] && \
   [ "$(jq -r '.rulesets.repo_active_branch_targeted | length' .tmp/dp_blockers.json)" -eq 0 ]; then
  echo "ℹ️  No detectable blocker for direct push. The push may have failed for another reason (network, auth, signed-commits, status checks). Inspect git stderr."
fi
```

### 9. [REQUIRES AUTHORIZATION] [Scenario B] Temporarily relax direct-push blockers

Apply the minimum relaxation needed. Each strategy snapshots its prior state into `.tmp/` so phase 7 can restore it. Strategies are additive — apply only those flagged in phase 8.

```bash
# Strategy 1: classic — temporarily DELETE required_pull_request_reviews (most common blocker for "Changes must be made through a pull request")
if [ "${RELAX_PR_REQUIREMENT:-auto}" = "auto" ] && [ "$HAS_PR_REQUIREMENT" = "yes" ] || [ "${RELAX_PR_REQUIREMENT:-}" = "1" ]; then
  jq '.required_pull_request_reviews // {}' .tmp/current_protection.json > .tmp/original_required_pr_reviews.json

  gtimeout 15 gh api -X DELETE \
    "repos/$OWNER/$REPO/branches/$BRANCH/protection/required_pull_request_reviews" >/dev/null
  echo "✅ Temporarily removed required_pull_request_reviews on $OWNER/$REPO@$BRANCH (will restore in phase 7)"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp DISABLE pr_required repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
fi

# Strategy 2: classic — add users in DIRECT_PUSH_USERS to restrictions.users (when push restrictions are set and any target user is missing)
DIRECT_PUSH_USERS="${DIRECT_PUSH_USERS:-$GITHUB_USERNAME,luisotsm}"
DIRECT_PUSH_USERS_JSON=$(printf '%s' "$DIRECT_PUSH_USERS" | tr ' ' '\n' | tr ',' '\n' \
  | jq -R 'gsub("^\\s+|\\s+$";"") | select(length>0)' | jq -s -c 'unique')
MISSING_DIRECT_PUSH_USERS=$(jq -r --argjson additions "$DIRECT_PUSH_USERS_JSON" '
  [ .restrictions.users[]? | (.login // .) ] as $cur
  | [ $additions[] | select(( $cur | index(.) | not )) ]
' .tmp/current_protection.json)
MISSING_COUNT=$(echo "$MISSING_DIRECT_PUSH_USERS" | jq 'length')

if [ "$HAS_PUSH_RESTRICTIONS" = "yes" ] && [ "$MISSING_COUNT" -gt 0 ]; then
  jq -r '[ .restrictions.users[]? | (.login // .) ]' .tmp/current_protection.json > .tmp/original_restrictions_users.json

  NEW_RESTR_USERS=$(jq -r --argjson additions "$DIRECT_PUSH_USERS_JSON" '
    ([ .restrictions.users[]? | (.login // .) ] + $additions) | unique
  ' .tmp/current_protection.json)
  KEEP_TEAMS_R=$(jq -r '[ .restrictions.teams[]? | (.slug // .name // .) ]' .tmp/current_protection.json)
  KEEP_APPS_R=$(jq -r  '[ .restrictions.apps[]?  | (.slug // .name // .) ]' .tmp/current_protection.json)
  DIRECT_PUSH_USERS_PRINT=$(echo "$DIRECT_PUSH_USERS_JSON" | jq -r 'join(", ")')

  jq -n \
    --argjson users "$NEW_RESTR_USERS" \
    --argjson teams "$KEEP_TEAMS_R" \
    --argjson apps  "$KEEP_APPS_R" \
    '{users: $users, teams: $teams, apps: $apps}' > .tmp/restrictions_patch.json

  gtimeout 15 gh api -X PUT \
    "repos/$OWNER/$REPO/branches/$BRANCH/protection/restrictions" \
    --input .tmp/restrictions_patch.json > /dev/null
  echo "✅ Added/updated push restrictions users on $OWNER/$REPO@$BRANCH: ${DIRECT_PUSH_USERS_PRINT}"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp ADD restrictions users=${DIRECT_PUSH_USERS_PRINT} repo=$OWNER/$REPO branch=$BRANCH actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
fi

# Strategy 3: rulesets — for each repo-level active ruleset that targets this branch, snapshot then disable
for rid in $(jq -r '.[]' <<<"$REPO_BLOCKING_RULESETS"); do
  [ -z "$rid" ] && continue
  gtimeout 10 gh api "repos/$OWNER/$REPO/rulesets/$rid" > ".tmp/ruleset_${rid}_original.json"
  jq '.enforcement = "disabled"' ".tmp/ruleset_${rid}_original.json" > ".tmp/ruleset_${rid}_disabled.json"

  gtimeout 15 gh api -X PUT \
    "repos/$OWNER/$REPO/rulesets/$rid" \
    --input ".tmp/ruleset_${rid}_disabled.json" > /dev/null
  echo "✅ Temporarily disabled repo ruleset id=$rid (will restore in phase 7)"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp DISABLE ruleset=$rid scope=Repository repo=$OWNER/$REPO actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
done

# Strategy 4 (informational): org rulesets cannot be bypassed at the repo level
if [ "$(jq -r 'length' <<<"$ORG_BLOCKING_RULESETS")" -gt 0 ]; then
  echo "⚠️  Org-level rulesets are active and cannot be bypassed by a repo admin."
  echo "    Affected ruleset IDs: $ORG_BLOCKING_RULESETS"
  echo "    Either escalate to an org owner, or add this user to the org ruleset bypass_actors via:"
  echo "      gh api orgs/$OWNER/rulesets/<id>   # GET to inspect, then PUT with updated bypass_actors"
fi

# If enforce_admins=true and you are admin, scenario B may still need phase 5 to disable it.
if [ "$ENFORCE_ADMINS" = "true" ]; then
  echo "ℹ️  enforce_admins=true detected. Run phase 5 next to temporarily disable it (otherwise the relaxations above may still not let an admin push directly)."
fi
```

### 10. [REQUIRES AUTHORIZATION] [Scenario B] Push directly to the branch

Performs the actual `git push`. Use `LOCAL_REF` to push something other than the current branch (e.g. `LOCAL_REF=HEAD` or `LOCAL_REF=feature/x`). The remote ref is always `$BRANCH` (the protected branch you targeted in phase 1).

If this environment's shell-level git guard is active (`rules/dadosfera/4_24_destructive_command_authorization.md`), pushing to `main`/`master` additionally requires `GIT_AUTHORIZE_MAIN_PUSH=true` set in the *same shell invocation* as the push. Confirm the exact push with the user first, then run e.g. `export GIT_AUTHORIZE_MAIN_PUSH=true && git push origin "${LOCAL_REF}:${BRANCH}"`. Asking the user to `export` it in their own terminal will not work — that variable never reaches this command's tool-invoked shell calls.

```bash
LOCAL_REF="${LOCAL_REF:-$(gtimeout 5 git branch --show-current)}"

if [ -z "$LOCAL_REF" ]; then
  echo "❌ Could not determine local ref to push (detached HEAD?). Set LOCAL_REF=<ref> and re-run."
  exit 1
fi

echo "Pushing $LOCAL_REF -> origin/$BRANCH on $OWNER/$REPO ..."

if gtimeout 30 git push origin "${LOCAL_REF}:${BRANCH}"; then
  echo "✅ Direct push succeeded: ${LOCAL_REF} -> origin/${BRANCH}"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) gbyp DIRECT_PUSH local=$LOCAL_REF branch=$BRANCH repo=$OWNER/$REPO actor=$GITHUB_USERNAME" >> logs/git_sync_operations.log
else
  echo "❌ Push still rejected. Re-run phase 8 to re-diagnose; an org-level ruleset, required signed commits, or required status checks may be the binding constraint."
  echo "   IMPORTANT: if rollback is desired, run phase 7 with REVERT_PROTECTION=1 to restore the relaxations applied in phase 9."
  exit 1
fi
```

## Scenarios

This command supports two scenarios. Run phases 1–3 first (shared, read-only context discovery), then choose ONE scenario:

- **Scenario A — PR is blocked from merging into main** → run phases 1, 2, 3 → 4 → 5 → 6 → 7
- **Scenario B — Direct commit is blocked from being pushed to main** → run phases 1, 2, 3 → 8 → 9 → (5 if needed) → 10 → 7

Phase 5 (temporarily disable `enforce_admins`) and Phase 7 (optional cleanup) are shared between scenarios. Phase 7 uses snapshots saved under `.tmp/`; it always restores core protections by default, and applies a full rollback of user-scoped allowances only when `REVERT_PROTECTION=1`.

Set `MODE=pr_merge` (default) or `MODE=direct_push` to drive any external orchestrator. The phases themselves can also be invoked individually.

### Scenario A — PR is blocked from merging into main

- **Check current bypass posture (read-only)**: run phases 1–3.
- **Add yourself to bypass and merge a single PR you authored**: run phases 1–7 (set `PR_NUMBER` if not on the PR head branch).
- **Merge multiple PRs in one session (stack or independent batch)**: run phases 1–5 once, then phase 6 separately per PR — confirm each merge is separately authorized, including any PR the agent itself opened as a byproduct of the session's work — then phase 7 once at the end. See 'Stack-mode operation' below.
- **Add another user permanently to bypass**: run phases 1, 2, 3, 4 with `TARGET_USERNAME=<user>`, then phase 7 with `KEEP_BYPASS=1`.
- **Remove a user from bypass**: run phases 1, 2, 3, then phase 7 with `TARGET_USERNAME=<user>` and `KEEP_BYPASS=0`.

### Scenario B — Direct commit is blocked from being pushed to main

- **Diagnose what blocks `git push origin main`**: run phases 1, 2, 3, then phase 8.
- **Single emergency direct push to main (admin, no PR feasible)**: run phases 1, 2, 3 → 8 → 9 → 5 (only if `enforce_admins=true`) → 10 → 7. Set `LOCAL_REF=<branch>` if pushing something other than the current branch.
- **Direct push that only needs the PR-requirement removed (no `enforce_admins`, no rulesets)**: run phases 1, 2, 3 → 8 → 9 (only Strategy 1 will fire) → 10 → 7.
- **Direct push blocked by a repo-level ruleset**: run phases 1, 2, 3 → 8 → 9 (Strategy 3 disables the ruleset) → 10 → 7.
- **Direct push blocked by an org-level ruleset**: this command cannot resolve it on its own. Phase 8 will surface the affected ruleset IDs; escalate to an org owner or have them add this user to the ruleset's `bypass_actors`.

### Scenario A (PR merge)

**`At least 1 approving review is required by reviewers with write access`** — Either `enforce_admins` is on or your user is not in `bypass_pull_request_allowances`. Run phases 4 and 5 (with authorization), then phase 6.

**`Can not approve your own pull request`** — GitHub policy, not bypassable. Use bypass instead of self-approval.

**`Resource not accessible by integration` / classic-protection PATCH succeeds but rule still blocks** — The rule is enforced by a Repository or Organization Ruleset, not classic protection. Inspect `.tmp/repo_rulesets.json` / `.tmp/org_rulesets.json` from phase 2 and patch the ruleset via `gh api repos/{owner}/{repo}/rulesets/{id}` instead.

**`required status check ... is expected`** — Required status checks are independent from review bypass. Pass them, or temporarily relax `required_status_checks` (and restore in phase 7).

**Org-ruleset blocked merge** — Repo admins cannot bypass org-level rulesets. Escalate to an org owner or to a user listed in the org ruleset bypass actors.

**`Pull Request has merge conflicts` right after a sibling PR merged cleanly moments earlier (`mergeable` had shown `MERGEABLE` in phases 1–3)** — Expected transient state, not a real blocker. It happens when two PRs in the same batch touch a shared file (e.g. a single plan-registry YAML or command-registry index) and the prior merge just advanced `main`, staling this PR's merge base. Treat it like any other merge conflict: `git fetch origin main`, merge `origin/main` into the PR branch inside an isolated `git worktree`, resolve, push, then retry `gh pr merge --admin`. When both sides of the conflict simply added distinct entries to the same list/section, combine both additions rather than picking one side — verify by reading both sides first; only combine independent nearby additions, not genuine same-line edits. Batching independent (not just dependency-stacked) PRs into a single bypass window, per 'Stack-mode operation' below, reduces how often this fires but does not eliminate it once the shared file changes more than once in the session.

### Scenario B (direct push)

**`! [remote rejected] main -> main (protected branch hook declined)`** — A classic protection rule (most often `required_pull_request_reviews`) is blocking. Run phase 8 to confirm, then phase 9 (Strategy 1).

**`Changes must be made through a pull request` / `Changes must be made through the merge queue`** — A repo or org Ruleset with the `pull_request` rule is active. Phase 8 will list the affected ruleset IDs; phase 9 (Strategy 3) disables repo-level rulesets. Org-level requires escalation.

**`Cannot push to a branch with branch protection rules: enforce_admins`** — Even as admin you are subject to all rules. Run phase 5 (after phase 9) to temporarily disable `enforce_admins`.

**`refusing to allow ... to push: required_signatures`** — Signed commits are required. This command does not relax `required_signatures` because that is a much wider protection regression. Sign your commits (`git commit --amend -S` then re-push), or temporarily disable required signatures via `gh api -X DELETE repos/$OWNER/$REPO/branches/$BRANCH/protection/required_signatures` and `POST` to restore (out-of-band; not handled in phase 7 by default).

**`! [remote rejected] main -> main (protection rule violations found)`** — Generic catch-all. Re-run phase 8 to inspect every active rule.

**Push succeeds but pre-receive hooks reject it** — Pre-receive hooks are server-side scripts independent of branch protection and rulesets. They cannot be bypassed by this command.

## Audit & Logging

Every write operation appends a line to `logs/git_sync_operations.log` with timestamp, action (ADD/REMOVE/DISABLE/RESTORE/MERGE), affected user, repo, branch, and the actor performing the change. The log is intentionally append-only and should be retained for compliance review.

## Stack-mode operation (merging multiple dependent PRs in one session)

When this command is invoked to merge a PR that is the *base* of a stack of open dependent PRs, do **not** restore branch protection between merges. Run Phase 7 exactly once, after the last PR in the stack has been merged. See `/merg_merge` 'Stacked-PR awareness' for retarget-before-delete. See `recurrent_errors/2026-06-09_pr_stack_premature_branch_delete.md`.

This also applies to a batch of otherwise-*independent* PRs (no base/dependent relationship) merged in the same sweep session: keeping them under one bypass window (phases 4/5 once, Phase 7 once at the end) still avoids repeatedly relaxing and restoring protection per PR. It does not, however, prevent transient merge-conflict failures on later PRs in the batch when they share a touched file with an earlier one — see the `Pull Request has merge conflicts` entry under Common Errors.
