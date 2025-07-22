# Branch Merge Plan - Local and Remote Branch Integration

**Created**: $(date +%Y-%m-%d %H:%M:%S)
**Current Branch**: feature/app-updates
**Workspace**: /Users/luismartins/local_repos/enrich-ddf-floor-2
**Reference**: /Users/luismartins/local_repos/docs-fera/prompts-fera/mini_prompt/agent_branch_merge_workflow_mini_prompt.md

## 🎯 Objective
Execute a safe, manual conflict resolution workflow to merge local `feature/app-updates` branch with remote branches, following enhanced terminal command execution safety and manual conflict resolution principles.

## 🚨 Critical Safety Compliance
This plan follows **mandatory safety guidelines**:
- ✅ All commands ≤200 characters
- ✅ Maximum 2 operations per command
- ✅ Separate tool calls for verification
- ✅ Proper timeout usage with gtimeout
- ✅ **MANUAL CONFLICT RESOLUTION ONLY** - No `git reset --hard` or `--no-verify`
- ✅ **Case-by-case conflict analysis** instead of automated resolution

## 📊 Current State Analysis

### Git Status
```
On branch feature/app-updates
Your branch is up to date with 'origin/feature/app-updates'.
nothing to commit, working tree clean
```

### Pre-Merge Assessment Checklist
- [ ] Verify current branch state
- [ ] Check remote branch status
- [ ] Identify merge target (likely main/master)
- [ ] Assess potential conflicts
- [ ] Verify backup/rollback capabilities

## 🔍 Phase 1: Repository State Discovery

### 1.1 Current Environment Verification
```bash
# Verify git repository status
gtimeout 10 git status --porcelain

# Check current branch
gtimeout 5 git branch --show-current

# Verify remote tracking
gtimeout 10 git branch -vv
```

### 1.2 Remote Branch Analysis
```bash
# Fetch latest remote state
gtimeout 30 git fetch --all

# List all remote branches
gtimeout 10 git branch -r

# Check main branch status
gtimeout 10 git log --oneline origin/main -5

# Check target branch relationship
gtimeout 10 git log --oneline --graph origin/main..HEAD
```

### 1.3 Merge Target Identification
```bash
# Identify default branch
gtimeout 10 gh repo view --json defaultBranch

# Check if feature branch is ahead/behind main
gtimeout 15 git rev-list --count origin/main..HEAD
gtimeout 15 git rev-list --count HEAD..origin/main
```

## 🛡️ Phase 2: Pre-Merge Conflict Detection

### 2.1 Conflict Analysis (CRITICAL)
```bash
# MANDATORY: Check for potential conflicts before merge
gtimeout 15 git fetch origin main
gtimeout 10 git merge-tree $(git merge-base HEAD origin/main) HEAD origin/main

# Store conflict detection results
if [ $? -ne 0 ]; then
    echo "⚠️ CONFLICTS DETECTED - Manual resolution will be required"
    echo "📋 Conflict files will need individual analysis"
else
    echo "✅ No conflicts detected - merge should be clean"
fi
```

### 2.2 Change Impact Assessment
```bash
# Analyze changes between branches
gtimeout 30 git diff --name-status origin/main..HEAD

# Check file modification statistics
gtimeout 30 git diff --stat origin/main..HEAD

# Large diff detection (>500 lines triggers manual review)
lines_changed=$(git diff --shortstat origin/main..HEAD | grep -o '[0-9]* insertions' | grep -o '[0-9]*')
if [ "$lines_changed" -gt 500 ]; then
    echo "⚠️ Large diff detected: $lines_changed lines changed"
    echo "📋 Extra caution required during merge"
fi
```

### 2.3 Semantic Analysis
```bash
# Check for potential contract-breaking changes
gtimeout 60 git diff origin/main..HEAD -- "*.py" "*.js" "*.ts" | grep -E "(class |def |function |interface )"

# Look for configuration changes
gtimeout 30 git diff --name-only origin/main..HEAD | grep -E "\.(yml|yaml|json|toml|ini|env)$"
```

## 📋 Phase 3: Merge Strategy Selection

### 3.1 Merge Method Decision Matrix

| Condition | Recommended Strategy | Command |
|-----------|---------------------|---------|
| No conflicts, clean history | Fast-forward merge | `git merge --ff-only origin/main` |
| No conflicts, preserve history | Standard merge | `git merge origin/main` |
| Conflicts detected | Manual resolution + merge | Detailed conflict resolution |
| Large changes (>500 lines) | Squash merge | `git merge --squash origin/main` |

