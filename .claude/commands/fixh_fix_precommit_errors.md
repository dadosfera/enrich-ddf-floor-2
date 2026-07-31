---
# Dadosfera Metadata
category: quality
criticality: high
scope: all
commandId: "084"
version: "2.0.0"
type: "fi_fix_hooks"
canonical: "docs-fera@/commands/fixh_fix_precommit_errors.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/fixh_fix_precommit_errors.md"
backlinks:
  - "commands/hook_hooks_setup.md"
  - "standards/git/git_hooks_standard.md"
  - "mini_prompt/lv1/git_hooks_optimization_lv1_mini_prompt.md"
  - "commands/rerr_recurrent_errors.md"
  - "guides/hooks_guide.md"

# Claude Code Metadata
name: "Fix Pre-commit Errors"
description: "Diagnose and fix non-trivial git hook errors with root cause analysis and prevention"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 084 -->
<!-- COMMAND_VERSION: 2.0.0 -->
<!-- COMMAND_TYPE: fi_fix_hooks -->
# /fixh_fix_precommit_errors

**Command**: `/fixh_fix_precommit_errors`

Diagnose and fix non-trivial git commit gating errors (primarily pre-commit / pre-push / commit-msg) by analyzing failures, identifying root causes, fixing configuration issues, and improving the enforcement workflow when it causes recurring problems.

## Purpose

This command diagnoses and fixes **non-trivial** git hook errors that cannot be resolved by simple fixes like:
- Missing dependencies (use `/hook_hooks_setup` instead)
- First-time hook installation (use `/hook_hooks_setup` instead)
- Simple configuration typos (can be fixed manually)

This command handles complex scenarios such as:
- Hook logic errors (incorrect file detection, regex patterns, conditional logic)
- Performance issues causing timeouts or hangs
- Recurring hook failures that indicate hook design problems
- Configuration conflicts between multiple hook systems (pre-commit, husky, custom hooks)
- Environment-specific failures (path issues, permission problems, missing tools)
- Hook execution order problems
- False positives/negatives in hook validation

## When to Use

- Pre-commit or pre-push hooks are failing with non-trivial errors
- Hooks are blocking legitimate commits incorrectly
- Hooks are too slow or timing out
- Same hook error occurs repeatedly (>2-3 times)
- Hook configuration conflicts exist
- Hook logic needs improvement based on failure patterns
- Environment-specific hook failures that aren't simple dependency issues

## When NOT to Use

- Simple missing dependencies (install them manually or use `/hook_hooks_setup`)
- First-time hook setup (use `/hook_hooks_setup`)
- Trivial configuration typos (fix manually)
- Intentional hook bypasses (use proper justification and `/gbyp_git_protection_bypass` if needed)

## Quick usage tip (discoverability)

- To find this command quickly in the palette, type **`/fixh`**.
- Searching for **`/hook`** will usually match `hook_hooks_setup` instead, because this command is prefixed with `fixh_...`.

## Command Sequence

**All commands must be run individually with `run_terminal_cmd` using `gtimeout`, no chaining with `&&`, and no `--no-verify` flags unless the hook failures were already remediated and user authorization was explicitly obtained after checking for concurrent active AI sessions.**

### Phase 1: Error Diagnosis

**Purpose**: Understand what's failing and why.

1. **Verify repository context**

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. **Identify which hook is failing**

```bash
# Check if this is a pre-commit, pre-push, or commit-msg error
HOOK_TYPE="${1:-pre-commit}"  # Default to pre-commit if not specified
echo "Diagnosing $HOOK_TYPE hook errors..."
```

3. **Capture current hook error output**

```bash
# Try to reproduce the error
if [ "$HOOK_TYPE" = "pre-commit" ]; then
  gtimeout 60 pre-commit run --all-files 2>&1 | tee /tmp/hook_error_output.log || true
elif [ "$HOOK_TYPE" = "pre-push" ]; then
  gtimeout 60 git push --dry-run 2>&1 | tee /tmp/hook_error_output.log || true
else
  echo "Testing $HOOK_TYPE hook..."
  gtimeout 30 .git/hooks/$HOOK_TYPE 2>&1 | tee /tmp/hook_error_output.log || true
fi
```

