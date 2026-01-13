# /crpl_create_central_plan_massive_scope

<!-- COMMAND_ID: 065 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: cr_create_plan -->

Create a central plan and batch structure for massive scope work (thousands of linting errors, test failures, duplications). This command sets up the structure; agents use `/btex_batch_execute_massive_scope` to work on batches.

**Local Reference**: `commands/crpl_create_central_plan_massive_scope.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/crpl_create_central_plan_massive_scope.md

**Note**: This command is repo-aware. For -fera repositories, plans are stored in `_dev/docs/plans/`. For all other repositories, plans are stored in `docs/plans/`.

Backlinks:
- commands/btex_batch_execute_massive_scope.md (execution command)
- mini_prompt/lv2/batch_execution_massive_scope_mini_prompt.md

## Purpose

Create the organizational structure for massive scope work:
- Central plan listing all problems
- Batch plans dividing work into manageable chunks (5 items per batch)
- Locking mechanism setup

**This command creates the structure. Use `/btex_batch_execute_massive_scope` for agents to start working.**

## When to Use

- When facing 100+ linting errors that need systematic fixing
- When dealing with 50+ test failures that need categorization
- When consolidating 100+ duplicate files
- When refactoring affects hundreds of files
- **Before agents start working** - this sets up the batch structure

## When NOT to Use

- For small scope work (< 20 items) - use regular plan creation instead
- When central plan already exists - use `/btex_batch_execute_massive_scope` instead
- For agent execution - use `/btex_batch_execute_massive_scope` instead

## Command Sequence

### Phase 1: Identify the Problem Scope

```bash
# Confirm repository context
REPO_ROOT=$(gtimeout 5 git rev-parse --show-toplevel)

# Detect repository type for correct plan paths
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
  PLANS_BASE="_dev/docs/plans"
else
  PLANS_BASE="docs/plans"
fi

# Identify problem type from conversation context
# Examples:
# - "thousands of linting errors" → PROBLEM_TYPE="linting_errors"
# - "hundreds of test failures" → PROBLEM_TYPE="test_failures"
# - "duplicate files" → PROBLEM_TYPE="duplicate_files"
# - "TypeScript errors" → PROBLEM_TYPE="typescript_errors"

PROBLEM_TYPE="linting_errors"  # Extracted from conversation
```

### Phase 2: Check for Existing Central Plan

```bash
# Check if central plan already exists
EXISTING_PLAN=$(find "${PLANS_BASE}/active" -name "${PROBLEM_TYPE^^}_CENTRAL_PLAN*.md" | head -1)

if [ -n "$EXISTING_PLAN" ]; then
  echo "⚠️  Central plan already exists: $(basename "$EXISTING_PLAN")"
  echo "💡 Use /btex_batch_execute_massive_scope to start working on batches"
  echo "💡 Or delete existing plan if you want to recreate it"
  exit 1
fi
```

### Phase 3: Collect All Problems

```bash
# Run analysis to collect all problems
# Example for linting errors:
# npx eslint . --format json > .tmp/linting_errors.json

# Example for test failures:
# npm test -- --reporter=json > .tmp/test_failures.json

# Example for TypeScript errors:
# npx tsc --noEmit --skipLibCheck 2>&1 | grep "error TS" | sed 's/^\([^(]*\)(.*/\1/' | sort -u > .tmp/typescript_files_with_errors.txt

# Count total problems
TOTAL_PROBLEMS=$(jq '.length' .tmp/${PROBLEM_TYPE}.json 2>/dev/null || wc -l < .tmp/${PROBLEM_TYPE}_files_with_errors.txt 2>/dev/null || echo "0")

if [ "$TOTAL_PROBLEMS" -lt 20 ]; then
  echo "⚠️  Only $TOTAL_PROBLEMS problems found. Consider using regular plan creation instead."
  exit 1
fi

echo "📊 Found $TOTAL_PROBLEMS problems to fix"
```

### Phase 4: Create Central Plan

```bash
# Generate central plan filename
TIMESTAMP=$(date +%Y%m%d)
CENTRAL_PLAN="${PLANS_BASE}/active/${PROBLEM_TYPE^^}_CENTRAL_PLAN_${TIMESTAMP}.md"

# Create central plan structure
cat > "$CENTRAL_PLAN" << EOF
# ${PROBLEM_TYPE^} Central Plan

**Status**: 🔄 ACTIVE
**Priority**: P0 - CRITICAL
**Created**: $(date +%Y-%m-%d)
**Total Problems**: $TOTAL_PROBLEMS

## 📊 Current Status

- **Total Problems**: $TOTAL_PROBLEMS
- **Batches Created**: 0
- **Batches Completed**: 0
- **Batches In Progress**: 0

