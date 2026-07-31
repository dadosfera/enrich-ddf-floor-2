---
category: planning
criticality: medium
scope: all
---
# /exal_xpand_all_active_plans
<!-- COMMAND_ID: 018 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_xpand_all_active_plans -->

Expand all active plans with detailed guidelines, macro strategy validation, and research findings to ensure comprehensive, actionable plans with clear acceptance criteria and implementation steps.

**Local Reference**: `commands/exal_xpand_all_active_plans.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/exal_xpand_all_active_plans.md`

Backlinks:
- commands/expp_xpand_plan.md
- commands/pfac_plan_from_active_tasks_conversation.md
- commands/reva_review_active_conversation.md

## When to Use

- When you have multiple active plans that all need expansion
- After creating several plans from conversations that feel sparse or incomplete
- Before starting execution on multiple complex or unfamiliar tasks
- When you want to ensure all active plans meet the minimum 500-line standard
- When you need to validate approaches across multiple plans against current best practices

## When NOT to Use

- For expanding a single plan (use /expp_xpand_plan instead)
- For simple, well-understood tasks (< 1 hour effort per plan)
- When plans already have detailed acceptance criteria and steps (> 1000 lines each)
- For urgent fixes where speed is critical
- When working offline (web search will be skipped automatically)

## Command sequence (run in order)

### 1. Validate repository context and discover active plans

```bash
# Confirm repository context
REPO_ROOT=$(gtimeout 5 git rev-parse --show-toplevel)

# Set options (with defaults)
WEB_SEARCH="${1:-true}"      # First argument: true/false (default: true)
DEPTH="${2:-standard}"        # Second argument: minimal/standard/comprehensive (default: standard)

# Detect repository type for correct plan paths
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
    PLANS_BASE="_dev/docs/plans"
else
    PLANS_BASE="docs/plans"
fi

ACTIVE_PLANS_DIR="$REPO_ROOT/$PLANS_BASE/active"
if [ ! -d "$ACTIVE_PLANS_DIR" ]; then
    echo "❌ Error: Active plans directory not found at $ACTIVE_PLANS_DIR"
    exit 1
fi

echo "📁 Active plans directory: $ACTIVE_PLANS_DIR"

# Find all plan files (exclude README.md, AGENTS.md, and other non-plan files)
PLAN_FILES=$(find "$ACTIVE_PLANS_DIR" -maxdepth 1 -type f -name "*.md" ! -name "README.md" ! -name "AGENTS.md" ! -name "index*.md" ! -name "*.yaml" 2>/dev/null | sort)

if [ -z "$PLAN_FILES" ]; then
    echo "⚠️  No active plans found in $ACTIVE_PLANS_DIR"
    echo "💡 Tip: Create plans first using /pfac_plan_from_active_tasks_conversation"
    exit 0
fi

# Count plans
PLAN_COUNT=$(echo "$PLAN_FILES" | wc -l | tr -d ' ')
echo "📋 Found $PLAN_COUNT active plan(s) to expand"
echo "🔍 Web search: $WEB_SEARCH"
echo "📏 Depth: $DEPTH"
echo ""
```

### 2. Process each plan sequentially

