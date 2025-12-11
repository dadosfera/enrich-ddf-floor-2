# /drep_delete_repository

<!-- COMMAND_ID: 048 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: dr_delete_repository -->

**CRITICAL: This command performs safety checks before allowing repository deletion. It does NOT automatically delete the repository - it verifies all safety conditions are met first.**

This command:

1. Checks what files are gitignored (to identify secrets/tokens)
2. **NEW**: Analyzes temporary directories for self-documented disposability (e.g., `.tmp/README.md`)
3. **NEW**: Identifies gitignored files that SHOULD be committed (e.g., `.vscode/settings.json` with project-specific settings)
4. Saves unrecoverable data (tokens, secrets) to OCI Vault respecting dadosfera documentation
5. Checks for unmerged local and remote branches (excluding canonical release branches)
6. After all checks pass, enables safe local repository deletion

**⚠️ WARNING**: This command will identify and backup secrets before deletion. Review all outputs carefully.

## OCI Vault Structure (Dadosfera Standard)

Based on `procedures/branch_environment_strategy.md`:

| Environment    | Tenancy             | Profile             | Compartment    | Vault            |
| -------------- | ------------------- | ------------------- | -------------- | ---------------- |
| Dev/Alpha/Beta | `oci_dadosfera_dev` | `OCI_DADOSFERA_DEV` | `apps-ddf-dev` | Shared DEV Vault |
| Production     | `oci_dadosfera_prd` | `OCI_DADOSFERA_PRD` | `apps-ddf-prd` | Shared PRD Vault |

**Secret Naming Convention**:

- Secrets are organized by **naming prefix only** (no OCI logical compartments inside vaults)
- Pattern: `{repo-name}-[{env-tier}-]{secret-type}`
- **NO `-dev` suffix** for DEV vault secrets (environment is implicit from vault)
- Examples:
  - Env file backup: `ai-flow-module-env-file`
  - Single environment: `auth-ddf-db-password`
  - Multi-tier: `deployer-ddf-alpha-api-key`

**Canonical Release Branches** (excluded from unmerged branch checks):

- `main`, `master`, `production`, `alpha`, `beta`

## Required AI execution flow (AI must run these commands individually):

### Phase 1: Repository Context Verification

1. **AI executes**: Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. **AI executes**: Get repository name

```bash
REPO_ROOT=$(gtimeout 5 git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
echo "Repository: $REPO_NAME"
```

3. **AI executes**: Verify we're not on a canonical release branch

```bash
CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)
CANONICAL_BRANCHES="main master production alpha beta"
if echo "$CANONICAL_BRANCHES" | grep -q "\b$CURRENT_BRANCH\b"; then
  echo "⚠️  WARNING: Currently on canonical branch '$CURRENT_BRANCH'"
  echo "Switch to a non-canonical branch before deletion"
  exit 1
fi
echo "✅ Current branch '$CURRENT_BRANCH' is safe for deletion context"
```

### Phase 2: Check Gitignored Files

4. **AI executes**: List all gitignored files

```bash
gtimeout 10 git ls-files --others --ignored --exclude-standard
```

5. **AI executes**: Check .gitignore patterns

```bash
if [ -f .gitignore ]; then
  echo "=== .gitignore patterns ==="
  gtimeout 5 cat .gitignore
else
  echo "⚠️  No .gitignore file found"
fi
```

6. **AI executes**: Identify potential secret files (common patterns)

```bash
SECRET_PATTERNS="\.env$|\.key$|\.pem$|\.p12$|\.pfx$|secret|token|password|credential|api[_-]?key"
gtimeout 10 git ls-files --others --ignored --exclude-standard | grep -iE "$SECRET_PATTERNS" || echo "No obvious secret files found in gitignored files"
```

### Phase 2.5: Analyze Temporary Directories (NEW)

This phase checks if temporary directories contain self-documentation indicating they're designed to be disposable.

7. **AI executes**: Check for .tmp/ directory and its documentation

