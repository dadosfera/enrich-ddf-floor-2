# /pla-plan_from_active_tasks_conversation

Align the current conversation with a single plan under `docs/plans/active/`: review the full conversation, identify (or create) the closest active plan, and fold all completed, in‑progress, pending, and blocked tasks into that plan with clear structure and context.

Backlink: mini_prompt/lv1/conversation_to_active_plan_mini_prompt.md

## Command sequence (run in order)

1) Verify repository context (for plan paths)
```bash
gtimeout 5 git rev-parse --show-toplevel
```

2) (Optional) Quick scan of existing active and prioritized plans
```bash
gtimeout 5 find docs/plans -type f -name "*.md" 2>/dev/null | grep "/active/" | head -50
```
```bash
gtimeout 5 find docs/plans -type f -name "*.md" 2>/dev/null | grep "/prioritized/" | head -50
```

3) Choose or define the target plan path (AI agent must extract from conversation)
```bash
# AI agent must analyze conversation to extract:
# - PRIORITY: CB (Critical Blocker), QW (Quick Win), HI_HE (High Impact High Effort), SEC (Security), etc.
# - EFFORT: Time estimate (30m, 1h, 2h, 1d, 5d, etc.)
# - IMPACT: CRITICAL, HIGH, MEDIUM, LOW
# - DESCRIPTION: Short kebab-case description (e.g., fix_plan_naming_standards)

# Example extraction from conversation:
# "This is a quick win task that should take about 2 hours and has high impact"
# → PRIORITY="QW", EFFORT="2h", IMPACT="HIGH", DESCRIPTION="fix_plan_naming_standards"

PRIORITY="QW"          # Extract from conversation context
EFFORT="2h"            # Extract from conversation context
IMPACT="HIGH"          # Extract from conversation context
DESCRIPTION="your_objective_description"  # Extract from conversation (kebab-case)

PLAN_DIR="docs/plans/active"
PLAN_FILE="${PLAN_DIR}/${PRIORITY}_${EFFORT}_${IMPACT}_${DESCRIPTION}.md"
```

4) Ensure the active plans directory exists (safe create)
```bash
gtimeout 5 mkdir -p "$PLAN_DIR"
```

5) If the plan does not yet exist, create a minimal skeleton for conversation alignment
```bash
if [ ! -f "$PLAN_FILE" ]; then
  DATE=$(date +%Y-%m-%d)
  # Convert description to title case for display
  TITLE=$(echo "$DESCRIPTION" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')
  cat > "$PLAN_FILE" << EOF
# ${TITLE}

**Status**: active
**Priority**: ${PRIORITY}
**Effort**: ${EFFORT}
**Impact**: ${IMPACT}
**Created**: ${DATE}
**Last synced from conversation**: ${DATE} (initial skeleton)

## Overview
Short description of the objective, scope, and constraints.

## Current Status Summary
- Initial skeleton created from conversation alignment command.

## Completed Tasks (from this conversation)
- [x] Task 1 – fill based on conversation

## In Progress Tasks
- [ ] Task 2 – fill based on conversation

## Pending Tasks (not started yet)
- [ ] Task 3 – fill based on conversation

## Blocked Tasks
- [ ] Task 4 – fill based on conversation

## Next Actions (immediately after this conversation)
1. Next step 1 – very concrete, derived from conversation
2. Next step 2

## Context from Conversation
- Key decisions, constraints, and assumptions from this conversation.

## Links
- Related backlog/prioritized plans
- Conversation archive (if created)
EOF
fi
```

