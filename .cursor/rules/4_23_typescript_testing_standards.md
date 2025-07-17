# TypeScript Testing Standards

## Rule: 4_23_typescript_testing_standards

### Floor 3 TypeScript Compliance
**CRITICAL**: Floor 3 projects must use TypeScript exclusively in `src/` directory.
- ✅ `.ts`/`.tsx` files only
- ❌ `.js` files in `src/` (convert to TypeScript)
- ❌ `require()` statements (use ES modules)

### Pre-Commit TypeScript Testing
**MANDATORY**: All Floor 3 projects must include TypeScript compilation testing in pre-commit hooks.

#### Required Files:
1. `tests/typescript-compilation.test.js` - Jest test suite for TypeScript validation
2. `scripts/test-typescript.sh` - Standalone script for pre-commit hooks
3. `.husky/pre-commit` - Updated to include TypeScript compilation check

#### Implementation Pattern:
```bash
# In .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run TypeScript compilation test (Floor 3 standard)
echo "🔧 Running TypeScript compilation check..."
bash scripts/test-typescript.sh

npx lint-staged
```

#### Package.json Script:
```json
{
  "scripts": {
    "test:typescript": "bash scripts/test-typescript.sh"
  }
}
```

### Test Coverage Requirements:
1. **Compilation Check**: `npx tsc --noEmit --project .`
2. **Config Validation**: Verify `tsconfig.json` files are valid
3. **Floor 3 Compliance**: Check for `.js` files in `src/` (warn only)
4. **Build Process**: Verify `npm run build` succeeds
5. **Strict Mode**: Check strict TypeScript compliance (warn only)

### Enforcement:
- **Pre-commit**: MUST pass TypeScript compilation before commit
- **CI/CD**: Include TypeScript tests in build pipeline
- **Floor Compliance**: Warn about `.js` files, encourage migration

### Fast Failure:
- Use timeouts for external commands
- Provide clear error messages with quick fixes
- Log TypeScript errors with file locations

### Benefits:
- Catch TypeScript errors before deployment
- Enforce Floor 3 standards automatically
- Provide immediate feedback to developers
- Prevent broken builds in CI/CD pipeline

## Usage:
**USE WHEN**: Setting up new Floor 3 projects or adding TypeScript compliance to existing projects
**ENFORCE**: All commits must pass TypeScript compilation in Floor 3 projects
