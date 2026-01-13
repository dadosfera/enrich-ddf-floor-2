# /btex_batch_execute_massive_scope

<!-- COMMAND_ID: 064 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ba_batch_execute -->

Execute massive scope work on existing central plans with batches. **Detects existing central plans** created by `/crpl_create_central_plan_massive_scope` and starts agent work on available batches. **Agents work on ONE batch only** - do not suggest working on other batches.

**🚨 CRITICAL**: When a batch is locked by another agent, **automatically check the next batch** without asking the user. Continue sequentially (Batch 1 → 2 → 3 → ...) until you find an available batch. Only report if ALL batches are locked. Never ask "which batch should I work on?" - just automatically proceed.

**Local Reference**: `commands/btex_batch_execute_massive_scope.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/btex_batch_execute_massive_scope.md

**Note**: This command is repo-aware. For -fera repositories, plans are stored in `_dev/docs/plans/`. For all other repositories, plans are stored in `docs/plans/`.

Backlinks:
- mini_prompt/lv2/batch_execution_massive_scope_mini_prompt.md
- commands/xect_execute_plan.md (similar locking mechanism)

## Purpose

Handle massive scope work that would be overwhelming as a single plan:
- Thousands of linting errors
- Hundreds of test failures
- Hundreds of duplicate files
- Large-scale refactoring tasks

This command creates a **central plan** listing all problems, then divides work into **batches** (typically 5 items per batch) with individual batch plans. Each batch uses a locking mechanism to prevent conflicts when multiple agents work sequentially.

## When to Use

- When facing 100+ linting errors that need systematic fixing
- When dealing with 50+ test failures that need categorization
- When consolidating 100+ duplicate files
- When refactoring affects hundreds of files
- When work scope is too large for a single plan

## When NOT to Use

- For small scope work (< 20 items) - use regular `/xect_execute_plan` instead
- For single-file fixes - use direct execution
- For exploratory work - use `/expp_xpand_plan` instead

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

### Phase 2: Collect All Problems

```bash
# Run analysis to collect all problems
# Example for linting errors:
# npx eslint . --format json > .tmp/linting_errors.json

# Example for test failures:
# npm test -- --reporter=json > .tmp/test_failures.json

# Count total problems
TOTAL_PROBLEMS=$(jq '.length' .tmp/${PROBLEM_TYPE}.json 2>/dev/null || echo "0")

if [ "$TOTAL_PROBLEMS" -lt 20 ]; then
  echo "⚠️  Only $TOTAL_PROBLEMS problems found. Consider using /xect_execute_plan instead."
  exit 1
fi

echo "📊 Found $TOTAL_PROBLEMS problems to fix"
```

### Phase 3: Create Central Plan

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

EOF

echo "✅ Created central plan: $CENTRAL_PLAN"
```

### Phase 4: Create Batch Plans

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

  # Extract problems for this batch
  jq ".[$((BATCH_START-1)):$BATCH_END]" .tmp/${PROBLEM_TYPE}.json > .tmp/batch_${BATCH_NUM}.json

  # Create batch plan
  cat > "$BATCH_PLAN" << EOF
# ${PROBLEM_TYPE^} Batch $(printf "%02d" $BATCH_NUM)