6) Run the mini prompt logic (AI agent steps, no extra shell commands)
- Read the entire conversation.
- **Extract naming metadata** from conversation context:
  - **PRIORITY**: Identify priority prefix (CB, QW, HI_HE, SEC, etc.) from conversation context
    - CB = Critical Blocker (blocks other work)
    - QW = Quick Win (≤4 hours, high impact)
    - HI_HE = High Impact High Effort (>3 days)
    - SEC = Security/Safety issues
    - Default to QW if unclear
  - **EFFORT**: Extract time estimate (30m, 1h, 2h, 1d, 5d, etc.) from conversation
  - **IMPACT**: Determine impact level (CRITICAL, HIGH, MEDIUM, LOW) from conversation
  - **DESCRIPTION**: Create kebab-case description from objective (e.g., `fix_plan_naming_standards`)
- **Select or create plan**:
  - Check for existing plan under `docs/plans/active/` that matches the objective
  - If no match, use `PLAN_FILE` with proper naming: `${PRIORITY}_${EFFORT}_${IMPACT}_${DESCRIPTION}.md`
  - If creating new plan, ensure filename follows naming standard exactly
- **Update plan content**:
  - Update **Status**, **Last synced from conversation**, **Current Status Summary**
  - Update **Priority**, **Effort**, **Impact** fields if they differ from filename
  - Update task sections:
    - **Completed Tasks (from this conversation)**
    - **In Progress Tasks**
    - **Pending Tasks**
    - **Blocked Tasks**
- Ensure every non‑trivial task from the conversation appears under one of these sections.
- Capture key decisions and constraints under **Context from Conversation**.
- Add links to any related backlog/prioritized plans or conversation archive docs.

7) Version control (optional, handled elsewhere)
- This command and mini prompt do not stage, commit, or push changes.
- Use your standard git‑sync / test‑driven‑commit workflows once the plan looks correct.

## Plan Naming Standards

**CRITICAL**: All plans must follow the naming convention: `{PRIORITY}_{EFFORT}_{IMPACT}_{DESCRIPTION}.md`

### Priority Prefixes
- `CB_` = Critical Blocker (blocks other work)
- `QW_` = Quick Win (≤4 hours, high impact)
- `HI_HE_` = High Impact High Effort (>3 days)
- `SEC_` = Security/Safety issues
- `HI_ME_` = High Impact Medium Effort (1-3 days)
- `MI_LE_` = Medium Impact Low Effort (≤1 day)
- `LI_` = Low Impact (any effort)
- `RES_` = Research/Exploration (uncertain effort/impact)

### Effort Format
- Minutes: `30m`, `90m`
- Hours: `1h`, `2h`, `4h`, `8h`
- Days: `1d`, `3d`, `5d`
- Weeks: `1w`, `2w`, `4w`
- Months: `1m`, `3m`, `6m`

### Impact Levels
- `CRITICAL` = Blocking production/development, security issues
- `HIGH` = Significant user value, performance improvements, major features
- `MEDIUM` = Moderate improvements, nice-to-have features
- `LOW` = Documentation, minor refactoring, experimental features

### Examples
- `CB_2h_CRITICAL_final_test_syntax_fixes.md`
- `QW_2h_HIGH_fix_plan_naming_standards.md`
- `HI_HE_5d_HIGH_migrate_flask_endpoints_to_fastapi.md`
- `SEC_4h_HIGH_env_security_fixes.md`

### AI Agent Responsibilities
1. **Extract metadata** from conversation context before creating plan
2. **Use proper naming format** - never use generic names like `plan.md` or `objective_plan.md`
3. **Match filename to metadata** - ensure Priority, Effort, Impact in filename match plan content
4. **Follow naming standards** - reference `docs/plans/AGENTS.md` Rule 5 for guidance

## Notes
- This command is **mid‑journey focused**: it aligns a conversation with a single `docs/plans/active/` plan.
- For backlog + archival flows, continue using `/archive` (`archive_conversation_review_and_plan_mini_prompt.md`).
- Keep commands short, non‑interactive, and guarded with `gtimeout` as shown; the heavy lifting happens in the plan editing guided by the mini prompt.
- **Naming is critical**: Plans without proper naming standards are harder to identify and prioritize.
