# /gpb_git_protection_bypass

**CRITICAL: Admin-only command for managing branch protection review rights and bypass allowances. Requires administrative privileges.**

- **Purpose**: Check, list, and manage branch protection bypass allowances (review rights) for users, teams, and apps
- **Authorization Required**: User must have administrative privileges on the repository
- **AI execution requirement**: After displaying this guidance, the AI must execute each step one-by-one, stopping on any error and reporting results
- **Safety first**: Verify admin status before proceeding. No automated scripts, no chaining. Read-only operations are safe; write operations require explicit authorization.

## Prerequisites

- User must be a repository administrator
- GitHub CLI (`gh`) must be authenticated with admin privileges
- Repository must have branch protection configured

## Required AI execution flow (AI must run these commands individually):

**AI must execute each of these commands individually using `run_terminal_cmd`:**

### Phase 1: Verify Context and Permissions

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

### Phase 2: Check Current Bypass Allowances (Read-Only)

5. **AI executes**: Get current branch protection settings

```bash
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection" > .tmp/current_protection.json
```

6. **AI executes**: List users with bypass allowances

```bash
gtimeout 10 jq -r '.required_pull_request_reviews.bypass_pull_request_allowances.users[]?' .tmp/current_protection.json
```

**Note**: If empty, no users have bypass rights. Output will show usernames if any exist.

7. **AI executes**: List teams with bypass allowances

```bash
gtimeout 10 jq -r '.required_pull_request_reviews.bypass_pull_request_allowances.teams[]?.slug?' .tmp/current_protection.json
```

8. **AI executes**: List apps with bypass allowances

```bash
gtimeout 10 jq -r '.required_pull_request_reviews.bypass_pull_request_allowances.apps[]?' .tmp/current_protection.json
```

9. **AI executes**: Check if current user has bypass rights

```bash
GITHUB_USERNAME=$(gtimeout 10 gh api user | jq -r '.login')
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection/required_pull_request_reviews" --jq ".bypass_pull_request_allowances.users[] | select(. == \"$GITHUB_USERNAME\")"
```

**Note**: If this returns the username, the user has bypass rights. If empty, they do not.

10. **AI executes**: Display full protection configuration summary

```bash
gtimeout 10 jq '{
  enforce_admins: .enforce_admins,
  required_approving_review_count: .required_pull_request_reviews.required_approving_review_count,
  require_code_owner_reviews: .required_pull_request_reviews.require_code_owner_reviews,
  bypass_users: .required_pull_request_reviews.bypass_pull_request_allowances.users,
  bypass_teams: .required_pull_request_reviews.bypass_pull_request_allowances.teams,
  bypass_apps: .required_pull_request_reviews.bypass_pull_request_allowances.apps
}' .tmp/current_protection.json
```

### Phase 3: Add User to Bypass List (Write Operation - Requires Authorization)

**Only execute if user explicitly authorized:**

11. **AI executes**: Verify target user exists (if adding a specific user)

```bash
# Replace TARGET_USERNAME with the username to add
TARGET_USERNAME="<username-to-add>"
gtimeout 10 gh api "users/$TARGET_USERNAME" --jq '.login' 2>/dev/null || echo "User not found"
```

**Note**: If user not found, stop and inform user.

12. **AI executes**: Extract existing bypass users

```bash
gtimeout 10 jq -r '.required_pull_request_reviews.bypass_pull_request_allowances.users[]?' .tmp/current_protection.json > .tmp/existing_bypass_users.txt
```

13. **AI executes**: Check if user is already in bypass list

```bash
gtimeout 5 grep -q "^$TARGET_USERNAME$" .tmp/existing_bypass_users.txt && echo "User already has bypass rights" || echo "User needs to be added"
```

**Note**: If user already has bypass rights, no action needed.

14. **AI executes**: Create updated protection config with new user added

```bash
gtimeout 10 cat > .tmp/update_branch_protection.json << EOF
{
  "required_status_checks": $(jq '.required_status_checks' .tmp/current_protection.json),
  "enforce_admins": $(jq -r '.enforce_admins // true' .tmp/current_protection.json),
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": $(jq -r '.required_pull_request_reviews.dismiss_stale_reviews // true' .tmp/current_protection.json),
    "require_code_owner_reviews": $(jq -r '.required_pull_request_reviews.require_code_owner_reviews // false' .tmp/current_protection.json),
    "required_approving_review_count": $(jq -r '.required_pull_request_reviews.required_approving_review_count // 1' .tmp/current_protection.json),
    "bypass_pull_request_allowances": {
      "users": $(jq -c '[.required_pull_request_reviews.bypass_pull_request_allowances.users[]?] + ["$TARGET_USERNAME"] | unique' .tmp/current_protection.json),
      "teams": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.teams // []' .tmp/current_protection.json),
      "apps": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.apps // []' .tmp/current_protection.json)
    }
  },
  "restrictions": $(jq '.restrictions // null' .tmp/current_protection.json)
}
EOF
```

