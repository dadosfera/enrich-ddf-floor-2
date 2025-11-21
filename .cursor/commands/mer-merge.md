# /mer-merge

Safely merge an agent branch into the default branch using zero-trust validation, isolation testing, manual conflict handling, and rollback points. This follows the practices in the referenced mini prompt and the terminal command safety guidelines (timeouts, no chaining, short commands).

Backlinks:

- mini_prompt/lv2/agent_branch_merge_mini_prompt.md
- standards/branch_convention.md
- standards/pull-request-best-practices.md

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

5. Establish baseline test results (allows longer timeout)

```bash
gtimeout 600 tests/run_tests.sh --all --baseline > .tmp/baseline_tests.log
```

6. Discover agent branches and open PRs (context before proceeding)

```bash
gtimeout 15 git branch -r | grep "agent-" || true
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

7. Create isolated test branch and merge agent branch without committing

```bash
gtimeout 10 git checkout -b test-agent-merge-$(date +%Y%m%d_%H%M%S)
```

```bash
gtimeout 30 git fetch origin "$AGENT_BRANCH"
```

```bash
gtimeout 30 git merge origin/"$AGENT_BRANCH" --no-commit --no-ff
```

8. If conflicts occur: STOP and resolve manually per the mini prompt (Enhanced Conflict Resolution). After manual resolution, continue. To inspect:

```bash
gtimeout 10 git status
```

9. Run full isolated tests on merged state (allows longer timeout)

```bash
gtimeout 600 tests/run_tests.sh --all --isolated > .tmp/agent_tests.log
```

10. Compare results and check for degradations

```bash
gtimeout 60 diff .tmp/baseline_tests.log .tmp/agent_tests.log > .tmp/test_diff.log
```

```bash
gtimeout 30 grep -c "FAILED" .tmp/agent_tests.log || true
```

```bash
gtimeout 30 grep -c "REGRESSION" .tmp/test_diff.log || true
```

11. Return to target branch and ensure clean tree

```bash
gtimeout 10 git checkout "$TARGET_BRANCH"
```

```bash
gtimeout 10 git status --porcelain
```

12. Pre-merge hooks

```bash
gtimeout 60 pre-commit run --all-files
```

13. Create rollback checkpoints (tags)

```bash
gtimeout 10 git tag pre-merge-checkpoint-$(date +%Y%m%d_%H%M%S)
```

```bash
gtimeout 15 git tag -a build-$(date +%Y%m%d-%H%M)-g$(git rev-parse --short HEAD) -m "Automated build tag"
```

14. Merge agent branch with clear history (no fast-forward)

```bash
gtimeout 30 git merge origin/"$AGENT_BRANCH" --no-ff -m "Merge agent changes after validation"
```

15. Post-merge validation (allows longer timeout)

```bash
gtimeout 600 tests/run_tests.sh --all --post-merge > .tmp/post_merge_tests.log
```

```bash
gtimeout 60 diff .tmp/baseline_tests.log .tmp/post_merge_tests.log > .tmp/post_merge_diff.log
```

16. Advance environment tags (optional, if you use env/dev tags)

```bash
gtimeout 15 git tag -f env/dev-prev $(git rev-parse env/dev 2>/dev/null || echo HEAD)
```

```bash
gtimeout 15 git tag -f env/dev $(git rev-parse HEAD)
```

```bash
gtimeout 15 git push origin env/dev env/dev-prev
```

17. Clean up isolated test branches (only if merge succeeded)

```bash
gtimeout 15 git branch -d $(git branch --list "test-agent-merge-*")
```

18. Push target branch and tags

```bash
gtimeout 15 git push origin "$TARGET_BRANCH"
```

```bash
gtimeout 15 git push origin --tags
```

19. Optional: Remote branch cleanup (choose deprecate or delete)

```bash
gtimeout 15 git push origin "$AGENT_BRANCH:refs/heads/deprecated-$AGENT_BRANCH"
```

```bash
gtimeout 15 git push origin --delete "$AGENT_BRANCH"
```

## Notes

- Conflicts must be resolved manually following the “Enhanced Manual Conflict Resolution Process” in `mini_prompt/lv2/agent_branch_merge_mini_prompt.md`
- Never use destructive commands (`git reset --hard`, `--no-verify`, force-push) unless explicitly authorized by policy
- Timeouts >20s are used only for tests; keep non-test operations ≤15s
- Execute each command individually; do not chain with `&&`
- Use this guide alongside the mini prompt for full zero-trust validation and rollback strategy

---

**Last updated**: 2025-11-14