**Status**: 🔓 Available
**Priority**: P0 - CRITICAL
**Created**: $(date +%Y-%m-%d)
**Batch**: $BATCH_NUM of $NUM_BATCHES
**Central Plan**: \`$(basename "$CENTRAL_PLAN")\`

## 📋 Problems in This Batch ($((BATCH_END - BATCH_START + 1)) items)

<!-- Problems will be listed here -->

## 🎯 Objectives

- Fix all problems in this batch
- Ensure no regressions
- Update batch plan with progress

## ✅ Completion Criteria

- All problems in batch fixed
- No new problems introduced
- All tests/linting passing for this batch

## 🔒 Locking Instructions

When starting work on this batch:
1. **CRITICAL: Check if batch is already locked**:
   ```bash
   ls ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).locked.*.md 2>/dev/null
   ```
   - **If files found**: Batch already locked - **IMMEDIATELY check the next batch** (Batch N+1) without asking the user
   - **If no files found**: Batch is available - proceed to step 2
2. **CRITICAL: Verify original batch file exists**:
   ```bash
   test -f ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md
   ```
   - **If file does NOT exist**: Batch may have been locked/renamed between checks - **IMMEDIATELY check the next batch**
   - **If file exists**: Proceed to step 3
3. Generate unique 5-letter hash (e.g., \`a3f7k\`)
4. Check no other \`.locked.{hash}.md\` files exist in \`/active\` (verify agent ID uniqueness)
5. **🚨 CRITICAL: ATOMIC RENAME (NOT COPY)**:
   ```bash
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md \
      ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).locked.{hash}.md
   ```
   - **MUST use `mv` command** (move/rename) - this is an atomic operation
   - **NEVER use `cp`** (copy) - this creates duplicates
   - **NEVER read + write + delete** - this is not atomic and causes race conditions
   - **If `mv` fails**: File was locked by another agent - **IMMEDIATELY check the next batch**
6. **Verify lock succeeded**:
   ```bash
   test -f ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).locked.{hash}.md
   ```
   - **If file exists**: Lock successful - proceed to step 7
   - **If file does NOT exist**: Lock failed - **IMMEDIATELY check the next batch**
7. Update central plan status to \`🔒 Locked by {hash}\`
8. Work on fixes (this is YOUR batch - work on this ONE batch only)

**IMPORTANT**:
- **ALWAYS use `mv` (rename), NEVER `cp` (copy)**
- If this batch is locked, **do not report it to the user or ask what to do**. Simply check the next batch number automatically and continue until you find an available one.

## 📦 Completion Workflow

When YOUR batch is complete:
1. **Unlock the batch** (atomic rename back):
   ```bash
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).locked.{hash}.md \
      ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md
   ```
   - **MUST use `mv` command** (move/rename) - this is an atomic operation
   - **NEVER use `cp`** (copy) - this creates duplicates
2. Update central plan: \`🔒 Locked by {hash}\` → \`✅ Completed\`
3. **Move THIS batch plan to \`/finished\`** (your batch work is done):
   ```bash
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md \
      ${PLANS_BASE}/finished/${PROBLEM_TYPE^^}_BATCH_$(printf "%02d" $BATCH_NUM).md
   ```
   - **MUST use `mv` command** to move the file
4. **Stop here** - do NOT suggest working on other batches

**If you're the last agent** (all other batches show \`✅ Completed\` in central plan):
1. Complete your batch (steps above)
2. Review central plan - verify all batches completed
3. **Move central plan to \`/finished\`** (all work complete)
EOF

  echo "✅ Created batch plan: $BATCH_PLAN"
done

# Update central plan with batch references
# (AI agent should update the central plan file)
```

### Phase 5: Execute First Batch

```bash
# List available batches
echo ""
echo "📦 Available batches:"
find "${PLANS_BASE}/active" -name "${PROBLEM_TYPE^^}_BATCH_*.md" ! -name "*.locked.*" | sort
```

## 📋 Agent Workflow: How to Start Working on Batches

**This workflow is embedded directly in this command for self-contained execution.**

**When an agent starts working on batches, follow this exact workflow:**

### 🔑 CRITICAL: Your Agent ID

**You MUST generate and remember a unique 5-letter alphanumeric ID** (e.g., `a3f7k`, `x9m2p`).

**Why this matters:**
- Your ID appears in the locked filename: `${PROBLEM_TYPE^^}_BATCH_01.locked.{YOUR_ID}.md`
- Your ID appears in your conversation messages
- **This connection lets you (and others) know which agent is working on which batch**
- **If you forget your ID, check the locked filename to recover it**

**Start every response with: `**Agent ID**: {YOUR_ID}`**

### 📝 Workflow (8 Steps)

1. **Check Available Batches**
   - Read `${PLANS_BASE}/active/${PROBLEM_TYPE^^}_CENTRAL_PLAN_*.md`
   - Find first batch marked `🔓 Available`
   - If all locked, wait or check back

2. **Check Batch is Not Already Locked** ⚠️ CRITICAL
   ```bash
   # Check if batch file already has a .locked.* extension
   ls ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.locked.*.md 2>/dev/null
   ```
   - **If MULTIPLE files found**: Lock conflict detected - **DO NOT work on this batch**, report conflict and find another available batch
   - **If ONE file found**: Batch already locked by another agent - **IMMEDIATELY check the next batch** without asking the user
   - **If no files found**: Batch is available - proceed to step 3

   **Lock Conflict Detection**:
   ```bash
   # Count lock files - if more than 1, there's a conflict
   LOCK_COUNT=$(ls ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.locked.*.md 2>/dev/null | wc -l | tr -d ' ')
   if [ "$LOCK_COUNT" -gt 1 ]; then
     echo "⚠️ Lock conflict: Multiple lock files detected for this batch"
     # Report and move to next batch
   fi
   ```