15. **AI executes**: Update branch protection with new bypass user

```bash
gtimeout 15 gh api "repos/$OWNER/$REPO/branches/main/protection" -X PUT --input .tmp/update_branch_protection.json
```

**Note**: If this fails, verify:
- User has admin permissions (step 4)
- Target user exists and is a collaborator
- Branch protection settings are valid

16. **AI executes**: Verify the update succeeded

```bash
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection/required_pull_request_reviews" --jq ".bypass_pull_request_allowances.users[] | select(. == \"$TARGET_USERNAME\")"
```

**Note**: Should return the username if update succeeded.

### Phase 4: Remove User from Bypass List (Write Operation - Requires Authorization)

**Only execute if user explicitly authorized:**

17. **AI executes**: Create updated protection config with user removed

```bash
gtimeout 10 cat > .tmp/update_branch_protection.json << EOF
{
  "required_status_checks": $(jq '.required_status_checks' .tmp/current_protection.json),
  "enforce_admins": $(jq -r '.enforce_admins // true' .tmp/current_protection.json),
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": $(jq -r '.required_pull_request_reviews.dismiss_stale_reviews // true' .tmp/current_protection.json),
    "require_code_owner_reviews": $(jq -r '.required_pull_request_reviews.require_code_owner_reviews // false' .tmp/current_protection.json),
    "required_approving_review_count": $(jq -r '.required_pull_request_reviews.required_approving_review_count // 1' .tmp/current_protection.json),
    "bypass_pull_request_allowances": {
      "users": $(jq -c '[.required_pull_request_reviews.bypass_pull_request_allowances.users[]?] | map(select(. != "$TARGET_USERNAME"))' .tmp/current_protection.json),
      "teams": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.teams // []' .tmp/current_protection.json),
      "apps": $(jq -c '.required_pull_request_reviews.bypass_pull_request_allowances.apps // []' .tmp/current_protection.json)
    }
  },
  "restrictions": $(jq '.restrictions // null' .tmp/current_protection.json)
}
EOF
```

18. **AI executes**: Update branch protection to remove user

```bash
gtimeout 15 gh api "repos/$OWNER/$REPO/branches/main/protection" -X PUT --input .tmp/update_branch_protection.json
```

19. **AI executes**: Verify the removal succeeded

```bash
gtimeout 10 gh api "repos/$OWNER/$REPO/branches/main/protection/required_pull_request_reviews" --jq ".bypass_pull_request_allowances.users[] | select(. == \"$TARGET_USERNAME\")"
```

**Note**: Should return empty if removal succeeded.

## Important Notes

- **Admin Only**: This command is strictly for authorized administrators. Non-admin users cannot modify branch protection settings.
- **Read Operations**: Steps 1-10 are read-only and safe to execute. They provide information about current bypass allowances.
- **Write Operations**: Steps 11-19 modify branch protection settings and require explicit user authorization.
- **Organizational Authorization**: In Dadosfera organization, ensure user has organizational approval for bypass operations.
- **Audit Trail**: All bypass allowance changes should be documented. Consider adding commit messages or documentation that indicates who was added/removed and why.

## Common Use Cases

### Check if current user has bypass rights
Execute steps 1-9 to verify current user's bypass status.

### List all users with bypass rights
Execute steps 1-6 to see all users with bypass allowances.

### Add current user to bypass list
Execute steps 1-16, setting `TARGET_USERNAME` to the current user's GitHub username.

### Add another user to bypass list
Execute steps 1-16, setting `TARGET_USERNAME` to the target user's GitHub username.

### Remove a user from bypass list
Execute steps 1-4, then steps 17-19, setting `TARGET_USERNAME` to the user to remove.

## Troubleshooting

### Error: "Protected branch update failed"
- **Solution**: Verify user has admin permissions (step 4)
- **Solution**: Check that target user exists and is a repository collaborator
- **Solution**: Verify branch protection settings are valid JSON

### Error: "Insufficient permissions"
- **Solution**: User needs repository admin role, not just write access
- **Solution**: Verify organizational permissions in Dadosfera

### Error: "User not found"
- **Solution**: Verify the username is correct (case-sensitive)
- **Solution**: Ensure the user is a collaborator on the repository

### Error: "Branch protection not configured"
- **Solution**: Branch protection must be enabled before managing bypass allowances
- **Solution**: Configure branch protection via GitHub UI or API first

---

**Last updated**: 2025-01-27
