# /arc_archive

Create plan documents from a conversation review across statuses: backlog (baseline) and prioritized (optional). Optionally store a conversation archive stub. Use objective-based naming; do not create `conversation_archiver_*` implementation plans.

**Critical rule**: this command is an end-of-journey / archival flow. It **must not leave related plans in `docs/plans/active/`**. Before archiving, it will:

- scan for related plans in `docs/plans/active/` matching `OBJ_SLUG`
- if those plans are clearly finished based on their canonical Status field (`Status:` / `**Status**:` set to `finished`, `completed`, or `done`), automatically move them to `docs/plans/finished/`
- if any related plan still has an active Status, abort the `/archive` flow so you can finish or reclassify work first (do not confuse “to be prioritized” or backlog items with truly in‑progress work).

Backlink: `mini_prompt/lv1/archive_conversation_review_and_plan_mini_prompt.md`

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Set objective slug, date, and create flags (edit values)

```bash
OBJ_SLUG="your_objective_slug"   # e.g., fix_conversation_archiver_output
DATE=$(date +%Y-%m-%d)

# Baseline backlog target (always created)
BL_TARGET="docs/plans/backlog/${OBJ_SLUG}_next_actions_${DATE}.md"

# Optional prioritized plan target (created only if flag set)
PR_TARGET="docs/plans/prioritized/${OBJ_SLUG}_plan.md"

CREATE_PRIORITIZED=false   # set to true if ready-to-begin soon
```

3. Ensure plan directories exist

```bash
gtimeout 5 mkdir -p docs/plans/backlog docs/plans/prioritized docs/plans/active docs/plans/finished
```

4. Pre-archive check for related active plans (auto-move when fully done, otherwise fail)

```bash
# Best-effort scan for related active plans (edit OBJ_SLUG or PLAN_GLOB as needed)
PLAN_GLOB="docs/plans/active/*${OBJ_SLUG}*_plan.md"
ACTIVE_PLANS=$(ls $PLAN_GLOB 2>/dev/null || true)

if [ -n "$ACTIVE_PLANS" ]; then
  echo "Found related active plan(s):"
  echo "$ACTIVE_PLANS"

  ALL_DONE="true"
  for PLAN in $ACTIVE_PLANS; do
    PLAN_DONE="false"

    # Prefer explicit status markers in the plan body/header
    STATUS_LINE=$(grep -iE '^(Status:|\*\*Status\*\*:)' "$PLAN" | head -1 | tr '[:upper:]' '[:lower:]')
    if echo "$STATUS_LINE" | grep -q 'finished\|completed\|done'; then
      PLAN_DONE="true"
    fi

    # Fallback: if there is an explicit status line but it is NOT finished/completed/done,
    # treat the plan as still active, regardless of checkbox usage.
    if [ "$PLAN_DONE" != "true" ]; then
      echo "Plan not clearly finished (status not finished/completed/done): $PLAN"
      ALL_DONE="false"
    fi
  done

  if [ "$ALL_DONE" = "true" ]; then
    echo "All related active plans appear complete; processing them for archival."
    mkdir -p docs/plans/finished
    for PLAN in $ACTIVE_PLANS; do
      BASENAME=$(basename "$PLAN")
      FINISHED_PLAN="docs/plans/finished/$BASENAME"

      if [ -f "$FINISHED_PLAN" ]; then
        echo "Duplicate detected: $FINISHED_PLAN already exists."
        echo "AI ACTION REQUIRED: Analyze and merge the two plan files:"
        echo "  - Active plan: $PLAN"
        echo "  - Existing finished plan: $FINISHED_PLAN"
        echo "  - Merge strategy: Combine unique content, preserve most recent updates, consolidate completed tasks"
        echo "  - Output: Write merged content to $FINISHED_PLAN"
        echo "  - After merge: Remove $PLAN from /active/"
        echo ""
        echo "The AI model executing this command should:"
        echo "  1. Read both files completely"
        echo "  2. Identify unique content in each (tasks, decisions, context, notes)"
        echo "  3. Merge into a single coherent plan document"
        echo "  4. Ensure Status remains 'finished'/'completed'/'done'"
        echo "  5. Write merged result to $FINISHED_PLAN"
        echo "  6. Remove $PLAN from /active/ after successful merge"
      else
        mv "$PLAN" "$FINISHED_PLAN"
        echo "Moved $PLAN -> $FINISHED_PLAN"
      fi
    done
  else
    echo "At least one related active plan still has active tasks."
    echo "Aborting /archive; finish or reclassify active work before archiving."
    echo "Do NOT treat backlog or to-be-prioritized tasks as 'active' here."
    exit 1
  fi
fi
```

