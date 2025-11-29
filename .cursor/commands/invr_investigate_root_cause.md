# /invr_investigate_root_cause

Investigate a problem to identify its root cause and propose a solution, without planning or implementing. Use this when you need to understand what's wrong and explore potential fixes before committing to action.

**Local Reference**: `commands/invr_investigate_root_cause.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/invr_investigate_root_cause.md`

Backlinks:

- `mini_prompt/lv1/problem_diagnosis_mini_prompt.md`
- `commands/exec_execute_plan.md`
- `commands/pfac_plan_from_active_tasks_conversation.md`
- `commands/invd_enhanced_deep_investigation.md`

## When to use this command

Use `/invr_investigate_root_cause` when:

1. A problem or bug exists but the root cause is unclear
2. You need to explore potential solutions without committing to implementation
3. You want to propose a fix and get feedback before planning or executing
4. Multiple solution approaches exist and need evaluation
5. You need time to think through a problem before deciding on next steps

Do **NOT** use when:

- You already know the fix and just need to implement it (use `/exec_execute_plan` instead)
- The problem is simple and obvious (just fix it directly)
- You need to create a formal plan (use `/pfac_plan_from_active_tasks_conversation` after this command)
- Surface-level investigation isn't enough (use `/invd_enhanced_deep_investigation` instead)

## Command sequence (run in order)

1. Verify repository context

```bash
gtimeout 5 git rev-parse --show-toplevel
```

2. Create a diagnosis document (or update if one exists)

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")

# Determine investigations directory for -fera repos
if [[ "$REPO_NAME" == *-fera ]]; then
  DIAGNOSIS_DIR="_dev/docs/investigations"
else
  DIAGNOSIS_DIR="docs/investigations"
fi

gtimeout 5 mkdir -p "$DIAGNOSIS_DIR"
```

3. Determine diagnosis file name

```bash
# Use a timestamp-based name or a descriptive slug if provided
DIAGNOSIS_SLUG="$(date +%Y-%m-%d)_problem_investigation"
DIAGNOSIS_FILE="$DIAGNOSIS_DIR/${DIAGNOSIS_SLUG}.md"
echo "Diagnosis file: $DIAGNOSIS_FILE"
```

4. Create diagnosis document structure

The AI should create or update a diagnosis file with the following sections:

```markdown
# Investigation: [Problem Title]

**Status**: IN_PROGRESS
**Date**: [ISO timestamp]
**Problem Reporter**: [User/context]

## Problem Statement

[Clear, concise description of what is broken or not working as expected]

### Symptoms

- [Observable symptom 1]
- [Observable symptom 2]
- [Any error messages or logs]

### Environment Context

- Repository: [repo name/path]
- Platform: [macOS/Linux/Docker/etc.]
- Related files/components: [list key files affected]
- Affected systems: [what users/systems are impacted]

## Investigation Process

### Step 1: Initial Exploration

- [What was checked first]
- [Key observations or files examined]
- [Relevant logs/output captured]

### Step 2: Root Cause Analysis

- [Hypotheses considered]
- [Evidence gathered]
- [Why other hypotheses were ruled out]

### Step 3: Verification

- [How root cause was confirmed]
- [Minimal reproduction case (if applicable)]
- [Proof or test that demonstrates the issue]

## Root Cause

[Clear, specific explanation of what is causing the problem]

### Why this happens

[Technical explanation of the mechanism]

### Contributing factors

- [Factor 1 that makes the problem worse/likely]
- [Factor 2]
- [etc.]

## Solution Options

### Option A: [Title]

**Approach**: [Brief description of approach]

**How it fixes the problem**: [Why this solves the root cause]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Estimated effort**: [Small/Medium/Large]

**Risk level**: [Low/Medium/High and why]

**Files/areas affected**:
- [File 1]
- [File 2]

---

### Option B: [Title] (if multiple approaches exist)

[Same structure as Option A]

---

## Recommendation

[Which solution(s) are recommended and why. Can be ranked by tradeoffs.]

