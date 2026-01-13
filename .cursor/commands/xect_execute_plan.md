# /xect_execute_plan
<!-- COMMAND_ID: 015 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ex_execute_plan -->

Execute the active plan related to the current conversation, showing the absolute path at the end.

**Local Reference**: `commands/xect_execute_plan.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/xect_execute_plan.md

**Note**: This command is repo-aware. For -fera repositories (docs-fera, scripts-fera, etc.), plans are stored in _dev/docs/plans/. For all other repositories, plans are stored in `docs/plans/`.

Backlinks:

- mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md
- mini_prompt/automated_execution_active_plans.md
- commands/jour_journey_meta_best_track.md
- commands/pfac_plan_from_active_tasks_conversation.md

## Purpose

This command executes the active plan that is related to the current conversation context. Unlike general plan execution, this command focuses specifically on the plan derived from or referenced in the ongoing conversation, and displays the absolute path to the plan file at the end.

## When to Use

- After creating a plan from the current conversation with `/pfac_plan_from_active_tasks_conversation`
- After expanding a conversation-related plan with `/expp_xpand_plan`
- When you want to execute the plan that was just discussed in the conversation
- When you need to show the absolute path to the plan being executed

## When NOT to Use

- When you want to execute any top-priority plan (use the automated execution mini prompt directly)
- When no conversation-related active plan exists (create one first with `/pfac_plan_from_active_tasks_conversation`)
- When you need to review conversation first (use `/reva_review_active_conversation`)

## Command Sequence

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

## Plan Prioritization Rules

### Priority Prefixes (in selection order)

1. **QW\_** (Quick Win) - Under 4 hours, high value
2. **CB\_** (Critical Blocker) - Blocking production/development
3. **SEC\_** (Security) - Security issues
4. **HI*ME*** (High Impact, Medium Effort) - Best ROI
5. **MI*LE*** (Medium Impact, Low Effort) - Easy wins
6. **HI*HE*** (High Impact, High Effort) - Major features
7. **LI\_** (Low Impact) - Minor improvements
8. **RES\_** (Research/Exploration) - Uncertain effort/impact

### Plan Naming Convention

```
{PRIORITY_PREFIX}_{EFFORT_ESTIMATE}_{IMPACT_LEVEL}_{SHORT_DESCRIPTION}
```

**Examples:**

- `QW_2h_HIGH_fix_broken_tests.md`
- `CB_1d_CRITICAL_resolve_deployment_blocker.md`
- `HI_HE_4w_MEDIUM_refactor_legacy_system.md`

### Effort Estimation Guidelines

- **Minutes**: `30m`, `90m` (tiny fixes)
- **Hours**: `2h`, `4h`, `8h` (small features/fixes)
- **Days**: `1d`, `3d`, `5d` (medium features)
- **Weeks**: `1w`, `2w`, `4w` (large features)
- **Months**: `1m`, `3m`, `6m` (major projects)

### Impact Assessment Levels

- **CRITICAL**: Blocking production/development, security issues
- **HIGH**: Significant user value, performance improvements, major features
- **MEDIUM**: Moderate improvements, nice-to-have features
- **LOW**: Documentation, minor refactoring, experimental features

## Lifecycle Management Rules

### CRITICAL: Active Plan Management

- **NEVER create new plans in `/active`** unless `/active` is completely empty
- **All new plans MUST be created in `/prioritized`** with effort-impact analysis
- **Only move ONE optimal plan from `/prioritized` to `/active`** when `/active` is empty
- **Active plan completion signals end of development cycle** - user can stop agent knowing work is complete

### Plan Selection Logic

1. **Complete ALL plans in `/active` first** (highest priority)
2. **⚠️ CRITICAL CHECK: ONLY when `/active` is COMPLETELY EMPTY**, scan `/prioritized` and select using priority order
   - **MANDATORY VERIFICATION**: Count files in `/active` directory - MUST be 0 files
   - **❌ NEVER move plans if `/active` contains ANY files**
   - **✅ ONLY proceed if `/active` directory is completely empty**
3. **If both `/active` and `/prioritized` are empty**, create ONE new plan in `/active`

## Usage Examples

### Example 1: Execute conversation-related plan

```bash
# After discussing "fix command collisions" in conversation
/xect_execute_plan

# Output:
# 📋 Found conversation-related plan: QW_1h_HIGH_fix_command_collisions.md
# ... (plan content and execution)
# 📍 Plan Location (Absolute Path):
# /Users/luismartins/local_repos/docs-fera/_dev/docs/plans/active/QW_1h_HIGH_fix_command_collisions.md
```

### Example 2: Full workflow with path display

```bash
# 1. Review conversation
/reva_review_active_conversation

# 2. Create plan from conversation
/pfac_plan_from_active_tasks_conversation
# Creates: _dev/docs/plans/active/QW_2h_HIGH_implement_feature.md (for -fera repos)

# 3. Expand plan with details
/expp_xpand_plan _dev/docs/plans/active/QW_2h_HIGH_implement_feature.md

# 4. Execute conversation-related plan
/xect_execute_plan
# Executes and shows:
# 📍 Plan Location (Absolute Path):
# /Users/luismartins/local_repos/docs-fera/_dev/docs/plans/active/QW_2h_HIGH_implement_feature.md
```

### Example 3: After plan completion

```bash
/xect_execute_plan

