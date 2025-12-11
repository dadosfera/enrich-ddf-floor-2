# /exal_expand_all_active_plans

Expand all active plans with detailed guidelines, macro strategy validation, and research findings to ensure comprehensive, actionable plans with clear acceptance criteria and implementation steps.

**Local Reference**: `commands/exal_expand_all_active_plans.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/exal_expand_all_active_plans.md`

Backlinks:
- commands/expp_expand_plan.md
- commands/pfac_plan_from_active_tasks_conversation.md
- commands/revw_review.md

## Purpose

This command addresses the need to expand multiple active plans at once. Unlike `/expp_expand_plan` which expands a single plan, this command discovers all plans in the active directory and expands each one systematically. This is useful when you have multiple active plans that need enrichment before execution.

## When to Use

- When you have multiple active plans that all need expansion
- After creating several plans from conversations that feel sparse or incomplete
- Before starting execution on multiple complex or unfamiliar tasks
- When you want to ensure all active plans meet the minimum 500-line standard
- When you need to validate approaches across multiple plans against current best practices

## When NOT to Use

- For expanding a single plan (use `/expp_expand_plan` instead)
- For simple, well-understood tasks (< 1 hour effort per plan)
- When plans already have detailed acceptance criteria and steps (> 1000 lines each)
- For urgent fixes where speed is critical
- When working offline (web search will be skipped automatically)

## Command Sequence

### 1. Validate repository context and discover active plans

```bash
# Confirm repository context
gtimeout 5 git rev-parse --show-toplevel

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

    # Expand this plan using the same logic as /expp_expand_plan
    echo "  🔧 Expanding plan..."

    # Create backup
    BACKUP_PATH="${PLAN_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$PLAN_PATH" "$BACKUP_PATH"
    echo "  💾 Backup created: $BACKUP_PATH"

    # AI Agent performs expansion here (same steps as expp_expand_plan)
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
echo "  • Execute plans using /exec_execute_plan"
echo "  • Use /next_next_plan_cycle to continue autonomous execution"
```

## Expansion Details

Each plan is expanded using the same comprehensive process as `/expp_expand_plan`:

1. **Task Expansion**: Each task gets:
   - 3-5 acceptance criteria (specific, measurable, verifiable)
   - 5-10 implementation steps (concrete actions)
   - Validation methods for each criterion
   - Dependencies clearly listed
   - Realistic duration estimates
   - Risk level assessment
   - Rollback plan

2. **Strategy Validation**: Adds or enhances:
   - Macro view of approach
   - 2-3 alternative approaches with pros/cons
   - 3-5 risks with mitigations
   - Testable assumptions

3. **Research Findings** (if web search enabled):
   - 3-5 relevant sources from last 12 months
   - Specific recommendations extracted
   - Clear application to current plan

4. **Edge Cases & Error Handling**:
   - Input validation edge cases
   - Runtime failure scenarios
   - Data quality issues (if applicable)

5. **Testing Strategy**:
   - Unit test coverage targets
   - Integration test scenarios
   - Security/performance tests (if applicable)

6. **Deployment Checklist**:
   - 10-15 specific checklist items

## Usage Examples

### Example 1: Basic expansion with web search (default)
```bash
/exal_expand_all_active_plans
```

### Example 2: Expansion without web search (offline mode)
```bash
/exal_expand_all_active_plans false
```

### Example 3: Minimal expansion (faster, less detail)
```bash
/exal_expand_all_active_plans true minimal
```

### Example 4: Comprehensive expansion (maximum detail)
```bash
/exal_expand_all_active_plans true comprehensive
```

## Expansion Depth Levels

Same as `/expp_expand_plan`:

### Minimal (fastest, ~2-3x expansion)
- Add acceptance criteria to all tasks
- Add basic implementation steps (3-5 per task)
- Add strategy validation (macro view only)
- Skip web search
- Skip detailed examples

### Standard (balanced, ~5-7x expansion)
- Full task expansion (acceptance criteria, steps, validation, dependencies)
- Complete strategy validation (alternatives, risks)
- Web search for 3-5 key topics
- Add edge cases section
- Add testing strategy
- Add 1 detailed example