3. **Generate Your Agent ID**
   - Create 5-letter alphanumeric ID (lowercase + numbers)
   - **Write it at top of your response**
   - **Include it in every message about this work**

4. **Verify ID is Unique**
   ```bash
   grep -r "\.locked\.{YOUR_ID}\.md" ${PLANS_BASE}/active/
   ```
   - If found, generate new ID
   - If not found, proceed

5. **Lock the Batch** 🚨 CRITICAL: Use atomic rename
   ```bash
   # CRITICAL: Use mv (move/rename) - this is atomic
   # NEVER use cp (copy) - this creates duplicates
   # NEVER read + write + delete - this causes race conditions
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.md \
      ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.locked.{YOUR_ID}.md

   # Verify lock succeeded
   if [ ! -f "${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.locked.{YOUR_ID}.md" ]; then
     echo "❌ Lock failed - file was locked by another agent"
     # IMMEDIATELY check the next batch
   fi
   ```
   - **MUST use `mv` command** (move/rename) - this is an atomic operation
   - **NEVER use `cp`** (copy) - this creates duplicates and lock conflicts
   - **NEVER read + write + delete** - this is not atomic and causes race conditions
   - **If `mv` fails or verification fails**: File was locked by another agent - **IMMEDIATELY check the next batch**

6. **Update Central Plan**
   - Edit `${PROBLEM_TYPE^^}_CENTRAL_PLAN_*.md`
   - Change: `🔓 Available` → `🔒 Locked by {YOUR_ID}`

7. **Fix the Problems**
   - Read the locked batch plan
   - Fix all problems listed in the batch
   - **Keep your ID in conversation context!**

8. **Unlock When Done** 🚨 CRITICAL: Use atomic rename
   ```bash
   # Unlock: atomic rename back
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.locked.{YOUR_ID}.md \
      ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.md

   # Move to finished: atomic move
   mv ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_XX.md \
      ${PLANS_BASE}/finished/${PROBLEM_TYPE^^}_BATCH_XX.md
   ```
   - **MUST use `mv` command** (move/rename) - this is an atomic operation
   - **NEVER use `cp`** (copy) - this creates duplicates
   - Update central plan: `🔒 Locked by {YOUR_ID}` → `✅ Completed`
   - **Move batch plan to `/finished`** (your batch work is complete)
   - **Do NOT suggest working on other batches** - you work on ONE batch only
   - **If you're the last agent** (all other batches completed), review central plan and move it to `/finished`

### ⚠️ Key Rules