# Output:
# ✅ Plan completed!
# 📁 Moved to: /Users/luismartins/local_repos/docs-fera/_dev/docs/plans/finished/QW_2h_HIGH_implement_feature.md
# 📍 Plan Location (Absolute Path):
# /Users/luismartins/local_repos/docs-fera/_dev/docs/plans/finished/QW_2h_HIGH_implement_feature.md
```

## Integration with Other Commands

### Typical Workflow

1. `/reva_review_active_conversation` → Extract tasks from conversation
2. `/pfac_plan_from_active_tasks_conversation` → Create initial plan
3. `/expp_xpand_plan` → Enrich plan with details and research
4. **`/xect_execute_plan`** → Execute the comprehensive plan
5. `/arch_archive` → Archive completed plans

### When to Use Each Command

- **`/reva_review_active_conversation`**: Classify and route tasks from conversation
- **`/pfac_plan_from_active_tasks_conversation`**: Create initial plan structure from conversation
- **`/expp_xpand_plan`**: Add depth, validation, and research to existing plan
- **`/xect_execute_plan`**: Execute the conversation-related plan and show its absolute path
- **`/arch_archive`**: Move completed plans to archive

## Attention Rules (Higher Priority)

### ATTENTION 01: Autonomy in Execution

- Proceed with installations autonomously
- Carry out tasks, todos, actions, and plans without waiting for further instruction
- Always finish and execute all active plans, and continuously update the meta plan
- If there are no active plans, create an active plan to improve robustness, professionalism, error resistance, linter compliance, and testing quality

### ATTENTION 02: Careful Prompt Handling & File Search

- Carefully read the entire prompt before responding
- Always execute the next top-priority action, rather than just answering without acting
- Perform a git sync at the end of each task
- Execute all active plans
- If a file is missing, always attempt to locate it before creating a new one:
  1. Search the local repository (using grep/find)
  2. Search the remote repository (using git ls-remote, gh api)
  3. Search the historical git history (using git log --all --full-history -- **filename**)

### ATTENTION 03: Smart Plan Prioritization & Lifecycle Management

- **NEVER create new plans in `/active`** unless `/active` is completely empty
- **All new plans MUST be created in `/prioritized`** with effort-impact analysis
- **Only move ONE optimal plan from `/prioritized` to `/active`** when `/active` is empty
- **Active plan completion signals end of development cycle** - user can stop agent knowing work is complete

## Terminal Command Safety Guidelines

### Command Execution Rules

- Create official tests indexed at `tests/index_tests.yaml` instead of running rogue tests by terminal commands
- Assure that all indexed tests are called by central test entry point: `tests/run_tests.sh` (with --all --e2e params)
- Follow smart plan prioritization rules: Prioritize Quick Wins (≤4h) and Critical Blockers over long-term projects
- Use timeout and sleep on terminal commands to avoid getting stuck (start with 1-5 seconds, increase progressively)
- Don't concatenate more than 1 command - break into separate steps
- If you need multiple commands: use `./.tmp/` folder to create temp scripts
- Move deleted files to `trash_git/` instead of permanent deletion
- Never use `--no-verify` or `git reset HEAD` for commits

## Error Handling

### No conversation-related plan found

```
❌ No active plan found related to conversation topic: <topic>
💡 Tip: Create a plan first with /pfac_plan_from_active_tasks_conversation
💡 Tip: Ensure the plan name matches the conversation context
```

### Multiple matching plans found

```
⚠️  Multiple plans found matching conversation topic
📋 Found plans:
  - QW_1h_HIGH_fix_command_collisions.md
  - QW_2h_HIGH_fix_command_collisions_v2.md
💡 Tip: Be more specific about which plan to execute
💡 Tip: Or complete/archive older plans first
```

### Plan execution blocked

```
❌ Plan execution blocked: <reason>
💡 Tip: Resolve blockers before continuing
💡 Tip: Update plan status to reflect blockers
```

### Cannot find plan path

```
❌ Error: Plan path not found or inaccessible
💡 Tip: Check if plan was moved or deleted
💡 Tip: Verify repository root is correct
```

## Notes

- This command focuses on **conversation-related plans** only
- Always displays the **absolute path** to the plan file at the end
- Different from general plan execution (which picks top-priority plan)
- Automatically manages plan lifecycle (active → finished)
- Integrates with git sync for progress tracking
- The absolute path is useful for:
  - Referencing the plan in future conversations
  - Opening the plan file directly
  - Tracking plan location after completion
  - Debugging plan-related issues

## Relationship to Other Commands

- **`/jour_journey_meta_best_track`**: Includes this command as part of Core Development Loop
- **`/pfac_plan_from_active_tasks_conversation`**: Creates plans that this command executes
- **`/expp_xpand_plan`**: Enriches plans before this command executes them
- **`/reva_review_active_conversation`**: Produces task lists that feed into plans
- **`/arch_archive`**: Archives completed plans after execution

## Testing

This command has a comprehensive white-box test suite that verifies the logic by extracting and executing the bash code blocks from this Markdown file.

### Running Tests

```bash
# Run the specific test suite
bash tests/commands/test_xect_execute_plan.sh

# Run as part of the full test suite
bash tests/run_tests.sh --category commands
```

### Test Strategy

- **Type**: White-box testing / Unit testing
- **Methodology**: Parses this Markdown file to extract bash code blocks (topic extraction, plan detection, path display) and executes them in an isolated test environment.
- **Coverage**:
  - Conversation topic extraction logic
  - Plan path detection (matching active plans)
  - Absolute path display formatting
  - Error handling (no plan found)
- **Why this approach**: Direct execution via `cursor-agent` requires interactive authentication which blocks automated CI/CD pipelines. White-box testing ensures the logic *inside* the command is correct without needing a live AI agent.

## Future Enhancements

- Interactive mode: Ask user questions during execution
- Parallel execution: Execute multiple independent tasks simultaneously
- Progress tracking: Real-time progress updates during execution
- Rollback support: Ability to undo partially completed plans
- Learning mode: Learn from past executions to improve future ones
- Metrics: Track execution time, success rate, and blockers