4. **Analyze hook configuration**

```bash
# Check for pre-commit config
gtimeout 5 test -f .pre-commit-config.yaml && echo "Found .pre-commit-config.yaml" || echo "No .pre-commit-config.yaml"

# Check for husky hooks
gtimeout 5 test -d .husky && echo "Found .husky directory" || echo "No .husky directory"

# Check for custom hooks
gtimeout 10 find .git/hooks -type f -name "*" -not -name "*.sample" | head -20
```

5. **Check hook execution environment**

```bash
# Verify required tools are available
gtimeout 5 command -v pre-commit >/dev/null 2>&1 && echo "pre-commit: available" || echo "pre-commit: missing"
gtimeout 5 command -v node >/dev/null 2>&1 && echo "node: available" || echo "node: missing"
gtimeout 5 command -v python3 >/dev/null 2>&1 && echo "python3: available" || echo "python3: missing"

# Check hook permissions
gtimeout 5 ls -la .git/hooks/ | grep -E "(pre-commit|pre-push|commit-msg)"
```

6. **Analyze staged changes that trigger the error**

```bash
# See what files are staged
gtimeout 10 git diff --cached --name-status | head -30

# Check for problematic patterns
gtimeout 10 git diff --cached --name-only | grep -E "(\.cursorignore|\.dadosferaignore|\.gitignore)" || echo "No ignore files changed"
```

### Phase 2: Root Cause Analysis

**Purpose**: Identify the underlying cause of the hook failure.

7. **Read hook error output and identify patterns**

```bash
# Analyze the error log
gtimeout 10 cat /tmp/hook_error_output.log | head -50
```

**AI analyzes**: Look for patterns like:
- Timeout errors
- Permission denied
- Missing dependencies
- Logic errors (incorrect file matching, regex failures)
- Configuration conflicts
- Environment path issues

8. **Check hook script logic (if custom hooks exist)**

```bash
# If custom hooks exist, examine them
if [ -f ".git/hooks/pre-commit" ] && ! grep -q "pre-commit run" .git/hooks/pre-commit; then
  echo "Custom pre-commit hook found, analyzing..."
  gtimeout 10 head -100 .git/hooks/pre-commit
fi
```

9. **Check for hook conflicts**

```bash
# Check if multiple hook systems are active
HOOK_COUNT=$(gtimeout 10 find .git/hooks .husky -type f -name "pre-commit" 2>/dev/null | wc -l | tr -d ' ')
echo "Found $HOOK_COUNT pre-commit hook(s)"

# Check if pre-commit framework is properly installed
gtimeout 10 pre-commit --version 2>&1 || echo "pre-commit not available"
```

10. **Identify recurring error patterns**

```bash
# Check git log for recent hook-related commits
gtimeout 15 git log --oneline --since="2 weeks ago" --grep="hook\|pre-commit\|pre-push" | head -10

# Check if this error has been seen before
gtimeout 10 grep -r "hook.*error\|pre-commit.*fail" _dev/docs/recurrent_errors/ 2>/dev/null | head -5 || echo "No previous hook errors documented"
```

### Phase 3: Fix Implementation

**Purpose**: Apply fixes based on root cause analysis.

11. **Create backup of current hooks**

```bash
BACKUP_DIR=".git/hooks/backup_$(date +%Y%m%d_%H%M%S)"
gtimeout 5 mkdir -p "$BACKUP_DIR"
gtimeout 10 cp -r .git/hooks/* "$BACKUP_DIR/" 2>/dev/null || true
echo "Hooks backed up to: $BACKUP_DIR"
```

12. **Fix configuration issues**

**If `.pre-commit-config.yaml` has errors:**

```bash
# Validate pre-commit config
gtimeout 15 pre-commit validate-config 2>&1 | tee /tmp/precommit_validation.log || true

# AI analyzes validation errors and fixes them
# (This is done by AI using file editing tools)
```

**If hook logic has errors:**

