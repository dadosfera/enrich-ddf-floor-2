# /merg_merge

<!-- COMMAND_ID: 035 -->
<!-- COMMAND_VERSION: 1.4.0 -->
<!-- COMMAND_TYPE: me_merge -->
<!-- UPDATED: 2025-12-11 - Added remote CI check and target branch sync -->

Safely merge an agent branch into the default branch using zero-trust validation, isolation testing, manual conflict handling, and rollback points. This follows the practices in the referenced mini prompt and the terminal command safety guidelines (timeouts, no chaining, short commands).

Backlinks:

- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- standards/git/branch_convention.md
- standards/git/pull-request-best-practices.md

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

4. Create safety backup and stash current work

```bash
gtimeout 5 git branch --show-current
```

```bash
gtimeout 10 git branch backup-pre-merge-$(date +%Y%m%d_%H%M%S)
```

```bash
gtimeout 15 git stash push -m "Pre-merge safety backup"
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

Reference: See Step 5.6 in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md` for actions to merge, close, or update the PR.

6b. Verify remote CI status for the agent branch (if PR exists)

```bash
[ -n "$PR_NUMBER" ] && gtimeout 15 gh pr checks "$PR_NUMBER" || echo "No PR or checks passed/skipped"
```

6c. Check if agent branch exists locally or remotely

```bash
gtimeout 10 git show-ref --verify --quiet refs/heads/"$AGENT_BRANCH" && echo "local branch found" || echo "local branch not found"
```

```bash
gtimeout 15 git for-each-ref --format='%(refname:short)' "refs/remotes/*/$AGENT_BRANCH" || true
```

```bash
REMOTE_BRANCH_REF=$(gtimeout 15 git for-each-ref --format='%(refname:short)' "refs/remotes/*/$AGENT_BRANCH" | head -n 1)
```

```bash
# Determine branch reference: prefer local if it exists, otherwise use the first matching remote branch
if gtimeout 10 git show-ref --verify --quiet refs/heads/"$AGENT_BRANCH" 2>/dev/null; then
  AGENT_BRANCH_REF="$AGENT_BRANCH"
elif [ -n "$REMOTE_BRANCH_REF" ]; then
  AGENT_BRANCH_REF="$REMOTE_BRANCH_REF"
else
  echo "Branch $AGENT_BRANCH not found locally or remotely"; exit 1
fi
echo "Using branch reference: $AGENT_BRANCH_REF"
```

7. Establish baseline test results (allows longer timeout)

```bash
gtimeout 600 tests/run_tests.sh --all --baseline > .tmp/baseline_tests.log
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
gtimeout 600 tests/run_tests.sh --all --isolated > .tmp/agent_tests.log
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

12. Return to target branch and ensure clean tree

```bash
gtimeout 10 git checkout "$TARGET_BRANCH"
```

```bash
gtimeout 15 git pull origin "$TARGET_BRANCH" --ff-only
```

```bash
gtimeout 10 git status --porcelain
```

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
gtimeout 600 tests/run_tests.sh --all --post-merge > .tmp/post_merge_tests.log
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
gtimeout 15 git branch -d $(git branch --list "test-agent-merge-*")
```

19. Push target branch and tags

```bash
gtimeout 15 git push origin "$TARGET_BRANCH"
```

```bash
gtimeout 15 git push origin --tags
```

20. Optional: Remote branch cleanup (choose deprecate or delete)

```bash
gtimeout 15 git push origin "$AGENT_BRANCH:refs/heads/deprecated-$AGENT_BRANCH"
```

```bash
gtimeout 15 git push origin --delete "$AGENT_BRANCH"
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
gtimeout 10 git branch -d backup-pre-merge-*
gtimeout 10 git push origin --delete deprecated-${AGENT_BRANCH}
gtimeout 10 git tag -d pre-merge-checkpoint-*
gtimeout 10 git push origin --delete pre-merge-checkpoint-*
```

**Option B (Standard - Recommended for Regular Operations)**

```bash
# Delete local artifacts immediately, keep remote for 30 days
# Delete immediately after tests pass
gtimeout 10 git branch -d backup-pre-merge-*

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
gtimeout 10 git branch -d backup-pre-merge-*

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
# Solution: Use force delete (only if you're sure)
git branch -D backup-pre-merge-* 2>/dev/null || true
```

**Issue**: Remote branch deletion permission denied

```bash
# Solution: Check GitHub permissions, may need admin to delete
# Or ask repo maintainer to delete the deprecated branch
```

**Issue**: Too many tags accumulated

```bash
# Solution: Batch delete old checkpoints (>60 days)
git tag -d $(git tag -l 'pre-merge-checkpoint-*') 2>/dev/null || true
git push origin --delete $(git tag -l 'pre-merge-checkpoint-*') 2>/dev/null || true
```

### Documentation References

- See `mini_prompt/lv2/agent_branch_merge_mini_prompt.md` for extended cleanup strategy
- See `standards/git/branch_convention.md` for branch naming conventions
- See `guides/cursor_commands_sync.md` for distribution of merge command updates

## Notes

- **Branch Detection**: The command now automatically detects whether a branch exists locally or remotely and uses the appropriate reference. Local branches are preferred when available.
- **Comprehensive Branch Discovery**: All branches (local and remote) are discovered and fetched before merge operations to ensure accurate branch state.
- Conflicts must be resolved manually following the “Enhanced Manual Conflict Resolution Process” in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md`
- Never use destructive commands (`git reset --hard`, `--no-verify`, force-push) unless explicitly authorized by policy
- Timeouts >20s are used only for tests; keep non-test operations ≤15s
- Execute each command individually; do not chain with `&&`
- Use this guide alongside the mini prompt for full zero-trust validation and rollback strategy

---

**Last updated**: 2025-12-11 (v1.4.0 - Added remote CI check and target branch sync)  
**Previous**: 2025-12-11 (v1.3.0 - Added comprehensive cleanup warnings)
