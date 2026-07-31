---
# Dadosfera Metadata
category: automation
criticality: critical
scope: all
commandId: "090"
version: "1.0.0"
type: "au_autonomous_loop"
canonical: "docs-fera@/commands/aulo_autonomous_loop.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/aulo_autonomous_loop.md"
backlinks:
  - "commands/cimp_continuous_improvement_loop.md"
  - "commands/cont_continue.md"
  - "commands/plor_plan_orchestrator.md"
  - "commands/next_next_plan_cycle.md"
  - "commands/chkp_check_pending.md"
  - "standards/agents/autonomous_execution.md"
  - "mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md"

# Claude Code Metadata
name: "Autonomous Loop"
description: "Run continuous improvement cycles autonomously until stopping condition is met"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 090 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: au_autonomous_loop -->
# /aulo_autonomous_loop

**Command**: `/aulo` or `/aulo_autonomous_loop`

**PURPOSE**: Execute continuous improvement cycles autonomously, continuing until a defined stopping condition is met. This is the "autopilot" mode for codebase improvement.

## Stopping Conditions

The autonomous loop stops when ANY of these conditions is met:

1. **Plans Exhausted**: No more active, prioritized, or backlog plans to execute
2. **Time Limit**: Defined time budget (default: 2 hours) is reached
3. **Iteration Limit**: Maximum number of cycles (default: 5) completed
4. **Blocker Encountered**: Critical issue requiring human decision
5. **User Interrupt**: User requests stop via conversation
6. **Quality Gate Failed**: Review phase finds critical issues 3 times consecutively
7. **Git Conflict**: Merge conflict or push failure requiring manual resolution

## Loop Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS LOOP                          │
│                                                             │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐              │
│   │ ASSESS  │────▶│ EXECUTE │────▶│ VERIFY  │              │
│   │ /invp   │     │ /next   │     │ /reva   │              │
│   └────┬────┘     └────┬────┘     └────┬────┘              │
│        │               │               │                    │
│        │               │               │                    │
│        ▼               ▼               ▼                    │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐              │
│   │  PLAN   │     │  TEST   │     │  SYNC   │              │
│   │ /pfac   │     │ /tcon   │     │ /gsyn   │              │
│   └─────────┘     └─────────┘     └─────────┘              │
│                                                             │
│        ◀──────────── REPEAT ────────────▶                   │
│                                                             │
│   STOP CONDITIONS:                                          │
│   • Plans exhausted   • Time limit   • Iteration limit      │
│   • Blocker found     • User stop    • Quality gate fail    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Configuration Options

### Time Budget
```
/aulo --time=2h      # 2 hours (default)
/aulo --time=30m     # 30 minutes
/aulo --time=4h      # 4 hours
```

### Iteration Limit
```
/aulo --iterations=5   # 5 cycles (default)
/aulo --iterations=10  # 10 cycles
/aulo --iterations=1   # Single cycle (same as /cimp)
```

### Mode Selection
```
/aulo --mode=full      # Full PDCA+L cycle each iteration
/aulo --mode=quick     # Investigate-Execute-Review only
/aulo --mode=focused   # Execute and test only (no investigation)
```

### Checkpoint Behavior
```
/aulo --checkpoint=commit   # Commit after each cycle (default)
/aulo --checkpoint=push     # Push after each cycle
/aulo --checkpoint=none     # No git operations between cycles
```

## Per-Cycle Output

### Cycle N Report

**Iteration**: `N of M`
**Time Elapsed**: `HH:MM:SS`
**Time Remaining**: `HH:MM:SS`

#### Cycle Summary
- Plans executed: `<count>`
- Tasks completed: `<count>`
- Tests passed/failed: `<pass>/<fail>`
- Issues found: `<critical>/<major>/<minor>`

#### Decision
- **Continue**: `<yes/no>`
- **Reason**: `<explanation>`

#### Next Cycle Plan
- Target plan: `<plan-name>`
- Estimated tasks: `<count>`

## Final Report

### Autonomous Loop Summary

**Total Iterations**: `<count>`
**Total Time**: `HH:MM:SS`
**Stop Reason**: `<reason>`

#### Aggregate Metrics
| Metric | Count |
|--------|-------|
| Plans completed | X |
| Tasks completed | X |
| Tests created | X |
| Tests passed | X |
| Issues fixed | X |
| Commits created | X |

#### Learning Insights
1. `<insight-1>`
2. `<insight-2>`

#### Recommendations for Next Session
1. `<recommendation-1>`
2. `<recommendation-2>`

## Safety Guardrails

1. **No Force Operations**: Never uses `--force` flags
2. **Reversible Changes**: All changes are git-backed
3. **Branch Protection**: Works on feature branch, not main
4. **Human Approval Gates**: Critical decisions pause for approval
5. **Audit Trail**: Full log of all operations and decisions

## Integration with Human Oversight

The loop respects `standards/agents/autonomous_execution.md`:

- **Level 1 Autonomy**: Read operations, analysis (always allowed)
- **Level 2 Autonomy**: Code edits, test runs (allowed with safety rails)
- **Level 3 Autonomy**: Config changes, cloud ops (requires explicit check)
- **Level 4 Autonomy**: Production deploys (never autonomous)

## When to Use

- **Overnight runs**: Set time budget and let agent work while you sleep
- **Weekend maintenance**: Clean up technical debt autonomously
- **Pre-release polish**: Execute all pending improvements before release
- **Post-incident recovery**: Systematically address all issues found

## Related Commands

| Command | Purpose |
|---------|---------|
| `/cimp_continuous_improvement_loop` | Single cycle execution |
| `/plor_plan_orchestrator` | Single plan execution |
| `/cont_continue` | Continue current work |
| `/chkp_check_pending` | Check what's pending |

## Example Session

```
User: /aulo --time=1h --iterations=3 --mode=quick

Agent: Starting autonomous improvement loop...
       Time budget: 1 hour
       Max iterations: 3
       Mode: quick (Investigate → Execute → Review)

       --- Cycle 1/3 ---
       [15:30] Investigating priorities...
       [15:32] Found 3 active plans, selecting highest priority
       [15:32] Executing: QW_2h_HIGH_fix_pre_commit_hooks.md
       [15:45] Completed 4/5 tasks
       [15:46] Running review...
       [15:47] Review: 0 critical, 2 minor issues
       [15:47] Committing: "fix: address pre-commit hook issues"
       ✅ Cycle 1 complete. Continuing...

       --- Cycle 2/3 ---
       [15:48] Investigating priorities...
       [15:49] Executing: CB_1h_MED_update_documentation.md
       [16:05] Completed 3/3 tasks
       [16:06] Review: 0 critical, 0 major, 1 minor
       [16:06] Committing: "docs: update README and AGENTS files"
       ✅ Cycle 2 complete. Continuing...

       --- Cycle 3/3 ---
       [16:07] Investigating priorities...
       [16:08] No more high-priority plans found
       [16:08] Executing: MAINT_30m_LOW_cleanup_deprecated.md
       [16:25] Completed 2/2 tasks
       [16:26] Review passed
       ✅ Cycle 3 complete. Iteration limit reached.

       === AUTONOMOUS LOOP COMPLETE ===
       Total time: 56 minutes
       Plans completed: 3
       Tasks completed: 9
       Stop reason: Iteration limit (3/3)

       Recommendations:
       1. Run /cprs to analyze patterns from these fixes
       2. Consider increasing iteration limit for next session
```

**Local Reference**: `commands/aulo_autonomous_loop.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/aulo_autonomous_loop.md`