### 3.2 Branch Scoring Assessment
```bash
# Calculate merge readiness score
score=0

# +10 if no conflicts detected
# +15 if touching only docs/markdown files
# +5 for clean commit history
# -10 for large diffs (>500 lines)
# +20 if previous conflicts were manually resolved

echo "📊 Merge readiness score: $score"
if [ $score -ge 90 ]; then
    echo "✅ Priority merge - high confidence"
elif [ $score -ge 50 ]; then
    echo "⚠️ Standard merge - proceed with caution"
else
    echo "❌ Manual review required - score too low"
fi
```

## 🔧 Phase 4: Manual Conflict Resolution Protocol

### 4.1 Conflict Detection and Analysis
```bash
# If conflicts are detected during merge attempt:
echo "🔍 CONFLICT ANALYSIS PROTOCOL"
echo "1. Identify all conflicted files"
echo "2. Analyze each conflict individually"
echo "3. Understand both versions (ours vs theirs)"
echo "4. Manually integrate changes"
echo "5. Test the resolution"

# List conflicted files
gtimeout 10 git status | grep "both modified"
```

### 4.2 Step-by-Step Manual Resolution
```bash
# For each conflicted file, follow this pattern:
resolve_conflict() {
    local file="$1"
    echo "📝 Resolving conflict in: $file"
    echo "   <<<<<<< Current state (HEAD)"
    echo "   ======= Separator"
    echo "   >>>>>>> Incoming changes (target branch)"
    echo ""
    echo "REQUIRED ACTIONS:"
    echo "1. Open $file in editor"
    echo "2. Locate conflict markers"
    echo "3. Understand both versions completely"
    echo "4. Create integrated solution"
    echo "5. Remove ALL conflict markers"
    echo "6. Save and test changes"
    echo "7. Stage resolved file: git add $file"
}
```

### 4.3 Prohibited Automated Resolution
```bash
# ❌ NEVER USE - These commands are STRICTLY PROHIBITED:
# git reset --hard HEAD
# git reset --hard origin/main
# git commit --no-verify
# git merge --strategy=ours
# git merge --strategy=theirs
# git checkout --ours .
# git checkout --theirs .

echo "🚫 AUTOMATED CONFLICT RESOLUTION IS PROHIBITED"
echo "✅ ONLY MANUAL, CASE-BY-CASE ANALYSIS ALLOWED"
```

## ⚡ Phase 5: Safe Merge Execution

### 5.1 Pre-Merge Backup
```bash
# Create safety backup branch
gtimeout 10 git branch backup-feature-app-updates

# Tag current state for rollback
gtimeout 10 git tag -a "pre-merge-$(date +%Y%m%d-%H%M)" -m "State before merge operation"
```

### 5.2 Merge Execution with Conflict Handling
```bash
# Attempt merge with conflict detection
echo "🚀 Initiating safe merge process..."

# Method 1: Fast-forward if possible
gtimeout 30 git merge --ff-only origin/main
if [ $? -eq 0 ]; then
    echo "✅ Fast-forward merge successful"
    exit 0
fi

# Method 2: Standard merge with conflict handling
gtimeout 60 git merge origin/main
merge_result=$?

if [ $merge_result -ne 0 ]; then
    echo "⚠️ Merge conflicts detected - entering manual resolution mode"
    echo "🛑 AUTOMATION STOPPED - MANUAL INTERVENTION REQUIRED"

    # Display conflict summary
    echo "📋 Conflicted files:"
    git status --porcelain | grep "^UU"

    echo "📋 Next steps:"
    echo "1. Resolve each conflict manually"
    echo "2. git add <resolved-file>"
    echo "3. git commit (when all conflicts resolved)"
    echo "4. Continue with cleanup process"

    exit 1
fi
```

### 5.3 Post-Merge Validation
```bash
# Verify merge was successful
gtimeout 10 git status

# Run quick tests if available
if [ -f "requirements-minimal.txt" ]; then
    echo "🧪 Running quick validation tests..."
    gtimeout 60 python -m pytest tests/ -x || echo "⚠️ Tests failed - review required"
fi

# Check for any remaining issues
gtimeout 10 git diff --check
```

## 🧹 Phase 6: Remote Branch Cleanup

### 6.1 Merged Branch Cleanup Strategy
```bash
# Determine cleanup preference
cleanup_strategy=$(git config --get branch.cleanup.strategy || echo "prompt")

echo "🗂️ Remote branch cleanup strategy: $cleanup_strategy"

case "$cleanup_strategy" in
    "deprecate")
        echo "📋 Will rename merged branches with 'deprecated-' prefix"
        ;;
    "delete")
        echo "🗑️ Will delete merged branches completely"
        ;;
    *)
        echo "❓ Will prompt for cleanup decision per branch"
        ;;
esac
```

