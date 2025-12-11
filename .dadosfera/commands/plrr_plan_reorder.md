# /plrr_plan_reorder

<!-- COMMAND_ID: 047 -->
<!-- COMMAND_VERSION: 1.0.0 -->
<!-- COMMAND_TYPE: pl_plan_reorder -->

**PURPOSE**: Run a repository-wide plan review and **reorder** priorities across `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` using the lv1 mini prompt.

## Usage

```bash
# In the agent interface
@mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md
```

## Description

This command is the high-level entry point for **plan reprioritization** when the code base or business context has changed and you need to realign work:

- Scan all plan and project folders under `plans/`, `docs/plans/`, and `projects/` (top-level and project-scoped).
- Include **all statuses**: `active/`, `prioritized/`, `backlog/`, `blocked/`, `canceled/`, and `finished/` (for historical context).
- Apply the enhanced effort–impact matrix from the mini prompt to reorder work and surface:
  - Immediate priorities: `QW_` quick wins, `CB_` critical blockers, `SEC_` security/safety.
  - High-value follow-ups: `HI_`, technical debt, and dependency-resolution plans.
- Propose concrete updates such as:
  - Which backlog items should move to `prioritized/`.
  - Which prioritized plans should be prepared for `active/`.
  - Which large plans should be split into smaller, executable chunks.
- Output a **clear shortlist of next 5–10 plans** to execute, plus consolidation opportunities; do **not** move or edit plan files directly—produce a change proposal that can be applied via normal plan lifecycle commands.

## Scope Boundaries

**Plan-scope only**: This command focuses on reordering plans within a single repository's plan structure (top-level plans in `plans/` or `docs/plans/`). It does **not** include project-scoped plans. For other scopes, use:

| Scope                       | Command                      | Description                                                                                      |
| --------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------ |
| **Portfolio with projects** | `/revp_prj_portfolio_review` | Portfolio review including project-level analysis (includes both plans and project-scoped plans) |
| **Portfolio-wide**          | `/pfrb_portfolio_rebalance`  | Portfolio-wide rebalancing across all repositories (broader operational scope, multi-repo)       |

**Note**: This command operates on repository-level plans only. For project-specific plan reprioritization, navigate to the project directory and use project planning commands.

## Related

- **Local Reference**: `mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md`
  **Git URL Reference**: `https://github.com/dadosfera/docs-fera/blob/main/mini_prompt/lv1/project_and_plans_review_reprioritize_mini_prompt.md`
- `/revp_prj_portfolio_review` (ID 042) - Portfolio review with project analysis (includes project-scoped plans)
- `/pfrb_portfolio_rebalance` (ID 046) - Portfolio-wide rebalancing across all repositories (broader scope)
- `/revl_review_all_plans` - Review all plans including meta plans
- `/next_next_plan_cycle` - Execute next plan in lifecycle
- `/prio_investigate_codebase_priorities` - Investigate codebase priorities
