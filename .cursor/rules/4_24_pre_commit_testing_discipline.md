# Pre-Commit Testing Discipline

## Rule: 4_24_pre_commit_testing_discipline

### Core Principle
**NEVER allow broken code to be committed.** Pre-commit hooks must catch errors before they enter the repository.

### Required Pre-Commit Checks (by Floor):

#### Floor 2 (Scalable Frameworks):
- ✅ Basic linting
- ✅ Unit tests (if any)
- ✅ Format validation

#### Floor 3 (Production Grade):
- ✅ TypeScript compilation (`scripts/test-typescript.sh`)
- ✅ Full test suite
- ✅ Linting and formatting
- ✅ Type checking
- ✅ Build process validation

### Pre-Commit Hook Structure:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Floor 3: TypeScript compilation check
echo "🔧 Running TypeScript compilation check..."
bash scripts/test-typescript.sh

# Standard linting and formatting
npx lint-staged

# Additional Floor 3 checks can be added here
```

### Test Script Requirements:
1. **Fast Execution**: Tests should complete in < 30 seconds
2. **Clear Output**: Use colored status indicators (✅❌⚠️)
3. **Helpful Errors**: Provide specific fixes for common issues
4. **Graceful Degradation**: Warn but don't fail for optional checks

### Error Handling Pattern:
```bash
# Use timeouts for potentially hanging commands
if timeout 30s npx tsc --noEmit --project . 2>&1; then
    print_status "SUCCESS" "TypeScript compilation successful"
else
    print_status "ERROR" "TypeScript compilation failed"
    echo "🔧 Quick fixes:"
    echo "  - Check syntax errors in .ts/.tsx files"
    echo "  - Run: npm install (missing dependencies)"
    exit 1
fi
```

### Bypass Procedures:
**ONLY in emergency situations with explicit authorization:**
- Document reason in commit message
- Create follow-up task to fix underlying issue
- Use `git commit --no-verify` (requires authorization per workspace rules)

### Benefits:
- Prevents broken builds from entering main branch
- Enforces code quality standards automatically
- Provides immediate developer feedback
- Reduces CI/CD pipeline failures
- Maintains repository health

## Usage:
**USE WHEN**: Setting up new repositories or improving existing pre-commit processes
**ENFORCE**: All Floor 3 projects must have comprehensive pre-commit testing