```bash
echo "=== TEMPORARY DIRECTORY ANALYSIS ==="
if [ -d ".tmp" ]; then
  echo "Found .tmp/ directory"

  # Check for self-documentation (README, DISPOSABLE marker, etc.)
  if [ -f ".tmp/README.md" ]; then
    echo "📄 Found .tmp/README.md - checking for disposal instructions..."
    if grep -qiE "safely remove|can be deleted|disposable|temporary|cleanup" .tmp/README.md 2>/dev/null; then
      echo "✅ .tmp/ is SELF-DOCUMENTED as disposable"
      echo "   Evidence: $(grep -iE 'safely remove|can be deleted|disposable|temporary|cleanup' .tmp/README.md | head -1)"
    else
      echo "⚠️  .tmp/README.md exists but no disposal instructions found"
      echo "   Manual review recommended"
    fi
  elif [ -f ".tmp/.disposable" ] || [ -f ".tmp/DISPOSABLE" ]; then
    echo "✅ .tmp/ has DISPOSABLE marker file - safe to delete"
  else
    echo "⚠️  .tmp/ has NO self-documentation"
    echo "   Files found: $(ls -1 .tmp/ 2>/dev/null | wc -l | tr -d ' ')"
    echo "   Manual review recommended before deletion"
  fi

  # List contents for transparency
  echo ""
  echo "Contents of .tmp/:"
  ls -la .tmp/ | head -20
else
  echo "✅ No .tmp/ directory found"
fi
```

8. **AI executes**: Check other common temporary directories

```bash
echo "=== OTHER TEMPORARY DIRECTORIES ==="
TEMP_DIRS=".cache .pytest_cache __pycache__ node_modules/.cache .next .nuxt dist build"

for dir in $TEMP_DIRS; do
  if [ -d "$dir" ]; then
    echo "📁 Found: $dir ($(du -sh "$dir" 2>/dev/null | cut -f1) - standard build/cache artifact)"
  fi
done

echo ""
echo "✅ Standard build/cache directories are auto-regenerated and safe to lose"
```

### Phase 2.6: Identify Committable Gitignored Files (NEW)

This phase identifies gitignored files that contain **project-specific settings** that SHOULD be committed to help all developers.

9. **AI executes**: Check for .vscode/settings.json with project-specific settings

```bash
echo "=== COMMITTABLE GITIGNORED FILES ANALYSIS ==="

# Check if .vscode is gitignored
if grep -q "\.vscode" .gitignore 2>/dev/null; then
  echo "📁 .vscode/ is in .gitignore"

  if [ -f ".vscode/settings.json" ]; then
    echo "   Found: .vscode/settings.json"

    # Analyze content for project-specific vs personal settings
    PROJECT_SETTINGS=0
    PERSONAL_SETTINGS=0

    # Project-specific patterns (should be committed)
    if grep -qE "extraPaths|defaultInterpreterPath|formatting\.provider|tabSize|rulers|defaultFormatter" .vscode/settings.json 2>/dev/null; then
      PROJECT_SETTINGS=1
    fi

    # Personal/machine-specific patterns (should NOT be committed)
    if grep -qE "terminal\.integrated\.|shellIntegration|automationProfile" .vscode/settings.json 2>/dev/null; then
      PERSONAL_SETTINGS=1
    fi

    if [ "$PROJECT_SETTINGS" -eq 1 ]; then
      echo ""
      echo "   ⚠️  RECOMMENDATION: This file contains PROJECT-SPECIFIC settings that would help all developers:"
      grep -oE '"python\.(defaultInterpreterPath|analysis\.extraPaths|formatting\.provider)"' .vscode/settings.json 2>/dev/null | head -5
      grep -oE '"editor\.(tabSize|rulers|defaultFormatter)"' .vscode/settings.json 2>/dev/null | head -5
      echo ""
      echo "   ACTION: Consider committing a clean version (without personal settings) before deletion"
      echo "   - Remove .vscode/ from .gitignore (or add .vscode/settings.json exception)"
      echo "   - Remove personal settings (terminal.*, shell*)"
      echo "   - Commit and push"
    fi

    if [ "$PERSONAL_SETTINGS" -eq 1 ]; then
      echo "   ℹ️  Also contains personal/machine-specific settings (terminal, shell) - these should be excluded"
    fi
  fi
else
  echo "✅ .vscode/ is not gitignored (or doesn't exist)"
fi
```

10. **AI executes**: Check for other potentially committable config files

```bash
echo ""
echo "=== OTHER POTENTIALLY COMMITTABLE CONFIGS ==="

# EditorConfig - should always be committed
if [ -f ".editorconfig" ]; then
  if git ls-files --error-unmatch .editorconfig >/dev/null 2>&1; then
    echo "✅ .editorconfig is tracked"
  else
    echo "⚠️  .editorconfig exists but is NOT tracked - should be committed"
  fi
fi

# Prettier config - should be committed
for config in .prettierrc .prettierrc.json .prettierrc.js prettier.config.js; do
  if [ -f "$config" ]; then
    if git ls-files --error-unmatch "$config" >/dev/null 2>&1; then
      echo "✅ $config is tracked"
    else
      echo "⚠️  $config exists but is NOT tracked - should be committed"
    fi
  fi
done

# ESLint config - should be committed
for config in .eslintrc .eslintrc.json .eslintrc.js eslint.config.js; do
  if [ -f "$config" ]; then
    if git ls-files --error-unmatch "$config" >/dev/null 2>&1; then
      echo "✅ $config is tracked"
    else
      echo "⚠️  $config exists but is NOT tracked - should be committed"
    fi
  fi
done

echo ""
echo "If any files above show ⚠️, consider committing them before deletion"
```