### Comprehensive (maximum detail, ~10-15x expansion)
- Everything in Standard, plus:
- Web search for all major technical decisions
- Multiple detailed examples (2-3)
- Extensive edge case coverage
- Complete deployment checklist
- Security and performance testing sections
- Rollback procedures for all tasks

## Quality Standards

Each expanded plan must meet these criteria (same as `/expp_expand_plan`):

1. **Minimum 500 lines** (for non-trivial objectives)
2. **All tasks have**:
   - 3-5 acceptance criteria (specific, measurable)
   - 5-10 implementation steps (concrete actions)
   - Validation methods for each criterion
   - Dependencies clearly listed
   - Realistic duration estimates
3. **Strategy validation includes**:
   - Macro view of approach
   - 2-3 alternative approaches with pros/cons
   - 3-5 risks with mitigations
4. **Research findings** (if web search enabled):
   - 3-5 relevant sources from last 12 months
   - Specific recommendations extracted
   - Clear application to current plan
5. **Testing strategy**:
   - Specific test scenarios (not just "write tests")
   - Coverage targets
   - Security/performance tests if applicable

## Error Handling

### Active plans directory not found
```
❌ Error: Active plans directory not found
💡 Tip: Check {PLANS_BASE}/active/ (_dev/docs/plans/active for -fera repos, docs/plans/active for others)
```

### No active plans found
```
⚠️  No active plans found in <directory>
💡 Tip: Create plans first using /pfac_plan_from_active_tasks_conversation
```

### Plan file not found (during processing)
```
⚠️  Warning: Plan file not found at <path>, skipping...
```
(Continues with next plan)

### Plan already comprehensive
```
⚠️  Warning: Plan already has <N> lines (> 1000)
💡 Skipping expansion (already comprehensive)
```
(Continues with next plan)

### Web search fails
```
⚠️  Warning: Web search unavailable (no internet connection)
✅ Proceeding with offline expansion (skipping research findings)
```
(Continues with expansion, skipping research section)

## Integration with Other Commands

### Typical Workflow
1. `/revw_review` → Extract tasks from conversation
2. `/pfac_plan_from_active_tasks_conversation` → Create initial plans
3. **`/exal_expand_all_active_plans`** → Enrich all active plans with details and research
4. `/exec_execute_plan` or `/next_next_plan_cycle` → Execute comprehensive plans

### When to Use Each Command
- **`/expp_expand_plan`**: Expand a single specific plan
- **`/exal_expand_all_active_plans`**: Expand all active plans at once
- **`/revw_review`**: Classify and route tasks from conversation
- **`/pfac_plan_from_active_tasks_conversation`**: Create initial plan structure
- **`/exec_execute_plan`**: Execute conversation-related active plan
- **`/next_next_plan_cycle`**: Execute next plan in queue (active → prioritized → backlog)
- **`/arch_archive`**: Move completed plans to archive

## Notes

- This command is **idempotent**: Running it twice on the same plans won't double the content (it detects existing sections and skips plans > 1000 lines)
- Always creates a backup before modifying each plan
- Web search is optional but recommended for unfamiliar technologies
- Expansion should add **value**, not just length
- Focus on making plans **actionable** and **execution-ready**
- Plans are processed sequentially to avoid overwhelming the system
- Each plan expansion follows the same quality standards as `/expp_expand_plan`

## Relationship to Other Commands

- **`/expp_expand_plan`**: Single-plan version of this command
- **`/revw_review`**: Produces task lists that feed into plans
- **`/pfac_plan_from_active_tasks_conversation`**: Creates initial plans that this command expands
- **`/exec_execute_plan`**: Executes conversation-related active plan
- **`/next_next_plan_cycle`**: Orchestrates autonomous execution loop
- **`/arch_archive`**: Archives completed plans after execution
- **`/test_test`**: Tests implementations based on expanded plan criteria

## Future Enhancements

- Parallel expansion: Process multiple plans simultaneously (with resource limits)
- Selective expansion: Expand only plans matching certain criteria (priority, size, etc.)
- Progress tracking: Save expansion state to resume if interrupted
- Batch reporting: Generate consolidated report across all expanded plans
- Template library: Pre-defined expansion templates for common plan types
- Learning mode: Learn from past expansions to improve future ones
