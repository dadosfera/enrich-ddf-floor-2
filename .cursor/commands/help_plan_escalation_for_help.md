# /help_plan_escalation_for_help
<!-- COMMAND_ID: 024 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: he_plan_escalation_for_help -->

**Escalation command for lower-register AI models.** When stuck after exhausting available tools (browser, web search, codebase search, grep, etc.) and unable to find root cause or solution, use this command to document the situation and request assistance from a higher-register model.

**Local Reference**: `commands/help_plan_escalation_for_help.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/help_plan_escalation_for_help.md

Backlinks:

- rules/cursor/1_02_autonomy_user_handoff.mdc
- commands/xect_execute_plan.md
- `commands/pfac_plan_from_active_tasks_conversation.md`

## When to Use This Command

Use `/help` when you (the AI model):

1. Have tried multiple diagnostic approaches (browser, web search, codebase search, grep, read_file)
2. Cannot identify the root cause of a problem
3. Cannot think of a viable solution path
4. Have hit a conceptual or technical wall
5. Need reasoning capabilities beyond your current model tier

**Do NOT use** for:

- Simple questions that require more searching
- Tasks that just need more time/patience
- Situations where you haven't exhausted available tools

## Command Sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Detect plans base and active plan

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")
if [[ "$REPO_NAME" == *-fera ]]; then
  PLANS_BASE="_dev/docs/plans"
else
  PLANS_BASE="docs/plans"
fi
echo "Plans base: $PLANS_BASE"

# List active plans to identify which one we're stuck on
gtimeout 5 ls -la "$PLANS_BASE/active/" 2>/dev/null | head -20
```

3. Create structured help request document

The AI must create or update a help request section in the active plan OR create a standalone help request file:

**Option A: Update Active Plan (Preferred)**

Add a `## 🆘 HELP REQUESTED` section to the current active plan with:

```markdown
## 🆘 HELP REQUESTED

**Requested By**: [Model identifier if known, e.g., "claude-3-5-sonnet", "gpt-4o-mini"]
**Requested At**: [ISO timestamp]
Status**: AWAITING_HIGHER_MODEL

### Problem Statement

[Clear, concise description of what you're trying to accomplish]

### What I've Tried
#### 1. Browser/Web Search Attempts

- Searched for: "[query 1]" → Result: [what was found/not found]
- Searched for: "[query 2]" → Result: [what was found/not found]
- Visited: [URLs] → Result: [relevant findings or why not helpful]

#### 2. Codebase Investigation

- Searched for: "[pattern/query]" in [directories] → Result: [findings]
- Read files: [list of files examined] → Key observations: [...]
- Grep patterns tried: [patterns] → Found: [results]

#### 3. Other Diagnostic Steps

- [Any other steps taken: terminal commands, linting, testing, etc.]

### Current Hypotheses
1. [Hypothesis 1 - why you think this might be the cause]
2. [Hypothesis 2 - alternative explanation]
3. [Hypothesis 3 - if applicable]

### Why I'm Stuck
 [Explain specifically why you cannot proceed - missing knowledge, conflicting information, complexity beyond reasoning capacity, etc.]

### Suggested Next Steps for Higher Model

 1. [What you think a higher model should investigate first]
 2. [Alternative approaches you couldn't fully evaluate]
 3. [Questions that need answering]

### Relevant Context

- Current active plan: [plan path]
- Related files: [list key files]
...
 5. **Update the help request status**:

```markdown
## 🆘 HELP REQUESTED - ✅ RESOLVED

**Resolved By**: [Higher model identifier]
**Resolved At**: [ISO timestamp]
**Resolution**: [Brief summary of solution]
```

6. **Continue execution** or return control to lower model with clear guidance

## Example Help Request

```markdown
## 🆘 HELP REQUESTED

**Requested By**: claude-3-5-sonnet
**Requested At**: 2025-11-28T14:30:00Z
**Status**: AWAITING_HIGHER_MODEL

### Problem Statement
Trying to fix authentication flow in React app. Users are getting logged out randomly after ~15 minutes, but the token expiry is set to 24 hours.
```

## Model Tier Guidance

| Model Tier      | Examples                                       | Typical Use                                               |
| --------------- | ---------------------------------------------- | --------------------------------------------------------- |
| Lower-register  | claude-3-5-sonnet, gpt-4o-mini, claude-3-haiku | Routine tasks, simple fixes, documentation                |
| Higher-register | claude-opus-4, gpt-4o, o1-preview              | Complex debugging, architecture decisions, novel problems |

## Help Request Resolution (for Higher Model)

When a higher-register model picks up a help request:

1. **Read the full help request section** carefully
2. **Review the investigation summary** - don't repeat failed approaches
3. **Address the problem** using advanced reasoning
4. **Document your findings** inline in the plan
5. **Update the help request status**:

  ```markdown
  ## 🆘 HELP REQUESTED - ✅ RESOLVED

  **Resolved By**: [Higher model identifier]
  **Resolved At**: [ISO timestamp]
  **Resolution**: [Brief summary of solution]
  ```

6. **Continue execution** or return control to lower model with clear guidance

## Example Help Request
```markdown
## 🆘 HELP REQUESTED

**Requested By**: claude-3-5-sonnet
**Requested At**: 2025-11-28T14:30:00Z
**Status**: AWAITING_HIGHER_MODEL

### Problem Statement
Trying to fix authentication flow in React app. Users are getting logged out randomly after ~15 minutes, but the token expiry is set to 24 hours.
```