```bash
# AI analyzes hook script and fixes logic errors
# (This is done by AI using file editing tools)
# Common fixes:
# - Fix regex patterns for file matching
# - Correct conditional logic
# - Fix path resolution issues
# - Add proper error handling
```

13. **Fix performance issues**

**If hooks are timing out:**

```bash
# Check hook execution time
START_TIME=$(date +%s)
gtimeout 60 pre-commit run --all-files >/dev/null 2>&1 || true
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Hook execution time: ${DURATION}s"

# If >30s, implement optimizations:
# - Add selective execution (only check changed files)
# - Add caching
# - Skip expensive checks for certain file types
# (This is done by AI using file editing tools)
```

14. **Fix environment issues**

**If paths or permissions are wrong:**

```bash
# Fix hook permissions
gtimeout 5 chmod +x .git/hooks/pre-commit .git/hooks/pre-push 2>/dev/null || true

# Fix path issues in hooks (AI edits hook files)
# (This is done by AI using file editing tools)
```

15. **Resolve hook conflicts**

**If multiple hook systems conflict:**

```bash
# Determine which system should be primary
# Usually: pre-commit framework > husky > custom hooks
# (This is done by AI analyzing and fixing configuration)
```

### Phase 4: Hook Improvement

**Purpose**: Improve hooks to prevent recurring failures.

16. **Add better error handling**

```bash
# AI improves hook scripts with:
# - Proper error messages
# - Graceful failure handling
# - Debug mode support
# (This is done by AI using file editing tools)
```

17. **Add selective execution for performance**

```bash
# AI modifies hooks to:
# - Only check changed files
# - Skip checks for certain patterns
# - Use caching for expensive operations
# (This is done by AI using file editing tools)
```

18. **Add criticality filtering for pre-push**

```bash
# AI adds criticality-based test filtering:
# - Critical changes: full test suite
# - High priority: focused tests
# - Medium/low: smoke tests or skip
# (This is done by AI using file editing tools)
```

19. **Improve hook validation logic**

```bash
# AI fixes false positives/negatives:
# - Correct file pattern matching
# - Fix regex patterns
# - Improve conditional logic
# - Add better edge case handling
# (This is done by AI using file editing tools)
```

### Phase 5: Testing and Validation

**Purpose**: Verify fixes work correctly.

20. **Test the fixed hooks**

```bash
# Test pre-commit hook
if [ "$HOOK_TYPE" = "pre-commit" ]; then
  echo "Testing fixed pre-commit hook..."
  gtimeout 60 pre-commit run --all-files || echo "Hook test completed with issues (review above)"
fi

# Test pre-push hook
if [ "$HOOK_TYPE" = "pre-push" ]; then
  echo "Testing fixed pre-push hook..."
  gtimeout 60 git push --dry-run || echo "Hook test completed with issues (review above)"
fi
```

21. **Verify hook performance**

```bash
# Measure execution time
START_TIME=$(date +%s)
gtimeout 60 pre-commit run --all-files >/dev/null 2>&1 || true
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ "$DURATION" -gt 30 ]; then
  echo "⚠️ WARNING: Hooks still slow (${DURATION}s). Consider further optimization."
else
  echo "✅ Hook performance acceptable: ${DURATION}s"
fi
```

22. **Test edge cases**

```bash
# Test with different file types
echo "# Test" > test.py && git add test.py
gtimeout 30 pre-commit run --files test.py || true
git reset HEAD test.py && rm test.py

# Test with empty commit
# Test with large changes
# Test with mixed file types
```

### Phase 6: Documentation and Cleanup

**Purpose**: Document the fix and prevent recurrence.

23. **Document recurring errors (if applicable)**

```bash
# If this error occurred >2 times, document it
if [ -d "_dev/docs/recurrent_errors" ] || [ -d "recurrent_errors" ]; then
  echo "Consider documenting this hook error if it recurs"
  # Use /rerr_recurrent_errors if needed
fi
```

24. **Update hook documentation**

```bash
# AI updates relevant documentation:
# - Hook setup guides
# - Troubleshooting docs
# - AGENTS.md files
# (This is done by AI using file editing tools)
```

25. **Stage and commit fixes**

```bash
gtimeout 10 git add -A
```