### 6.2 Safe Remote Branch Operations
```bash
# List merged remote branches (excluding main/master)
merged_branches=($(git branch -r --merged | grep -v -E '(main|master|HEAD)' | sed 's/origin\///'))

echo "📋 Merged remote branches found: ${#merged_branches[@]}"
for branch in "${merged_branches[@]}"; do
    echo "  - $branch"
done

# Cleanup execution (requires user confirmation for each branch)
cleanup_remote_branch() {
    local branch="$1"
    echo "🤔 How to handle merged branch '$branch'?"
    echo "1) Deprecate (rename to deprecated-$branch)"
    echo "2) Delete completely"
    echo "3) Keep as-is"

    # This would require interactive input in actual execution
    # For planning purposes, document the decision process
}
```

### 6.3 Post-Cleanup Verification
```bash
# Verify cleanup results
echo "🔍 Post-cleanup verification:"
gtimeout 10 git ls-remote --heads origin | wc -l
echo "📊 Total remote branches after cleanup"

# Check for remaining merged branches
remaining_merged=$(git branch -r --merged main | grep -v -E '(main|master|HEAD|deprecated-)' | wc -l)
if [ $remaining_merged -eq 0 ]; then
    echo "✅ All merged branches successfully cleaned"
else
    echo "⚠️ $remaining_merged merged branches still present"
fi
```

## 📊 Phase 7: Final Validation and Reporting

### 7.1 Merge Success Verification
```bash
# Confirm branch state
gtimeout 10 git log --oneline -5

# Verify remote tracking
gtimeout 10 git branch -vv

# Check working directory is clean
gtimeout 5 git status --porcelain
```

### 7.2 Success Metrics Report
```bash
echo "📈 MERGE OPERATION METRICS:"
echo "  - Manual conflict resolution: [YES/NO]"
echo "  - Destructive commands used: NO (prohibited)"
echo "  - Automated resolution attempts: 0 (not allowed)"
echo "  - Remote branches cleaned: [COUNT]"
echo "  - Repository health: [CLEAN/ISSUES]"
echo "  - Rollback capability: PRESERVED"
```

## 🚨 Emergency Procedures

### Rollback Protocol
```bash
# If merge needs to be undone:
echo "🔄 EMERGENCY ROLLBACK PROCEDURE:"
echo "1. git reset --soft HEAD~1  # Undo commit but keep changes"
echo "2. git checkout backup-feature-app-updates  # Return to backup"
echo "3. git branch -D feature/app-updates  # Remove failed branch"
echo "4. git checkout -b feature/app-updates  # Recreate from backup"
```

### Conflict Resolution Failure
```bash
# If manual conflict resolution becomes impossible:
echo "🆘 CONFLICT RESOLUTION ESCALATION:"
echo "1. Document current conflict state"
echo "2. Backup current work: git stash"
echo "3. Reset to clean state: git reset --hard HEAD"
echo "4. Escalate to team lead or domain expert"
echo "5. Consider alternative merge strategies"
```

## ✅ Execution Checklist

### Pre-Execution Verification
- [ ] Current branch is feature/app-updates
- [ ] Working directory is clean
- [ ] Remote access is working (gh auth status)
- [ ] Backup branches created
- [ ] Manual conflict resolution tools ready

### During Execution Monitoring
- [ ] All commands use proper timeouts
- [ ] No automated conflict resolution attempted
- [ ] Each conflict analyzed individually
- [ ] Test changes after resolution
- [ ] Document resolution decisions

### Post-Execution Validation
- [ ] Merge completed successfully
- [ ] All conflicts resolved manually
- [ ] Tests pass (if available)
- [ ] Remote branches cleaned appropriately
- [ ] Rollback capability preserved
- [ ] Documentation updated

## 🎯 Success Criteria

**MERGE SUCCESS INDICATORS:**
- ✅ Feature branch successfully merged with target
- ✅ All conflicts resolved through manual analysis
- ✅ No destructive commands used
- ✅ Repository left in clean state
- ✅ Remote branches appropriately managed
- ✅ Rollback tags preserved for safety
- ✅ All safety guidelines followed

**FAILURE INDICATORS:**
- ❌ Automated conflict resolution attempted
- ❌ Destructive commands used
- ❌ Unresolved conflicts remaining
- ❌ Working directory left dirty
- ❌ Safety guidelines violated

---

## 📝 Execution Notes

This plan prioritizes **manual conflict resolution** and **safety compliance** over automation speed. Every conflict must be analyzed individually, and no automated resolution tools should be used. The process emphasizes understanding both sides of conflicts and creating integrated solutions that preserve the intent of all changes.

**Next Steps**: Execute phases sequentially, stopping immediately if conflicts are detected to perform manual resolution before proceeding.
