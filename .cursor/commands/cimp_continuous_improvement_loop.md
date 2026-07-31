---
# Dadosfera Metadata
category: planning
criticality: critical
scope: all
commandId: "089"
version: "1.0.0"
type: "ci_continuous_improvement_loop"
canonical: "docs-fera@/commands/cimp_continuous_improvement_loop.md"
github: "https://github.com/dadosfera/docs-fera/blob/main/commands/cimp_continuous_improvement_loop.md"
backlinks:
  - "commands/invp_investigate_priorities.md"
  - "commands/pfac_plan_from_active_tasks_conversation.md"
  - "commands/next_next_plan_cycle.md"
  - "commands/reva_review_active_conversation.md"
  - "commands/tcon_test_conversation.md"
  - "commands/cprs_commits_prs_rules_analysis.md"
  - "commands/chkp_check_pending.md"
  - "commands/gsyn_git_sync.md"
  - "commands/plcy_plan_lifecycle_management.md"
  - "standards/agents/autonomous_execution.md"
  - "mini_prompt/lv2/automated_execution_active_plans_mini_prompt.md"

# Claude Code Metadata
name: "Continuous Improvement Loop"
description: "Full autonomous improvement cycle: Investigate → Plan → Execute → Test → Review → Learn → Sync"
platforms:
  - cursor
  - dadosfera
  - claude
---
<!-- COMMAND_ID: 089 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: ci_continuous_improvement_loop -->
# /cimp_continuous_improvement_loop

**Command**: `/cimp` or `/cimp_continuous_improvement_loop`

**PURPOSE**: Execute a complete autonomous improvement cycle following the PDCA+L (Plan-Do-Check-Act + Learn) methodology. Chains investigation, planning, execution, testing, review, and learning phases in a bounded, reversible manner.

## Loop Phases

The continuous improvement loop consists of **7 phases** that can be executed fully or partially:

### Phase 1: INVESTIGATE (Discovery)
**Command**: `/invp_investigate_priorities`

- Scan codebase for priorities, debt, and opportunities
- Identify top 5 plans and 5 projects worth pursuing
- Output: Priority assessment and improvement suggestions

### Phase 2: PLAN (Strategy)
**Command**: `/pfac_plan_from_active_tasks_conversation`

- Create or align conversation with active plan
- Group tasks into Completed/In Progress/Pending/Blocked
- Output: Structured plan document in `_dev/docs/plans/active/`

### Phase 3: EXECUTE (Implementation)
**Command**: `/next_next_plan_cycle`

- Pick and execute the next plan in queue (Active → Prioritized → Backlog)
- Skip already finished plans
- Execute tasks sequentially with proper validation
- Output: Completed tasks and updated plan status

### Phase 4: TEST (Verification)
**Command**: `/tcon_test_conversation`

- Create, adapt, or retire tests for behavior touched in conversation
- Use test taxonomy (category/subcategory/criticality)
- Output: Test results and coverage assessment

### Phase 5: REVIEW (Quality Check)
**Command**: `/reva_review_active_conversation`

- Multi-layered quality analysis (Critical/Major/Minor)
- Scrutinize completed tasks for lazy completion
- Apply "No Lazy Done" policy
- Output: Quality findings and improvement suggestions

### Phase 6: LEARN (Pattern Extraction)
**Command**: `/cprs_commits_prs_rules_analysis`

- Analyze recent commits and PRs for recurring mistakes
- Propose rule improvements
- Identify churn/stability patterns
- Output: Rules improvement proposal and systemic fixes

### Phase 7: SYNC (Persistence)
**Command**: `/gsyn_git_sync`

- Commit and push all changes
- Ensure improvements persist across sessions
- Output: Clean git status

## Execution Modes

### Mode A: Full Cycle (Default)
Execute all 7 phases in sequence. Use for comprehensive improvement sessions.

```
/cimp --mode=full
```

