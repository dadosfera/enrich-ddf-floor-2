# /gam_git_admin_push

**CRITICAL: Admin-only command for direct push and merge to main branch. Requires administrative privileges and bypass authorization.**

- **Purpose**: Allows authorized admin users to push and merge directly to `main` branch, bypassing branch protection rules (PR requirements, double approval, etc.)
- **Authorization Required**: User must have administrative privileges and be in the bypass allowances list for branch protection
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results
- **Safety first**: Verify admin status before proceeding. No automated scripts, no chaining, no force-push, no `--no-verify`

## Prerequisites

- User must be a repository administrator
- User must be in the branch protection bypass allowances list
- GitHub CLI (`gh`) must be authenticated with admin privileges
- Repository must have branch protection configured

## Required AI execution flow (AI must run these commands individually):

**AI must execute each of these commands individually using `run_terminal_cmd`:**

1. **AI executes**: Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. **AI executes**: Get current user information

```bash
gtimeout 10 gh api user | jq -r '.login'
```

3. **AI executes**: Get repository information dynamically

```bash
gtimeout 10 gh repo view --json owner,name
```

```bash
REPO_INFO=$(gtimeout 10 gh repo view --json owner,name)
OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
REPO=$(echo "$REPO_INFO" | jq -r '.name')
```

4. **AI executes**: Verify admin permissions

```bash
gtimeout 10 gh api "repos/$OWNER/$REPO/collaborators/$(gh api user | jq -r '.login')/permission" --jq '.permission'
```

**Note**: Must return "admin". If not, stop and inform user they lack admin privileges.

5. **AI executes**: Verify bypass allowances (check if user is in bypass list)

```bash
GITHUB_USERNAME=$(gtimeout 10 gh api user | jq -r '.login')
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection/required_pull_request_reviews" --jq ".bypass_pull_request_allowances.users[] | select(. == \"$GITHUB_USERNAME\")"
```

**Note**: If this returns empty, the user is not in the bypass list. Proceed to step 6 to add them, or stop if unauthorized.

6. **AI executes**: (Optional) Add current user to bypass list if not present

**Only execute if user explicitly authorized and step 5 returned empty:**

```bash
# Get current protection settings
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection" > .tmp/current_protection.json
```

```bash
# Extract existing bypass users
gtimeout 10 jq -r '.required_pull_request_reviews.bypass_pull_request_allowances.users[]' .tmp/current_protection.json > .tmp/existing_bypass_users.txt
```

```bash
# Create updated protection config with current user added
gtimeout 10 cat > .tmp/update_branch_protection.json << EOF
{
  "required_status_checks": $(jq '.required_status_checks' .tmp/current_protection.json),
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": $(jq -r '.required_pull_request_reviews.dismiss_stale_reviews // true' .tmp/current_protection.json),
    "require_code_owner_reviews": $(jq -r '.required_pull_request_reviews.require_code_owner_reviews // false' .tmp/current_protection.json),
    "required_approving_review_count": $(jq -r '.required_pull_request_reviews.required_approving_review_count // 1' .tmp/current_protection.json),
    "bypass_pull_request_allowances": {
      "users": $(jq -c '[.required_pull_request_reviews.bypass_pull_request_allowances.users[]] + ["$GITHUB_USERNAME"] | unique' .tmp/current_protection.json),
      "teams": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.teams // []' .tmp/current_protection.json),
      "apps": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.apps // []' .tmp/current_protection.json)
    }
  },
  "restrictions": $(jq '.restrictions' .tmp/current_protection.json)
}
EOF
```

```bash
# Update branch protection
gtimeout 15 gh api /repos/$OWNER/$REPO/branches/main/protection -X PUT --input .tmp/update_branch_protection.json
```

7. **AI executes**: Sync remotes

```bash
gtimeout 10 git fetch --all --prune
```

8. **AI executes**: Verify current branch

```bash
gtimeout 5 git branch --show-current
```

**Note**: Confirm you're on the intended branch. For direct push to main, you should be on `main` or the branch you want to merge.

9. **AI executes**: Stage all changes

```bash
gtimeout 10 git add -A
```

10. **AI executes**: Verify what was staged

```bash
gtimeout 5 git status --short
```

11. **AI executes**: Run pre-commit hooks

```bash
gtimeout 60 pre-commit run --all-files
```

12. **AI executes**: Re-stage files if hooks modified them

```bash
gtimeout 10 git add -A
```

13. **AI executes**: Commit changes

```bash
gtimeout 10 git commit -m "<meaningful commit message describing changes>"
```

14. **AI executes**: Verify branch before push (CRITICAL SAFETY CHECK)

```bash
gtimeout 5 git branch --show-current
```

**Note**: Double-check you're pushing to the intended branch (main or target branch).

15. **AI executes**: Push directly to main (bypasses branch protection for admin users in bypass list)

```bash
gtimeout 15 git push origin main
```

**Note**: If pushing fails with branch protection error, verify:
- User is in bypass allowances list (step 5)
- User has admin permissions (step 4)
- Branch protection is configured correctly

16. **AI executes**: (Optional) If there's an open PR to merge, merge it using admin privileges

```bash
PR_NUMBER=$(gtimeout 10 gh pr list --state open --base main --json number --jq '.[0].number' 2>/dev/null || echo "")
```

```bash
[ -n "$PR_NUMBER" ] && gtimeout 15 gh pr merge $PR_NUMBER --admin --merge --delete-branch
```

## Important Notes

- **Admin Only**: This command is strictly for authorized administrators. Non-admin users must use standard PR workflow.
- **Bypass Authorization**: The user must be explicitly added to the bypass allowances list in branch protection settings.
- **Direct Commits**: This allows direct commits to `main`, bypassing PR requirements and approval requirements.
- **Audit Trail**: All admin operations should be documented. Consider adding commit messages that indicate admin bypass.
- **Safety**: Always verify branch name before pushing. Never force-push to main.
- **Organizational Authorization**: In Dadosfera organization, ensure user has organizational approval for bypass operations.

## Troubleshooting

### Error: "Protected branch update failed"
- **Solution**: Verify user is in bypass allowances list (step 5)
- **Solution**: Verify user has admin permissions (step 4)
- **Solution**: Check branch protection settings via GitHub API

### Error: "Insufficient permissions"
- **Solution**: User needs repository admin role, not just write access
- **Solution**: Verify organizational permissions in Dadosfera

### Error: "User not in bypass list"
- **Solution**: Add user to bypass list (step 6) if authorized
- **Solution**: Contact repository administrator to add user to bypass allowances

---

**Last updated**: 2025-01-27