```bash
gtimeout 5 git status --short | head -30
```

```bash
# Run hooks to verify they work
gtimeout 60 pre-commit run --all-files || echo "Pre-commit had issues, review above"
```

```bash
# Re-stage if hooks modified files
gtimeout 10 git add -A
```

```bash
gtimeout 10 git commit -m "fix(hooks): resolve $HOOK_TYPE hook errors

- Fixed [specific issue identified]
- Improved [specific improvement made]
- Performance: [execution time before/after]
- Backup: $BACKUP_DIR"
```

## Common Scenarios

### Scenario 1: Hook Logic Error (False Positive)

**Symptoms**: Hook blocks legitimate commits (e.g., deletion of `.cline/` directory)

**Fix**:
1. Analyze hook script logic
2. Fix file pattern matching (e.g., handle deletions correctly)
3. Test with actual commit scenario
4. Improve hook to distinguish between creation and deletion

### Scenario 2: Performance Timeout

**Symptoms**: Hooks timeout or take >30 seconds

**Fix**:
1. Identify slow operations
2. Add selective execution (only check changed files)
3. Implement caching
4. Add criticality filtering for pre-push

### Scenario 3: Configuration Conflict

**Symptoms**: Multiple hook systems conflict (pre-commit + husky)

**Fix**:
1. Identify which system should be primary
2. Consolidate hook configuration
3. Remove duplicate hooks
4. Ensure proper execution order

### Scenario 4: Recurring Hook Failures

**Symptoms**: Same error occurs repeatedly

**Fix**:
1. Document error with `/rerr_recurrent_errors`
2. Improve hook logic to prevent recurrence
3. Add better error handling
4. Update hook design based on failure patterns

### Scenario 5: Environment-Specific Failures

**Symptoms**: Hooks work on some machines but not others

**Fix**:
1. Identify environment differences
2. Fix path resolution issues
3. Add environment detection
4. Make hooks more portable

## Constraints

### Must Do

- **Diagnose before fixing**: Always understand root cause before applying fixes
- **Backup hooks**: Always create backup before modifying hooks
- **Test fixes**: Always test hooks after fixing
- **Improve hooks**: When errors recur, improve hook design, don't just fix symptoms
- **Document recurring errors**: Use `/rerr_recurrent_errors` for patterns
- **Preserve functionality**: Don't remove valid checks when fixing errors
- **Use timeouts**: All commands must use `gtimeout` for safety

### Must Not Do

- **Bypass hooks**: Never use `--no-verify` unless explicitly authorized after fix-attempts and a concurrency check.
- **Remove valid checks**: Don't disable hooks to fix errors
- **Skip testing**: Always test fixes before committing
- **Ignore recurring patterns**: If error recurs >2 times, improve hook design
- **Chain commands**: Never chain commands with `&&`, run individually
- **Delete backups**: Keep hook backups for at least 7 days

## Output Format

The command should produce:

1. **Diagnosis Report**:
   - Hook type and error details
   - Root cause analysis
   - Affected files/configurations

2. **Fix Summary**:
   - Changes made
   - Performance improvements
   - Hook improvements

3. **Validation Results**:
   - Test results
   - Performance metrics
   - Edge case coverage

## Related Commands

- `/hook_hooks_setup` - Initial hook setup (use for simple setup issues)
- `/rerr_recurrent_errors` - Document recurring hook errors
- `/gbyp_git_protection_bypass` - Bypass hooks (only with proper justification)
- `/lint_lint` - Linting (may be called by hooks)

## Notes

- **Non-trivial focus**: This command is for complex hook issues, not simple setup problems
- **Improvement over fixing**: When errors recur, improve hook design rather than repeatedly fixing symptoms
- **Performance matters**: Hooks should execute quickly (<10s for pre-commit, <30s for pre-push)
- **Safety first**: Always backup hooks before modification
- **Test thoroughly**: Test fixes with various scenarios before committing

---

**Last Updated**: 2026-01-21
**Version**: 2.0.0

**Local Reference**: `commands/fixh_fix_precommit_errors.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/fixh_fix_precommit_errors.md`