### Mode B: Quick Cycle
Execute phases 1-3-5 only (Investigate → Execute → Review). Use for rapid iteration.

```
/cimp --mode=quick
```

### Mode C: Learning Cycle
Execute phases 1-6-7 only (Investigate → Learn → Sync). Use for periodic learning without execution.

```
/cimp --mode=learn
```

### Mode D: Single Phase
Execute only a specific phase. Use for targeted work.

```
/cimp --phase=investigate
/cimp --phase=plan
/cimp --phase=execute
/cimp --phase=test
/cimp --phase=review
/cimp --phase=learn
/cimp --phase=sync
```

## Output Template

### Continuous Improvement Loop Report

**Repository**: `<repo-name>`
**Started**: `<timestamp>`
**Mode**: `<full|quick|learn|single>`

#### Phase 1: Investigation Results
- Top priorities identified: `<count>`
- Debt items found: `<count>`
- Recommended next actions: `<list>`

#### Phase 2: Planning Results
- Active plan: `<absolute-path>`
- Tasks planned: `<count>`
- Estimated effort: `<hours>`

#### Phase 3: Execution Results
- Tasks completed: `<count>`
- Tasks remaining: `<count>`
- Blockers encountered: `<list>`

#### Phase 4: Testing Results
- Tests created: `<count>`
- Tests passed: `<count>`
- Tests failed: `<count>`
- Coverage change: `<delta>`

#### Phase 5: Review Results
- Critical issues: `<count>`
- Major issues: `<count>`
- Minor issues: `<count>`
- Lazy completion detected: `<yes/no>`

#### Phase 6: Learning Results
- Patterns identified: `<count>`
- Rules to update: `<list>`
- Stability fixes proposed: `<list>`

#### Phase 7: Sync Results
- Commits created: `<count>`
- Branch: `<branch-name>`
- Push status: `<success/pending>`

#### Next Iteration Recommendations
1. `<recommendation-1>`
2. `<recommendation-2>`
3. `<recommendation-3>`

## Integration with Autonomous Execution

This command follows `standards/agents/autonomous_execution.md`:
- Bounded execution (one full cycle per invocation)
- Reversible changes (git-backed)
- Clear checkpoints between phases
- User can interrupt between phases

## When to Use

- **Daily**: Quick cycle (`--mode=quick`) for routine improvement
- **Weekly**: Full cycle (`--mode=full`) for comprehensive review
- **Monthly**: Learning cycle (`--mode=learn`) for pattern extraction and rule updates
- **After incidents**: Single phase investigate + plan for root cause analysis

## Related Commands

| Phase | Primary Command | Alternative |
|-------|-----------------|-------------|
| Investigate | `/invp_investigate_priorities` | `/revc_review_codebase_priorities` |
| Plan | `/pfac_plan_from_active_tasks_conversation` | `/plor_plan_orchestrator` |
| Execute | `/next_next_plan_cycle` | `/xect_execute_plan`, `/xqpa_xqt_plan_all` |
| Test | `/tcon_test_conversation` | `/tall_tests_all`, `/dtao_deep_test_analyze_optimize` |
| Review | `/reva_review_active_conversation` | `/chkp_check_pending` |
| Learn | `/cprs_commits_prs_rules_analysis` | `/matc_code_quality_maturity_assessment` |
| Sync | `/gsyn_git_sync` | `/gful_git_full_sync` |

## Additional Commands for Extended Loops

For more comprehensive autonomous operation, consider adding:

- `/plcy_plan_lifecycle_management` - Clean up plan lifecycle (cancel outdated, verify completed)
- `/plrr_plan_reorder` - Reorder plans based on new priorities
- `/rerr_recurrent_errors` - Fix and prevent recurring errors
- `/depc_deprecation_sweep` - Clean up deprecated files
- `/hook_hooks_setup` - Ensure hooks are properly configured

**Local Reference**: `commands/cimp_continuous_improvement_loop.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/cimp_continuous_improvement_loop.md`