## Next Steps (for user)

The user can now:

1. **Create a plan**: Use `/pfac_plan_from_active_tasks_conversation` to create a detailed plan from this diagnosis
2. **Execute directly**: If the solution is simple, proceed directly with implementation
3. **Get feedback**: Share this diagnosis with the team for discussion before committing
4. **Further investigation**: If more information is needed, use `/invd_enhanced_deep_investigation` to add instrumentation

## Open Questions (if applicable)

[Any remaining unknowns or questions that need answering before proceeding]

---

**Generated**: [timestamp]
**Investigation by**: [AI model/agent identifier]
```

5. Fill the diagnosis document (AI must complete all sections)

The AI should:
- Thoroughly investigate using browser, web search, codebase search, grep, and file reading
- Document findings clearly with evidence
- Provide multiple solution options if applicable
- Avoid making implementation decisions; focus on analysis and options
- Be specific about tradeoffs and risks

6. Save the diagnosis document

```bash
# The AI completes the markdown file with all sections filled
# File is saved to $DIAGNOSIS_FILE
gtimeout 5 ls -la "$DIAGNOSIS_FILE"
```

7. Output summary for user

After investigation is complete, output:

```
════════════════════════════════════════════════════════════════
✅ INVESTIGATION COMPLETE
════════════════════════════════════════════════════════════════

Diagnosis saved to:
  ${DIAGNOSIS_FILE}

Root Cause Identified:
  [1-line summary]

Solution Options:
  [List option titles with estimated effort]

Status:
  Ready for next steps:
  - Option 1: Create a plan with /pfac_plan_from_active_tasks_conversation
  - Option 2: Execute directly with /exec_execute_plan
  - Option 3: Share for team feedback
  - Option 4: Deep investigation with /invd_enhanced_deep_investigation

════════════════════════════════════════════════════════════════
```

8. Optional: Commit diagnosis to version control (if team collaboration is needed)

```bash
gtimeout 10 git add "$DIAGNOSIS_FILE"
```

```bash
gtimeout 5 git status --short | head -20
```

```bash
gtimeout 10 git commit -m "Investigation: root cause analysis and solution options"
```

```bash
gtimeout 15 git push
```

## Checklist

- [ ] Problem statement is clear and specific
- [ ] Root cause is identified with evidence, not guesses
- [ ] Symptoms are documented with logs/errors
- [ ] At least one solution option is documented with clear tradeoffs
- [ ] Solutions explain how they address the root cause
- [ ] Risk levels and effort estimates are realistic
- [ ] Open questions are documented if unknowns remain
- [ ] Investigation file is saved to version control (optional but recommended)
- [ ] AI has not made implementation decisions; only proposes options

## Sequential Command Usage

After investigation is complete, you can sequence commands:

### Option 1: Create a Plan

```
# After /invr_investigate_root_cause completes:
/pfac_plan_from_active_tasks_conversation
```

The diagnosis becomes the basis for a detailed plan with tasks, timeline, and acceptance criteria.

### Option 2: Execute Directly

```
# After /invr_investigate_root_cause completes:
/exec_execute_plan
```

If the solution is straightforward, proceed directly to execution (skipping formal planning).

### Option 3: Deep Investigation

```
# After /invr_investigate_root_cause completes (but didn't provide enough insight):
/invd_enhanced_deep_investigation
```

Add instrumentation and deeper monitoring to understand system behavior.

### Option 4: Escalate or Discuss

```
# After /invr_investigate_root_cause completes:
# Share the diagnosis file with the team, then use /hlp_escalation if needed
```

## Related Commands

- `/exec_execute_plan` - Execute a solution directly after investigation
- `/pfac_plan_from_active_tasks_conversation` - Create a formal plan from a diagnosis
- `/invd_enhanced_deep_investigation` - Add instrumentation for deeper investigation
- `/hlp_escalation` - Request help if investigation is inconclusive
- `/rerr_recurrent_errors` - Create a recurrent error entry if this is a known issue

---

**Last updated**: 2025-11-29