### Phase 3: Save Secrets to OCI Vault

11. **AI executes**: Determine environment (DEV or PRD) based on current branch

```bash
CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)
if echo "$CURRENT_BRANCH" | grep -qiE "^(main|alpha|beta|dev)"; then
  ENV="dev"
  PROFILE="OCI_DADOSFERA_DEV"
  COMPARTMENT="apps-ddf-dev"
else
  ENV="prd"
  PROFILE="OCI_DADOSFERA_PRD"
  COMPARTMENT="apps-ddf-prd"
fi
echo "Environment: $ENV"
echo "OCI Profile: $PROFILE"
echo "Compartment: $COMPARTMENT"
```

12. **AI executes**: Verify OCI CLI is available and authenticated

```bash
if ! command -v oci >/dev/null 2>&1; then
  echo "❌ OCI CLI not found. Install: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm"
  exit 1
fi

gtimeout 10 oci iam region list --profile "$PROFILE" >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ OCI authentication failed for profile $PROFILE"
  echo "Configure OCI: oci setup config --profile $PROFILE"
  exit 1
fi
echo "✅ OCI CLI authenticated for profile $PROFILE"
```

13. **AI executes**: Get vault OCID (you may need to list vaults first)

```bash
# List vaults in compartment to find the shared vault
gtimeout 15 oci vault vault list --compartment-id $(oci iam compartment get --name "$COMPARTMENT" --profile "$PROFILE" --query 'data.id' --raw-output) --profile "$PROFILE" --query 'data[0].id' --raw-output
```

**Note**: If vault doesn't exist, you may need to create it or use a different method to store secrets.

14. **AI executes**: For each gitignored secret file, save to vault

```bash
# This is a template - adjust based on actual secret files found
SECRET_FILES=$(gtimeout 10 git ls-files --others --ignored --exclude-standard | grep -iE "\.env$|\.key$|secret|token" | head -20)

if [ -z "$SECRET_FILES" ]; then
  echo "✅ No secret files found to backup"
else
  echo "Found secret files to backup:"
  echo "$SECRET_FILES"
  echo ""
  echo "⚠️  MANUAL STEP REQUIRED:"
  echo "For each secret file, create a vault secret:"
  echo ""
  echo "Pattern: {repo-name}-{secret-type} (NO -dev suffix for DEV vault)"
  echo ""
  echo "Examples:"
  echo "  - .env file: $REPO_NAME-env-file"
  echo "  - API key: $REPO_NAME-api-key"
  echo "  - SSH key: $REPO_NAME-ssh-key"
  echo ""
  echo "  oci vault secret create-base64 \\"
  echo "    --compartment-id <compartment-ocid> \\"
  echo "    --vault-id <vault-ocid> \\"
  echo "    --key-id <key-ocid> \\"
  echo "    --secret-name \"$REPO_NAME-env-file\" \\"
  echo "    --secret-content-content \"\$(base64 < .env)\" \\"
  echo "    --description \"Environment variables for $REPO_NAME\" \\"
  echo "    --profile $PROFILE"
  echo ""
  echo "Or use OCI Console to create secrets manually."
  echo ""
  echo "See: procedures/branch_environment_strategy.md for full documentation"
fi
```

**Alternative**: If OCI vault is not set up, save secrets to a secure location:

```bash
# Create backup directory outside repository
BACKUP_DIR="$HOME/.repo-backups/$(date +%Y%m%d_%H%M%S)_$REPO_NAME"
mkdir -p "$BACKUP_DIR"

# Copy secret files
SECRET_FILES=$(gtimeout 10 git ls-files --others --ignored --exclude-standard | grep -iE "\.env$|\.key$|secret|token" || true)
if [ -n "$SECRET_FILES" ]; then
  echo "$SECRET_FILES" | while read -r file; do
    if [ -f "$file" ]; then
      mkdir -p "$BACKUP_DIR/$(dirname "$file")"
      cp "$file" "$BACKUP_DIR/$file"
      echo "✅ Backed up: $file"
    fi
  done
  echo "Backup location: $BACKUP_DIR"
  echo "⚠️  IMPORTANT: Move these secrets to OCI Vault manually"
fi
```

