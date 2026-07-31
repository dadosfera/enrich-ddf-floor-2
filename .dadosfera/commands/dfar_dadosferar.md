---
category: automation
criticality: high
scope: all
---
# /dfar_dadosferar
<!-- COMMAND_ID: 094 -->
<!-- COMMAND_VERSION: 1.1.0 -->
<!-- COMMAND_TYPE: df_dadosferar -->

Master slash command for Dadosfera software evolution. **Shortcut**: `dadosferar` (invoke as `/dadosferar` or `/dfar`). Loads the canonical skill `.cursor/skills/dadosferar/SKILL.md` and routes to sub-commands: init, sync-docs, map, plan, task, design, implement, review, test, docs, sweep, deploy, rollback, monitor, govern, diagnose, optimize, evolve.

**Critical rule**: Authoritative workflow lives in skill `dadosferar` — follow SKILL.md and reference/ sub-files.

**Critical rule**: Requests to clean a repo, merge all PRs, settle branches/worktrees/stashes, or reach a clean slate route through `/gswp_git_sweep` and must finish with its exit-criteria ledger.

**Critical rule**: Distinguish branch-specific blockers from repository-wide baseline debt; do not pollute a PR with unrelated all-files hook fixer churn.

**Critical rule**: Production deployment requires policy gates and human approval for high-risk changes.

**Critical rule**: Jenkins is the only approved CI/CD platform — never GitHub Actions.

**Critical rule**: HTTP 200 alone does not prove deployment on shared pre-alpha LB — verify identity marker and /health.

**Local Reference**: `commands/dfar_dadosferar.md`
**Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/commands/dfar_dadosferar.md`

Backlinks:
- .cursor/skills/dadosferar/SKILL.md
- guides/dadosfera_deployment/deployment_status_index.md
- standards/deployment/deployment_standard.md
- standards/agents/autonomous_execution.md
- guides/commands_and_mini_prompts_distinction.md
- commands/plor_plan_orchestrator.md
- commands/gswp_git_sweep.md
- commands/rols_role_senior_autonomous_engineer.md

## When to Use

- Evolving Dadosfera platform software, Data Apps, pipelines, or integrations
- Planning and organizing multi-step engineering work with agent specialization
- Preparing policy-gated deployment to Dadosfera environments
- Coordinating clean-repo/git hygiene work across PRs, branches, stashes, and worktrees
- Syncing docs-fera knowledge (commands, skills, agents, deployment playbooks)
- End-to-end flow: map → plan → implement → review → test → docs → deploy → monitor

## When NOT to Use

- Pure frontend design polish without platform scope — use skill `impeccable` instead
- Read-only analysis with no evolution intent — use `/moda_ask_mode`
- Single-repo git sync only — use `/gsyn_git_sync`
- Single-resource git cleanup with no orchestration need — use the direct owning command (`/merg_merge`, `/gsta_git_stash`, or `/gswp_git_sweep`) instead
- Executing an existing active plan file only — use `/xect_execute_plan` or `/plor_plan_orchestrator`

## Command sequence (run in order)

### 1. Load canonical skill

```bash
# Read authoritative workflow (docs-fera canonical source):
# .cursor/skills/dadosferar/SKILL.md
# If sub-command invoked, also read reference/<sub-command>.md
```

### 2. Parse sub-command

```bash
# Sub-command = second token after /dadosferar or /dfar
# Examples: plan, deploy, map, implement, sync-docs
# Default (no sub-command): classify intent and recommend next sub-command
```

### 3. Build context

```bash
# Load .dadosferar/ workspace if present
# Index docs-fera: commands/index_commands.yaml, deployment status, standards/deployment
# Map affected modules, repos, services, risk level
```

### 4. Route git-hygiene intent

```bash
# If request includes clean repo/tree, merge all PRs, remove stale branches,
# settle stashes, or remove transient worktrees:
#   delegate to /gswp_git_sweep
#   require its sweep ledger + exit criteria in the final report
#   treat new PRs opened by the sweep as requiring explicit PR-number authorization
```

### 5. Execute sub-command workflow

```bash
# Follow skill sub-command behavior
# Enforce SECURITY_BOUNDARIES and detector rules (reference/detectors.md)
# Route tasks to specialized agents per Agent Registry
```

### 6. Report and propose next step

```bash
# Emit structured artifact: plan | PR summary | deploy report | review | sweep ledger | etc.
# Separate branch blockers from baseline debt and propose the logical next /dadosferar sub-command
```

## Git hygiene orchestration

When the user asks for a clean repository, merged PRs, cleared worktrees, removed stale branches, or no stashes, `/dadosferar` routes to `/gswp_git_sweep` rather than improvising ad hoc git commands. The final answer must include the sweep exit criteria: default branch sync, local branches, remote branches, open PRs, stashes, worktrees, unresolved data-loss flags, and branch-protection posture after any bypass.

## Baseline debt classification

Repository-wide audits such as `pre-commit run --all-files` can expose historical debt outside the active branch. Classify those failures as baseline debt unless they are caused by the current change. Keep branch-specific fixes in the PR under review; do not commit unrelated formatter/hook churn created by an all-files audit unless the user explicitly expands scope.

## Sub-commands

| Sub-command | Purpose |
|-------------|----------|
| init | Initialize `.dadosferar/` workspace |
| sync-docs | Index docs-fera knowledge |
| map | Impact map |
| plan | Execution plan + task graph |
| task | Organized tasks and owners |
| design | Technical design (ADR, API) |
| implement | Agent-driven implementation + PR |
| review | Multi-domain review + detectors |
| test | Risk-scoped test matrix |
| docs | Documentation updates |
| sweep | Clean repo state via `/gswp_git_sweep` |
| deploy | Policy-gated deployment |
| rollback | Safe revert |
| monitor | Observability check |
| govern | IAM and compliance |
| diagnose | Root-cause investigation |
| optimize | Performance/cost improvements |
| evolve | Continuous improvement proposals |

## Examples

```
/dadosferar plan "Create Data App deployment workflow with IAM validation and rollback"
/dadosferar sweep "Review open PRs, settle stashes/worktrees, and leave the repo clean"
/dadosferar deploy environment=staging
/dadosferar sync-docs
/dfar map "Fix IAM permission in Data Apps sharing"
```

## Related

- Skill: `.cursor/skills/dadosferar/SKILL.md`
- Git hygiene: `/gswp_git_sweep`
- Deployment: `guides/dadosfera_deployment/`, skill `deploy-standalone`
- Planning: `/plor_plan_orchestrator`, `/xect_execute_plan`
- Role: `/rols_role_senior_autonomous_engineer`

## Related Commands

- `/plor_plan_orchestrator`
- `/pfac_plan_from_active_tasks_conversation`
- `/xect_execute_plan`
- `/gswp_git_sweep`
- `/rols_role_senior_autonomous_engineer`
- `/docu_document`
- `/gsyn_git_sync`