## 🎯 Objective

Systematically fix all $TOTAL_PROBLEMS ${PROBLEM_TYPE} by organizing them into manageable batches.

## 📋 Batch Plans

<!-- Batches will be listed here as they are created -->

## 🔒 Locking Mechanism

See: \`docs/plans/active/AI_AGENT_LOCKING_PROMPT.md\`

When an agent starts working on a batch:
1. Generate unique 5-letter agent ID
2. Lock batch: \`BATCH_XX_NAME.md\` → \`BATCH_XX_NAME.locked.{ID}.md\`
3. Update this central plan status
4. Work on fixes
5. Unlock when complete

## 📝 Progress Tracking

- **Total Batches**: 0 (will be calculated when batches are created)
- **Batches Completed**: 0
- **Batches In Progress**: 0
- **Batches Available**: 0

## 🎯 Success Criteria

- All problems fixed
- All batch plans moved to \`/finished\` upon completion
- Central plan moved to \`/finished\` when all batches complete

EOF

echo "✅ Created central plan: $CENTRAL_PLAN"
```

### Phase 5: Create Batch Plans

```bash
# Calculate number of batches (5 items per batch)
BATCH_SIZE=5
NUM_BATCHES=$(( (TOTAL_PROBLEMS + BATCH_SIZE - 1) / BATCH_SIZE ))

# Create batch plans
for BATCH_NUM in $(seq 1 $NUM_BATCHES); do
  BATCH_START=$(( (BATCH_NUM - 1) * BATCH_SIZE + 1 ))
  BATCH_END=$(( BATCH_NUM * BATCH_SIZE ))
  if [ $BATCH_END -gt $TOTAL_PROBLEMS ]; then
    BATCH_END=$TOTAL_PROBLEMS
  fi

  BATCH_PLAN="${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md"

  # Extract problems for this batch (format depends on problem type)
  # For JSON-based problems:
  # jq ".[$((BATCH_START-1)):$BATCH_END]" .tmp/${PROBLEM_TYPE}.json > .tmp/batch_${BATCH_NUM}.json
  # For file-list problems:
  # sed -n "${BATCH_START},${BATCH_END}p" .tmp/${PROBLEM_TYPE}_files_with_errors.txt > .tmp/batch_${BATCH_NUM}_files.txt

  # Create batch plan (content depends on problem type - AI agent should adapt)
  # See examples in batch_execute_massive_scope.md for structure

  echo "✅ Created batch plan: $BATCH_PLAN"
done

# Update central plan with batch references
# (AI agent should update the central plan file with batch list)
```

### Phase 6: Summary

```bash
echo ""
echo "✅ Central plan and batch structure created!"
echo "📋 Central Plan: $CENTRAL_PLAN"
echo "📦 Batches Created: $NUM_BATCHES"
echo ""
echo "📋 Next Steps:"
echo "1. Agents can now use /btex_batch_execute_massive_scope to start working"
echo "2. See: docs/plans/active/COPY_THIS_PROMPT.md for agent workflow"
```

## Examples

### Example 1: Create Structure for Linting Errors

```bash
# User: "I have 500 ESLint errors to fix"
/crpl_create_central_plan_massive_scope

# Command:
# 1. Runs: npx eslint . --format json > .tmp/linting_errors.json
# 2. Creates: LINTING_ERRORS_CENTRAL_PLAN_20260107.md
# 3. Creates: LINTING_ERRORS_BATCH_01.md through LINTING_ERRORS_BATCH_100.md
# 4. Agents then use /btex_batch_execute_massive_scope to work on batches
```

### Example 2: Create Structure for Test Failures

```bash
# User: "I have 188 test failures"
/crpl_create_central_plan_massive_scope

# Command:
# 1. Runs: npm test -- --reporter=json > .tmp/test_failures.json
# 2. Creates: TEST_FAILURES_CENTRAL_PLAN_20260107.md
# 3. Creates: TEST_FAILURES_BATCH_01.md through TEST_FAILURES_BATCH_38.md
# 4. Agents then use /btex_batch_execute_massive_scope to work on batches
```

## Notes

- **Separation of Concerns**: This command creates structure; `/btex_batch_execute_massive_scope` executes work
- **Idempotency**: Checks for existing central plans to prevent duplicates
- **Batch Size**: Default is 5 items per batch. Adjust based on complexity.
- **Problem Type Detection**: Extracts from conversation context

## Related Commands

- `/btex_batch_execute_massive_scope` - Execute work on existing central plan batches
- `/xect_execute_plan` - Execute single plan (for smaller scope)
- `/pfac_plan_from_active_tasks_conversation` - Create regular plans

---

**End Command**