### Phase 4: Check for Unmerged Branches

15. **AI executes**: Fetch latest from remote

```bash
gtimeout 15 git fetch --all --prune
```

16. **AI executes**: Check for unmerged local branches (excluding canonical)

```bash
CANONICAL_BRANCHES="main master production alpha beta"
CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)

# Get all local branches except canonical and current
ALL_LOCAL=$(gtimeout 10 git branch --format='%(refname:short)')
UNMERGED_LOCAL=""

for branch in $ALL_LOCAL; do
  if echo "$CANONICAL_BRANCHES" | grep -q "\b$branch\b"; then
    continue  # Skip canonical branches
  fi
  if [ "$branch" = "$CURRENT_BRANCH" ]; then
    continue  # Skip current branch
  fi

  # Check if branch is merged into main/master
  if ! gtimeout 10 git branch --merged main 2>/dev/null | grep -q "^  $branch$"; then
    if ! gtimeout 10 git branch --merged master 2>/dev/null | grep -q "^  $branch$"; then
      UNMERGED_LOCAL="$UNMERGED_LOCAL $branch"
    fi
  fi
done

if [ -z "$UNMERGED_LOCAL" ]; then
  echo "✅ No unmerged local branches found (excluding canonical branches)"
else
  echo "⚠️  WARNING: Found unmerged local branches:"
  echo "$UNMERGED_LOCAL"
  echo ""
  echo "Review these branches before deletion:"
  for branch in $UNMERGED_LOCAL; do
    echo "  - $branch: git log main..$branch"
  done
fi
```

17. **AI executes**: Check for unmerged remote branches (excluding canonical)

```bash
CANONICAL_BRANCHES="main master production alpha beta"

# Get all remote branches
ALL_REMOTE=$(gtimeout 10 git branch -r --format='%(refname:short)' | sed 's|origin/||' | grep -v HEAD)

UNMERGED_REMOTE=""

for branch in $ALL_REMOTE; do
  if echo "$CANONICAL_BRANCHES" | grep -q "\b$branch\b"; then
    continue  # Skip canonical branches
  fi

  # Check if remote branch is merged into main/master
  if ! gtimeout 10 git branch -r --merged main 2>/dev/null | grep -q "origin/$branch$"; then
    if ! gtimeout 10 git branch -r --merged master 2>/dev/null | grep -q "origin/$branch$"; then
      UNMERGED_REMOTE="$UNMERGED_REMOTE $branch"
    fi
  fi
done

if [ -z "$UNMERGED_REMOTE" ]; then
  echo "✅ No unmerged remote branches found (excluding canonical branches)"
else
  echo "⚠️  WARNING: Found unmerged remote branches:"
  echo "$UNMERGED_REMOTE"
  echo ""
  echo "These branches exist on remote and are not merged:"
  for branch in $UNMERGED_REMOTE; do
    echo "  - origin/$branch"
  done
fi
```

18. **AI executes**: Summary of unmerged branches

```bash
echo "=== UNMERGED BRANCHES SUMMARY ==="
if [ -n "$UNMERGED_LOCAL" ] || [ -n "$UNMERGED_REMOTE" ]; then
  echo "⚠️  ACTION REQUIRED:"
  echo ""
  if [ -n "$UNMERGED_LOCAL" ]; then
    echo "Local unmerged branches:"
    echo "$UNMERGED_LOCAL"
    echo ""
  fi
  if [ -n "$UNMERGED_REMOTE" ]; then
    echo "Remote unmerged branches:"
    echo "$UNMERGED_REMOTE"
    echo ""
  fi
  echo "Options:"
  echo "  1. Merge these branches before deletion"
  echo "  2. Create PRs for these branches"
  echo "  3. Delete branches if they're no longer needed (use caution)"
  echo ""
  echo "⚠️  Repository deletion should wait until branches are handled"
else
  echo "✅ All non-canonical branches are merged or safe to ignore"
fi
```

### Phase 5: Final Safety Checks

19. **AI executes**: Check for uncommitted changes

```bash
if [ -n "$(gtimeout 5 git status --porcelain)" ]; then
  echo "⚠️  WARNING: Uncommitted changes detected:"
  gtimeout 5 git status --short
  echo ""
  echo "Options:"
  echo "  1. Commit changes: git add -A && git commit -m 'message'"
  echo "  2. Stash changes: git stash"
  echo "  3. Discard changes (if safe): git reset --hard"
  exit 1
else
  echo "✅ No uncommitted changes"
fi
```

20. **AI executes**: Check for unpushed commits

