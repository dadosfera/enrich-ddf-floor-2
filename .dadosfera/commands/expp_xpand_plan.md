# /expp_xpand_plan
<!-- COMMAND_ID: 017 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_xpand_plan -->

Expand an existing plan with detailed guidelines, macro strategy validation, and research findings to ensure comprehensive, actionable plans with clear acceptance criteria and implementation steps.

**Local Reference**: `commands/expp_xpand_plan.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/expp_xpand_plan.md

Backlinks:
- commands/pfac_plan_from_active_tasks_conversation.md
- commands/reva_review_active_conversation.md

## Purpose
Enriches sparse plans (< 500 lines) into comprehensive, execution-ready documents with detailed tasks, strategy validation, and research.

## When to Use
- Plan is < 500 lines
- Objective is non-trivial or unfamiliar
- Tasks lack acceptance criteria
- Strategy needs validation

## Command Sequence

### 1. Validate inputs and read plan
bash
PLAN_PATH="$1"
WEB_SEARCH="${2:-true}"
DEPTH="${3:-standard}"

# Validation logic...
``

### 2. Analyze structure
```bash
# Check for required sections (Problem, Success, Strategy, Tasks)
# Count tasks vs acceptance criteria
```

### 3. Expand Tasks
Add detailed structure to each task:
- Acceptance Criteria (3-5)
- Implementation Steps (5-10)
- Validation Methods
- Dependencies
- Risk/Rollback

**See**: `guides/commands/expp_xpand_plan_guide.md` for expansion templates.

### 4. Strategy Validation
Add/enhance:
- Macro View
- Alternative Approaches
- Risk Assessment
- Assumptions

### 5. Research (if enabled)
Perform web searches and add "Research Findings" section.

### 6. Finalize
Add:
- Edge Cases & Error Handling
- Detailed Examples (Before/After)
- Testing Strategy
- Deployment Checklist

### 7. Write & Validate
- Create backup
- Write expanded plan
- Verify quality (>500 lines, all sections present)

## Usage Examples

```bash
# Standard expansion
/expp_xpand_plan plans/active/QW_feature.md

# Offline mode
/expp_xpand_plan plans/active/QW_feature.md false

# Comprehensive mode
/expp_xpand_plan plans/active/QW_feature.md true comprehensive
```

## Reference
For detailed templates, logic, and examples, see:
- `guides/commands/expp_xpand_plan_guide.md`
