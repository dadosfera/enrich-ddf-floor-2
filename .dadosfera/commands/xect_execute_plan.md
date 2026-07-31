---
category: automation
criticality: high
scope: all
---
# /xect_execute_plan
<!-- COMMAND_ID: 015 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_execute_plan -->

Execute the active plan related to the current conversation, showing the absolute path at the end.

**Local Reference**: `commands/xect_execute_plan.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/xect_execute_plan.md`

Backlinks:
- mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md
- mini_prompt/automated_execution_active_plans.md
- commands/jour_journey_meta_best_track.md
- commands/pfac_plan_from_active_tasks_conversation.md

## When to Use

- After creating a plan from the current conversation with `/pfac_plan_from_active_tasks_conversation`
- After expanding a conversation-related plan with `/expp_xpand_plan`
- When you want to execute the plan that was just discussed in the conversation
- When you need to show the absolute path to the plan being executed

## When NOT to Use

- When you want to execute any top-priority plan (use the automated execution mini prompt directly)
- When no conversation-related active plan exists (create one first with `/pfac_plan_from_active_tasks_conversation`)
- When you need to review conversation first (use `/reva_review_active_conversation`)

## Command sequence (run in order)

### 1. Identify conversation-related plan

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

# Extract plan context from conversation
# AI agent must analyze conversation to identify the relevant plan
# This could be:
# - A plan just created with /pfac_plan_from_active_tasks_conversation
# - A plan mentioned or discussed in the conversation
# - A plan that was expanded with /expp_xpand_plan

# Topic Extraction Strategy:
# 1. Look for explicit plan names or topics mentioned in conversation
# 2. Extract key phrases (convert to kebab-case: "topic extraction" → "topic_extraction")
# 3. Remove common words: "test", "work on", "need to", etc.
# 4. Match against plan filenames (case-insensitive, partial match)
# 5. Prioritize exact matches, then partial matches

# Example extraction patterns:
# "I need to work on topic extraction test" → "topic_extraction"
# "fix command collisions" → "fix_command_collisions"
# "work on the abs path test" → "abs_path"
# "execute the nonexistent_xyz_plan" → "nonexistent_xyz"

# Extract topic from conversation (AI agent implementation)
CONVERSATION_TOPIC="topic_extraction"  # Extracted from: "topic extraction test"

# Find matching active plan
PLAN_PATH=$(find "$REPO_ROOT/$PLANS_BASE/active" -type f -name "*${CONVERSATION_TOPIC}*.md" 2>/dev/null | head -1)

if [ -z "$PLAN_PATH" ]; then
    echo "❌ No active plan found related to conversation topic: $CONVERSATION_TOPIC"
    echo "💡 Tip: Create a plan first with /pfac_plan_from_active_tasks_conversation"
    exit 1
fi

echo "📋 Found conversation-related plan: $(basename "$PLAN_PATH")"
```

### 2. Read and display plan content

```bash
# Display plan header and key sections
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "📄 Plan: $(basename "$PLAN_PATH")"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Read plan content
cat "$PLAN_PATH"

echo ""
echo "═══════════════════════════════════════════════════════════"
```

### 3. Execute plan tasks

```bash
# AI agent performs the actual execution based on plan content
# This includes:
# - Reading task list from plan
# - Executing each task in order
# - Updating task status (Pending → In Progress → Completed)
# - Handling blockers and dependencies
# - Running tests and validation

echo ""
echo "🚀 Executing plan tasks..."
echo ""

# Execute tasks from plan
# (AI agent performs the actual execution based on plan content)
```

### 4. Update plan status

```bash
# Check if plan is completed
# (AI agent determines completion based on task status)

PLAN_COMPLETED=false  # Set by AI based on task completion

if [ "$PLAN_COMPLETED" = true ]; then
    echo ""
    echo "✅ Plan completed!"

    # Move to finished
    PLAN_NAME=$(basename "$PLAN_PATH")
    FINISHED_PATH="$REPO_ROOT/$PLANS_BASE/finished/${PLAN_NAME}"

    mv "$PLAN_PATH" "$FINISHED_PATH"
    echo "📁 Moved to: $FINISHED_PATH"

    # Update PLAN_PATH to finished location
    PLAN_PATH="$FINISHED_PATH"
else
    echo ""
    echo "⏳ Plan in progress - continue execution in next session"
fi
```

### 5. Display absolute path

```bash
# Display absolute path to plan file
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "📍 Plan Location (Absolute Path):"
echo "═══════════════════════════════════════════════════════════"
echo "$PLAN_PATH"
echo "═══════════════════════════════════════════════════════════"
echo ""
```

### 6. Git sync after execution

```bash
# Perform git sync to commit progress
echo "🔄 Performing git sync..."
gtimeout 10 git status --short
```