```bash
CURRENT_BRANCH=$(gtimeout 5 git branch --show-current)
if gtimeout 10 git rev-list HEAD..origin/$CURRENT_BRANCH 2>/dev/null | grep -q .; then
  echo "⚠️  WARNING: Unpushed commits detected"
  echo "Push commits before deletion: git push origin $CURRENT_BRANCH"
  exit 1
else
  echo "✅ No unpushed commits"
fi
```

21. **AI executes**: Final confirmation summary

```bash
echo "=== DELETION SAFETY CHECK SUMMARY ==="
echo "Repository: $REPO_NAME"
echo "Location: $REPO_ROOT"
echo ""
echo "✅ Checks passed:"
echo "  - Not on canonical branch"
echo "  - Gitignored files identified"
echo "  - Secrets backed up (verify manually)"
echo "  - No unmerged branches (or handled)"
echo "  - No uncommitted changes"
echo "  - No unpushed commits"
echo ""
echo "⚠️  FINAL STEP: Delete repository directory"
echo "  rm -rf \"$REPO_ROOT\""
echo ""
echo "⚠️  WARNING: This action is irreversible!"
echo "  Make sure all secrets are safely stored in OCI Vault"
echo "  Verify backup location: $BACKUP_DIR (if used)"
```

### Phase 6: Repository Deletion (Manual Confirmation Required)

22. **AI executes**: Display deletion command (DO NOT AUTO-EXECUTE)

```bash
echo "=== REPOSITORY DELETION COMMAND ==="
echo ""
echo "To delete the repository, run:"
echo "  cd $(dirname "$REPO_ROOT")"
echo "  rm -rf \"$REPO_NAME\""
echo ""
echo "⚠️  CRITICAL: This command does NOT auto-execute deletion"
echo "⚠️  User must manually confirm and execute the deletion command"
echo ""
echo "Before deletion, verify:"
echo "  1. All secrets are in OCI Vault: oci vault secret list --compartment-id <ocid> --profile $PROFILE"
echo "  2. Backup location (if used): $BACKUP_DIR"
echo "  3. No important unmerged branches"
echo "  4. Repository is not needed anymore"
```

## Notes

- **OCI Vault Setup**: If vaults don't exist, they need to be created first or use alternative backup methods
- **Secret Naming (Real Pattern)**: `{repo-name}-[{env-tier}-]{secret-type}` — not `{repo}-{secret}-{env}`
  - **CRITICAL FINDING**: Secrets organized by NAMING PREFIX ONLY (no OCI logical compartments inside vaults)
  - **DEV Vault**: `shared-apps-ddf-dev` (36 secrets)
  - **PRD Vault**: `deployer-ddf-vault` (7 secrets, not `shared-apps-ddf-prd`)
- **Compartment Names**: IAM compartments are `apps-ddf-dev` and `apps-ddf-prd`; NO logical compartments inside vaults
- **Secret Organization**: By naming prefix convention only (requires naming discipline)
- **Canonical Branches**: Always excluded from unmerged branch checks
- **Safety First**: This command prioritizes safety - it identifies issues but does not force deletion

### v1.1.0 Improvements (Temporary Directories & Committable Configs)

**Learning: `.tmp/` Directory Analysis**

- Temporary directories often contain self-documentation (README.md) that explicitly states they're disposable
- Example from real use case: `.tmp/README.md` contained "After completing all work, you can safely remove this directory"
- The command now checks for disposal markers: README.md with disposal keywords, `.disposable` files
- This prevents wasting time analyzing files that are designed to be thrown away

**Learning: Committable Gitignored Files**

- Some gitignored files contain **project-specific settings** that SHOULD be committed to help all developers
- Example: `.vscode/settings.json` with:
  - `python.defaultInterpreterPath` - tells devs where venv is
  - `python.analysis.extraPaths` - helps with import resolution
  - `editor.tabSize`, `editor.rulers` - coding standards (e.g., Black's 88/120 line limits)
  - `editor.defaultFormatter` - team formatter choice
- These are NOT personal preferences - they're team conventions that reduce onboarding friction
- The command now flags these files and recommends committing a clean version (without personal settings like `terminal.*`) before deletion

## Related Commands

- `/gsyn_git_sync` - Git synchronization
- `/arch_archive` - Archive repository before deletion
- `/gful_git_full_sync` - Full git sync before deletion

## References

- `procedures/branch_environment_strategy.md` - OCI tenancy and compartment structure
- `mini_prompt/lv1/hardcoding_ports_ips_and_secrets_elimination_mini_prompt.md` - Secret management
- `_dev/scripts/cleanup_repository.sh` - Branch cleanup patterns