5. Create backlog next-actions document (baseline)

```bash
cat > "$BL_TARGET" << EOF
# ${OBJ_SLUG} – next actions

Status: backlog
Created from: Conversation review on ${DATE}
Objective: ${OBJ_SLUG}
Priority: Medium
Estimated effort: [AI hours] / [Human hours]

## Next actions (not-yet-tried / unplanned)
- [ ] Action 1 (clear verb, scope, owner/context if known)
- [ ] Action 2
- [ ] Action 3

## Context from conversation
- Key decisions, constraints, and notes that justify the next actions

## Links
- Related plans (if any) and references
EOF
```

6. OPTIONAL: Create prioritized plan if needed (safe create; skip if exists)

```bash
if [ "$CREATE_PRIORITIZED" = "true" ]; then
  if [ ! -f "$PR_TARGET" ]; then
    cat > "$PR_TARGET" << EOF
# ${OBJ_SLUG} Plan

**Status**: prioritized
**Created from**: Conversation review on ${DATE}
**Priority**: High
**Estimated effort**: [AI hours] / [Human hours]

## Overview
Brief description and scope.

## Current Status
- Not started; ready to begin

## Pending Tasks
### High Priority
- [ ] Task 1

### Medium Priority
- [ ] Task 2

## Next Actions
1. Immediate step 1
2. Immediate step 2

## Context from Conversation
- Key decisions and constraints

## Success Criteria
- Expected outcomes and quality bars
EOF
  fi
fi
```

7. OPTIONAL: Create a conversation archive stub (stores links/summary)

```bash
# Repo-aware archive directory selection (best-guess; no prompts)
REPO_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null)
if [[ "$REPO_NAME" == *-fera ]]; then
  ARCHIVE_DIR="_dev/conversations"
else
  ARCHIVE_DIR="docs/conversations"
fi

# Note: For cross-repo sharing across dadosfera, save into the docs-fera repository at project-level /conversations (outside this repo flow)

ARCHIVE_FILE="${ARCHIVE_DIR}/${DATE}_${OBJ_SLUG}.md"
gtimeout 5 mkdir -p "$ARCHIVE_DIR"
cat > "$ARCHIVE_FILE" << EOF
# Conversation archive – ${OBJ_SLUG} (${DATE})

Summary
- Brief synopsis of the conversation and outcomes

Backlog doc
- ${BL_TARGET}

Related plans
- Prioritized: ${PR_TARGET}

Notes
- Any important context not captured elsewhere
EOF
```

8. Version control (optional)
   This command intentionally does not stage, commit, or push changes. Handle version control separately if desired.

## Notes

- Baseline: always produce the backlog next-actions doc.
- Use objective-based naming and link plan files in the backlog doc.
- Only create prioritized plans when justified by readiness; otherwise keep in backlog.
- Do not create or update `docs/plans/active/` plans from this `/archive` flow; the only allowed interaction with `docs/plans/active/` here is **moving fully completed plans out to `docs/plans/finished/` during archival**. Active-plan alignment and editing belong to the mid-journey command (`/plan_from_active_tasks_conversation`).
- **Duplicate handling**: If a plan with the same name already exists in `docs/plans/finished/`, the AI model executing this command must analyze both files and merge them intelligently. The merge should combine unique content, preserve the most recent updates, consolidate completed tasks, and ensure the merged plan maintains `Status: finished`/`completed`/`done`. After successful merge, remove the plan from `/active/`.
- Never overwrite existing plan files without merging; always analyze and combine content when duplicates are detected.
- Do not create `conversation_archiver_*` implementation plans from this flow.
- Keep commands unchained and short; one command per step.

**Checkbox notation**

- `- [ ]` / `- [x]` are recommended for task lists inside plans but not required. `/archive` and related automation rely on each plan’s canonical Status field to determine completion; missing checkboxes must not prevent archival when Status is `finished`/`completed`/`done`.

See also

- `standards/planning_docs_ci_standards.md` — global planning/docs/CI rules, including Status and checkbox expectations.
- `templates/plan_management_system.md` — detailed plan lifecycle and completion rules that `/archive` follows.
- `mini_prompt/lv1/archive_conversation_review_and_plan_mini_prompt.md` — conversation-to-plan workflow that typically precedes this command.