```bash
# Process each plan
PLAN_NUM=0
for PLAN_PATH in $PLAN_FILES; do
    PLAN_NUM=$((PLAN_NUM + 1))
    PLAN_NAME=$(basename "$PLAN_PATH")

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Plan $PLAN_NUM/$PLAN_COUNT: $PLAN_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Validate plan exists
    if [ ! -f "$PLAN_PATH" ]; then
        echo "  ⚠️  Warning: Plan file not found at $PLAN_PATH, skipping..."
        echo ""
        continue
    fi

    # Check current line count
    LINE_COUNT=$(wc -l < "$PLAN_PATH" 2>/dev/null || echo "0")
    echo "  📊 Current line count: $LINE_COUNT"

    # Check if plan is already comprehensive
    if [ "$LINE_COUNT" -gt 1000 ]; then
        echo "  ⚠️  Warning: Plan already has $LINE_COUNT lines (> 1000)"
        echo "  💡 Skipping expansion (already comprehensive)"
        echo ""
        continue
    fi

    # Analyze plan structure
    echo "  🔍 Analyzing plan structure..."

    SECTIONS_FOUND=0
    grep -q "## Problem Statement" "$PLAN_PATH" && ((SECTIONS_FOUND++)) || echo "    ⚠️  Missing: Problem Statement"
    grep -q "## Success Criteria" "$PLAN_PATH" && ((SECTIONS_FOUND++)) || echo "    ⚠️  Missing: Success Criteria"
    grep -q "## Strategy Validation" "$PLAN_PATH" && ((SECTIONS_FOUND++)) || echo "    ⚠️  Missing: Strategy Validation"
    grep -q "## Tasks" "$PLAN_PATH" && ((SECTIONS_FOUND++)) || echo "    ⚠️  Missing: Tasks section"

    echo "  ✅ Found $SECTIONS_FOUND/4 core sections"

    # Count tasks
    TASK_COUNT=$(grep -c "^#### Task [0-9]" "$PLAN_PATH" 2>/dev/null || echo "0")
    TASKS_WITH_CRITERIA=$(grep -c "Acceptance Criteria" "$PLAN_PATH" 2>/dev/null || echo "0")

    echo "  📝 Tasks found: $TASK_COUNT"
    echo "  ✓ Tasks with acceptance criteria: $TASKS_WITH_CRITERIA"
    echo ""

    # Expand this plan using the same logic as /expp_xpand_plan
    echo "  🔧 Expanding plan..."

    # Create backup (store under /canceled to avoid clutter next to active plans)
    CANCELED_DIR="$REPO_ROOT/$PLANS_BASE/canceled"
    mkdir -p "$CANCELED_DIR"
    BACKUP_PATH="${CANCELED_DIR}/${PLAN_NAME}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$PLAN_PATH" "$BACKUP_PATH"
    echo "  💾 Backup created: $BACKUP_PATH"

    # AI Agent performs expansion here (same steps as expp_xpand_plan)
    # 1. Expand tasks with detailed structure
    # 2. Add or enhance Strategy Validation section
    # 3. Perform web searches (if enabled)
    # 4. Add edge cases and error handling section
    # 5. Add detailed examples section
    # 6. Enhance testing and validation sections

    # Report metrics after expansion
    NEW_LINE_COUNT=$(wc -l < "$PLAN_PATH" 2>/dev/null || echo "0")
    LINES_ADDED=$((NEW_LINE_COUNT - LINE_COUNT))

    if [ "$LINES_ADDED" -gt 0 ]; then
        EXPANSION_RATIO=$(echo "scale=1; $NEW_LINE_COUNT / $LINE_COUNT" | bc 2>/dev/null || echo "N/A")
        echo "  ✅ Expansion complete!"
        echo "  📊 Expansion metrics:"
        echo "    • Original lines: $LINE_COUNT"
        echo "    • New lines: $NEW_LINE_COUNT"
        echo "    • Lines added: $LINES_ADDED"
        echo "    • Expansion ratio: ${EXPANSION_RATIO}x"
    else
        echo "  ⚠️  No expansion performed (plan may already be comprehensive)"
    fi

    echo ""
    echo "  📁 Expanded plan: $PLAN_PATH"
    echo "  💾 Backup: $BACKUP_PATH"
    echo ""
done
```

### 3. Summary report

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Expansion Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Processed $PLAN_NUM plan(s)"
echo "📁 Active plans directory: $ACTIVE_PLANS_DIR"
echo ""
echo "All active plans have been expanded with:"
echo "  • Detailed acceptance criteria"
echo "  • Implementation steps"
echo "  • Strategy validation"
echo "  • Edge cases and error handling"
echo "  • Testing strategies"
echo ""
echo "💡 Next steps:"
echo "  • Review expanded plans in $ACTIVE_PLANS_DIR"
echo "  • Execute plans using the xect_execute_plan command"
echo "  • Use the next_next_plan_cycle command to continue autonomous execution"
```

## Purpose

Expand all active plans with detailed guidelines, macro strategy validation, and research findings. Ensures comprehensive, actionable plans with clear acceptance criteria and implementation steps before execution begins.

## Command Sequence

### 1. Validate repository context and discover active plans

### 2. Process each plan sequentially

### 3. Summary report

### Example 1: Basic expansion with web search (default)

Use `/exal_xpand_all_active_plans` (no parameters).

### Example 2: Expansion without web search (offline mode)

Use `/exal_xpand_all_active_plans false`.

### Example 3: Minimal expansion (faster, less detail)

Use `/exal_xpand_all_active_plans true minimal`.

### Example 4: Comprehensive expansion (maximum detail)

Use `/exal_xpand_all_active_plans true comprehensive`.

### Minimal (fastest, ~2-3x expansion)

- Add acceptance criteria to all tasks

### Standard (balanced, ~5-7x expansion)

- Full task expansion (acceptance criteria, steps, validation, dependencies)

### Comprehensive (maximum detail, ~10-15x expansion)

- Everything in Standard, plus:

### Typical Workflow

1. `/reva_review_active_conversation` → Extract tasks from conversation