- ✅ **Check locks first** (agents work sequentially)
- ✅ **Lock before working** (prevent conflicts)
- ✅ **Remember your ID** (it's your identity - check filename if forgotten)
- ✅ **Update status** (keep central plan synchronized)
- ✅ **Unlock when done** (don't leave files locked)
- ✅ **Work on ONE batch only** - do not suggest working on other batches after completion
- ✅ **Move batch to `/finished`** when your batch is complete
- ✅ **Central plan stays in `/active`** until ALL batches are done
- ✅ **Last agent** (when all batches complete) should review and move central plan to `/finished`

### 📋 Example Start Response

```
**Agent ID**: a3f7k

Starting work on Batch 1: TypeScript Errors - Files 1-5

1. ✅ Checked central plan - Batch 1 available
2. ✅ Verified batch not already locked (no .locked.* files found)
3. ✅ Generated agent ID: a3f7k
4. ✅ Verified ID unique
5. ✅ Locked: TYPESCRIPT_ERRORS_BATCH_01.locked.a3f7k.md
6. ✅ Updated central plan: 🔒 Locked by a3f7k

Now fixing the 5 files in this batch...
```

**Remember: Your ID connects your conversation to the locked plan file. Keep it visible!**

## 🎯 CRITICAL: Batch Selection Workflow

**When executing this command, you MUST follow this exact workflow:**

1. **Read the central plan** to identify all batches
2. **Start from Batch 1** and check availability:
   ```bash
   ls ${PLANS_BASE}/active/${PROBLEM_TYPE^^}_BATCH_01.locked.*.md 2>/dev/null
   ```
3. **If batch is LOCKED** (lock files exist):
   - **DO NOT ask the user what to do**
   - **DO NOT report that it's locked and stop**
   - **IMMEDIATELY proceed to the next batch** (Batch 2, then 3, then 4, etc.)
   - Continue checking sequentially until you find an available batch
4. **If batch is AVAILABLE** (no lock files):
   - Lock it immediately with your agent ID
   - Start working on it
   - **STOP HERE** - work only on this one batch
5. **If ALL batches are locked**:
   - Report: "All batches are currently locked by other agents. No work available at this time."
   - **DO NOT ask what to do next** - just report the status

**Key Rules:**
- ✅ **Automatically continue** to next batch if current batch is locked
- ✅ **Work on the first available batch** you find
- ✅ **Never ask for user input** about which batch to work on
- ❌ **Never stop and ask** "Should I work on Batch X?" when a batch is locked
- ❌ **Never report** "Batch X is locked, what should I do?" - just move to the next one

**Lock Conflict Detection**:
If you find multiple `.locked.*.md` files for the same batch (e.g., `BATCH_08.locked.BE66B.md` and `BATCH_08.locked.k9x2m.md`):
- **DO NOT work on this batch** - it has a lock conflict from a previous error
- **Report the conflict** briefly: "⚠️ Lock conflict detected on Batch X (multiple lock files)"
- **IMMEDIATELY check the next batch** without asking what to do
- The conflict will need manual resolution later, but you should continue with other batches

## Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│         /btex_batch_execute_massive_scope                    │
├─────────────────────────────────────────────────────────┤
│ 1. Identify problem scope (linting/test/duplicates)     │
│ 2. Collect all problems (run analysis tools)            │
│ 3. Create central plan listing all problems             │
│ 4. Divide into batches (5 items per batch)             │
│ 5. Create individual batch plans                        │
│ 6. Agents work sequentially - ONE batch per agent       │
│ 7. Batch plans move to /finished when complete          │
│ 8. Central plan moves to /finished when ALL done        │
└─────────────────────────────────────────────────────────┘
```

### Batch Selection Example

**Correct behavior** (automatic progression):
```
1. Check Batch 1 → Locked by agent "abc12"
2. Check Batch 2 → Locked by agent "xyz78"
3. Check Batch 3 → Locked by agent "def45"
4. Check Batch 4 → AVAILABLE ✅
5. Lock Batch 4 with agent ID "k9x2m"
6. Start working on Batch 4
7. Complete Batch 4
8. Report completion and stop
```

**Incorrect behavior** (asking user):
```
1. Check Batch 1 → Locked by agent "abc12"
2. ❌ "Batch 1 is locked. Should I work on Batch 2?"
3. ❌ "Multiple batches are locked. What should I do?"
4. ❌ "I found locked batches. Which batch should I work on?"
```

**Rule**: If a batch is locked, automatically check the next batch. Only report if ALL batches are locked.

## Examples

### Example 1: Linting Errors

```bash
# User: "I have 500 ESLint errors to fix"
/btex_batch_execute_massive_scope

# Command:
# 1. Runs: npx eslint . --format json > .tmp/linting_errors.json
# 2. Creates: LINTING_ERRORS_CENTRAL_PLAN_20260107.md
# 3. Creates: LINTING_ERRORS_BATCH_01.md through LINTING_ERRORS_BATCH_100.md
# 4. Each batch contains 5 linting errors to fix
```

### Example 2: Test Failures

```bash
# User: "I have 188 test failures"
/btex_batch_execute_massive_scope

# Command:
# 1. Runs: npm test -- --reporter=json > .tmp/test_failures.json
# 2. Creates: TEST_FAILURES_CENTRAL_PLAN_20260107.md
# 3. Creates: TEST_FAILURES_BATCH_01.md through TEST_FAILURES_BATCH_38.md
# 4. Each batch contains 5 test files to fix
```

### Example 3: Duplicate Files

```bash
# User: "I have 200 duplicate files to consolidate"
/btex_batch_execute_massive_scope

# Command:
# 1. Runs duplicate detection analysis
# 2. Creates: DUPLICATE_FILES_CENTRAL_PLAN_20260107.md
# 3. Creates batch plans for consolidation work
```

## Notes

- **Batch Size**: Default is 5 items per batch. Adjust based on complexity.
- **Locking**: Uses same mechanism as `/xect_execute_plan` but with agent IDs
- **Sequential Work**: Agents work one batch at a time, checking locks first
- **Single Batch Focus**: **Agents work on ONE batch only** - do not suggest working on other batches after completion
- **Progress Tracking**: Central plan tracks all batch statuses
- **Batch Completion**: When a batch is complete, move the batch plan to `/finished`
- **Central Plan Completion**: Central plan only moves to `/finished` when ALL batches are completed. The last agent to finish the last batch should review the central plan and move it to `/finished`

## Related Commands

- `/xect_execute_plan` - Execute single plan (for smaller scope)
- `/xqpa_xqt_plan_all` - Execute all plans (different use case)
- `/tall_tests_all` - Run all tests (for test failures context)

---

**End Command**
